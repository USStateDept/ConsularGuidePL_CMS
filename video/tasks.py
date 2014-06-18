# -*- coding: utf-8 -*-
# Author Artur Baćmaga <artur.bacmaga@agitive.com>
# Author Szymon Nowicki <szymon.nowicki@agitive.com>
# (C) Agitive sp. z o. o. 2014

from __future__ import unicode_literals, absolute_import
from celery import shared_task
import subprocess
from django.conf import settings
from video.utils import generate_android_filename, generate_m3u8_filename, generate_media_path

ANDROID_VIDEO1_PREFIX = "andr1_video.mp4"
ANDROID_VIDEO2_PREFIX = "andr2_video.mp4"
ANDROID_VIDEO3_PREFIX = "andr3_video.mp4"
IOS_VIDEO1_PREFIX = "ios1"
IOS_VIDEO2_PREFIX = "ios2"
IOS_VIDEO3_PREFIX = "ios3"

# ultrafast, superfast, veryfast, faster, fast, medium, slow, slower, veryslow, placebo
FFMPEG_PRESET = 'fast'
# high, main, baseline
FFMPEG_PROFILE = 'baseline'


@shared_task()
def convert_all_video(video, m3u8url, slave_m3u8url):

	video.conversion = True
	video.save()

	original_movie_path = video.video_original.path
	android_movie1_path = generate_android_filename(original_movie_path, ANDROID_VIDEO1_PREFIX)
	android_movie2_path = generate_android_filename(original_movie_path, ANDROID_VIDEO2_PREFIX)
	android_movie3_path = generate_android_filename(original_movie_path, ANDROID_VIDEO3_PREFIX)
	ios_movie1_path = generate_m3u8_filename(original_movie_path, IOS_VIDEO1_PREFIX)
	ios_movie2_path = generate_m3u8_filename(original_movie_path, IOS_VIDEO2_PREFIX)
	ios_movie3_path = generate_m3u8_filename(original_movie_path, IOS_VIDEO3_PREFIX)

	message = ""
	try:
		convert_android_video(original_movie_path, android_movie1_path, preset=FFMPEG_PRESET, profile=FFMPEG_PROFILE,
								vbitrate=str(settings.BITRATE1) + 'k', vbufsize=str(2 * settings.BITRATE1) + 'k',
								vframerate=30, abitrate='192k')
		video.video_android1 = generate_media_path(android_movie1_path)
	except subprocess.CalledProcessError as e:
		message = message + "<br/><h1>Convert android 1000k video error</h1><br/>"
		video.video_android1 = None

	try:
		convert_android_video(original_movie_path, android_movie2_path, preset=FFMPEG_PRESET, profile=FFMPEG_PROFILE,
								vbitrate=str(settings.BITRATE2) + 'k', vbufsize=str(2 * settings.BITRATE2) + 'k',
								vframerate=30, abitrate='128k')
		video.video_android2 = generate_media_path(android_movie2_path)
	except subprocess.CalledProcessError as e:
		message = message + "<br/><h1>Convert android 500k video error</h1><br/>"
		video.video_android2 = None

	try:
		convert_android_video(original_movie_path, android_movie3_path, preset=FFMPEG_PRESET, profile=FFMPEG_PROFILE,
								vbitrate=str(settings.BITRATE3) + 'k', resolution='176x144',
								vbufsize=str(settings.BITRATE3 * 2) + 'k', vframerate=12, abitrate='24k')
		video.video_android3 = generate_media_path(android_movie3_path)
	except subprocess.CalledProcessError as e:
		message = message + "<br/><h1>Convert android 56k video error</h1><br/>"
		video.video_android3 = None

	try:
		convert_ios_video(original_movie_path, ios_movie1_path, preset=FFMPEG_PRESET, profile=FFMPEG_PROFILE,
							video_bitrate=str(settings.BITRATE1) + 'k', video_framerate=30, audio_bitrate='192k')
		video.video_ios1 = generate_media_path(ios_movie1_path)
	except subprocess.CalledProcessError as e:
		message = message + "<br/><h1>Convert iOS 1000k video error</h1><br/>"
		video.video_ios1 = None

	try:
		convert_ios_video(original_movie_path, ios_movie2_path, preset=FFMPEG_PRESET, profile=FFMPEG_PROFILE,
							video_bitrate=str(settings.BITRATE2) + 'k', video_framerate=30, audio_bitrate='96k')
		video.video_ios2 = generate_media_path(ios_movie2_path)
	except subprocess.CalledProcessError as e:
		message = message + "<br/><h1>Convert iOS 500k video error</h1><br/>"
		video.video_ios2 = None

	try:
		convert_ios_video(original_movie_path, ios_movie3_path, preset=FFMPEG_PRESET, profile=FFMPEG_PROFILE,
							video_bitrate=str(settings.BITRATE3) + 'k', video_framerate=10, audio_bitrate='40k')
		video.video_ios3 = generate_media_path(ios_movie3_path)
	except subprocess.CalledProcessError as e:
		message = message + "<br/><h1>Convert iOS 56k video error</h1><br/>"
		video.video_ios3 = None

	if message == "":
		message = "<br/>Video conversion is done."
		video.active = True
		video.generate_variant_m3u8(m3u8url, slave_m3u8url)

	video.conversion = False
	video.save()
	return message


