from django.contrib import admin
from .models import Project, ProjectImage, ProjectTag,Comment,Rate
# Register your models here.


admin.site.register(Project)
admin.site.register(ProjectImage)
admin.site.register(ProjectTag)

admin.site.register(Rate)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'body', 'proj', 'created_on', 'active')
    list_filter = ('active', 'created_on')
    search_fields = ('name', 'email', 'body')
    actions = ['approve_comments']

    def approve_comments(self, request, queryset):
        queryset.update(active=True)



class ReviewAdmin(admin.ModelAdmin):
    model = Rate
    list_display = ('rating',)