from django.contrib import admin

# Register your models here.
from photoalbum.models import (Comment, Photo, Vote)



@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    list_display = ("like", "voting_photo")


@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    list_display = ("votes", "path", "creation_date", "photo")


admin.site.register(Comment)

