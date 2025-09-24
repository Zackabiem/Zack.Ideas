from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from .forms import AssignmentForm, RegisterForm
from .models import Assignment, Subject, Profile, Submission, TeacherProfile, StudentProfile, ClassRoom

#########################################
# User Authentication
#########################################

def register(request):
    """Register a new user with custom form."""
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Registration successful. You can now log in.')
            return redirect('login')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = RegisterForm()
    return render(request, 'tracker/register.html', {'form': form})


def user_login(request):
    """Handle user login."""
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("dashboard")  # go to role-based dashboard
        else:
            messages.error(request, "Invalid username or password")
    return render(request, "tracker/login.html")


def user_logout(request):
   ##"""Logout user and return home."""
    logout(request)
    return redirect('home')


#########################################
# Dashboards (redirect by role)
#########################################

@login_required
def redirect_dashboard(request):
    """Redirect to the appropriate dashboard depending on role."""
    profile, created = Profile.objects.get_or_create(user=request.user)

    if profile.role == "teacher":
        return redirect("teacher_dashboard")
    elif request.user.is_superuser or request.user.is_staff:
        return redirect("admin_dashboard")
    else:
        return redirect("student_dashboard")



def home(request):
    """Landing page view."""
    return render(request, "tracker/index.html")


#########################################
# Teacher Dashboard
#########################################

# @login_required
# def teacher_dashboard(request):
#     teacher_profile = get_object_or_404(TeacherProfile, user=request.user)

#     # Get all assignments created by this teacher
#     assignments = Assignment.objects.filter(
#         teacher=request.user
#     ).select_related("subject", "subject__classroom").order_by("-created_at")

#     # Get all submissions for those assignments
#     submissions = Submission.objects.filter(
#         assignment__in=assignments
#     ).select_related("student__user", "assignment__subject__classroom")

#     return render(request, "tracker/teacher_dashboard.html", {
#         "teacher": teacher_profile,
#         "assignments": assignments,
#         "submissions": submissions,
#     })

@login_required
def teacher_dashboard(request):
    teacher_profile = get_object_or_404(TeacherProfile, user=request.user)

    # Get the subjects assigned to this teacher
    assigned_subjects = teacher_profile.assigned_subjects.select_related("classroom").all()

    # Get assignments created by this teacher
    assignments = Assignment.objects.filter(
        teacher=request.user
    ).select_related("subject", "subject__classroom").order_by("-created_at")

    # Get submissions for those assignments
    submissions = Submission.objects.filter(
        assignment__in=assignments
    ).select_related("student__user", "assignment__subject__classroom")

    return render(request, "tracker/teacher_dashboard.html", {
        "teacher": teacher_profile,
        "assigned_subjects": assigned_subjects,  
        "assignments": assignments,
        "submissions": submissions,
    })


@login_required
def assignment_list(request):
    assignments = Assignment.objects.all()
    return render(request, "tracker/assignment_list.html", {"assignments": assignments})

@login_required
def assignment_create(request):
    """Teacher creates a new assignment for their class/subject."""
    teacher = get_object_or_404(TeacherProfile, user=request.user)

    if request.method == "POST":
        form = AssignmentForm(request.POST, request.FILES)
        if form.is_valid():
            assignment = form.save(commit=False)
            assignment.teacher = request.user
            assignment.save()
            messages.success(request, "Assignment created successfully.")
            return redirect("teacher_dashboard")
    else:
        form = AssignmentForm()

    return render(
        request, "tracker/assignment_form.html", {"form": form, "title": "New Assignment"}
    )

# @login_required
# def assignment_create(request):
#     if request.method == "POST":
#         form = AssignmentForm(request.POST, request.FILES)
#         if form.is_valid():
#             assignment = form.save(commit=False)
#             assignment.teacher = request.user  # ✅ must be a User, not TeacherProfile
#             assignment.save()
#             return redirect("assignment_list")
#     else:
#         form = AssignmentForm()
#     return render(request, "tracker/assignment_form.html", {"form": form, "title": "Create Assignment"})

@login_required
def assignment_update(request, pk):
    assignment = get_object_or_404(Assignment, pk=pk, teacher=request.user)
    if request.method == "POST":
        form = AssignmentForm(request.POST, request.FILES, instance=assignment)
        if form.is_valid():
            form.save()
            return redirect("assignment_list")
    else:
        form = AssignmentForm(instance=assignment)
    return render(request, "tracker/assignment_form.html", {"form": form, "title": "Edit Assignment"})

@login_required
def assignment_detail(request, pk):
    assignment = get_object_or_404(Assignment, pk=pk, teacher=request.user)
    submissions = assignment.submissions.select_related("student")
    return render(request, "tracker/assignment_detail.html", {
        "assignment": assignment,
        "submissions": submissions,
    })


#########################################
# Student Dashboard
#########################################


