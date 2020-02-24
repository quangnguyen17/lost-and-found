import os
import sys
import datetime
from django.db import models
from login_n_registration_app.models import User, Campus
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
from uuid import uuid4


def path_and_rename(instance, filename):
    upload_to = 'images/'
    ext = filename.split('.')[-1]
    if instance.pk:
        filename = '{}.{}'.format(instance.pk, ext)
    else:
        filename = '{}.{}'.format(uuid4().hex, ext)
    return os.path.join(upload_to, filename)


class ItemManager(models.Manager):
    def item_valid(self, POST, FILES):
        errors = {}

        if len(POST['name']) < 3:
            errors['name'] = "Item's name must be longer than 3 characters"
        if len(POST['desc']) < 5:
            errors['desc'] = "Item's description must be longer than 5 characters"
        image_extension = self.get_ext(FILES['image'].name)
        if image_extension.lower() not in self.VALID_IMAGE_EXTENSIONS():
            errors['image'] = "Filetype not supported, please upload your image in valid formats. We only support: JPG, JPEG"

        return errors

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


class Item(models.Model):
    name = models.CharField(max_length=255, null=True)
    desc = models.TextField(blank=True)
    image = models.ImageField(upload_to=path_and_rename, null=True)
    found = models.BooleanField(default=False)

    found_by_whom = models.ForeignKey(
        User, related_name="found_items", on_delete=models.CASCADE, null=True)
    owner = models.ForeignKey(
        User, related_name="items", on_delete=models.CASCADE, null=True)
    campus = models.CharField(max_length=255, choices=[
                              (tag, tag.value) for tag in Campus], null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = ItemManager()

    def save(self, *args, **kwargs):
        if not self.id:
            self.image = self.compress(self.image)
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
