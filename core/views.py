# -*- coding: utf-8 -*-
# Author Artur Baćmaga <artur.bacmaga@agitive.com>
# Author Witold Sosnowski <albi@jabster.pl>
# Author Szymon Nowicki <szymon.nowicki@agitive.com>
# (C) Agitive sp. z o. o. 2014

from django.contrib.auth.decorators import permission_required, login_required
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.shortcuts import render_to_response, get_object_or_404
from django.template.context import RequestContext
from django.contrib.auth.models import User
from django.contrib.auth.forms import SetPasswordForm
from core.forms import CustomUserChangeForm, CustomCreateUserForm, CustomPasswordChangeForm


@permission_required('auth.change_user')
def manage_users(request):
	form = CustomCreateUserForm(request.user.is_superuser)
	if request.user.is_superuser:
		user_list = User.objects.all()
	else:
		user_list = User.objects.filter(is_superuser=False)
	return render_to_response('core/manage_users.html', {'user_list': user_list, 'form': form},
								context_instance=RequestContext(request))


@permission_required('auth.add_user')
def adduser(request):
	if not request.is_ajax():
		raise Http404()
	if request.method == 'POST':
		form = CustomCreateUserForm(request.user.is_superuser, request.POST)
		if form.is_valid():
			form.save()
			return HttpResponse('')
	else:
		form = CustomCreateUserForm(request.user.is_superuser)
	return render_to_response('core/add_user.html', {'edit': False, 'form': form},
								context_instance=RequestContext(request))


@permission_required('auth.change_user')
def edit_user(request, user_id):
	if not request.is_ajax():
		raise Http404()
	user = get_object_or_404(User, pk=user_id)
	if user.is_superuser and not request.user.is_superuser:
		raise Http404()
	if request.method == 'POST':
		form = CustomUserChangeForm(request.user.is_superuser, request.POST, instance=user)
		if form.is_valid():
			form.save()
			return HttpResponse('')
	else:
		form = CustomUserChangeForm(request.user.is_superuser, instance=user)

	return render_to_response('core/edit_user.html', {'edit': True, 'form': form, 'user_object': user},
								context_instance=RequestContext(request))


@permission_required('auth.delete_user')
def delete_user(request):
	user = get_object_or_404(User, pk=request.POST['user_id'])
	user.delete()
	return HttpResponseRedirect('/accounts/manage_users/')


@permission_required('auth.change_user')
def admin_change_password(request, user_id):
	if not request.is_ajax():
		raise Http404()
	user = get_object_or_404(User, pk=user_id)
	if user.is_superuser and not request.user.is_superuser:
		raise Http404()
	if request.method == 'POST':
		form = CustomPasswordChangeForm(user, request.POST)
		if form.is_valid():
			form.save()
			if request.is_ajax():
				return HttpResponse('OK')
			else:
				return HttpResponseRedirect('/accounts/manage_users/')
	else:
		form = CustomPasswordChangeForm(None)

	return render_to_response('core/admin_change_password.html', {'form': form, 'edit_user': user},
								context_instance=RequestContext(request))

@permission_required('auth.change_user')
def user_data(request):
	if request.method == 'POST':
		form = CustomUserChangeForm(request.user.is_superuser, request.POST, instance=request.user)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect('/')
	else:
		form = CustomUserChangeForm(request.user.is_superuser, instance=request.user)
	return render_to_response('core/user_data.html', {'form': form, },
								context_instance=RequestContext(request))

@login_required
def user_password(request):
	if request.method == 'POST':
		form = CustomPasswordChangeForm(request.user, request.POST)
		if form.is_valid():
			profile = request.user.get_profile()
			profile.force_password_change = False
			profile.save()
			form.save()
			return HttpResponseRedirect('/')
	else:
		form = CustomPasswordChangeForm(None)
	return render_to_response('core/user_password.html', {'form': form, },
								context_instance=RequestContext(request))



