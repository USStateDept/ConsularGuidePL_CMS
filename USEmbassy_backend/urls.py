# coding=utf-8
from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib import admin
from django.conf import settings


admin.autodiscover()

urlpatterns = patterns('',
                       url(r'^api/post/data', 'api.views.post_data'),
                       url(r'^api/json', 'api.views.json_data'),
)

if settings.IS_MASTER:
	urlpatterns += patterns('',
							url(r'^$', 'USEmbassy_backend.views.home', name='home'),

							url(r'^admin/', include(admin.site.urls)),
							url(r'^push_notification/', include('push_notification.urls')),
							url(r'^accounts/', include('core.urls')),

							url(r'^api/post/jq_thumb/(?P<video_id>\d+)/', 'api.views.video_poster'),

							url(r'^cms/', include('page.urls')),
							url(r'^video/', include('video.urls')),
							url(r'^banner/', include('banner.urls')),
							url(r'^files/', include('file_manager.urls')),
							url(r'^feedback/', include('feedback.urls')),

							url(r'^upload$', 'images.views.upload', name='image-upload'),

	)
else:
	urlpatterns += patterns('',
                       url(r'^$', 'USEmbassy_backend.views.landing_page', name='landing-page'),
    )

if settings.DEBUG:
	urlpatterns += patterns('',
								(r'^media/(?P<path>.*)$', 'django.views.static.serve',
									{'document_root': settings.MEDIA_ROOT}),
	)
	urlpatterns += staticfiles_urlpatterns()
