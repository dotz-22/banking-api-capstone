from django.urls import path
from .views import AccountsView
urlpatterns = [
        path('account/', AccountsView.as_view(),name='accounts'),
        path('account/<int:account_number>/', AccountsView.as_view(),name='accounts_id'),

]


