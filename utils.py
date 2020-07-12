import random
from datetime import datetime, timedelta

from accounts.models import *
from meters.models import *

from django.contrib.auth import get_user_model
User = get_user_model()

user_meters = UserMeter.objects.all()
for obj in user_meters:
    days = random.randint(2, 10)
    for i in range(0, days):
        reading_date = datetime.date(datetime.today() - timedelta(i))
        MeterHealth.objects.create(user_meter=obj, meter_status="installed", meter_reading=random.randint(6000, 10000), reading_date=reading_date)