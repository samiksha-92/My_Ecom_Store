from django.urls import path
from . import views

urlpatterns = [
   path('',views.all_products,name = 'products'),
   path('product/<int:pk>/',views.product_detail, name = 'product_detail'),
   path('product/product_management/', views.product_management, name='product_management'),
    path('add/', views.add_product, name='add_product'),
    path('update_product/<int:product_id>/', views.update_product, name='update_product'),
    path('delete_product/<int:product_id>/', views.delete_product, name='delete_product'),
    path('create_review/<int:product_id>/', views.create_review, name='create_review'),
    path('update_review/<int:review_id>/', views.update_review, name='update_review'),
    path('delete_review/<int:review_id>/', views.delete_review, name='delete_review'),
   
]