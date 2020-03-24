from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import RedirectView

urlpatterns = [
    # Home page / Dashboard is router to github_stats_app.urls
    path('', include('github_stats_app.urls')),
    # Admin section
    path('admin/', admin.site.urls),
]
