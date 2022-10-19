"""journals URL patterns"""

from django.urls import path
from . import views

app_name = 'journals'
urlpatterns = [
    #Home page
    path('', views.index, name='index'),
    #Topics page
    path('topics/', views.topics, name='topics'),
    #Single topic page
    path('topics/<int:topic_id>/', views.topic, name='topic'),
    #Adding new topic page
    path('new_topic/', views.new_topic, name='new_topic'),
    #New entry page
    path('new_entry/<int:topic_id>/', views.new_entry, name='new_entry'),
    #Editting entry page
    path('edit_entry/<int:entry_id>/', views.edit_entry, name='edit_entry'),
]