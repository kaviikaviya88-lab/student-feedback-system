from django.contrib import admin
from django.contrib.auth.models import Group
from .models import Feedback

admin.site.unregister(Group)

@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):

    list_display = (
        'name',
        'degree',
        'year',
        'course',
        'overall_rating',
        'timestamp'
    )

    list_filter = (
        'degree',
        'year',
        'course',
        'overall_rating',
    )

    search_fields = (
        'name',
        'course',
        'comment'
    )

    readonly_fields = (
        'timestamp',
    )

    list_per_page = 20