from django.urls import path
from . import views
from django.views.generic import TemplateView


urlpatterns = [
	path('home/',TemplateView.as_view(template_name='pages/index.html'), name="home-page"),
]