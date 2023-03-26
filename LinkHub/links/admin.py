from django.contrib import admin
from .models import Project, Theme, Head, Link, Comment


class CustomProject(admin.ModelAdmin):
    list_display = ('id', 'title', 'description', 'created', 'last_edit', 'is_private', 'is_group_project')
    list_filter = ('created',)
    list_editable = ('title', 'description', 'is_private', 'is_group_project')


admin.site.register(Project, CustomProject)