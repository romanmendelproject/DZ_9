from django.http import HttpResponse
from django_rq import job
from django.core.mail import send_mail

@job
def send_mail_job(*args):
    send_mail(*args)