@login_required 
def student_dashboard(request):
    student_profile = StudentProfile.objects.get(user=request.user)

    assignments = Assignment.objects.filter(
        subject__classroom=student_profile.classroom
    )

    return render(request, "tracker/student_dashboard.html", {
        "assignments": assignments,
    })


@login_required
def submit_assignment(request, assignment_id):
    assignment = get_object_or_404(Assignment, id=assignment_id)

    if request.method == "POST":
        answer_file = request.FILES.get("answer_file")
        answer_text = request.POST.get("answer_text")

        # enforce file upload
        if not answer_file:
            messages.error(request, "File upload is required.")
            return redirect("student_dashboard")

        try:
            student_profile = StudentProfile.objects.get(user=request.user)
        except StudentProfile.DoesNotExist:
            messages.error(request, "You must be a student to submit assignments.")
            return redirect("student_dashboard")

        # Create submission
        Submission.objects.create(
            assignment=assignment,
            student=student_profile,
            answer_file=answer_file,
            answer_text=answer_text,
        )

        messages.success(request, "Assignment submitted successfully!")
        return redirect("student_dashboard")

    return render(request, "tracker/submit_assignment.html", {"assignment": assignment})



#########################################
# Grading (Teachers/Admins)
#########################################
@login_required
def grade_submission(request, submission_id):
    """Teacher or admin grades a student submission."""
    submission = get_object_or_404(Submission, id=submission_id)

    # Security: Only staff, superuser, or assignment's teacher can grade
    if not (
        request.user.is_superuser
        or request.user.is_staff
        or submission.assignment.teacher.user == request.user
    ):
        messages.error(request, "You are not authorized to grade this submission.")
        return redirect("teacher_dashboard")

    if request.method == "POST":
        score = request.POST.get("score")
        feedback = request.POST.get("feedback")

        #Validate score
        try:
            score = float(score)
            if score > submission.assignment.max_score:
                messages.warning(request, f"Score capped at {submission.assignment.max_score}")
                score = submission.assignment.max_score
        except ValueError:
            messages.error(request, "Invalid score. Please enter a number.")
            return render(request, "tracker/grade_submission.html", {"submission": submission})

        #  Save grading
        submission.score = score
        submission.feedback = feedback
        submission.is_reviewed = True
        submission.save()

        messages.success(request, "Submission graded successfully.")
        return redirect("teacher_dashboard")

    return render(request, "tracker/grade_submission.html", {"submission": submission})


#########################################
# Admin Dashboard
#########################################
@login_required
def admin_dashboard(request):
    """Admin view to oversee teachers, students, classes, and assignments."""
    if not (request.user.is_superuser or request.user.is_staff):
        messages.error(request, "Access denied.")
        return redirect("redirect_dashboard")

    teachers = TeacherProfile.objects.all()
    students = StudentProfile.objects.all()
    classes = ClassRoom.objects.all()
    subjects = Subject.objects.all()

    assignments = Assignment.objects.all()
    submissions = Submission.objects.all()

    # Simple reminders
    pending_assignments = assignments.filter(submissions__isnull=True)  # no submissions yet
    ungraded_submissions = submissions.filter(is_reviewed=False)        # waiting for review

    return render(request, "tracker/admin_dashboard.html", {
        "teachers": teachers,
        "students": students,
        "classes": classes,
        "subjects": subjects,
        "assignments": assignments,
        "submissions": submissions,
        "pending_assignments": pending_assignments,
        "ungraded_submissions": ungraded_submissions,
    })


#########################33
## Student Results View
#########################33

@login_required
def student_results(request):
    """Allow students to view grades and feedback on their submissions"""
    if hasattr(request.user, "studentprofile"):
        student = request.user.studentprofile
        submissions = Submission.objects.filter(student=student).select_related("assignment")
    else:
        submissions = []  # not a student
    
    return render(request, "tracker/results.html", {"submissions": submissions})


@login_required
def assignment_delete(request, pk):
    assignment = get_object_or_404(Assignment, pk=pk)

    # Authorization check
    if assignment.teacher != request.user and not request.user.is_staff and not request.user.is_superuser:
        messages.error(request, 'You are not authorized to delete this assignment.')
        return redirect('teacher_dashboard')

    if request.method == 'POST':
        assignment.delete()
        messages.success(request, 'Assignment deleted.')
        return redirect('teacher_dashboard')

    return render(request, 'tracker/delete_confirm.html', {'object': assignment})


################
## Mark Reviewed
####   

@login_required
def mark_reviewed(request, pk):
    """Mark an assignment as reviewed (teacher/admin only)."""
    assignment = get_object_or_404(Assignment, pk=pk)

    if not (request.user.is_staff or request.user.is_superuser):
        messages.error(request, "You are not authorized to perform this action.")
        return redirect("teacher_dashboard")

    assignment.is_reviewed = True
    assignment.save()
    messages.success(request, f"Assignment '{assignment.title}' marked as reviewed.")
    return redirect("teacher_dashboard")
