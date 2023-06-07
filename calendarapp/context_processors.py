from datetime import datetime, timedelta
from django.http import HttpRequest

from .models.event import Event

def event_renderer(request: HttpRequest):
    return {
       'my_events': Event.objects.filter(
            user=request.user,
            is_active=True,
            is_deleted=False,
            end_time__gte=datetime.now().date(),
            end_time__lte=(datetime.now().date() + timedelta(days=5)),
        ).order_by("end_time") 
    }
    