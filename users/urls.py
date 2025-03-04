from django.urls import path
from .views import UserRegistrationView, UserLoginView, home
# from rest_framework_simplejwt.views import (TokenObtainPairView, TokenRefreshView)


urlpatterns = [ 
    path('register/', UserRegistrationView.as_view(),name='user_registration'),
    path('login/', UserLoginView.as_view(),name='user_login'),
    path('', home.as_view(),name='user_login'),

    # path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),   
]