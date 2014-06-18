# -*- coding: utf-8 -*-
# Author Artur Baćmaga <artur.bacmaga@agitive.com>
# Author Szymon Nowicki <szymon.nowicki@agitive.com>
# (C) Agitive sp. z o. o. 2014

from django.http.response import HttpResponseRedirect, HttpResponse, Http404
from django.shortcuts import render_to_response, get_object_or_404
from django.template.context import RequestContext
from django.contrib.auth.decorators import permission_required, login_required
from django.conf import settings
from video.forms import VideoForm, VideoPosterForm
from video.models import Video
from video.utils import generate_media_path, get_video_thumb, generate_image_path, get_video_duration
from video.tasks import convert_all_video, generate_poster_thumbnails

VIDEO_THUMB_NAME = "video_thumb.jpg"


@permission_required('video.change_video')
def video_list(request):
	form = VideoForm()
	video_list = Video.objects.all()
	convert_count = Video.objects.filter(conversion=True).count()
	site = 'http://' + str(request.META.get('HTTP_HOST', ""))
	return render_to_response('video/video_list.html', {'convert_count': convert_count, 'video_list': video_list, 'site': site, 'form': form},
	                          context_instance=RequestContext(request))

@login_required
def video_preview(request, video_id):
	if not request.is_ajax():
		raise Http404()
	video = get_object_or_404(Video, pk=video_id)
	return render_to_response('video/video_preview.html', {'video': video})

@permission_required('video.add_video')
def video_add(request):
	if request.method == 'POST':
		form = VideoForm(request.POST, request.FILES)
		if form.is_valid():
			video = form.save()
			if video.is_local():
				video_path = video.video_original.path
				img_file_path = generate_image_path(video_path, VIDEO_THUMB_NAME)
				get_video_thumb(video_path, img_file_path)
				video.poster = generate_media_path(img_file_path)
				video.save()
				return HttpResponseRedirect('/video/convert/{0}'.format(video.id))
			video.active = True
			video.save()
			video.get_yt_poster()
			return HttpResponse('')
	else:
		form = VideoForm()
	return render_to_response('video/video_add.html', {'form': form },
	                          context_instance=RequestContext(request))


@permission_required('video.change_video')
def video_edit(request, video_id):
	if not request.is_ajax():
		raise Http404()
	video = get_object_or_404(Video, pk=video_id)
	if request.method == 'POST':
		form = VideoForm(request.POST, request.FILES, instance=video)
		if form.is_valid():
			convert = 'video_original' in form.changed_data
			video = form.save()
			if video.is_local():
				if convert:
					video_path = video.video_original.path
					img_file_path = generate_image_path(video_path, VIDEO_THUMB_NAME)
					get_video_thumb(video_path, img_file_path)
					video.poster = generate_media_path(img_file_path)
					video.active = False
					video.save()
					return HttpResponseRedirect('/video/convert/{0}'.format(video.id))
				else:
					return HttpResponse('')
			video.active = True
			video.save()
			video.get_yt_poster()
			return HttpResponse('')
	else:
		form = VideoForm(instance=video)
	return render_to_response('video/video_edit.html', {'form': form, 'video': video },
	                          context_instance=RequestContext(request))

@permission_required('video.delete_video')
def video_delete(request):
	video_id = request.POST.get('video_id', None)
	if video_id is None:
		raise Http404()
	video = get_object_or_404(Video, pk=video_id)
	video.delete()
	return HttpResponseRedirect('/video/')


@permission_required('video.change_video')
def video_convert(request, video_id):
	if not request.is_ajax():
		raise Http404()
	video = get_object_or_404(Video, pk=video_id)
	if not video.is_local():
		raise Http404()
	seconds = get_video_duration(video.video_original.path)
	form = VideoPosterForm(seconds=seconds)

	return render_to_response('video/video_convert.html', {'video': video, 'form': form},
	                          context_instance=RequestContext(request))


@permission_required('video.change_video')
def video_convert_all(request, video_id):
	video = get_object_or_404(Video, pk=video_id)
	if not video.is_local():
		raise Http404()
	generate_poster_thumbnails.delay(video)
	if not video.active:
		video.conversion = True
		video.video_ios_generated_on = 'http://' + str(request.META.get('HTTP_HOST', ""))
		video.save()
		convert_all_video.delay(video, video.video_ios_generated_on, settings.MIRROR_SERVER_HTTP_ADDRESS)
	return render_to_response('video/video_convert_message.html',
	                          context_instance=RequestContext(request))
