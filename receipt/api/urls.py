from django.urls import path
from receipt.api import views

urlpatterns = [
    path('receipts/', views.ReceiptList.as_view()),
    path('receipts/<int:pk>/', views.ReceiptDetail.as_view()),
    path('receipts/image/<int:receipt_id>/', views.get_receipt_image),
    path('receipts/thumbnail/<int:receipt_id>/', views.get_thumbnail_image),
]