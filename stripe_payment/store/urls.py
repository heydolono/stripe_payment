from django.urls import path
from . import views

urlpatterns = [
    path('buy/<int:id>/', views.create_checkout_session,
         name='create_checkout_session'),
    path('item/<int:id>/', views.item_detail, name='item_detail'),
    path('buy/order/<int:id>/', views.create_order_checkout_session,
         name='buy_order'),
    path('order/<int:order_id>/', views.order_detail, name='order-detail'),
]
