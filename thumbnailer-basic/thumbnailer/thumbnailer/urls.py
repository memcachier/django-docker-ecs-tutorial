from django.conf.urls import url

from main.views import ThumbnailView

urlpatterns = [
    url(r'^$', ThumbnailView.as_view(), name='index')
]
