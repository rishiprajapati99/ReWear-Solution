from django.urls import path
from django.contrib.auth.views import LogoutView

from .views import (
    UserListCreateAPIView,
    ItemListCreateAPIView,
    SwapRequestListCreateAPIView,
    SwapRequestUpdateAPIView,
    ChatListCreateAPIView,
    PracticeLogAPIView,
     HomePageView,
    ItemsPageView,
    LoginPageView,
    SignUpPageView,
)

urlpatterns = [
    path('users/', UserListCreateAPIView.as_view(), name='user-list-create'),
    path('items/', ItemListCreateAPIView.as_view(), name='item-list-create'),
    path('swaps/', SwapRequestListCreateAPIView.as_view(), name='swap-list-create'),
    path('swaps/<int:id>/', SwapRequestUpdateAPIView.as_view(), name='swap-update'),
    path('swaps/<int:swap_id>/chats/', ChatListCreateAPIView.as_view(), name='chat-list-create'),
    path('practice-log/', PracticeLogAPIView.as_view(), name='practice-log'),
    path('home/', HomePageView.as_view(), name='home'),
    path('items-page/', ItemsPageView.as_view(), name='items-page'),
    path('login-page/', LoginPageView.as_view(), name='login'),
    path('signup-page/', SignUpPageView.as_view(), name='signup'),
    path('signup/', SignUpPageView.as_view(), name='signup-form'),
    path('login/', LoginPageView.as_view(), name='login-form'),
    path('logout/', LogoutView.as_view(next_page='login-form'), name='logout'),
   

]


