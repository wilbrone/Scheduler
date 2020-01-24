from django import template
from django.template.defaultfilters import stringfilter
from django.contrib.sites.models import Site
from django.utils.http import urlquote_plus
from django.contrib.sites.shortcuts import get_current_site


register = template.Library()

@register.filter()
def google_calendarize(event):
    st = event.time
    en = event.time 
    tfmt = '%Y%m%dT000000'

    dates = '%s%s%s' % (st.strftime(tfmt), '%2F', en.strftime(tfmt))
    name = urlquote_plus(event.title)

    s = ('http://www.google.com/calendar/event?action=TEMPLATE&' +
         'text=' + name + '&' +
         'dates=' + dates + '&' +
         'sprop=website:' + urlquote_plus(Site.objects.get_current().domain))

    if event.location:
        s = s + '&location=' + urlquote_plus(event.location)

    return s + '&trp=false'

google_calendarize.safe = True
