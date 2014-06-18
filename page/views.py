# -*- coding: utf-8 -*-
# Author Artur Baćmaga <artur.bacmaga@agitive.com>
# Author Bartłomiej Wójcicki <bartlomiej.wojcicki@agitive.com>
# Author Witold Sosnowski <albi@jabster.pl>
# Author Szymon Nowicki <szymon.nowicki@agitive.com>
# (C) Agitive sp. z o. o. 2014

from django.contrib.auth.decorators import login_required, permission_required
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render_to_response, render, get_object_or_404
from django.template.context import RequestContext
from django.views.decorators.csrf import csrf_exempt
from page.forms import get_tree_level, AddPageForm, ModalPageForm, get_page_form, TEXT, LIST, MENU, STEPS, CONTACT, FAQ, \
	create_form, SimpleAddPageForm
from page.models import Page, HEADLINES, CATEGORY
import json


# Views
from page.utils import clean_content


@login_required
def manage_pages(request):
	page_list = Page.objects.filter(active=True)
	return render_to_response('page/manage_pages.html', {'tree': get_tree_level(request.user)},
								context_instance=RequestContext(request))

@login_required
def content_tree(request, page_id=0):
	page = None
	if page_id > 0:
		page = Page.objects.get(id=page_id)
	
	return HttpResponse(json.dumps(get_tree_level(request.user, page)), content_type="application/json")


@login_required
def page_list(request):
	def to_list(page):
		return [page.title_en, unicode(page.id)]
	page_list = Page.objects.exclude(page_type__in=[MENU, HEADLINES]).filter(active=True)
	pages = map(to_list, page_list)
	return HttpResponse(json.dumps(pages), content_type="application/json")

@login_required
def children_list(request, page_id):
	def to_list(page):
		return [page.title_en, unicode(page.id)]
	page = get_object_or_404(Page, pk=page_id)
	page_list = page.child_page.filter(active=True)
	pages = map(to_list, page_list)
	return HttpResponse(json.dumps(pages), content_type="application/json")


@login_required
@csrf_exempt
def clean_text(request):
	if request.method == 'POST':
		data = request.POST.get('data', None)

		if data is not None:
			return HttpResponse(clean_content(data))

	raise Http404()


@login_required
def add_page(request):
	if request.method == 'POST':
		if request.user.is_superuser:
			form = AddPageForm(request.user, request.POST)
		else:
			form = SimpleAddPageForm(request.user, request.POST)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect('/cms/edit_page/'+unicode(form.instance.id)+'/')
	else:
		if request.user.is_superuser:
			form = AddPageForm(request.user)
		else:
			form = SimpleAddPageForm(request.user)

	data = {
		'form': form, 
		'tree': get_tree_level(request.user),
		'page_template': 'page/edit_page_partial.html'
	}

	return render_to_response('page/edit_page.html', data, context_instance=RequestContext(request))


@login_required
def add_page_modal(request, page_id):
	if not request.is_ajax():
		raise Http404()
	page = Page.objects.get(id=page_id)
	if request.method == 'POST':
		form = ModalPageForm(request.user, request.POST)
		if form.is_valid():
			form.save()
			return HttpResponse(form.instance.id)
	else:
		form = ModalPageForm(request.user, initial={'parent_page': page_id, 'level': page.level+1, 'place': 0})

	return render(request, 'page/add_page_modal.html', {'form':form, 'page_id': page_id})


@login_required
def add_child_page(request, page_id):
	page = Page.objects.get(id=page_id)
	if not page.user_can_add_children(request.user):
		raise Http404()
	if request.method == 'POST':
		if request.user.is_superuser:
			form = AddPageForm(request.user, request.POST)
		else:
			form = SimpleAddPageForm(request.user, request.POST)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect('/cms/edit_page/'+page_id+'/')
	else:
		if request.user.is_superuser:
			form = AddPageForm(request.user, initial={'parent_page': page_id, 'level': page.level+1, 'place': 0})
		else:
			form = SimpleAddPageForm(request.user, initial={'parent_page': page_id, 'level': page.level+1, 'place': 0})

	return render_to_response('page/edit_page.html', {'form': form, 'tree': get_tree_level(request.user, page), 'page_template': 'page/edit_page_partial.html'},
								context_instance=RequestContext(request))


