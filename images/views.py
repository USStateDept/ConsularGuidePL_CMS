from django.contrib.auth.decorators import permission_required
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from models import *


@csrf_exempt
@permission_required('images.add_image')
def upload(request):
	func_num = request.GET.get('CKEditorFuncNum', None)
	# ck_editor = request.GET.get('CKEditor', None)
	# lang_code = request.GET.get('langCode', None)

	img = Image(image=request.FILES['upload'])
	img.save()
	return HttpResponse(
		'<script type="text/javascript"> window.parent.CKEDITOR.tools.callFunction(%(func_num)s,"%(url)s")</script>' % {
			"func_num": func_num, "url": img.image.url})

