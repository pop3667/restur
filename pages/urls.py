from django.urls import path
from . import views
from django.shortcuts import redirect
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.decorators import user_passes_test
from django.contrib import admin
app_name = "pages"

urlpatterns = [
    path("home/",views.home,name="home"),
    path("", lambda request:redirect("pages:home") ),
    path("add_food_in_cart/",views.add_food_in_cart,name="add_food_in_cart"),
    path("basket/",views.basket,name="basket"),
    path("remove_from_cart/",views.remove_cartitem,name="remove_cartitem"),
    path("succes_payment/",views.sucess_payemnt,name="sucess_payemnt"),
    path("checkout/",views.checkout,name="checkout"),
    path("stripe-webhook/",views.stripe_webhook,name="stripe_webhook"),
    path("book_package/",views.book_package,name="book_package"),
    path("download_PDF_file/",views.download_PDF_file,name="download_PDF_file"),
    path("admin/",user_passes_test(lambda user : user.is_staff )(admin.site.urls)),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
handler404   = "pages.views.page_not_found_erorr"