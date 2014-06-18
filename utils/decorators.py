# -*- coding: utf-8 -*-
# Author Szymon Nowicki <szymon.nowicki@agitive.com>
# (C) Agitive sp. z o. o. 2014

from __future__ import unicode_literals

from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import permission_required, login_required


# source: http://stackoverflow.com/a/8429311/828765
def class_view_decorator(function_decorator):

	def simple_decorator(view_class):
		view_class.dispatch = method_decorator(function_decorator)(view_class.dispatch)
		return view_class

	return simple_decorator


def class_permission_required(perm, login_url=None, raise_exception=False):
	return class_view_decorator(permission_required(perm, login_url, raise_exception))


class_login_required = class_view_decorator(login_required)
