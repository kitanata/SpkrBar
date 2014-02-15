from django.http import HttpResponseNotFound, HttpResponseBadRequest

def event_upload_confirm(request):
    if request.method == "POST":
        return HttpResponseNotFound()

    return HttpResponseBadRequest()