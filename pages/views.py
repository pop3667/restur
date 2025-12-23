from django.shortcuts import render
from .models import  Food,Chef,ResturFeatures
from django.http import JsonResponse
import json
from django.http import FileResponse
from django.views.decorators.csrf import csrf_exempt
from . import models
from django.urls import reverse
from django.core.serializers import serialize
import json
import stripe
from django.conf import  settings
from django.core.mail import send_mail
import termcolor
from django.http import HttpResponse
import os
stripe.api_key = settings.STRIPE_SECRET_KEY

def home(request):
    if request.method == "POST":
        termcolor.cprint("hello","red")
        
        if request.POST.get("task")  == "Reserve Your Table Today":
            subject  = f"A request from Savora is Reserve Your Table Today "
            message = f'''
            from { request.POST.get("full-name")},
            his phone number is {request.POST.get("phone-number")} , 
            his email is {request.POST.get("email")}
            and he book table of {request.POST.get("number-of-people")}
            his special request is {request.POST.get("special-request") if request.POST.get("special-request") else "No"}
            and reservation date and time is {request.POST.get("date")} ,
            time is {request.POST.get("time")}
            '''
            send_mail(subject,message,f"from {request.POST.get("full-name")} ",["yaljmly4@gmail.com"])
            models.TableBooking.objects.create(
                user = request.user,
                full_name = request.POST.get("full-name"),
                email = request.POST.get("email"),
                number_of_people = int(request.POST.get("number-of-people")),
                reservation_date = request.POST.get("date"),
                reservation_Time = request.POST.get("time"),
                special_requests= request.POST.get("special-request"),
                phone_number = request.POST.get("phone-number")
            )
        elif request.POST.get("task") == 'Plan Your Next Event':
            subject  = f"A request from Savora is Plan Your Next Event "
            message = f'''
            from { request.POST.get("name")},
            his phone number is {request.POST.get("phone")} , 
            his email is {request.POST.get("email")}
            and he book table of {request.POST.get("guest_count")}
            his event type is {request.POST.get("event_type")}
            and reservation date  {request.POST.get("date")} ,
            message is {request.POST.get("message")}
            '''
            send_mail(subject,message,f"from {request.POST.get("full-name")} ",["yaljmly4@gmail.com"])
        elif request.POST.get("task") == 'contact':
            subject  = f"A request from Savora is contact "
            message = f'''
            from { request.POST.get("name")},,
            his email is {request.POST.get("email")}
            his subject is {request.POST.get("subject")} ,
            message is {request.POST.get("message")}
            '''
            send_mail(subject,message,f"from {request.POST.get("full-name")} ",["yaljmly4@gmail.com"])



    chefs = Chef.objects.all()
    two_excutive_chefs = Chef.objects.filter(is_executive_chef=True).order_by("-years_of_work")[:2]
    url_of_add_in_basket = f"{request.scheme}://{request.get_host()}{reverse("pages:add_food_in_cart")}"
    food_starters = Food.objects.filter(category = "starters")
    food_main_courses= Food.objects.filter(category = "main courses")
    food_desserts = Food.objects.filter(category = "desserts")
    food_beverages = Food.objects.filter(category = "beverages")
    gallery_items = models.imageGallery.objects.all()
    with open(r"D:\work\يحيي\Savora\restur\about_resturant.json", 'r') as f:
        about_resturnt = json.load(f) 

    
   

    return render(request,"pages/home.html",{
        "food_starters_json":serialize("json",food_starters),
        "food_main_courses_json":serialize("json",food_main_courses),
        "food_desserts_json":serialize("json",food_desserts),
        "food_beverages_json":serialize("json",food_beverages),
        "food_starters":food_starters[:5],
        "food_main_courses":food_main_courses[:5],
        "food_desserts":food_desserts[:5],
        "food_beverages":food_beverages[:5],
        "two_excutive_chefs":two_excutive_chefs
        ,"url_of_add_in_basket":url_of_add_in_basket,
        "chefs":chefs,
        "three_foods_in_home":Food.objects.filter(show_in_home = True)[:3],
        "restur_featuers":ResturFeatures.objects.all(),
        "packages":models.Package.objects.all(),
        "request":request,
        "about_resturnt":about_resturnt,
        "gallery_items":gallery_items,
        "events":models.Event.objects.all(),
        "packages_are_bought":models.BookPackage.objects.filter(user=request.user) if request.user.is_authenticated else {},

        })

