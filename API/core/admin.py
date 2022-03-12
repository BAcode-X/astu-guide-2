from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, QuestionPost, AnswerPost, BlogPost, Location

# Register your models here.

class CustomUserAdmin(UserAdmin):
    ordering = ["id"]
    list_display = [
        "username",
        "first_name",
        "last_name",
        "email",
        "reputation",
        "is_admin",
        "is_superuser",
    ]
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "username",
                    "first_name",
                    "last_name",
                    "password",
                    "email",
                    "reputation",
                    "is_admin",
                    "is_superuser",
                ),
            },
        ),
    )


admin.site.register(User, CustomUserAdmin)
admin.site.register(QuestionPost)
admin.site.register(AnswerPost)
admin.site.register(BlogPost)
admin.site.register(Location)