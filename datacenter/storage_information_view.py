from datacenter.models import Visit
from django.shortcuts import render
from django.utils.timezone import localtime


def storage_information_view(request):
    non_closed_visits = []
    not_leaved_visits = Visit.objects.filter(leaved_at=None)
    for visit in not_leaved_visits:
        entered_at_localtime = localtime(visit.entered_at)
        non_closed_visits.append(
            {
                'who_entered': visit.passcard.owner_name,
                'entered_at': entered_at_localtime,
                'duration': visit.format_duration(visit.get_current_time_duration),
            })

    context = {
        'non_closed_visits': non_closed_visits,
    }
    return render(request, 'storage_information.html', context)
