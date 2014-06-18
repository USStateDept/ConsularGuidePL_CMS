# -*- coding: utf-8 -*-
# Author Artur Baćmaga <artur.bacmaga@gmail.com>
# Author Szymon Nowicki <szymon.nowicki@agitive.com>
# (C) Agitive sp. z o. o. 2014

from __future__ import unicode_literals
import urllib2
import re
from lxml import html, etree
from datetime import datetime
from time import mktime
from django.db import models
from django.conf import settings
from django.utils.timezone import utc


class RssNews(models.Model):
	RSS_LANGUAGE = (
		('PL', 'Polski'),
		('EN', 'English'),
	)
	language = models.CharField('Language', max_length=2, choices=RSS_LANGUAGE)
	title = models.CharField('Title', max_length=settings.DESCRIPTION_LENGTH)
	subtitle = models.CharField('Subtitle', max_length=settings.TITLE_LENGTH, null=True, blank=True)
	link = models.URLField(max_length=settings.URL_LENGTH)
	description = models.TextField('Description', max_length=settings.DESCRIPTION_LENGTH)
	pub_date_rss = models.DateTimeField('RSS Publish Date', unique=True)
	text = models.TextField('Text', max_length=settings.LONG_TEXT_LENGTH)

	def get_article(self):
		data = urllib2.urlopen(self.link)
		tree = html.parse(data)
		root = tree.getroot()
		if 'travel.state.gov' in self.link:
			article = root.cssselect('#main .section')[0]
		else:
			article = root.get_element_by_id('middle-content-article')
			subtitle = article.cssselect('h6')
			if len(subtitle) > 0:
				self.subtitle = subtitle[0].text
				article.remove(subtitle[0])
		self._clean_article(article)

	def _clean_article(self, article):
		if len(article.cssselect('h1')) > 0:
			article.remove(article.cssselect('h1')[0])
		for e in article.cssselect('p,br,ul,li'):
			e.tail = '\n' + (e.tail if e.tail else '')
		etree.strip_tags(article, '*')
		text = unicode(article.text_content()).strip()
		self.text = re.sub(r'\W*\n\W*', '\n\n', text)

	@classmethod
	def create_model_for_entry(cls, entry, lang):
		dt = datetime.fromtimestamp(mktime(entry.published_parsed), utc)
		if RssNews.objects.filter(pub_date_rss=dt).count() == 0:
			news = RssNews()
			news.language = lang
			news.title = entry.title
			news.link = entry.link
			news.description = entry.summary
			news.pub_date_rss = dt
			return news
		else:
			return None
