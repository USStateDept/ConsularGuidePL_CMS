from django.http import HttpResponseRedirect

import re
from core.models import UserProfile
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings


class PasswordChangeMiddleware:
	def process_request(self, request):
		whitelist = (
			settings.MEDIA_URL,
			settings.STATIC_URL,
			'/accounts/logout/',
		)
		if settings.IS_MASTER \
				and not any(re.match(path, request.path) for path in whitelist):
			if request.user.is_authenticated() and not re.match(r'^/accounts/user_password/$', request.path):
				try:
					profile = request.user.get_profile()
				except ObjectDoesNotExist:
					UserProfile.objects.create(user=request.user)
				if profile.force_password_change:
					return HttpResponseRedirect('/accounts/user_password/')