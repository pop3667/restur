from django.db import models
from django.core.validators import MinValueValidator,MaxValueValidator
import uuid
from django.contrib.auth.models import User
import datetime
import decimal
class Food(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    price_before_discount = models.DecimalField(max_digits=5,decimal_places=2)
    discount = models.PositiveSmallIntegerField(validators=[
        MinValueValidator(0),MaxValueValidator(99)
    ])
    image = models.ImageField(upload_to="food/%y/%m/%d")
    show_in_home = models.BooleanField(default=False)
    icon_description  = models.CharField(choices=[("fire","fire"),("leaf","leaf"),("check-circle","check-circle"),("star-fill","star-fill")])
    created = models.DateTimeField(auto_now_add=True)
    special_badge  =  models.CharField(max_length=20,blank=True,null=True)
    tag  = models.CharField(choices=[("vegetarian","vegetarian"),("spicy","spicy"),("gluten-free","gluten-free"),("premium","premium")])
    category = models.CharField(choices=[("starters","starters"),("main courses","main courses"),("desserts","desserts"),("beverages","beverages")])
    @property
    def price_after_discount(self):
        if self.discount != 0:
            return round(float(self.price_before_discount)-( float(self.price_before_discount) * (self.discount/100)),2)
        return  decimal.Decimal(str(self.price_before_discount))
    class Meta:
        ordering = ["-created"]
        indexes = [
            models.Index(fields=["-created"])
        ]

class Chef(models.Model):
    name = models.CharField(max_length=50)
    work = models.CharField(max_length=30)
    description = models.TextField()
    image = models.ImageField(upload_to="chefs/%y/%m/%d")
    is_executive_chef = models.BooleanField()
    years_of_work = models.PositiveIntegerField()
    chef_quote=models.TextField(null=True,blank=True)
    signature  = models.ImageField(upload_to="signatures/%y/%m/%d",null=True,blank=True)
    @property
    def from_year(self):
        return datetime.datetime.now().year - self.years_of_work


class Awards(models.Model):
    title = models.CharField(max_length=30)
    icon = models.CharField(choices=[("award","award"),("star","star"),("trophy-fill","trophy-fill")])
    chefs = models.ForeignKey(to=Chef,on_delete=models.PROTECT,related_name="awards")

class  Link(models.Model):
    link_it_self = models.CharField(max_length=1000)
    icon = models.CharField(choices=[("instagram","instagram"),("linkedin","linkedin")])
    chefs = models.ForeignKey(to=Chef,on_delete=models.CASCADE,related_name="links")

class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,related_name="profile")
    address = models.CharField(max_length=400)
    phone_number = models.CharField(max_length=15)


class Cart(models.Model):
    owner = models.OneToOneField(User, on_delete=models.CASCADE, related_name="cart")
    id= models.UUIDField(primary_key=True,unique=True,default=uuid.uuid4,auto_created=True,editable=False)
    @property
    def total_price(self):
        return sum([ item.total_price for item in CartItems.objects.filter(cart_id=self.id)])
class  Order(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="orders")
    id= models.UUIDField(primary_key=True,unique=True,default=uuid.uuid4,auto_created=True,editable=False)
class  CartItems(models.Model):

    cart = models.ForeignKey(Cart,on_delete=models.PROTECT,related_name="cartitems")
    food = models.ForeignKey(Food,on_delete=models.PROTECT)
    quntatiy = models.PositiveSmallIntegerField(validators=[
        MinValueValidator(1),MaxValueValidator(1000)
    ])
    @property
    def total_price(self):
        return round(decimal.Decimal(self.food.price_after_discount  * self.quntatiy),2)
    
class  OrderItems(models.Model):
    order = models.ForeignKey(Order,on_delete=models.PROTECT,related_name="orderitems")
    food = models.ForeignKey(Food,on_delete=models.PROTECT)
    quntatiy = models.PositiveSmallIntegerField(validators=[
        MinValueValidator(1),MaxValueValidator(1000)
    ])

class ResturFeatures(models.Model):
    title = models.CharField(max_length=1000)
    description = models.TextField()
    image  = models.ImageField(upload_to="restur-features/%y/%m/%d")

class imageGallery(models.Model):
    image = models.ImageField(upload_to="gallery/%y/%m/%d")
    description = models.TextField(default="hello")
    name = models.CharField(max_length=30)
    category = models.CharField(max_length=40)

class TableBooking(models.Model):
    user = models.ForeignKey(to=User,on_delete=models.PROTECT,related_name="table_booking",default=1)
    full_name = models.CharField(max_length=80,default="S")
    email = models.EmailField(default="NO")
    number_of_people = models.PositiveSmallIntegerField(validators=[
        MinValueValidator(1),MaxValueValidator(500)
    ])
    phone_number=models.CharField(max_length=15)
    reservation_date=models.DateField()
    reservation_Time = models.TimeField()
    special_requests = models.TextField()




class Package(models.Model):
    category = models.CharField(max_length=80)
    price = models.PositiveSmallIntegerField(validators=[
        MinValueValidator(1),MaxValueValidator(10000)
    ],default=20)
    icon  = models.CharField(max_length=30,default="star")
    capacity_from = models.PositiveSmallIntegerField(validators=[
        MinValueValidator(1),MaxValueValidator(10000)
    ],default=1)
    capacity_to = models.PositiveSmallIntegerField(validators=[
        MinValueValidator(1),MaxValueValidator(10000)
    ],default=10)
    fetures = models.JSONField(default=list)
    most_popular = models.BooleanField()
    per = models.CharField(max_length=50)
    class Meta:
        ordering = ["id"]
        indexes = [
            models.Index(fields=["id"])
        ]

class BookPackage(models.Model):
    user = models.ForeignKey(User,models.PROTECT,)
    package = models.ForeignKey(Package,models.PROTECT,related_name="package")

class Event(models.Model):
    name = models.CharField(max_length=70)
    image = models.ImageField(upload_to="events/%y/%m/%d")





