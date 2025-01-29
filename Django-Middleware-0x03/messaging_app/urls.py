"""
URL configuration for messaging_app project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from rest_framework_nested.routers import DefaultRouter, NestedDefaultRouter
from chats.views import ConversationViewSet, MessageViewSet

# Main Router
router = DefaultRouter()
router.register(r'conversations', ConversationViewSet, basename='conversation')

# Nested Router for Messages under Conversations
nested_router = NestedDefaultRouter(router, r'conversations', lookup='conversation')
nested_router.register(r'messages', MessageViewSet, basename='conversation-messages')

urlpatterns = [
    path('admin/', admin.site.urls),  # Admin panel route
    path('api/', include(router.urls)),  # API routes
    path('api/', include(nested_router.urls)),  # Nested API routes
    path('api-auth/', include('rest_framework.urls')),  # DRF authentication routes
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),  # JWT Token Obtain
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # JWT Token Refresh
]
