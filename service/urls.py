from django.urls import path
from service.views import ServiceDetailsView, add_to_cart, CartAllItemsView, Cartview, CancelServiceView,AdminCancelServiceView,confirm_oder

urlpatterns = [
    path('service/<int:id>/details/', ServiceDetailsView.as_view(), name='details'),
    path('service/<int:id>/add_review/', ServiceDetailsView.as_view(), name='review'),
    path('service/<int:id>/add_to_cart/', add_to_cart, name='add_to_cart'),
    path('cart_items/', CartAllItemsView.as_view(), name='cart_items'),
    path('cart/', Cartview.as_view(), name='cart'),
    path('service/<int:pk>/cancel_service/', CancelServiceView.as_view(), name='cancel'),
    path('service/<int:pk>/delete_service/', AdminCancelServiceView.as_view(), name='admin_cancel'),
    path('service/<int:id>/confirm_service/', confirm_oder, name='confirm'),
]
