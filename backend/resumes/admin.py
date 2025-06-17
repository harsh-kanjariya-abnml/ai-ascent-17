from django.contrib import admin
from .models import CandidateProfile

# Register your models here.

@admin.register(CandidateProfile)
class CandidateProfileAdmin(admin.ModelAdmin):
    list_display = ['name', 'fe_score', 'be_score', 'seniority', 'qualifications', 'created_at']
    list_filter = ['seniority', 'qualifications', 'created_at']
    search_fields = ['name', 'skills']
    readonly_fields = ['id', 'created_at', 'updated_at']
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'skills')
        }),
        ('Scores', {
            'fields': ('fe_score', 'be_score')
        }),
        ('Professional Information', {
            'fields': ('seniority', 'qualifications')
        }),
        ('Metadata', {
            'fields': ('id', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).order_by('-created_at')
