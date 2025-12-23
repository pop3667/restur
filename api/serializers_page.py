from rest_framework import serializers
from pages import models
from django.contrib.auth.models import User
from rest_framework.exceptions import ValidationError

class USerSerialize(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username","first_name","last_name","email"]

class FoodSerializer(serializers.ModelSerializer):
    price_after_discount = serializers.DecimalField(read_only=True,max_digits=12,decimal_places=2)
    class Meta:
        fields = ["title","description","price_before_discount","discount","image","show_in_home","icon_description","created","special_badge","tag","category","price_after_discount","pk"]
        model = models.Food
        
class ChefSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ["name","work","description","image","is_executive_chef","years_of_work","chef_quote","signature","from_year","pk"]
        model = models.Chef

class AwardsSerializer(serializers.ModelSerializer):
    class Meta:
        fields = "__all__"
        model = models.Awards
        
class LinkSerializer(serializers.ModelSerializer):
    class Meta:
        fields = "__all__"
        model = models.Link

class ResturFeaturesSerializer(serializers.ModelSerializer):
    class Meta:
        fields = "__all__"
        model = models.ResturFeatures

class imageGallerySerializer(serializers.ModelSerializer):
    class Meta:
        fields = "__all__"
        model = models.imageGallery

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        fields = "__all__"
        model = models.Event

class PackageSerializer(serializers.ModelSerializer):
    class Meta:
        fields = "__all__"
        model = models.Package
    def create(self, validated_data):
        if not self.context["request"].user.is_staff:
            raise ValidationError("you are not allowed  to create order")
        return super().create(validated_data)
    def update(self, instance, validated_data):
        if not self.context["request"].user.is_staff:
            raise ValidationError("you are not allowed  to update order")
        return super().update(instance, validated_data)
class Cartserializer(serializers.ModelSerializer):
    id = serializers.UUIDField()
    class Meta:
        fields = ["owner","id","total_price"]
        model = models.Cart

class TableBookingserializer(serializers.ModelSerializer):
    class Meta:
        fields = "__all__"
        model = models.TableBooking
    def create(self, validated_data):
        if not self.context["request"].user.is_staff:
            raise ValidationError("you are not allowed  to create order")
        return super().create(validated_data)
    def update(self, instance, validated_data):
        if not self.context["request"].user.is_staff:
            raise ValidationError("you are not allowed  to update order")
        return super().update(instance, validated_data)

class Orderserializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only = True)
    class Meta:
        fields = "__all__"
        model = models.Order
    def create(self,validated_data):
        if not self.context["request"].user.is_staff:
            raise ValidationError("you are not allowed  to create order")
        return super().create(validated_data)
    def update(self, instance, validated_data):
        if not self.context["request"].user.is_staff:
            raise ValidationError("you are not allowed  to update order")
        return super().update(instance, validated_data)

class CartItemsserializer(serializers.ModelSerializer):
    class Meta:
        fields = ["cart","food","quntatiy","total_price","id"]
        model = models.CartItems

class OrderItemsserializer(serializers.ModelSerializer):
    class Meta:
        fields = "__all__"
        model = models.OrderItems

class Profileserializer(serializers.ModelSerializer):
    user = USerSerialize(read_only = True)
    class Meta:     
        fields = "__all__"
        model = models.Profile
    def create(self, validated_data):
        validated_data["user_id"] = self.context["request"].user.id
        the_user = models.Profile.objects.filter(user_id = self.context["request"].user.id)
        if not  the_user:
            the_user =  super().create(validated_data)
        return the_user
    
        
    
