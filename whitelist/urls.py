from django.urls import path
from . import views

app_name = 'whitelist'

urlpatterns = [
    path('', views.whitelist_form, name='form'),
    path('success/', views.success, name='success'),
    path('submissions/', views.submissions, name='submissions'),
    path('submissions/<int:pk>/done/', views.mark_done, name='mark_done'),
]
