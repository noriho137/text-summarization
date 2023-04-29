from django.urls import path
from .views import SummaryView

app_name = 'summary'
urlpatterns = [
    path('', SummaryView.as_view(), name='summary'),
]