@csrf_exempt
def  add_food_in_cart(request):
    if request.method =="POST":
            the_food_id = json.loads(request.body).get("food_id")
            cart = request.user.cart
            try:
                cartitem = models.CartItems.objects.get(cart=cart,food_id=the_food_id)
                cartitem.quntatiy +=1
                cartitem.save()
            except:
                models.CartItems(cart=cart,food_id=the_food_id,quntatiy=1).save()
    return JsonResponse({"message":"hello!"})

def basket(request):
    foods = request.user.cart.cartitems.all()
    href_remove_from_cart = f"{request.scheme}://{request.get_host()}{reverse("pages:remove_cartitem")}"
    href_of_check_out = f"{request.scheme}://{request.get_host()}{reverse("pages:checkout")}"
    return render(request,"pages/basket.html",{"foods":foods,"href_remove_from_cart":href_remove_from_cart,"href_of_check_out":href_of_check_out})
@csrf_exempt
def remove_cartitem(request):
    if request.method == "POST":
        cartitem_id = json.loads(request.body).get("id")
        models.CartItems.objects.get(id=cartitem_id).delete()
        return JsonResponse({"message":"it removed"})

    
@csrf_exempt
def checkout(request):

    sucess_url = f"{request.scheme}://{request.get_host()}{reverse("pages:sucess_payemnt")}"
    session = stripe.checkout.Session.create(
        mode="payment",
        line_items=[
            {
                "price_data":{
                    "currency":"usd",
                    "product_data":{
                        "name":"savora"
                    },
                    "unit_amount":int(request.user.cart.total_price* 100),

                },
                "quantity":1
            },
        ],
        success_url=sucess_url,
        metadata={"user_id":request.user.id,"task":"order"}

    )
    return JsonResponse({"url":session.url})

def sucess_payemnt(request):
    return JsonResponse({"SDSD":"SDSD"})

@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.headers["Stripe-Signature"]
    secret_key = settings.WEBHOOK_SECRET_KEY
    event = stripe.Webhook.construct_event(payload,sig_header,secret_key)
    user = models.User.objects.get(id=event["data"]["object"]["metadata"]["user_id"])

    
    if event["type"] == "checkout.session.completed":
        if event["data"]["object"]["metadata"]["task"] == "order":
            termcolor.cprint("hello","blue")

            order = models.Order.objects.create(owner_id = event["data"]["object"]["metadata"]["user_id"])
            orderitems = [
                models.OrderItems(
                order= order
                ,food = item.food
                ,quntatiy = item.quntatiy
            ) for item in models.CartItems.objects.filter(cart = models.Cart.objects.get(owner=user)) 
            ]
            models.OrderItems.objects.bulk_create(orderitems)
            models.CartItems.objects.filter(cart = models.Cart.objects.get(owner=user)).delete()
            subject  = f"A request from Savora is order "
            message = f'''
            from { user.first_name + user.last_name},
            his email is {user.email} and his address is {user.profile.address}
            '''
            send_mail(subject,message,f"User {user.email}",["yaljmly4@gmail.com"])
        elif event["data"]["object"]["metadata"]["task"] == "book_package":
            termcolor.cprint("hello","green")

            package_id = event["data"]["object"]["metadata"]["package_id"]
            models.BookPackage(
                user = user,
                package_id = package_id
            ).save()
            subject  = f"A request from Savora is Book Package "
            message = f'''
                from { user.username}, 
                his email is {user.email}
                and his address is {user.profile.address}
                '''
            send_mail(subject,message,f"User {user.email}",["yaljmly4@gmail.com"])

    return HttpResponse(status=200)
    
@csrf_exempt
def book_package(request):
    if request.method == "POST":
        package =  models.Package.objects.get(id = json.loads(request.body).get("package_id"))
        sucess_url = f"{request.scheme}://{request.get_host()}{reverse("pages:sucess_payemnt")}"
        session = stripe.checkout.Session.create(
            mode="payment",
            line_items=[
                {
                    "price_data":{
                        "currency":"usd",
                        "product_data":{
                            "name":"savora"
                        },
                        "unit_amount":int(package.price* 100),

                    },
                    "quantity":1
                },
            ],
            success_url=sucess_url,
            metadata={"user_id":request.user.id,"package_id":json.loads(request.body).get("package_id"),"task":"book_package"}

    )
    return JsonResponse({"url":session.url})


def download_PDF_file(request):
    return FileResponse(open(os.path.join(settings.BASE_DIR,"menu.pdf"),"rb"),as_attachment=True,filename="menu.pdf")



def  page_not_found_erorr(request,exception):
    return render(request,"404.html",status=404)