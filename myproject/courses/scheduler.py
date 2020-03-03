from datetime import datetime

import django_rq

from courses.tasks import send_mail_job


def send_mail_scheduler(*args, **kwargs):
    scheduler = django_rq.get_scheduler('default')
    job = scheduler.schedule(datetime.utcnow(), func=send_mail_job, args=[*args])
    print('run')
