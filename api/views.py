from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet,ReadOnlyModelViewSet,GenericViewSet
from rest_framework.mixins import RetrieveModelMixin,CreateModelMixin,ListModelMixin
from pages import models
from . import serializers_page
from rest_framework.pagination import PageNumberPagination
class  FoodViewSet(ModelViewSet):
    queryset = models.Food.objects.all()
    serializer_class = serializers_page.FoodSerializer
    pagination_class = PageNumberPagination

class  ChefViewSet(ModelViewSet):
    queryset = models.Chef.objects.all()
    serializer_class = serializers_page.ChefSerializer
    pagination_class = PageNumberPagination

class  AwardsViewSet(ModelViewSet):
    queryset = models.Awards.objects.all()
    serializer_class = serializers_page.AwardsSerializer
    pagination_class = PageNumberPagination

class  LinkViewSet(ModelViewSet):
    queryset = models.Link.objects.all()
    serializer_class = serializers_page.LinkSerializer
    pagination_class = PageNumberPagination

class  ResturFeaturesViewSet(ModelViewSet):
    queryset = models.ResturFeatures.objects.all()
    serializer_class = serializers_page.ResturFeaturesSerializer
    pagination_class = PageNumberPagination

class  imageGalleryViewSet(ModelViewSet):
    queryset = models.imageGallery.objects.all()
    serializer_class = serializers_page.imageGallerySerializer
    pagination_class = PageNumberPagination

class EventViewSet(ModelViewSet):
    queryset = models.Event.objects.all()
    serializer_class = serializers_page.EventSerializer

class PackageViewSet(GenericViewSet,ListModelMixin,RetrieveModelMixin,CreateModelMixin):
    queryset = models.Package.objects.all()
    serializer_class = serializers_page.PackageSerializer
    pagination_class = PageNumberPagination
    

class CartViewSet(RetrieveModelMixin,ListModelMixin,GenericViewSet):
    serializer_class = serializers_page.Cartserializer
    def get_queryset(self):
        if self.request.user.is_staff:
            return models.Cart.objects.all()
        return models.Cart.objects.filter(owner_id = self.request.user.id)
    
# models.Profile(
#                 address = request.data["address"],
#                 phone_number = request.data["phone_number"],
#                 user = self.request.user
#             ).save()
class ProfileViewSet(ListModelMixin,RetrieveModelMixin,CreateModelMixin,GenericViewSet):
    serializer_class = serializers_page.Profileserializer
    def get_queryset(self):
        if self.request.user.is_staff:
            return models.Profile.objects.all()
        return models.Profile.objects.filter(user_id = self.request.user.id)


    
    
class OrderViewSet(RetrieveModelMixin,ListModelMixin,CreateModelMixin,GenericViewSet):
    serializer_class = serializers_page.Orderserializer
    
    def get_queryset(self):
        if self.request.user.is_staff:
            return models.Order.objects.all()
        return self.request.user.orders.all()

    

class CartItemsViewSet(ModelViewSet):

    serializer_class = serializers_page.CartItemsserializer
    def get_queryset(self):
        return self.request.user.cart.cartitems.all()
    
class TableBookingViewSet(ModelViewSet):

    serializer_class = serializers_page.TableBookingserializer
    def get_queryset(self):
        if self.request.user.is_staff:
            return models.TableBooking.objects.all()
        return self.request.user.table_booking.all()
    
class OrderItemsViewSet(ModelViewSet):
    serializer_class = serializers_page.OrderItemsserializer

    def get_queryset(self):
        return models.OrderItems.objects.filter(order_id = self.kwargs["nested_1_pk"])