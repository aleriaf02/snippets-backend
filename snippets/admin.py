from django.contrib import admin
from .models import Snippet, File, Comment

admin.site.register(Snippet)
admin.site.register(File)
admin.site.register(Comment)
