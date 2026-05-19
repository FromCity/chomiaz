from rest_framework import routers
from . import views

api_router = routers.SimpleRouter()

api_router.register(
    r"messages",
    views.BotViewSet,
    basename="bot_webhook",
    )