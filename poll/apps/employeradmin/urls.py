from django.urls import path

from apps.employeradmin import views

app_name = 'employeradmin'

urlpatterns = [
    path('event/',views.Events.as_view(),name='events'),
    path('eventlist/',views.EventList.as_view(),name='eventslist')
    ]