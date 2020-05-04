from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin
from django.urls import path
from graphene_django.views import GraphQLView

from .schema import schema

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('courses.urls', namespace='courses')),
    path('django-rq/', include('django_rq.urls')),
    path('coursesapi/user/', include('userapi.urls')),
    path('coursesapi/', include('coursesapi.urls')),
    path("graphql/", GraphQLView.as_view(graphiql=True, schema=schema)),
]
if settings.DEBUG:
    import debug_toolbar
    urlpatterns += (
        url(r'^__debug__/', include(debug_toolbar.urls)),
    )
