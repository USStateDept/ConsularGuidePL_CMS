# -*- coding: utf-8 -*-
# Author Artur Baćmaga <artur.bacmaga@agitive.com>
# Author Szymon Nowicki <szymon.nowicki@agitive.com>
# (C) Agitive sp. z o. o. 2014

import os
import json
import subprocess
import random
import string
from django.conf import settings


def generate_media_path(abs_path):
	return abs_path[len(settings.MEDIA_ROOT) + 1:]


def generate_new_filename(old_path, prefix):
	old_filename = os.path.basename(old_path)
	old_folder = old_path[:-len(old_filename)]
	new_filename = prefix + "_" + old_filename
	return os.path.join(old_folder, new_filename)


def generate_android_filename(old_path, prefix):
	old_filename = os.path.basename(old_path)
	old_folder = old_path[:-len(old_filename)]
	new_filename = prefix
	return os.path.join(old_folder, new_filename)


def generate_m3u8_filename(old_path, prefix):
	old_filename = os.path.basename(old_path)
	old_folder = old_path[:-len(old_filename)]
	new_filename = prefix + "_out.m3u8"
	return os.path.join(old_folder, new_filename)


def generate_image_path(old_path, filename):
	old_filename = os.path.basename(old_path)
	old_folder = old_path[:-len(old_filename)]
	return os.path.join(old_folder, filename)


def get_video_duration(video_abs_path):
	cmd = [settings.FFMPEG_HOME + '/bin/ffprobe', '-v', 'quiet', '-print_format', 'json', '-show_format',
			video_abs_path]
	process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
	stdout, stderr = process.communicate()
	data = json.loads(stdout)
	seconds = int(float(data['format']['duration']))
	return seconds


def get_video_thumb(video_abs_path, thumb_abs_path, time_s='00:00:01'):
	arg = [settings.FFMPEG_HOME + '/bin/ffmpeg', '-y', '-i', video_abs_path, '-r', '1', '-vframes', '1', '-ss',
			time_s, thumb_abs_path]
	if settings.PYTHON27:
		ret = subprocess.check_output(arg, stderr=subprocess.STDOUT)
	else:
		ret = subprocess.call(arg, stderr=subprocess.STDOUT)
	print ret

def generate_random_foldername(size=8):
	chars = string.ascii_uppercase + string.digits
	return ''.join(random.choice(chars) for x in range(size))
