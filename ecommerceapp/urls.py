from django.urls import path
from .import views

urlpatterns = [
    path('', views.index, name='index' ),

    path('category/<int:catid>/', views.category, name='category'),
    path('details/<int:proid>/', views.details, name='details'),
    path('search/', views.search, name='search'),
    path('cart/', views.cart_detail, name='cart_detail'),
    path('add/<int:product_id>/', views.add_cart, name='add_cart'),
    path('remove/<int:product_id>/', views.cart_remove, name='cart_remove'),
    path('full_remove/<int:product_id>/', views.full_remove, name='full_remove'),

]