# -*- coding: utf-8 -*-
# Author Artur Baćmaga <artur.bacmaga@gmail.com>
# Author Bartłomiej Wójcicki <bartlomiej.wojcicki@agitive.com>
# Author Witold Sosnowski <albi@jabster.pl>
# Author Szymon Nowicki <szymon.nowicki@agitive.com>
# (C) Agitive sp. z o. o. 2014

from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from django.conf import settings
import json


# content types
MENU = 'menu'
TEXT = 'text'
LIST = 'list'
STEPS = 'stps'
CONTACT = 'cont'
CATEGORY = 'cate'

# special types
HEADLINES = 'head'
VIDEOS = 'vids'
FACEBOOK = 'face'

# file manager
FILES = 'file'

# faq
FAQ = 'faqs'

# visa application status
STATUS = 'stat'
PASSPORT = 'pasp'


# zoom
LOW = 11
NORMAL = 13
HIGH = 15

class Page(models.Model):
	TYPES_WITH_CONTENT = (TEXT, LIST, STEPS, CONTACT, CATEGORY)
	PARENT_TYPES = (MENU, LIST, STEPS, CATEGORY)
	SPECIAL_TYPES = (HEADLINES, VIDEOS, FILES, FAQ)
	PAGE_TYPES = (
		(MENU, 'Menu'),
		(TEXT, 'Text'),
		(LIST, 'List'),
		(STEPS, 'Steps'),
		(CATEGORY, 'Table structure'),
		(CONTACT, 'Contact info'),
		(STATUS, 'Visa application status'),
		(PASSPORT, 'Passport tracker'),
		(FAQ, 'Frequently Asked Questions'),
		(VIDEOS, 'Videos'),
		(FILES, 'File Manager'),
		(HEADLINES, 'Headlines'),
		(FACEBOOK, 'Facebook'),
	)
	STATUS_CHOICES = (
		(LOW, 'Low'),
		(NORMAL, 'Normal'),
		(HIGH, 'High'),
	)

	parent_page = models.ForeignKey('self', blank=True, null=True, related_name='child_page',
									limit_choices_to={'page_type__in': PARENT_TYPES})

	permission_parent = models.ForeignKey('self', blank=True, null=True, related_name='permission_child_page',
											editable=False)
	is_permission_parent = models.BooleanField(default=False)

	page_type = models.CharField(max_length=4, choices=PAGE_TYPES, default=TEXT)

	title_pl = models.CharField('Title (PL)', max_length=settings.TITLE_LENGTH)
	title_en = models.CharField('Title (EN)', max_length=settings.TITLE_LENGTH)

	version = models.IntegerField(default=0)
	created = models.DateTimeField(default=timezone.now)
	modified = models.DateTimeField(default=timezone.now)

	active = models.BooleanField(default=True, editable=False)

	#dane dotyczace struktury drzewa
	level = models.IntegerField(default=0, editable=False)  #parent.level+1
	place = models.IntegerField(default=0, editable=False)  #kolejność

	content_pl = models.TextField(verbose_name='Content (PL)', blank=True)
	content_en = models.TextField(verbose_name='Content (EN)', blank=True)

	additional_pl = models.TextField(verbose_name='Additional (PL)', blank=True)
	additional_en = models.TextField(verbose_name='Additional (EN)', blank=True)

	latitude = models.FloatField("Latitude", blank=True, null=True, default=52.229902,
	                             help_text="degrees, floating point, South is negative")
	longitude = models.FloatField("Longitude", blank=True, null=True, default=21.012669,
	                              help_text="degrees, floating point, West is negative")

	zoom = models.IntegerField(blank=True, null=True, default=NORMAL, choices=STATUS_CHOICES)

	editors = models.ManyToManyField(User, related_name='edited_pages')

	def to_dict(self):
		def child_to_dict(child):
			return {
				'id': child[0],
				'index': child[1],
				'title_pl': child[2],
				'title_en': child[3]
			}

		def fix_content(content):
			if content == '':
				return '<content></content>'
			fixed_content = content.replace('&nbsp;', ' ')
			fixed_content = fixed_content.replace('<p><a', '<a').replace('</a></p>', '</a>')
			fixed_content = fixed_content.replace('<li><p>', '<li>').replace('</p></li>', '</li>')
			fixed_content = fixed_content.replace('\t', '').replace('\r', '').replace('\n', '')
			fixed_content = fixed_content.replace('<br />', '\n').replace('<br/>', '\n')
			return fixed_content

		def fix_faq(content):
			try:
				faq_list = json.loads(content)
			except:
				return '[]'

			for question in faq_list:
				question['answer'] = fix_content(question['answer'])

			return json.dumps(faq_list)

		parent_id = 0
		if self.parent_page_id is not None:
			parent_id = self.parent_page_id

		data = {
			'id': self.id,
			'parent_id': parent_id,
			'title_pl': self.title_pl,
			'title_en': self.title_en,
			'version': self.version,
			'type': self.type(),
			'index': self.place,
			#'created': self.created.date().isoformat(),
			#'modified': self.modified.date().isoformat(),
			#'level': self.level,
			#'place': self.place
		}

		type = self.page_type
		if type in self.TYPES_WITH_CONTENT:
			data['content_pl'] = fix_content(self.content_pl)
			data['content_en'] = fix_content(self.content_en)
			if self.additional_en and self.additional_pl:
				data['additional_pl'] = fix_content(self.additional_pl)
				data['additional_en'] = fix_content(self.additional_en)

		if type == CONTACT:
			if self.latitude:
				data['latitude'] = self.latitude
			if self.longitude:
				data['longitude'] = self.longitude
			if self.zoom:
				data['zoom'] = self.zoom

		if type == FAQ:
			data['faq_en'] = fix_faq(self.content_en)
			data['faq_pl'] = fix_faq(self.content_pl)

		if type == CATEGORY:
			# type CATEGORY is used only server side
			data['type'] = TEXT

		children = self.child_page.filter(active=True).values_list('id', 'place', 'title_pl', 'title_en')
		data['children'] = map(child_to_dict, children)
		return data

	def to_json(self):
		data = self.to_dict()
		return json.dumps(data)

	def save(self, *args, **kwargs):
		self.version += 1
		self.modified = timezone.now()
		previous_level = self.level
		previous_permission_parent = self.permission_parent

		if self.parent_page is not None:
			self.level = self.parent_page.level + 1
			if self.is_permission_parent:
				self.permission_parent = None
			else:
				if self.parent_page.is_permission_parent:
					self.permission_parent = self.parent_page
				else:
					self.permission_parent = self.parent_page.permission_parent
		else:
			self.permission_parent = None
			self.is_permission_parent = True
			self.level = 0

		super(Page, self).save(*args, **kwargs)

		if self.level != previous_level or self.permission_parent != previous_permission_parent:
			for child in self.child_page.filter(active=True):
				child.save()

	def __unicode__(self):
		return unicode(self.title_en)

	def get_children_set(self):
		return set(Page.objects.filter(parent_page=self, active=True))

	def type(self):
		return self.page_type

	def type_name(self):
		return dict(Page.PAGE_TYPES).get(self.page_type)

	def user_can_add_children(self, user):
		if self.user_can_edit(user):
			return True
		if self.is_permission_parent:
			perm_parent = self
			while perm_parent is not None and perm_parent.editors.filter(pk=user.pk).count() == 0:
				perm_parent = perm_parent.parent_page
				if perm_parent is None:
					break
				# goto next permission parent
				if not perm_parent.is_permission_parent:
					perm_parent = perm_parent.permission_parent

			return perm_parent is not None
		return False

	def user_can_edit(self, user):
		if user.has_perm('page.change_page'):
			return True
		if self.is_permission_parent:
			return False
		return self.permission_parent.editors.filter(pk=user.pk).count() > 0

	def user_can_remove(self, user):
		if self.is_permission_parent:
			return False
		return self.user_can_edit(user)

	def are_children_valid(self, children):
		if children is None:
			return True
		
		children = list(children)
		child_pages = Page.objects.filter(pk__in=children)
		valid = not any(self.is_descendant(child) for child in child_pages)
		return valid

	def update_children(self, children):
		children = list(children)
		if self.child_page.filter(active=True, is_permission_parent=True).count() > 0:
			children_check = self.child_page.filter(active=True).values_list('id', flat=True)
			if set(children_check) != set(children):
				raise Exception('Cannot delete a permission parent!')
		for child in self.child_page.filter(active=True):
			try:
				child.place = children.index(child.id)
				children[child.place] = 0
				child.save()
			except Exception, e:
				child.deactivate()

		for id in children:
			if id > 0:
				page = Page.objects.get(id=id)
				page.move_to_parent(self)
				page.place = children.index(id)
				page.save()

	def move_to_parent(self, parent):
		old_parent = self.parent_page

		if old_parent == parent:
			return

		self.parent_page = parent

		i = 0
		for child in old_parent.child_page.filter(active=True).order_by('place'):
			child.place = i
			child.save()
			i += 1

		# self.save() called later

	def deactivate(self):
		self.active = False
		self.save()
		map(lambda x: x.deactivate(), self.child_page.filter(active=True))

	def convert_to_data_args(self):
		def data_args(content):
			fixed_content = content.replace('page=', 'data-page=')
			fixed_content = fixed_content.replace('url=', 'data-url=')
			fixed_content = fixed_content.replace('address=', 'data-address=')
			fixed_content = fixed_content.replace('number=', 'data-number=')
			return fixed_content

		changed = False
		if self.content_en:
			self.content_en = data_args(self.content_en)
			changed = True
		if self.content_pl:
			self.content_pl = data_args(self.content_pl)
			changed = True
		if self.additional_en:
			self.additional_en = data_args(self.additional_en)
			changed = True
		if self.additional_pl:
			self.additional_pl = data_args(self.additional_pl)
			changed = True
		if changed:
			self.save()

	def is_descendant(self, page):
		current_page = self

		while current_page.parent_page is not None and current_page.parent_page != page:
			current_page = current_page.parent_page

		return current_page.parent_page is not None

	def convert_to_categories(self):
		def has_categories(content):
			index = content.find("\"categories\"")
			return index != -1

		if self.page_type == CATEGORY:
			return

		convert = False
		if self.content_en and has_categories(self.content_en):
			convert = True
		if self.content_pl and has_categories(self.content_pl):
			convert = True

		if convert:
			self.page_type = CATEGORY
			self.save()


def get_tree_level(user, page=None):
	def tree_node_to_dict(node, children, user):
		parent_title_en = ''
		count = node.child_page.count()
		if node.parent_page:
			parent_title_en = node.parent_page.title_en

		return dict(
			id=node.id, 
			title_en=node.title_en, 
			title_pl=node.title_pl, 
			page_type_en=node.type_name(), 
			parent_title_en=parent_title_en,
			items=children,
			items_count=count,
			can_edit=node.user_can_add_children(user),
			can_remove=node.user_can_remove(user),
		)
	def subtree(user, node):
		children = list()
		for p in node.child_page.filter(active=True):
			children.append(tree_node_to_dict(p, list(), user))
		return tree_node_to_dict(node, children, user)


	if page is None:
		pages = Page.objects.filter(level=0, active=True)

		tree = list()
		for p in pages:
			tree.append(subtree(user, p))

		return tree
	else:
		tree = list()
		tree.append(subtree(user, page))
		return tree


