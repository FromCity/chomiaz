"""
URL configuration for chomiaz project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from chat_bot.urls import api_router
from chat_bot import views


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/webhooks/", include(api_router.urls)),
    path("api/users/<str:user_id>/messages", views.Messages),
    path("api/messages/<int:id>", views.MessageDetail),

]
