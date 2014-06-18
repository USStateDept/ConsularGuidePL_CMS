# -*- coding: utf-8 -*-
# Author Artur Baćmaga <artur.bacmaga@gmail.com>
# Author Szymon Nowicki <szymon.nowicki@agitive.com>
# (C) Agitive sp. z o. o. 2014

from __future__ import unicode_literals
from celery import shared_task
import feedparser
from rss.models import RssNews

RSS_URLS = {
	'EN': (
		'http://poland.usembassy.gov/events_2013/press-relases-2013.rss',
    	'http://poland.usembassy.gov/dyn/press-releases-2014.rss',
		'http://poland.usembassy.gov/poland/warden/recent-messages-for-us-citizens.rss',
	),
	'PL': (
		'http://polish.poland.usembassy.gov/komunikaty-prasowe-2013.rss',
		'http://polish.poland.usembassy.gov/dyn/komunkaty-2014.rss',
		'http://polish.poland.usembassy.gov/poland-pl/warden/security-message-listing.rss',
	),
}

@shared_task()
def get_all_news():
	for lang, urls in RSS_URLS.iteritems():
		for url in urls:
			feed = feedparser.parse(url)
			for entry in feed.entries:
				news = RssNews.create_model_for_entry(entry, lang)
				if news is not None:
					news.get_article()
					news.save()

@shared_task()
def delete_all_news():
	for news in RssNews.objects.all():
		news.delete()
