# -*- coding: utf-8 -*-
# Author Artur Baćmaga <artur.bacmaga@agitive.com>
# Author Szymon Nowicki <szymon.nowicki@agitive.com>
# (C) Agitive sp. z o. o. 2014

from __future__ import unicode_literals
import shutil
import urllib2
import os
import unicodedata
from django.core.files.base import File
from django.core.files.temp import NamedTemporaryFile
from django.db import models
from django.utils import timezone
from django.conf import settings
from django.db.models import F
from video.tasks import generate_poster_thumbnails
from video.utils import generate_media_path
from video.processors import ResizeToEdge
from imagekit.models import ImageSpecField
from pilkit.processors import ResizeCanvas

from core.models import SyncableFileModel

YT_IMG_API = "http://img.youtube.com/vi/{0}/0.jpg"
VARIANT_FILE = "variant.m3u8"
VARIANT_SLAVE_FILE = "variant_slave.m3u8"
SCREEN320 = 320
SCREEN480 = 480
SCREEN768 = 768
SCREEN720 = 720
SCREEN1152 = 1152
SCREEN640 = 640
SCREEN960 = 960
SCREEN1536 = 1536
FILL_COLOR = (0, 0, 0, 255)

LOCAL = 'LC'
YOUTUBE = 'YT'


def get_video_upload_path(instance, filename):
	filename = unicode(filename).replace(" ", "")
	path = os.path.join('video', unicode(instance.date.strftime("%Y_%m_%d__%H_%M_%S")).replace(" ", "") + "_" + unicode(
		instance.title_en[:40]).replace(" ", ""), filename)
	return unicodedata.normalize('NFKD', path).encode('ascii', 'ignore')


def get_image_field_specs(size):
	width = size
	height = int((size / 16.0) * 9)
	return {
		'source': 'poster',
		'processors': [ResizeToEdge(width, height, upscale=True), ResizeCanvas(width, height, FILL_COLOR)],
		'format': 'JPEG',
		'options': {'quality': 80}
	}