#setting maxrate to bitrate and bufsize to 2x bitrate gives good results.
@shared_task()
def convert_android_video(source_path, dest_path, preset='fast', profile='baseline', vbitrate=None, vbufsize=None,
							vframerate=None, abitrate=None, resolution=None):
	arg = [settings.FFMPEG_HOME + '/bin/ffmpeg', '-i', source_path, '-vcodec', 'libx264', '-profile', profile,
			'-preset', preset]

	if vbitrate is not None:
		arg += ['-vb', vbitrate, '-maxrate', vbitrate]
		if vbufsize is None:
			arg += ['-bufsize', vbitrate]
		else:
			arg += ['-bufsize', vbufsize]

	if resolution is not None:
		arg += ['-s', resolution]

	arg += ['-strict', '-2', '-ar', '44100', '-ac', '2']

	if abitrate is not None:
		arg += ['-ab', abitrate]

	if vframerate is not None:
		arg += ['-r', unicode(vframerate)]

	arg += ['-movflags', 'faststart', '-y', dest_path]

	if settings.PYTHON27:
		ret = subprocess.check_output(arg, stderr=subprocess.STDOUT)
	else:
		ret = subprocess.call(arg, stderr=subprocess.STDOUT)
	print ret


@shared_task()
def convert_ios_video(source_path, ts_file_path, preset='ultrafast', profile='baseline', video_bitrate=None,
						video_framerate=None, audio_bitrate=None, segment_time=10):

	arg = [settings.FFMPEG_HOME + '/bin/ffmpeg', '-y', '-i', source_path, '-strict', 'experimental', '-acodec', 'aac',
			'-ac', '2']

	if audio_bitrate is not None:
		arg += ['-ab', audio_bitrate]

	arg += ['-ar', '44100', '-vcodec', 'libx264', '-pix_fmt', 'yuv420p', '-profile', profile, '-preset', preset]

	if video_bitrate is not None:
		arg += ['-vb', video_bitrate]

	if video_framerate is not None:
		arg += ['-r', unicode(video_framerate)]

	arg += ['-f', 'hls', '-hls_time', unicode(segment_time), '-hls_list_size', '999', ts_file_path]

	if settings.PYTHON27:
		ret = subprocess.check_output(arg, stderr=subprocess.STDOUT)
	else:
		ret = subprocess.call(arg, stderr=subprocess.STDOUT)
	print ret


# ffmpeg -i libx264_test7.mp4 -c:v libx264 -b:v 128k -flags -global_header -map 0 -f segment -segment_time 10
# -segment_list test.m3u8 -segment_format mpegts stream%05d.ts
# ffmpeg -y -i libx264_test7.mp4 -c:v libx264 -profile:v baseline -strict -2 -flags +cgop segment -segment_list index
# .m3u8 -segment_time 10 -segment_format mpeg_ts -segment_list_type m3u8 segment%05d.ts
# ffmpeg -y -i test7.mp4 -c:v libx264 -flags -global_header -map 0 -f segment -segment_list index.m3u8 -segment_time
# 10 -segment_format mpegts segment%05d.ts

# ios
# ffmpeg -y -i test7.mp4 -strict experimental -c:a aac -ac 2 -b:a 96k -ar 44100 -c:v libx264 -pix_fmt yuv420p -profile:v baseline -preset ultrafast -b:v 600K -r 24 -f hls -hls_time 10 -hls_list_size 999 s_out.m3u8

@shared_task()
def generate_poster_thumbnails(video):
	video.delete_thumbnails_folder()
	video.poster_480.generate()
	video.poster_768.generate()
	video.poster_720.generate()
	video.poster_1152.generate()
	video.poster_640.generate()
	video.poster_960.generate()
	video.poster_1536.generate()
	video.poster_320.generate()
