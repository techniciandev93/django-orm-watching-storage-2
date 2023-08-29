from django.db import models
from django.utils.timezone import localtime


class Passcard(models.Model):
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now=True)
    passcode = models.CharField(max_length=200, unique=True)
    owner_name = models.CharField(max_length=255)

    def __str__(self):
        if self.is_active:
            return self.owner_name
        return f'{self.owner_name} (inactive)'


class Visit(models.Model):
    created_at = models.DateTimeField(auto_now=True)
    passcard = models.ForeignKey(Passcard, on_delete=models.CASCADE)
    entered_at = models.DateTimeField()
    leaved_at = models.DateTimeField(null=True)

    def is_visit_long(self, minutes=60):
        if self.leaved_at is not None:
            seconds = minutes * 60
            delta_time = self.leaved_at - self.entered_at
            if delta_time.total_seconds() > seconds:
                return True
        return False

    @property
    def get_current_time_duration(self):
        entered_at_localtime = localtime(self.entered_at)
        duration = localtime() - entered_at_localtime
        return duration

    @property
    def get_visit_duration(self):
        entered_at_localtime = localtime(self.entered_at)
        leaved_at_localtime = localtime(self.leaved_at)
        duration = leaved_at_localtime - entered_at_localtime
        return duration

    @staticmethod
    def format_duration(duration):
        days, seconds = duration.days, duration.seconds
        hours = days * 24 + seconds // 3600
        minutes = (seconds % 3600) // 60
        seconds = (seconds % 60)
        return f'{hours}:{minutes}:{seconds}'

    def __str__(self):
        return '{user} entered at {entered} {leaved}'.format(
            user=self.passcard.owner_name,
            entered=self.entered_at,
            leaved=(
                f'leaved at {self.leaved_at}'
                if self.leaved_at else 'not leaved'
            )
        )
