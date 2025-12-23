from django.urls import path,include
from . import  views
from rest_framework.routers import DefaultRouter
from rest_framework_nested.routers import NestedSimpleRouter
router = DefaultRouter()

router.register("food",views.FoodViewSet,"food")
router.register("chef",views.ChefViewSet,"chef")
router.register("award",views.AwardsViewSet,"award")
router.register("link_of_chef",views.LinkViewSet,"link_of_chef")
router.register("restur_fetures",views.ResturFeaturesViewSet,"restur_fetures"),
router.register("image_gallery",views.imageGalleryViewSet,"image_gallery"),
router.register("event",views.EventViewSet,"event"),
router.register("package",views.PackageViewSet,"package"),
router.register("cart",views.CartViewSet,"cart"),
router.register("order",views.OrderViewSet,"order"),
router.register("table_booking",views.TableBookingViewSet,"table_booking"),
router.register("profiles",views.ProfileViewSet,"profiles"),

cart_router = NestedSimpleRouter(router,"cart")
cart_router.register("items",views.CartItemsViewSet,"items")

order_router = NestedSimpleRouter(router,"order")
order_router.register("items",views.OrderItemsViewSet,"items")


urlpatterns = [
    path("",include(router.urls)),
    path("",include(cart_router.urls)),
    path("",include(order_router.urls))
]