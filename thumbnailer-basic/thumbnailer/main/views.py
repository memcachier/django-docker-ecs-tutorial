from django.http import HttpResponseBadRequest
from django.shortcuts import render
from django.views.generic.edit import FormView
import requests
import time
import socket

from .forms import ThumbnailForm
from .utils import make_thumbnail


class ThumbnailView(FormView):
    template_name = 'main/index.html'
    form_class = ThumbnailForm
    success_url = '/'

    def form_valid(self, form):
        start = time.time()
        try:
            # Extract original image URL and request thumbnail size
            # from form data.
            url = form.cleaned_data['image_url']
            sz = int(form.cleaned_data['thumbnail_size'])

            # Generate thumbnail data URL.
            data = make_thumbnail(url, sz)

            # Render result view.
            duration = time.time() - start
            server_name = socket.gethostname()
            return render(self.request, 'main/result.html',
                          {'url': url, 'thumbnail_size': sz,
                           'duration': int(duration * 1000),
                           'server_name': server_name,
                           'thumbnail_data': data})
        except requests.exceptions.RequestException:
            return HttpResponseBadRequest("<p>Can't open image URL!</p>")
        except IOError:
            return HttpResponseBadRequest("<p>Can't process input image!</p>")
