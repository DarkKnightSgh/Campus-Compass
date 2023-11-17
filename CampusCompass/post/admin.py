from django.contrib import admin

# Register your models here.
from .models import Post
from .models import PostComment

admin.site.register(Post)
admin.site.register(PostComment)
