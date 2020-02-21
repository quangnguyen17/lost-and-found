from django.db import models
from datetime import datetime
import re


class UserManager(models.Manager):
    def EMAIL_REGEX(self):
        return re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

    def register_validator(self, data):
        errors = {}

        if len(data['name']) < 2:
            errors['name'] = "Name - required; at least 8 characters; letters only"
        if not self.EMAIL_REGEX().match(data['email']):
            errors['email'] = "Invalid email address!"
        if len(data['password']) < 8:
            errors['password'] = "Password - required; at least 8 characters;"
        if data['password'] != data['confirm_pw']:
            errors['confirm_pw'] = "Passwords don't match, matches password confirmation"

        return errors

    def login_validator(self, data):
        errors = {}

        if not self.EMAIL_REGEX().match(data['email']):
            errors['email'] = "Invalid email address!"
        if len(data['password']) < 8:
            errors['password'] = "Password - required; at least 8 characters;"

        return errors


class User(models.Model):
    name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    # DATETIME
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()
