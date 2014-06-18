from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext

__author__ = 'Artur Bacmaga'


@login_required
def home(request):
	return HttpResponseRedirect("/cms")


def landing_page(request):
	return render_to_response('landing_page.html', context_instance=RequestContext(request))