from django.utils.timezone import localtime
from datacenter.models import Passcard
from datacenter.models import Visit
from django.shortcuts import render, get_object_or_404


def passcard_info_view(request, passcode):
    passcard = get_object_or_404(Passcard, passcode=passcode)
    visits = Visit.objects.filter(passcard=passcard)
    this_passcard_visits = []

    for visit in visits:
        entered_at_localtime = localtime(visit.entered_at)
        this_passcard_visits.append(
            {
                'entered_at': entered_at_localtime,
                'duration': visit.format_duration(visit.get_visit_duration),
                'is_strange': visit.is_visit_long()
            })

    context = {
        'passcard': passcard,
        'this_passcard_visits': this_passcard_visits
    }
    return render(request, 'passcard_info.html', context)
