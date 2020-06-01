from django.urls import path
from receipt.api import views

urlpatterns = [
    path('receipts/', views.ReceiptList.as_view()),
    path('receipts/<int:pk>/', views.ReceiptDetail.as_view()),
]