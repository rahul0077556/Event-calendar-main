from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.utils import timezone

from calendarapp.models import Event

class DashboardView(LoginRequiredMixin, View):
    login_url = "accounts:signin"
    template_name = "calendarapp/dashboard.html"

    def get(self, request, *args, **kwargs):
        events = Event.objects.get_all_events(user=request.user)
        running_events = Event.objects.get_running_events(user=request.user)
        latest_events = Event.objects.filter(user=request.user).order_by("-id")[:10]
        
        clashes = []
        for event in latest_events:
            for other_event in latest_events:
                if event != other_event:
                    if (event.start_time <= other_event.start_time <= event.end_time) or (event.start_time <= other_event.end_time <= event.end_time):
                        clash_message = f"Event '{other_event.title}' clashes with event '{event.title}'"
                        if clash_message not in clashes:
                            clashes.append(clash_message)

        context = {
            "total_event": events.count(),
            "running_events": running_events,
            "latest_events": latest_events,
            "clashes": clashes,
        }
        return render(request, self.template_name, context)
