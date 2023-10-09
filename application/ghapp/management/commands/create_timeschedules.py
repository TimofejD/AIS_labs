import datetime
import pytz

from django.core.management.base import BaseCommand
from ...models import Greenhouse, CultureType, TnTData, TimeSchedule


class Command(BaseCommand):
    help = 'Create TimeSchedule objects'

    def handle(self, *args, **options):
        # Create Greenhouse objects
        tz = pytz.timezone('Europe/Moscow')
        timeschedule1 = TimeSchedule.objects.create(
            Time=tz.localize(datetime.datetime.now()).replace(microsecond=0),
            ReqAction='Dip the vegetables',
            OkAnswer='Ok'
        )

        timeschedule2 = TimeSchedule.objects.create(
            Time=tz.localize(datetime.datetime.now()).replace(microsecond=0),
            ReqAction='Dip the vegetables',
            OkAnswer='Not Ok'
        )

        # Print a message to indicate success
        self.stdout.write(self.style.SUCCESS(' Successfully created TimeSchedule objects'))


