from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Assignment, Submission, Profile, TeacherProfile, StudentProfile

#########################################
# Assignment form (for teachers)
#########################################


# class AssignmentForm(forms.ModelForm):
#     class Meta:
#         model = Assignment
#         fields = ["title", "description", "file", "subject", "max_score"]

##################
# Assignment form with Bootstrap styling##
#################

class AssignmentForm(forms.ModelForm):
    class Meta:
        model = Assignment
        fields = ["title", "description", "file", "subject", "max_score"]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 4}),
            "file": forms.ClearableFileInput(attrs={"class": "form-control"}),
            "subject": forms.Select(attrs={"class": "form-select"}),
            "max_score": forms.NumberInput(attrs={"class": "form-control"}),
        }

#########################################
# Submission form (for students)
#########################################
class SubmissionForm(forms.ModelForm):
    """Form for students to submit answers to assignments."""
    class Meta:
        model = Submission
        fields = ["answer_text", "answer_file"]


#########################################
# User Registration with Role Selection
#########################################
class RegisterForm(UserCreationForm):
    ROLE_CHOICES = (
        ('student', 'Student'),
        ('teacher', 'Teacher'),
    )
    role = forms.ChoiceField(choices=ROLE_CHOICES)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    # def save(self, commit=True):
    #     """Save user and attach role to profile."""
    #     user = super().save(commit=commit)
    #     role = self.cleaned_data.get("role", "student")
    #     if commit:
    #         Profile.objects.get_or_create(user=user)
    #         user.profile.role = role
    #         user.profile.save()
    #     return user
    
    
def save(self, commit=True):
    """Save user and attach role to profile + specific role profile."""
    user = super().save(commit=commit)
    role = self.cleaned_data.get("role", "student")

    if commit:
        profile, _ = Profile.objects.get_or_create(user=user)
        profile.role = role
        profile.save()

        # Create role-specific profile
        if role == "teacher":
            TeacherProfile.objects.get_or_create(user=user)
        elif role == "student":
            StudentProfile.objects.get_or_create(user=user)

    return user