class Video(SyncableFileModel):
	VIDEO_TYPES = (
		(YOUTUBE, 'You Tube'),
		(LOCAL, 'Local video'),
	)

	conversion = models.BooleanField(default=False)

	video_type = models.CharField(max_length=2, choices=VIDEO_TYPES, default=LOCAL)

	title_pl = models.CharField('Title (PL)', max_length=settings.FILE_TITLE_LENGTH)
	title_en = models.CharField('Title (EN)', max_length=settings.FILE_TITLE_LENGTH)

	date = models.DateTimeField(default=timezone.now)

	active = models.BooleanField(default=False)

	video_original = models.FileField(upload_to=get_video_upload_path, null=True, blank=True)
	video_android1 = models.FileField(upload_to=get_video_upload_path, null=True, blank=True)
	video_android2 = models.FileField(upload_to=get_video_upload_path, null=True, blank=True)
	video_android3 = models.FileField(upload_to=get_video_upload_path, null=True, blank=True)
	video_ios1 = models.FileField(upload_to=get_video_upload_path, null=True, blank=True)
	video_ios2 = models.FileField(upload_to=get_video_upload_path, null=True, blank=True)
	video_ios3 = models.FileField(upload_to=get_video_upload_path, null=True, blank=True)
	video_ios_variant = models.FileField(upload_to=get_video_upload_path, null=True, blank=True)
	video_ios_variant_slave = models.FileField(upload_to=get_video_upload_path, null=True, blank=True)
	video_ios_generated_on = models.CharField(max_length=settings.FILE_TITLE_LENGTH, blank=True)

	poster = models.ImageField(upload_to=get_video_upload_path, null=True, blank=True)
	poster_time = models.PositiveIntegerField(default=1)
	poster_320 = ImageSpecField(**get_image_field_specs(SCREEN320))
	poster_480 = ImageSpecField(**get_image_field_specs(SCREEN480))
	poster_768 = ImageSpecField(**get_image_field_specs(SCREEN768))
	poster_720 = ImageSpecField(**get_image_field_specs(SCREEN720))
	poster_1152 = ImageSpecField(**get_image_field_specs(SCREEN1152))
	poster_640 = ImageSpecField(**get_image_field_specs(SCREEN640))
	poster_960 = ImageSpecField(**get_image_field_specs(SCREEN960))
	poster_1536 = ImageSpecField(**get_image_field_specs(SCREEN1536))

	url = models.URLField(max_length=settings.URL_LENGTH, null=True, blank=True)

	views = models.PositiveIntegerField(default=0)

	syncable_file_fields = [
		'video_original',
		'video_android1',
		'video_android2',
		'video_android3',
		'video_ios1',
		'video_ios2',
		'video_ios3',
		'video_ios_variant',
		'poster_320',
		'poster_480',
		'poster_768',
		'poster_720',
		'poster_1152',
		'poster_640',
		'poster_960',
		'poster_1536',
	]

	def get_syncable_file_paths(self):
		paths = super(Video, self).get_syncable_file_paths()
		paths.append(self.thumbnails_folder())
		return paths

	def __unicode__(self):
		return unicode(self.title_en)

	def delete(self, using=None):
		try:
			shutil.rmtree(self.video_original.path[:-len(os.path.basename(self.video_original.path))])
		except:
			pass

		try:
			shutil.rmtree(self.poster.path[:-len(os.path.basename(self.poster.path))])
		except:
			pass

		self.delete_thumbnails_folder()

		super(Video, self).delete()

	def generate_variant_writer(self, site, variant_filename):
		m3u8_file_path = os.path.join(self.video_original.path[:-len(os.path.basename(self.video_original.path))],
		                              variant_filename)
		m3u8_file = open(m3u8_file_path, 'w+')
		m3u8_file.write('#EXTM3U\n')
		m3u8_file.write('#EXT-X-STREAM-INF:BANDWIDTH={0}\n'.format(settings.BITRATE3 * 1024))
		m3u8_file.write(str(site) + str(self.video_ios3.url) + '\n')
		m3u8_file.write('#EXT-X-STREAM-INF:BANDWIDTH={0}\n'.format(settings.BITRATE2 * 1024))
		m3u8_file.write(str(site) + str(self.video_ios2.url) + '\n')
		m3u8_file.write('#EXT-X-STREAM-INF:BANDWIDTH={0}\n'.format(settings.BITRATE1 * 1024))
		m3u8_file.write(str(site) + str(self.video_ios1.url) + '\n')
		m3u8_file.close()
		return m3u8_file_path

	def generate_variant_m3u8(self, site, slave_site):
		m3u8_file_path = self.generate_variant_writer(site, VARIANT_FILE)
		self.video_ios_variant = generate_media_path(m3u8_file_path)

		slave_m3u8_file_path = self.generate_variant_writer(slave_site, VARIANT_SLAVE_FILE)
		self.video_ios_variant_slave = generate_media_path(slave_m3u8_file_path)

	def to_dict(self):
		data = dict(id=self.id, type=self.video_type, title_pl=self.title_pl, title_en=self.title_en,
		            date=self.date.date().isoformat(), count=self.views)

		if self.video_type == LOCAL:
			try:
				data['android_urls'] = [self.video_android1.url, self.video_android2.url, self.video_android3.url]
			except:
				data['android_urls'] = None
			try:
				data['ios_urls'] = [self.video_ios1.url, self.video_ios2.url, self.video_ios3.url]
			except:
				data['ios_urls'] = None
			try:
				if self.video_ios_generated_on == settings.MIRROR_SERVER_HTTP_ADDRESS:
					# generated on mirror - current server was slave at that moment
					data['ios_variant'] = self.video_ios_variant_slave.url
				else:
					data['ios_variant'] = self.video_ios_variant.url
			except:
				data['ios_variant'] = None
			try:
				posters = dict()
				try:
					posters['main'] = self.poster.url
				except:
					posters['main'] = None
				try:
					posters['poster_320'] = self.poster_320.url
				except:
					posters['poster_320'] = None
				try:
					posters['poster_480'] = self.poster_480.url
				except:
					posters['poster_480'] = None
				try:
					posters['poster_768'] = self.poster_768.url
				except:
					posters['poster_768'] = None
				try:
					posters['poster_720'] = self.poster_720.url
				except:
					posters['poster_720'] = None
				try:
					posters['poster_1152'] = self.poster_1152.url
				except:
					posters['poster_1152'] = None
				try:
					posters['poster_640'] = self.poster_640.url
				except:
					posters['poster_640'] = None
				try:
					posters['poster_1536'] = self.poster_1536.url
				except:
					posters['poster_1536'] = None
				try:
					posters['poster_960'] = self.poster_960.url
				except:
					posters['poster_960'] = None
				data['poster'] = posters
				#data['poster'] = {'main': self.poster.url, 'poster_320': self.poster_320.url,
				#				'poster_480': self.poster_480.url, 'poster_768': self.poster_768.url,
				#				'poster_720': self.poster_720.url, 'poster_1152': self.poster_1152.url,
				#				'poster_640': self.poster_640.url, 'poster_960': self.poster_960.url,
				#				'poster_1536': self.poster_1536.url}
			except:
				data['poster'] = None
		elif self.video_type == 'YT':
			data['yt_url'] = self.url
			try:
				data['poster'] = {'main': self.poster.url, 'poster_320': self.poster_320.url,
									'poster_480': self.poster_480.url, 'poster_768': self.poster_768.url,
									'poster_720': self.poster_720.url, 'poster_1152': self.poster_1152.url,
									'poster_640': self.poster_640.url, 'poster_960': self.poster_960.url,
									'poster_1536': self.poster_1536.url}
			except:
				data['poster'] = None

		return data

	def increment_view_count(self):
		self.views = F('views') + 1
		self.save()

	def get_yt_id(self):
		return unicode(self.url).split('?v=')[-1]

	def get_yt_poster(self):
		if self.video_type == LOCAL:
			return
		filename = u"yt_thumb.jpg"
		url = YT_IMG_API.format(self.get_yt_id())
		temp_file = NamedTemporaryFile(delete=True)
		temp_file.write(urllib2.urlopen(url).read())
		temp_file.flush()
		if self.poster:
			os.remove(self.poster.path)
		self.poster.save(filename, File(temp_file))
		generate_poster_thumbnails(self)

	def video_type_name(self):
		if self.video_type == LOCAL:
			return 'Local'
		else:
			return 'Youtube'

	def is_local(self):
		return self.video_type == LOCAL

	def thumbnails_folder(self):
		return self.poster_320.path[:-len(os.path.basename(self.poster_320.path))]

	def delete_thumbnails_folder(self):
		try:
			shutil.rmtree(self.thumbnails_folder())
		except:
			pass

