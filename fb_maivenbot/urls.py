from django.conf.urls import include, url
from .views import MaivenBotView

urlpatterns = [
	url(r'^3c44fe5315d135324464ae2d70759146a31579a44abc03814a/?$', MaivenBotView.as_view())
]