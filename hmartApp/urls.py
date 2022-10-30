from django.urls import path
from .views import delete_wishlist, delete_cart, detail_brand, home, about, cart, checkout, shop, contact, update_cart, wishlist, detail_product, detail_category, add_cart, add_wishlist

urlpatterns = [
    path('', home, name='home'),
    path('about/', about, name='about'),
    path('cart/', cart, name='cart'),
    path('checkout/', checkout, name='checkout'),
    path('shop/', shop, name='shop'),
    path('contact/', contact, name='contact'),
    path('wishlist/', wishlist, name='wishlist'),
    path('single_product/<int:pk>/', detail_product, name='single_product'),
    path('detail_category/<int:pk>/', detail_category, name='detail_category'),
    path('detail_brand/<int:pk>/', detail_brand, name='detail_brand'),
    path('delete_cart/<int:pk>/', delete_cart, name='delete_item'),
    path('add_cart/<int:pk>/', add_cart, name='add_cart'),
    path('add_wishlist/<int:pk>/', add_wishlist, name='add_wishlist'),
    path('delete_wishlist/<int:pk>/', delete_wishlist, name='delete_wishlist'),
    path('update_cart/<int:pk>/', update_cart, name='update_cart'),
    
    
]