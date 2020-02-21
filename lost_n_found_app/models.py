from django.db import models
from login_n_registration_app.models import User


class ItemManager(models.Manager):
    def item_valid(self, POST, FILES):
        errors = {}

        # POST['name']
        if len(POST['name']) < 3:
            errors['name'] = "Item's name must be longer than 3 characters"

        # POST['desc']
        if len(POST['desc']) < 5:
            errors['desc'] = "Item's description must be longer than 5 characters"

        # FILES['image']
        image_extension = self.get_ext(FILES['image'].name)
        if image_extension not in self.VALID_IMAGE_EXTENSIONS():
            errors['image'] = "Filetype not supported, please upload your image in these formats: JPG, JPEG, PNG, GIF"

        return errors

    def VALID_IMAGE_EXTENSIONS(self):
        return ["jpg", "jpeg", "png", "gif"]

    def get_ext(self, filename):
        ext = ''

        for index in range(len(filename) - 1, -1, -1):
            char = filename[index]
            if char == '.':
                return ''.join(reversed(ext))
            else:
                ext += str(char)

        return ext


class Item(models.Model):
    # NAME, DESCRIPTION, IMAGE, FOUND
    name = models.CharField(max_length=255, null=True)
    desc = models.TextField(blank=True)
    image = models.ImageField(upload_to='images/', null=True)
    found = models.BooleanField(default=False)
    # RELATIONSHIPS
    found_by_whom = models.ForeignKey(
        User, related_name="found_items", on_delete=models.CASCADE, null=True)
    owner = models.ForeignKey(
        User, related_name="items", on_delete=models.CASCADE, null=True)
    # DATETIME
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = ItemManager()
