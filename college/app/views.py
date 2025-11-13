from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages,auth
from django.contrib.auth import authenticate, login
from .models import Course, Student, Teacher
from django.contrib.auth.hashers import check_password
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.decorators import login_required



# ---------------- LANDING PAGE ----------------
def landing(request):
    return render(request, 'landing.html')


# ---------------- ADMIN DASHBOARD ----------------
@login_required(login_url='loginfun')
def admin_dashboard(request):
    courses_count = Course.objects.count()
    students_count = Student.objects.count()
    teachers_count = Teacher.objects.count()

    context = {
        'courses_count': courses_count,
        'students_count': students_count,
        'teachers_count': teachers_count,
    }
    return render(request, 'admin_dashboard.html', context)


# ---------------- COURSE SECTION ----------------
@login_required(login_url='loginfun')
def course(request):
    return render(request, 'course.html')

@login_required(login_url='loginfun')
def add_course(request):
    if request.method == 'POST':
        coursename = request.POST.get('course')
        fees = request.POST.get('fee')
        if coursename and fees:
            Course.objects.create(coursename=coursename, fees=fees)
            messages.success(request, f"Course '{coursename}' added successfully!")
            return redirect('admin_dashboard')
       
    return render(request, 'course.html')


# ---------------- STUDENT SECTION ----------------
@login_required(login_url='loginfun')
def student(request):
    crs = Course.objects.all()
    return render(request, 'student.html', {'course': crs})

@login_required(login_url='loginfun')
def add_student(request):
    if request.method == 'POST':
        courseid = request.POST.get('c')
        studentname = request.POST.get('name')
        address = request.POST.get('address')
        age = request.POST.get('age')
        date = request.POST.get('date')

        course = get_object_or_404(Course, id=courseid)
        Student.objects.create(
            course=course,
            studentname=studentname,
            address=address,
            age=age,
            joiningdate=date
        )
        messages.success(request, f"Student '{studentname}' added successfully!")
        return redirect('show_details')
    return redirect('student')

@login_required(login_url='loginfun')
def show_details(request):
    std = Student.objects.select_related('course').all()
    return render(request, 'show_details.html', {'student': std})


# ---------------- TEACHER SECTION ----------------
def teacher_signup(request):
    courses = Course.objects.all()

    if request.method == 'POST':
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        username = request.POST.get('username')
        address = request.POST.get('address')
        age = request.POST.get('age')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        password = request.POST.get('password')
        confirmpw = request.POST.get('confirmpw')
        image = request.FILES.get('image')
        course_id = request.POST.get('course')

        if len(password) < 8:
            messages.error(request, "Password must be at least 8 characters long!")
            return redirect('teacher_signup')

        if password != confirmpw:
            messages.error(request, "Passwords do not match!")
            return redirect('teacher_signup')

        if Teacher.objects.filter(username=username).exists():
            messages.error(request, "Username already exists!")
            return redirect('teacher_signup')

        if Teacher.objects.filter(email=email).exists():
            messages.error(request, "Email already registered!")
            return redirect('teacher_signup')

        if Teacher.objects.filter(phone=phone).exists():
            messages.error(request, "Phone number already registered!")
            return redirect('teacher_signup')

        # Validate email format
        if not email.endswith('.com'):
            messages.error(request, "Email must end with '.com' extension!")
            return redirect('teacher_signup')

        # Validate phone number format (must be digits and exactly 10 characters)
        if not (phone.isdigit() and len(phone) == 10):
            messages.error(request, "Phone number must contain exactly 10 digits!")
            return redirect('teacher_signup')

        try:
            course = Course.objects.get(id=course_id)
            Teacher.objects.create(
                fname=fname,
                lname=lname,
                username=username,
                address=address,
                age=age,
                email=email,
                phone=phone,
                password=make_password(password), 
                image=image,
                course=course
            )
            messages.success(request, "Teacher registered successfully!")
            return redirect('loginfun')
        except Exception as e:
            messages.error(request, f"Error: {e}")

    return render(request, 'teacher_signup.html', {'courses': courses})

@login_required(login_url='loginfun')
def show_teachers(request):
    teachers = Teacher.objects.select_related('course').all()
    return render(request, 'show_teachers.html', {'teachers': teachers})


