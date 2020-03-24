from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('repos', views.repos, name='repos'),
    path('contributors/<str:org>/<int:n>/<int:m>/<str:repo_name>', views.contributors, name='contributors'),
]
