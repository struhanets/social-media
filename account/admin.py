from django.contrib import admin

from account.models import Profile, Post, Comment, Reaction

admin.site.register(Profile)
admin.site.register(Post)
admin.site.register(Reaction)
admin.site.register(Comment)
