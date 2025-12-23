from django.shortcuts import render,redirect
from .forms import UserCreateForm
from django.contrib.auth import login
from pages.models import Cart,Profile
def signup(request):
    if request.method == "POST":
        form = UserCreateForm(request.POST)
        if form.is_valid():
            user = form.save()
            Cart.objects.create(owner = user)
            Profile.objects.create(
                user = user,
                address=form.cleaned_data["address"],
                phone_number=form.cleaned_data["phone_number"])
            login(request,user=user)

            return redirect("/")
    else:
        form = UserCreateForm()
    return render(request,"accounts/signup.html",{"form":form})

