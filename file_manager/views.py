from forms import *
from django.contrib.auth.decorators import permission_required
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.shortcuts import render_to_response, get_object_or_404
from django.template.context import RequestContext


@permission_required('file_manager.change_file')
def manage_files(request):
	files = File.objects.all()
	form = FileForm()
	return render_to_response('file_manager/manage_files.html', {'files': files, 'form': form},
	                          context_instance=RequestContext(request))


@permission_required('file_manager.add_file')
def add_file(request):
	if not request.is_ajax():
		raise Http404()
	if request.method == 'POST':
		form = FileForm(request.POST, request.FILES)
		if form.is_valid():
			form.save()
			return HttpResponse('OK')
	else:
		form = FileForm()

	return render_to_response('file_manager/add_file.html', dict(form=form),
	                          context_instance=RequestContext(request))


@permission_required('file_manager.change_file')
def edit_file(request, file_id):
	if not request.is_ajax():
		raise Http404()
	pdf_file = get_object_or_404(File, pk=file_id)
	if request.method == 'POST':
		form = FileForm(request.POST, request.FILES, instance=pdf_file)
		if form.is_valid():
			form.save()
			return HttpResponse('OK')
	else:
		form = FileForm(instance=pdf_file)

	return render_to_response('file_manager/edit_file.html', dict(form=form, edit=True, file=pdf_file),
	                          context_instance=RequestContext(request))


def get_en_file(request, file_id):
	pdf_file = get_object_or_404(File, pk=file_id)
	return HttpResponseRedirect(pdf_file.file_en.url)

def get_pl_file(request, file_id):
	pdf_file = get_object_or_404(File, pk=file_id)
	return HttpResponseRedirect(pdf_file.file_pl.url)

@permission_required('file_manager.delete_file')
def delete_file(request):
	pdf_file = get_object_or_404(File, pk=request.POST['file_id'])
	pdf_file.delete()
	return HttpResponseRedirect('/files/')
