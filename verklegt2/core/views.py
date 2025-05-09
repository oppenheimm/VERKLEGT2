from django.shortcuts import render, redirect
from item.models import Item, Category
from .forms import SignUpForm
from property.models import Property
from django.contrib.auth import logout


def index(request):
    properties = Property.objects.filter(is_published=True, is_sold=False)[:6]
    categories = Category.objects.all()
    context = {
        "featured_properties": properties,
        "categories": categories,
    }
    return render(request, "core/index.html", context)


def contact(request):
    return render(request, "core/contact.html")


def signup(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("/login/")
    else:
        form = SignUpForm()  # <- Correct capitalization

    return render(request, "core/signup.html", {"form": form})


def logout_view(request):
    logout(request)
    return redirect('core:index')