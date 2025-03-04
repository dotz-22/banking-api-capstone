from django.urls import path
from .views import SupportView

urlpatterns = [
    path('support/', SupportView.as_view(), name="support"),
    path('support/<int:id>/', SupportView.as_view(), name="support_id"),
]