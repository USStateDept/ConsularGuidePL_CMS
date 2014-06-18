# -*- coding: utf-8 -*-
# Author Artur Baćmaga <artur.bacmaga@agitive.com>
# Author Bartłomiej Wójcicki <bartlomiej.wojcicki@agitive.com>
# Author Szymon Nowicki <szymon.nowicki@agitive.com>
# (C) Agitive sp. z o. o. 2014

from django.core.exceptions import ObjectDoesNotExist
from django.forms.models import model_to_dict
from api.errors import ApiError
from file_manager.models import File
from itertools import chain
from video.models import Video
from page.models import Page
from banner.models import Banner
from feedback.models import Feedback
from rss.models import RssNews
from push_notifications.models import APNSDevice, GCMDevice


class BaseMethod(object):
	master_only = False
	def process(self, request):
		raise NotImplementedError()


class JsonMethod(BaseMethod):
	def __init__(self):
		self.data = None

	def set_data(self, data):
		self.data = data


class UpdatePages(JsonMethod):
	def process(self, request):
		resp = Response()
		get_pages_diff(self.data, resp)
		return resp


def get_pages_diff(data, resp):
	pages = data.get('pages', None)

	if pages is None or not isinstance(pages, dict):
		resp.set_error(ApiError.INCORRECT_POST_FIELD)
		return

	db_pages = Page.objects.filter(active=True)
	updated = list()
	new = list()

	for db_page in db_pages:
		page = pages.pop(unicode(db_page.id), None)
		if page is None:
			new.append(db_page.to_dict())
		elif page['version'] < db_page.version:
			updated.append(db_page.to_dict())

	removed = map(lambda item: item, pages)

	result = dict(new=new, updated=updated, removed=removed)
	resp.set_result(result)
	return


class AddFeedback(BaseMethod):
	master_only = True
	def process(self, request):
		resp = Response()
		email = request.POST.get('email', None)
		from_page = request.POST.get('from_page', None)
		feedback = request.POST.get('feedback', None)

		if feedback is not None:
			f = Feedback(text=feedback)
			if email is not None:
				f.email = email
			if from_page is not None:
				try:
					f.from_page = Page.objects.get(pk=int(from_page))
				except ValueError:
					return resp.set_error(ApiError.INCORRECT_POST_FIELD)
				except ObjectDoesNotExist:
					# id == 0 - Home Screen
					pass
			f.save()
			return resp.set_ok()
		else:
			return resp.set_error(ApiError.MISSING_POST_FIELD)


class GetPdfs(BaseMethod):
	def process(self, request):
		resp = Response()
		pdfs = dict(pdfs=map(lambda pdf: pdf.to_dict(), File.objects.all()))
		return resp.set_result(pdfs)


class WatchVideo(BaseMethod):
	master_only = True
	def process(self, request):
		resp = Response()
		video_id = request.POST.get('video_id', None)
		if video_id is None:
			return resp.set_error(ApiError.MISSING_POST_FIELD)
		try:
			video = Video.objects.get(pk=video_id)
		except Video.DoesNotExist:
			return resp.set_error(ApiError.MISSING_VIDEO)

		video.increment_view_count()
		return resp.set_ok()


class GetVideos(BaseMethod):
	def process(self, request):
		resp = Response()
		vids = dict(videos=map(lambda vid: vid.to_dict(), Video.objects.filter(active=True).order_by('-date')))
		try:
			vids['most_viewed'] = Video.objects.filter(active=True).order_by('-views')[0].to_dict()
		except:
			vids['most_viewed'] = None
		return resp.set_result(vids)


class GetBanner(BaseMethod):
	def process(self, request):
		resp = Response()
		banner = Banner.objects.get()
		return resp.set_result(model_to_dict(banner, exclude='id'))


class GetRssNews(BaseMethod):
	def process(self, request):
		resp = Response()
		news_objects = RssNews.objects.all().order_by('-pub_date_rss')
		count = request.POST.get('count', None)
		if count is not None:
			try:
				pl_news = news_objects.filter(language='PL')[:int(count)]
				en_news = news_objects.filter(language='EN')[:int(count)]
				news_objects = list(chain(pl_news, en_news))
			except:
				pass
		news_list = [model_to_dict(news, exclude=['id', 'pub_date_rss']) for news in news_objects]
		return resp.set_result(news_list)


class AddIosDevice(BaseMethod):
	master_only = True
	def process(self, request):
		resp = Response()
		device_token = request.POST.get('new_device_token', None)
		if device_token:
			add_ios_device(device_token)
			return resp.set_ok()
		else:
			return resp.set_error(ApiError.MISSING_POST_FIELD)


class ChangeIosDevice(BaseMethod):
	master_only = True
	def process(self, request):
		resp = Response()
		old_device_token = request.POST.get('old_device_token', None)
		new_device_token = request.POST.get('new_device_token', None)
		if old_device_token and new_device_token:
			if not change_ios_device(old_device_token, new_device_token):
				return resp.set_error(ApiError.MISSING_IOS_DEVICE)
			return resp.set_ok()
		else:
			return resp.set_error(ApiError.MISSING_POST_FIELD)


class AddAndroidDevice(BaseMethod):
	master_only = True
	def process(self, request):
		resp = Response()
		registration_id = request.POST.get('new_registration_id', None)
		if registration_id:
			add_android_device(registration_id)
			return resp.set_ok()
		else:
			return resp.set_error(ApiError.MISSING_POST_FIELD)


class ChangeAndroidDevice(BaseMethod):
	master_only = True
	def process(self, request):
		resp = Response()
		old_registration_id = request.POST.get('old_registration_id', None)
		new_registration_id = request.POST.get('new_registration_id', None)
		if old_registration_id and new_registration_id:
			if not change_android_device(old_registration_id,new_registration_id):
				return resp.set_error(ApiError.MISSING_ANDROID_DEVICE)
			return resp.set_ok()
		else:
			return resp.set_error(ApiError.MISSING_POST_FIELD)


def add_ios_device(device_token):
	try:
		APNSDevice.objects.get(registration_id=device_token)
	except APNSDevice.DoesNotExist:
		new_device = APNSDevice(registration_id=device_token)
		new_device.save()
	except:
		pass


def change_ios_device(old_device_token, new_device_token):
	try:
		old_device = APNSDevice.objects.get(registration_id=old_device_token)
	except APNSDevice.DoesNotExist:
		return False
	old_device.device_token = new_device_token
	if len(APNSDevice.objects.filter(registration_id=new_device_token)) > 0:
		old_device.delete()
	else:
		old_device.save()
	return True


def add_android_device(registration_id):
	try:
		GCMDevice.objects.get(registration_id=registration_id)
	except GCMDevice.DoesNotExist:
		new_device = GCMDevice(registration_id=registration_id)
		new_device.save()
	except:
		pass


def change_android_device(old_registration_id, new_registration_id):
	try:
		old_device = GCMDevice.objects.get(registration_id=old_registration_id)
	except:
		return False
	old_device.registration_id = new_registration_id
	if len(GCMDevice.objects.filter(registration_id=new_registration_id)) > 0:
		old_device.delete()
	else:
		old_device.save()
	return True


class Response(object):
	result = None
	error = None

	def to_dict(self):
		return {'result': self.result, 'error': self.error}

	def set_error(self, error_msg):
		self.result = None
		self.error = error_msg
		return self

	def set_ok(self):
		self.result = 'ok'
		self.error = None
		return self

	def set_result(self, res):
		self.result = res
		self.error = None
		return self
