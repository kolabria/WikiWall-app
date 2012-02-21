from django.shortcuts import HttpResponse, render_to_response
import datetime

def index(request):
    return HttpResponse('Hello World')

def date(request):
    today = datetime.date.today()
    return render_to_response('home/date.html', {'current_date': today})

def current_datetime(request):
    now = datetime.datetime.now()
    html = '<html><body>The time is now %s</body></html>' % now
    return HttpResponse(html)

def hours_ahead(request, offset):
    try:
        offset = int(offset)
    except ValueError:
        raise Http404()
    dt = datetime.datetime.now() + datetime.timedelta(hours=offset)
    html = "<html><body>In %s hour(s) the time "
    html += "will be %s.</body></html>" % (offset, dt)
    return HttpResponse(html)

