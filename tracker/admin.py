from django.contrib import admin
from django.contrib.auth.models import User
from .models import (
    ClassRoom, Subject, Profile, TeacherProfile,
    StudentProfile, Assignment, Submission
)

# ===========================
# TeacherProfile Admin
# ===========================
class TeacherProfileAdmin(admin.ModelAdmin):
    list_display = ("user",)
    filter_horizontal = ("assigned_subjects", "assigned_classes")

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "user":
            kwargs["queryset"] = User.objects.filter(profile__role="teacher")
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


# ===========================
# StudentProfile Admin
# ===========================
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "classroom")

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "user":
            kwargs["queryset"] = User.objects.filter(profile__role="student")
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

# ===========================
# Subject Admin
# ===========================
class SubjectAdmin(admin.ModelAdmin):
    list_display = ("name", "classroom")  # 


# ===========================
# Assignment Admin
# ===========================
class AssignmentAdmin(admin.ModelAdmin):
    list_display = ("title", "subject", "teacher", "created_at", "max_score")
    list_filter = ("subject", "teacher", "created_at")

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "teacher":
            kwargs["queryset"] = User.objects.filter(profile__role="teacher")
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


# ===========================
# Submission Admin
# ===========================
class SubmissionAdmin(admin.ModelAdmin):
    list_display = ("assignment", "student", "submitted_at", "score", "is_reviewed")
    list_filter = ("is_reviewed", "submitted_at")  #  changed reviewed → is_reviewed


# ===========================
# Register Models
# ===========================
admin.site.register(ClassRoom)
admin.site.register(Subject, SubjectAdmin)
admin.site.register(Profile)

admin.site.register(Assignment, AssignmentAdmin)
admin.site.register(Submission, SubmissionAdmin)
admin.site.register(TeacherProfile, TeacherProfileAdmin)
admin.site.register(StudentProfile, StudentProfileAdmin)
