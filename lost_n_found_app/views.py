from django.shortcuts import render, redirect, HttpResponse
from .models import Item
from login_n_registration_app.models import User, Campus
from django.contrib import messages
from PIL import Image
import enum


# USERS AUTH


def user_logged_in(request):
    if 'user_id' in request.session:
        if request.session['user_id'] != None:
            return True

    return False


def log_out(request):
    request.session.clear()
    return redirect("/")


# VIEWS


def index(request):
    return redirect("/home") if user_logged_in(request) else redirect("/welcome")


def home(request):
    if user_logged_in(request):
        all_users = User.objects.all()
        user_id = request.session['user_id']
        user = all_users.get(id=user_id)

        context = {
            'user': user,
            'users_at_campus': all_users.filter(campus=user.campus).exclude(id=user.id),
            'items': Item.objects.all().order_by("-created_at"),
        }

        request.session['previous_route'] = None
        return render(request, 'home.html', context)

    return redirect("/welcome")


def profile(request, user_id):
    if user_logged_in(request):
        user = User.objects.all().get(id=user_id)

        campuses = []
        for campus in Campus:
            campuses.append(campus.value)

        context = {
            'user': user,
            'items': Item.objects.all().filter(owner=user),
            'campuses': campuses
        }

        request.session['previous_route'] = f"/home/profile/{user_id}"
        return render(request, 'profile.html', context)

    return redirect("/")


def add(request):
    user_id = request.session['user_id']
    user = User.objects.all().get(id=user_id)

    context = {
        'user': user
    }

    return render(request, 'add.html', context)


def add_item(request):
    errors = Item.objects.item_valid(request.POST, request.FILES)

    def create_item():
        owner_id = request.session['user_id']
        owner = User.objects.all().get(id=owner_id)
        name = request.POST['name']
        desc = request.POST['desc']
        image = request.FILES['image']
        item = Item.objects.create(
            name=name, desc=desc, image=image, owner=owner, campus=owner.campus)
        return redirect("/")

    def catch_errors():
        messages.error(request, ", ".join(errors.values()))
        return redirect("/home/add")

    return catch_errors() if len(errors) > 0 else create_item()


def found_item(request, item_id):
    return handle_item(request, item_id, "found")


def unfound_item(request, item_id):
    return handle_item(request, item_id, "unfound")


def remove_item(request, item_id):
    return handle_item(request, item_id, "delete")


def handle_item(request, item_id, action):
    item = Item.objects.all().get(id=item_id)

    def update():
        user_id = request.session['user_id']
        user = User.objects.all().get(id=user_id)

        item.found = True if (action == "found") else False
        item.found_by_whom = user
        item.save()

    item.delete() if action == "delete" else update()

    if 'previous_route' in request.session:
        if request.session['previous_route'] != None:
            return redirect(request.session['previous_route'])

    return redirect("/home")


def update_campus(request):
    if not user_logged_in(request):
        return redirect("/welcome")

    campus = request.GET['campus']
    user_id = request.session['user_id']
    user = User.objects.all().get(id=user_id)
    user.campus = campus
    user.save()
    return HttpResponse("success")
