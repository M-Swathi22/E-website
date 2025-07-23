from django.urls import path
from.import views

urlpatterns =[
    path('',views.main_page,name='main_page'),
    path('home',views.home,name='home'),
    path('register/',views.register_view,name='register'),
    path('login/',views.login_view,name='login'),
    path('logout/',views.logout_view,name='logout'),
    path('products/',views.product_list,name='product'),
    path('products/<int:category_id>/',views.view_products,name='view_products'),
    path('collections/<str:cname>/<str:pname>',views.product_detail,name='product_detail'),
    path('add-to-cart/<int:product_id>/',views.add_to_cart,name='add_to_cart'),
    path('view-cart/',views.view_cart,name='view_cart'),
    path('order/<int:customer_id>/',views.place_order,name='order'),
    path('order/success',views.order_success,name='order_success'),
]

# Create your views here.
