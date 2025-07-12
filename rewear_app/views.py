from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from django.contrib.auth import get_user_model
from django.views.generic import TemplateView
from .models import Item, SwapRequest, Chat, PracticeLog
from .serializers import (
    UserSerializer, ItemSerializer,
    SwapRequestSerializer, ChatSerializer,
    PracticeLogSerializer
)

User = get_user_model()


# ------------------ USERS ------------------
class UserListCreateAPIView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]


# ------------------ ITEMS ------------------
class ItemListCreateAPIView(generics.ListCreateAPIView):
    queryset = Item.objects.all().order_by('-created_at')
    serializer_class = ItemSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


# ------------------ SWAPS ------------------
class SwapRequestListCreateAPIView(generics.ListCreateAPIView):
    queryset = SwapRequest.objects.all().order_by('-created_at')
    serializer_class = SwapRequestSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        item_from = serializer.validated_data['item_from']
        item_to = serializer.validated_data['item_to']
        if item_from.owner == item_to.owner:
            raise ValidationError("You cannot swap with your own item.")
        serializer.save()


class SwapRequestUpdateAPIView(generics.UpdateAPIView):
    queryset = SwapRequest.objects.all()
    serializer_class = SwapRequestSerializer
    lookup_field = 'id'
    permission_classes = [permissions.IsAuthenticated]



# ------------------ CHATS ------------------
class ChatListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = ChatSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Chat.objects.filter(swap_request__id=self.kwargs['swap_id'])

    def perform_create(self, serializer):
        swap = SwapRequest.objects.get(pk=self.kwargs['swap_id'])
        if swap.status != 'approved':
            raise ValidationError("Chat is only allowed for approved swaps.")
        serializer.save(sender=self.request.user, swap_request=swap)


# ------------------ PRACTICE LOG ------------------
class PracticeLogAPIView(generics.RetrieveAPIView):
    serializer_class = PracticeLogSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return PracticeLog.objects.get(user=self.request.user)
    
# ------------------ PAGES (TemplateViews) ------------------

class HomePageView(TemplateView):
    template_name = 'rewear_app/home.html'

class ItemsPageView(TemplateView):
    template_name = 'rewear_app/items.html'

from django.contrib.auth.views import LoginView
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from .forms import CustomUserCreationForm
from django.contrib.auth import login

class SignUpPageView(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'rewear_app/signup.html'
    success_url = reverse_lazy('home')  # or reverse_lazy('login')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return super().form_valid(form)

class LoginPageView(LoginView):
    template_name = 'rewear_app/login.html'
    redirect_authenticated_user = True



