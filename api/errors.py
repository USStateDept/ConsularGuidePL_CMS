# coding=utf-8
from django.utils.translation import ugettext as _
__author__ = 'Artur Bacmaga'


class ApiError(object):
	MISSING_METHOD = {'code': 1, 'msg': _("Provided method does not exist")}
	MISSING_POST_FIELD = {'code': 2, 'msg': _("Missing required POST field")}
	MISSING_IOS_DEVICE = {'code': 3, 'msg': _("iOS device does not exist")}
	MISSING_ANDROID_DEVICE = {'code': 4, 'msg': _("Android device does not exist")}
	INCORRECT_POST_FIELD = {'code': 5, 'msg': _("Incorrect POST field")}
	MISSING_PAGE = {'code': 6, 'msg': _("Page does not exist")}
	MISSING_VIDEO = {'code': 7, 'msg': _("Video does not exist")}
	WRONG_SERVER = {'code': 8, 'msg': _("Wrong server")}
	INCORRECT_JSON = {'code': 9, 'msg': _("Incorrect json")}
