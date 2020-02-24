import os
import sys
import re
import enum
from django.db import models
from datetime import datetime
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
from uuid import uuid4


def path_and_rename(instance, filename):
    upload_to = 'profile_images/'
    ext = filename.split('.')[-1]
    if instance.pk:
        filename = '{}.{}'.format(instance.pk, ext)
    else:
        filename = '{}.{}'.format(uuid4().hex, ext)
    return os.path.join(upload_to, filename)


class Level(enum.Enum):
    instructor = "Instructor"
    student = "Student"

    def to_string(self):
        return str(self.value)


class Campus(enum.Enum):
    arlington = "Arlington, VA"
    boise = "Boise, ID"
    chicago = "Chicago, IL"
    dallas = "Dallas, TX"
    los_angeles = "Los Angeles, CA"
    oakland = "Oakland, CA"
    orange_county = "Orange County, CA"
    seatle = "Seatle, WA"
    silicon_valley = "Silicon Valley, CA"
    tulsa = "Tulsa, OK"

    def to_string(self):
        return str(self.value)


class UserManager(models.Manager):
    def EMAIL_REGEX(self):
        return re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

    def VALID_IMAGE_EXTENSIONS(self):
        return ["jpg", "jpeg"]

    def get_ext(self, filename):
        file_ext = ''

        for index in range(len(filename) - 1, -1, -1):
            char = filename[index]
            if char == '.':
                return ''.join(reversed(file_ext))
            else:
                file_ext += str(char)

        return file_ext

    def register_validator(self, POST, FILES):
        errors = {}

        image_extension = self.get_ext(FILES['profile_image'].name)
        if image_extension.lower() not in self.VALID_IMAGE_EXTENSIONS():
            errors['profile_image'] = "Filetype not supported, please upload your image in valid formats. We only support: JPG, JPEG"
        if len(POST['first_name']) < 2:
            errors['first_name'] = "First Name - required; at least 2 characters; letters only"
        if len(POST['last_name']) < 2:
            errors['last_name'] = "Last Name - required; at least 2 characters; letters only"

        if len(POST['level']) < 0:
            errors['level'] = "Level - required; Please identify yourself as Student or Instructor"
        if len(POST['campus']) < 0:
            errors['level'] = "Campus - required; Please select campus that you're currently attending"

        if not self.EMAIL_REGEX().match(POST['email']):
            errors['email'] = "Invalid email address!"

        if len(POST['password']) < 8:
            errors['password'] = "Password - required; at least 8 characters;"
        if POST['password'] != POST['confirm_pw']:
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
    profile_image = models.ImageField(upload_to=path_and_rename, null=True)
    first_name = models.CharField(max_length=255, null=True)
    last_name = models.CharField(max_length=255, null=True)
    level = models.CharField(max_length=255, choices=[
                             (tag, tag.value) for tag in Level], null=True)
    campus = models.CharField(max_length=255, choices=[
                              (tag, tag.value) for tag in Campus], null=True)
    email = models.CharField(max_length=255, null=True)
    password = models.CharField(max_length=255, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

    def save(self, *args, **kwargs):
        if not self.id:
            self.profile_image = self.compress(self.profile_image)
        super().save(*args, **kwargs)

    def compress(self, uploadedImage):
        imageTemproary = Image.open(uploadedImage)
        outputIoStream = BytesIO()
        imageTemproaryResized = imageTemproary.resize((2048, 2048))
        imageTemproary.save(outputIoStream, format='JPEG', quality=75)
        outputIoStream.seek(0)
        uploadedImage = InMemoryUploadedFile(outputIoStream, 'ImageField', "%s.jpg" % uploadedImage.name.split('.')[
                                             0], 'image/jpeg', sys.getsizeof(outputIoStream), None)
        return uploadedImage
