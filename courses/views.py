from django.shortcuts import render,get_object_or_404
from .models import Course,Instructor,LectureMaterial
import base64

# Create your views here.
def courseListPage(request):
    courses = Course.objects.all()
    instructors = Instructor.objects.all()

    # Decode binary fields for images
    for course in courses:
        if course.course_image_box:
            course.course_image_box = base64.b64encode(course.course_image_box).decode('utf-8')
        if course.course_image_list:
            course.course_image_list = base64.b64encode(course.course_image_list).decode('utf-8')
        if course.course_intro_video:
            course.course_intro_video = base64.b64encode(course.course_intro_video).decode('utf-8')

    for instructor in instructors:
        if instructor.profile_photo:
            instructor.profile_photo = base64.b64encode(instructor.profile_photo).decode('utf-8')

    return render(request, 'courses/course-list.html', {'courses': courses, 'instructors': instructors})

from django.db.models import Sum, Max

def course_details(request, course_id):
    # Fetch the course object by course_id
    course = get_object_or_404(Course, course_id=course_id)

    # Decode course image for display
    if course.course_image_list:
        course.course_image_list = base64.b64encode(course.course_image_list).decode('utf-8')

    # Fetch the instructor for the course
    instructor = get_object_or_404(Instructor, id=course.instructor.id)

    # Decode instructor profile photo for display
    if instructor.profile_photo:
        instructor.profile_photo = base64.b64encode(instructor.profile_photo).decode('utf-8')

    # Retrieve all lecture materials related to the course
    lecture_materials = course.lecture_materials.all()

    # Count the number of lecture materials
    lecture_count = lecture_materials.count()

    # Get the latest lecture created date
    latest_lecture_date = lecture_materials.aggregate(Max('created_date'))['created_date__max']

    # Calculate the total course duration in minutes
    total_duration_minutes = lecture_materials.aggregate(Sum('lecture_duration'))['lecture_duration__sum'] or 0

    # Convert total duration to hours and minutes
    hours = total_duration_minutes // 60
    minutes = total_duration_minutes % 60

    # Retrieve 3 courses with the same category
    related_courses = Course.objects.filter(category=course.category).exclude(course_id=course_id)[:3]
    for course in related_courses:
        if course.course_image_box:
            course.course_image_box = base64.b64encode(course.course_image_box).decode('utf-8')

    instructors = Instructor.objects.all()

    # Render the template with additional context
    return render(
        request,
        'Courses/course-details-2.html',
        {
            'course': course,
            'instructor': instructor,
            'lecture_materials': lecture_materials,
            'lecture_count': lecture_count,
            'latest_lecture_date': latest_lecture_date,
            'total_duration_hours': hours,
            'total_duration_minutes': minutes,
            'related_courses': related_courses,
            'instructors':instructors
        }
    )