@login_required
def edit_page(request, page_id):
	page = Page.objects.get(id=page_id)
	if not page.active:
		raise Http404()

	page_type = page.type()
	if not page.user_can_add_children(request.user):
		raise Http404()

	post_children_order = request.POST.get('children_order', None)
	children_order = None
	if post_children_order is not None and page_type in (MENU, LIST, STEPS):
		children_order = json.loads(post_children_order)

	saved = False
	children_error = None
	form = get_page_form(page, request)
	if request.method == 'POST':
		if form.is_valid():
			if page.are_children_valid(children_order):
				form.save()
				if children_order is not None:
					page.update_children(children_order)
				form = create_form(page.type(), {'user': request.user, 'instance': page})
				saved = True
			else:
				children_error = "Cannot add ancestors to children set."

	children = []
	if children_order is not None and len(children_order) > 0:
		objects = Page.objects.in_bulk(children_order)
		children = [objects[id] for id in children_order]
	else:
		children = page.child_page.filter(active=True).order_by('place')

	if page_type == MENU or page_type == LIST or page_type == STEPS:
		return render_to_response('page/edit_page.html', {
										'form': form, 
										'page': page, 
										'children': children, 
										'tree': get_tree_level(request.user, page),
										'full_tree': get_tree_level(request.user),
		                                'children_error': children_error,
										'page_template': 'page/edit_list.html',
		                                'saved': saved
									},
									context_instance=RequestContext(request))

	if page_type == TEXT or page_type == CATEGORY:
		return render_to_response('page/edit_page.html',
									{'form': form, 'page': page, 'tree': get_tree_level(request.user, page),
									 'page_template': 'page/edit_page_partial.html', 'saved': saved},
									context_instance=RequestContext(request))
	if page_type == CONTACT:
		return render_to_response('page/edit_page.html',
									{'form': form, 'page': page, 'tree': get_tree_level(request.user, page),
									 'page_template': 'page/edit_page_partial.html', 'saved': saved},
									context_instance=RequestContext(request))

	if page_type == FAQ:
		return render_to_response('page/edit_page.html',
									{'form': form, 'page': page, 'tree': get_tree_level(request.user, page),
									 'page_template': 'page/edit_faq.html', 'saved': saved},
									context_instance=RequestContext(request))

	return render_to_response('page/edit_page.html',
	                          {'form': form,
	                           'page': page,
	                           'children': children,
	                           'edit': True,
	                           'tree': get_tree_level(request.user, page),
	                           'children_error': children_error,
	                           'page_template': 'page/edit_page_partial.html',
	                           'saved': saved
	                          },
	                          context_instance=RequestContext(request))


@login_required
def edit_page_partial(request, page_id):
	if not request.is_ajax():
		raise Http404()
	page = Page.objects.get(id=page_id)
	if not page.active:
		raise Http404()

	page.page_type = page_type = request.GET['page_type']

	if not page.user_can_add_children(request.user):
		raise Http404()

	children = page.child_page.filter(active=True).order_by('place')
	form = get_page_form(page, request)

	if page_type == MENU or page_type == LIST or page_type == STEPS:
		return render_to_response('page/edit_list.html', {
										'form': form, 
										'page': page, 
										'children': children, 
										'tree': get_tree_level(request.user, page),
										'full_tree': get_tree_level(request.user),
										'page_template': 'page/edit_list.html'
									},
									context_instance=RequestContext(request))

	if page_type == TEXT:
		return render_to_response('page/edit_page_partial.html',
									{'form': form, 'page': page, 'tree': get_tree_level(request.user, page), 'page_template': 'page/edit_page_partial.html'},
									context_instance=RequestContext(request))
	if page_type == CONTACT:
		return render_to_response('page/edit_page_partial.html',
									{'form': form, 'page': page, 'tree': get_tree_level(request.user, page), 'page_template': 'page/edit_page_partial.html'},
									context_instance=RequestContext(request))

	if page_type == FAQ:
		return render_to_response('page/edit_faq.html',
									{'form': form, 'page': page, 'tree': get_tree_level(request.user, page), 'page_template': 'page/edit_faq.html'},
									context_instance=RequestContext(request))

	return render_to_response('page/edit_page_partial.html',
						{'form': form, 'page': page, 'children': children, 'edit': True, 'tree': get_tree_level(request.user, page), 'page_template': 'page/edit_page_partial.html'},
						context_instance=RequestContext(request))


@login_required
def delete_page(request):
	page = get_object_or_404(Page, pk=request.POST['page_id'])
	if not page.active:
		raise Http404()
	
	if not page.user_can_edit(request.user) or page.is_permission_parent:
		raise Http404()

	if page.parent_page is not None:
		for child in page.parent_page.child_page.filter(active=True, place__gt=page.place):
			child.place -= 1
			child.save()

	page.deactivate()

	if request.is_ajax():
		return HttpResponse('OK')
	else:
		return HttpResponseRedirect('/cms/')
