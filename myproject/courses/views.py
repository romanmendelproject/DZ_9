import time

from django.contrib import auth
from django.core.mail import BadHeaderError, send_mail
from django.db import transaction
from django.forms import inlineformset_factory
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView, DeleteView, DetailView, ListView, UpdateView)
from django_rq import job

from courses.forms import ContactForm, LessonForm
from courses.models import Course, Lesson
from courses.scheduler import send_mail_scheduler
from courses.tasks import send_mail_job


class CourseListView(ListView):
    model = Course

    def get_queryset(self):
        return self.model.objects.filter(is_active=True)


class CourseCreateView(CreateView):
    model = Course
    success_url = reverse_lazy('courses:index')
    fields = '__all__'


class CourseDetailView(DetailView):
    model = Course

    queryset = Course.objects.prefetch_related('user')


class CourseUpdateView(UpdateView):
    model = Course
    success_url = reverse_lazy('courses:index')
    fields = '__all__'

    def get_context_data(self, **kwargs):
            data = super().get_context_data(**kwargs)
            CourseFormSet = inlineformset_factory(Course, Lesson, form=LessonForm, extra=1)
            data['lesson_courses'] = CourseFormSet(self.request.POST or None, instance=self.object)
            return data

    def form_valid(self, form):
        context = self.get_context_data()
        lesson_courses = context['lesson_courses']

        with transaction.atomic():
            self.object = form.save()
            if lesson_courses.is_valid():
                lesson_courses.instance = self.object
                lesson_courses.save()

        return super().form_valid(form)


class CourseDeleteView(DeleteView):
    model = Course
    success_url = reverse_lazy('courses:index')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.is_active = False
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())


def contactform(reguest):
    if reguest.method == 'POST':
        form = ContactForm(reguest.POST)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            sender = form.cleaned_data['sender']
            message = form.cleaned_data['message']
            copy = form.cleaned_data['copy']
            recepients = ['owpdjangotest@gmail.com']
            if copy:
                recepients.append(sender)
            send_mail_scheduler(subject, message, 'owpdjangotest@gmail.com', recepients)
            return HttpResponseRedirect('/course/goodsend/')
    else:
        form = ContactForm()
    return render(reguest, 'courses/contact.html', {'form': form, 'username': auth.get_user(reguest).username})

def goodsend(reguest):
    goodsend = 'goodsend'
    return render(reguest, 'courses/goodsend.html', {'goodsend': goodsend})