# ---------------- LOGIN FUNCTION ----------------
def loginfun(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Try authenticating Django user
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            if user.is_superuser or user.is_staff:
                messages.success(request, f"Welcome Admin {user.username}!")
                return redirect('admin_dashboard')
            else:
                messages.success(request, f"Welcome {user.username}!")
                return redirect('teacher_dashboard')

        # Check custom Teacher model
        try:
            teacher = Teacher.objects.get(username=username)
            if check_password(password, teacher.password):  # ✅ Works with hashed password
                request.session['teacher_id'] = teacher.id
                messages.success(request, f"Welcome {teacher.fname}!")
                return redirect('teacher_dashboard')
            else:
                messages.error(request, "Incorrect password!")
        except Teacher.DoesNotExist:
            messages.error(request, "Invalid username or password!")

        return redirect('loginfun')

    return render(request, 'loginfun.html')



# ---------------- TEACHER DASHBOARD ----------------
def teacher_dashboard(request):
    teacher_id = request.session.get('teacher_id')
    if not teacher_id:
        messages.error(request, "Please log in first!")
        return redirect('loginfun')

    teacher = get_object_or_404(Teacher, id=teacher_id)
    std = Student.objects.select_related('course').filter(course=teacher.course)

    context = {'teacher': teacher, 'student': std}
    return render(request, 'teacher_dashboard.html', context)


# ---------------- EDIT & DELETE ----------------

def edit(request, id):
    student = get_object_or_404(Student, id=id)
    courses = Course.objects.all()
    if request.method == 'POST':
        student.studentname = request.POST.get('name')
        student.address = request.POST.get('address')
        student.age = request.POST.get('age')
        student.joiningdate = request.POST.get('date')
        course_id = request.POST.get('c')
        student.course = get_object_or_404(Course, id=course_id)
        student.save()
        messages.success(request, "Student updated sucessfully!")
        return redirect('show_details')
    return render(request, 'edit_students.html', {'student': student, 'courses': courses})


def delete(request, id):
    student = get_object_or_404(Student, id=id)
    student_name = student.studentname
    student.delete()
    messages.success(request, f"Student '{student_name}' deleted successfully!")
    return redirect('show_details')





def edit_teacher(request, id):
    teacher = get_object_or_404(Teacher, id=id)
    courses = Course.objects.all()

    if request.method == 'POST':
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        username = request.POST.get('username')
        address = request.POST.get('address')
        age = request.POST.get('age')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        course_id = request.POST.get('course')

        # ---------------- VALIDATIONS ----------------
        # Check for duplicate username (excluding current teacher)
        if Teacher.objects.filter(username=username).exclude(id=id).exists():
            messages.error(request, "Username already exists!")
            return redirect('edit_teacher', id=id)

        # Check for duplicate email (excluding current teacher)
        if Teacher.objects.filter(email=email).exclude(id=id).exists():
            messages.error(request, "Email already registered!")
            return redirect('edit_teacher', id=id)

        # Check for duplicate phone number (excluding current teacher)
        if Teacher.objects.filter(phone=phone).exclude(id=id).exists():
            messages.error(request, "Phone number already registered!")
            return redirect('edit_teacher', id=id)

        # Validate email format
        if not email.endswith('.com'):
            messages.error(request, "Email must end with '.com' extension!")
            return redirect('edit_teacher', id=id)

        # Validate phone number (must be digits and 10 digits long)
        if not (phone.isdigit() and len(phone) == 10):
            messages.error(request, "Phone number must contain exactly 10 digits!")
            return redirect('edit_teacher', id=id)

        # ---------------- UPDATE TEACHER DETAILS ----------------
        teacher.fname = fname
        teacher.lname = lname
        teacher.username = username
        teacher.address = address
        teacher.age = age
        teacher.email = email
        teacher.phone = phone
        teacher.course = get_object_or_404(Course, id=course_id)

        # If a new image is uploaded, update it
        if 'image' in request.FILES:
            teacher.image = request.FILES['image']

        teacher.save()
        messages.success(request, "Teacher details updated successfully!")
        return redirect('teacher_dashboard')

    return render(request, 'edit_teacher.html', {'teacher': teacher, 'courses': courses})

@login_required(login_url='loginfun')
def delete_teacher(request, id):
    teacher = get_object_or_404(Teacher, id=id)
    teacher_name = teacher.fname
    teacher.delete()
    messages.success(request, f"Teacher'{teacher_name}' deleted by admin successfully!")
    return redirect('show_teachers')

def logout_fun(request):
    auth.logout(request)
    return redirect('loginfun')