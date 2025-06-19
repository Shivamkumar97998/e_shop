"""
URL configuration for e_shops project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from app.views import *
from django.conf.urls.static import static      
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path("",homepage),

    #category view 
    path("create/",Create_category,name='create_category'),
    path("category/edit/<int:id>/",edit_category,name="edit_category"),
    path("category/delete/<int:id>/",delete_cat,name="delete_Cat"),

    #subcategory view
    path("sub_category/<int:id>/",sub_category,name="sub_category"),
    path("create_subcategory/<int:id>/",create_subcategory,name="create_subcategory"),
    path("edit_sub_cat/<int:subcategory_id>/",edit_sub_cat,name="edit_sub_cat"),

    #product page
    path("create_product/<int:subcategory_id>/",create_product,name="create_product"),
    path("products_list_page/<int:subcategory_id>/",product_list_page),
    path("product_detail/<int:product_id>/",product_detail,name="product_detail"),

    

    # cart option 
    path("add_to_cart/<int:product_id>/",add_to_cart,name="add_to_cart"),
    path("cart/",view_cart,name="cart"),

    #order urls
    path('order/', proceed_order, name="proceed_order"),
    path("buy-now/<int:product_id>/",Buy_Now,name="buy-now"),
    path("order/confirmation/<int:order_id>/",order_confirmation,name="order_confirmation"),
    path("product/<int:product_id>/add_review/",add_review,name="add_review"),


    #get profile
    path("profile/",get_pro),

    #user authentications view
    path("create_user/",createuser,name='createuser'),
    path("login/",userlogin),
    path("logout/",userlogout,name='userlogout'),


]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 
 

   