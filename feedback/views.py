from django.http import HttpResponse
from django.views.decorators.http import require_POST
from models import *
from django.shortcuts import render_to_response, get_object_or_404
from django.template.context import RequestContext
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required


@login_required
def feedback_list(request):
	feedback = Feedback.objects.filter(active=True).order_by('-date')
	paginator = Paginator(feedback, 10)

	page = request.GET.get('page')

	try:
		feed = paginator.page(page)
	except PageNotAnInteger:
		feed = paginator.page(1)
	except EmptyPage:
		feed = paginator.page(paginator.num_pages)

	return render_to_response('feedback/feedback.html', {'feedback':feed},
	                          context_instance=RequestContext(request))


@require_POST
def deactivate(request):
	feedback = get_object_or_404(Feedback, pk=request.POST['f_id'])
	feedback.active = False
	feedback.save()
	return HttpResponse('OK')
