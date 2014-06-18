CMI
=========

Content management interface for US Embassy Mobile application.

  - [US Embassy Mobile for iOS] [ios]
  - [US Embassy Mobile for Android] [android]


Server functionality
-----------

* CMI - Content Management Interface, main tool of interaction between content editors and the content itself. It contains all page management structures, platform for sharing media files and documents, and editor of content.
* Video Streaming - Server provides functionality of converting videos to iOS/Android formats and streaming them to mobile application. Without converting, it is highly probable that some of the videos (depending on file extension) wouldn’t run on all mobile devices.
* RSS parsing - Back-end is automatically receiving content from selected RSS feeds and presenting them in text format in mobile application.
* API - API module provides communication between server and mobile application. On each time mobile application is started, it communicates with server via API to verify state of local content. If an update is found, it is downloaded onto device. API allows sending push notifications and banners to mobile devices.


[ios]:https://itunes.apple.com/pl/app/us-embassy-mobile/id877737194?mt=8
[android]:https://play.google.com/store/apps/details?id=com.agitive.usembassy
