from django.urls import path
from loyaltycard.api import views

urlpatterns = [
    path('loyaltycards/', views.LoyaltycardList.as_view()),
    path('loyaltycards/<int:pk>/', views.LoyaltycardDetail.as_view()),
    path('loyaltycards/image/<int:loyaltycard_id>/', views.get_loyaltycard_image),
    path('loyaltycards/share/<int:loyaltycard_id>/<str:username>/', views.share_loyalty_card),
]