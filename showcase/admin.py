from django.contrib import admin
from .models import Category, Project, ProjectImage, Contact  # Import the new model

# This lets you upload multiple images inside the Project page
class ProjectImageInline(admin.TabularInline):
    model = ProjectImage
    extra = 1

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'is_featured', 'completed_date')
    list_filter = ('category',)
    inlines = [ProjectImageInline]

admin.site.register(Category)


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'email', 'sent_at') # Columns to show in the list
    search_fields = ('name', 'phone') # Adds a search bar
    list_filter = ('sent_at',) # Adds a filter sidebar by date
    readonly_fields = ('name', 'email', 'phone', 'message', 'sent_at') # Protects data from being changed accidentally

