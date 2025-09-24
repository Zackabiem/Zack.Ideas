from django.db import models
from django.contrib.auth.models import User


# ==============================
# ClassRoom model
# ==============================
class ClassRoom(models.Model):
    """Represents a class group (e.g., Primary 5, SS2, etc.)"""
    name = models.CharField(max_length=100, unique=True)  

    def __str__(self):
        return self.name


# ==============================
# Subject model
# ==============================
class Subject(models.Model):
    """Represents a subject (e.g., Mathematics, English, etc.)
       Each subject belongs to a class (e.g., Math in Primary 5).
    """
    name = models.CharField(max_length=100)
    classroom = models.ForeignKey(
        ClassRoom, on_delete=models.CASCADE, related_name="subjects"
    )

    def __str__(self):
        return f"{self.name} ({self.classroom.name})"


# ==============================
# Profile model (basic role flag)
# ==============================
class Profile(models.Model):
    """General user profile to identify whether a user is a student or a teacher"""
    ROLE_CHOICES = (
        ('student', 'Student'),
        ('teacher', 'Teacher'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='student')

    def __str__(self):
        return f"{self.user.username} ({self.role})"


# ==============================
# TeacherProfile model
# ==============================
class TeacherProfile(models.Model):
    """Extra info for teachers:
       - Which subjects they teach
       - Which classes they handle
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    assigned_subjects = models.ManyToManyField(Subject, blank=True)
    assigned_classes = models.ManyToManyField(ClassRoom, blank=True)

    def __str__(self):
        return self.user.username


# ==============================
# StudentProfile model
# ==============================
class StudentProfile(models.Model): 
    """Extra info for students:
       - Which class they belong to
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    classroom = models.ForeignKey(
        ClassRoom, on_delete=models.SET_NULL, null=True, blank=True
    )

    def __str__(self):
        return self.user.username

# ==============================
# Assignment model
# ==============================

class Assignment(models.Model): # an assignment created by a teacher
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    file = models.FileField(upload_to="assignments/", blank=True, null=True)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, null=True, blank=True)
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, related_name="created_assignments")
    created_at = models.DateTimeField(auto_now_add=True)
    max_score = models.PositiveIntegerField(default=100)  # max possible score

    def __str__(self):
        return self.title



# ==============================
# Submission model
# ==============================
class Submission(models.Model): # student submission to an assignment
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE, related_name="submissions")
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE)
    answer_file = models.FileField(upload_to="assignment_answers/", blank=True, null=True)
    answer_text = models.TextField(blank=True, null=True)
    submitted_at = models.DateTimeField(auto_now_add=True)

    # grading fields
    score = models.FloatField(blank=True, null=True)
    feedback = models.TextField(blank=True, null=True)
    is_reviewed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.assignment.title} - {self.student.user.username}"


# # ==============================
# # Signals to auto-create Profile
# # ==============================
from django.db.models.signals import post_save
from django.dispatch import receiver

# @receiver(post_save, sender=User)
# def create_profile_for_new_user(sender, instance, created, **kwargs):
#     """Create a Profile whenever a new User is made"""
#     if created:
#         Profile.objects.create(user=instance)

# @receiver(post_save, sender=User)
# def save_profile_for_user(sender, instance, **kwargs):
#     """Ensure profile exists and is saved"""
#     Profile.objects.get_or_create(user=instance)
#     instance.profile.save()

@receiver(post_save, sender=User)
def create_profile_for_new_user(sender, instance, created, **kwargs):
    #"""Create Profile and matching Student/TeacherProfile for new users."""#
    if created:
        profile = Profile.objects.create(user=instance)
        if profile.role == "student":
            StudentProfile.objects.get_or_create(user=instance)
        elif profile.role == "teacher":
            TeacherProfile.objects.get_or_create(user=instance)


@receiver(post_save, sender=User)
def save_profile_for_user(sender, instance, **kwargs):
   ## """Ensure profile exists and is saved"""
    profile, _ = Profile.objects.get_or_create(user=instance)
    profile.save()

    # Also make sure extended profiles exist
    if profile.role == "student":
        StudentProfile.objects.get_or_create(user=instance)
    elif profile.role == "teacher":
        TeacherProfile.objects.get_or_create(user=instance)
