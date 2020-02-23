from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from django.views.generic import View
from .models import *
import bcrypt


class LoginRegistration(View):
    def get(self, request):
        if 'user_id' in request.session:
            if request.session['user_id'] != None:
                return redirect("/")

        campuses = []
        for campus in Campus:
            campuses.append(campus.value)

        context = {
            'campuses': campuses
        }

        return render(request, 'welcome.html', context)

    def catch_errors(self, request, errors):
        messages.error(request, errors)
        return redirect("/")

    def post(self, request):
        if 'register' in request.POST:

            errors = User.objects.register_validator(
                request.POST, request.FILES)

            if len(errors) > 0:
                return self.catch_errors(request, errors.values())

            level = None
            for level_obj in Level:
                if level_obj.value == request.POST['level']:
                    level = level_obj

            campus = None
            for campus_obj in Campus:
                if campus_obj.value == request.POST['campus']:
                    campus = campus_obj

            password = bcrypt.hashpw(
                request.POST['password'].encode(), bcrypt.gensalt()).decode()
            user = User.objects.create(
                first_name=request.POST['first_name'],
                last_name=request.POST['last_name'],
                profile_image=request.FILES['profile_image'],
                email=request.POST['email'],
                password=password, level=level.value, campus=campus.value)

            request.session['user_id'] = user.id
            return redirect("/")

        if 'login' in request.POST:
            errors = User.objects.login_validator(request.POST)

            if len(errors) > 0:
                return self.catch_errors(request, errors.values())

            for user in User.objects.all():
                password_matched = bcrypt.checkpw(
                    request.POST['password'].encode(), user.password.encode())
                if password_matched and (user.email == request.POST['email']):
                    request.session['user_id'] = user.id
                    return redirect("/")

            return self.catch_errors(request, "Password and Email do not match.")

        return redirect("/")
