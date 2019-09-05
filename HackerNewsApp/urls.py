from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^home/', views.Home),
    url(r'^fetch-top-articles/', views.FetchTopArticles),
    url(r'^search/', views.Search),
]

