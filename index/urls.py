from django.urls import path
from index import views

urlpatterns = [
    path('', views.index),
    path('logout/', views.logout, name="logout"),
    path('funding/', views.fundingCheck, name="fundingCheck"),
    path('transaction/eth/', views.ethSending, name="ethSending"),
]
