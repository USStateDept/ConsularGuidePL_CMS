# Create your views here.
from django.conf import settings
from django.http.response import HttpResponse, HttpResponseServerError
import json
from django.views.decorators.csrf import csrf_exempt
from .errors import ApiError
from .methods import Response, AddIosDevice, ChangeIosDevice, AddAndroidDevice, ChangeAndroidDevice, GetPdfs, UpdatePages, AddFeedback, GetBanner, GetVideos, WatchVideo, GetRssNews
from video.models import Video
from video.views import get_video_thumb


def find_method(method_name):
	if not method_name:
		return None

	# Content-Type application/x-www-form-urlencoded
	if method_name == "AddIosDevice":
		return AddIosDevice()
	if method_name == "ChangeIosDevice":
		return ChangeIosDevice()
	if method_name == "AddAndroidDevice":
		return AddAndroidDevice()
	if method_name == "ChangeAndroidDevice":
		return ChangeAndroidDevice()
	if method_name == "GetPdfs":
		return GetPdfs()
	if method_name == "GetVideos":
		return GetVideos()
	if method_name == "AddFeedback":
		return AddFeedback()
	if method_name == "GetBanner":
		return GetBanner()
	if method_name == "GetRssNews":
		return GetRssNews()
	if method_name == "WatchVideo":
		return WatchVideo()

	# Content-Type application/json
	if method_name == "UpdatePages":
		return UpdatePages()
	return None


@csrf_exempt
def post_data(request):
	resp = Response()
	if request.method == 'POST':
		method_name = request.POST.get('method', None)
		method = find_method(method_name)
		if method:
			if method.master_only and not settings.IS_MASTER:
				resp.set_error(ApiError.WRONG_SERVER)
			else:
				resp = method.process(request)
		else:
			resp.set_error(ApiError.MISSING_METHOD)
	else:
		return HttpResponse(status=405, content="Method Not Allowed", )

	return HttpResponse(json.dumps(resp.to_dict(), ensure_ascii=False, indent=1),
	                    content_type='text/json;charset=UTF-8')

@csrf_exempt
def json_data(request):
	resp = Response()
	if request.method == 'POST':
		try:
			data = json.loads(request.body)
		except:
			resp.set_error(ApiError.INCORRECT_JSON)
			return HttpResponse(json.dumps(resp.to_dict(), ensure_ascii=False, indent=1),
	                    content_type='text/json;charset=UTF-8')
		method_name = data.get('method', None)
		method = find_method(method_name)
		if method:
			if method.master_only and not settings.IS_MASTER:
				resp.set_error(ApiError.WRONG_SERVER)
			else:
				method.set_data(data)
				resp = method.process(request)
		else:
			resp.set_error(ApiError.MISSING_METHOD)
	else:
		return HttpResponse(status=405, content="Method Not Allowed", )

	return HttpResponse(json.dumps(resp.to_dict(), ensure_ascii=False, indent=1),
	                    content_type='text/json;charset=UTF-8')

@csrf_exempt
def video_poster(request, video_id):
	if request.method == 'GET':
		second = request.GET.get('second', None)
		try:
			second = int(second)
		except:
			return HttpResponseServerError
		hours = second / 3600
		second -= hours * 3600
		minutes = second / 60
		second -= minutes * 60
		time = "%02d:%02d:%02d" % (hours, minutes, second)
		source_url = request.META.get('HTTP_REFERER', None)
		video = Video.objects.get(pk=video_id)
		get_video_thumb(video.video_original.path, video.poster.path, time_s=time)

		response = {"url": video.poster.url}
		return HttpResponse(json.dumps(response), mimetype="application/json")
	else:
		return HttpResponseServerError()

