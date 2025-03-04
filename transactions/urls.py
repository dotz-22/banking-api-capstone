from django.urls import path
from .views import TrasanctionViews

urlpatterns = [
        path('transaction/', TrasanctionViews.as_view(),name='transaction'),
        path('transaction/<int:id>/', TrasanctionViews.as_view(),name='transaction_id'),

]