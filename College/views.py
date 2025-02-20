import base64
import json
from django.shortcuts import render,get_object_or_404
from django.utils.timezone import now
from datetime import timedelta

from IdeaSubmission.models import IdeaSubmission
from community.models import user_detail
from video_call.models import Attendance
from .models import bannerupload
from internship.models import InternTeams, commonquestionanswer,dailyquestionanswer,weeklyquestionanswer
from .models import InternRegistartion
from College.models import collegeRegistartion
from django.db.models import Count, OuterRef, Subquery, Value, IntegerField, Q, Sum
from django.db.models.functions import Coalesce, TruncMonth


 
def progress(request, user_id):  
    # ✅ Fetch the correct student details using user_id from the URL
    user = get_object_or_404(InternRegistartion, user_id=user_id)

    # ✅ Fetch Daily, Weekly, and Common Challenge Answers for the Correct User
    ud = dailyquestionanswer.objects.filter(user_id=user_id).values()
    uw = weeklyquestionanswer.objects.filter(user_id=user_id).values()
    uc = commonquestionanswer.objects.filter(user_id=user_id).values()

    # ✅ Compute token values correctly
    udt = [int(i['token']) for i in ud]
    uwt = [int(i['token']) for i in uw]
    uct = [int(i['token']) for i in uc]

    ds = sum(udt)
    ws = sum(uwt)
    cs = sum(uct)
    score = ds + ws + cs

    # ✅ Calculate completed tasks
    def add(a, b):
        return a + b
    
    taskcom = add(len(ud), len(uw))
    fullcom = add(taskcom, len(uc))
    
    # ✅ Fetch ranking for the selected user
    wr = weeklyquestionanswer.objects.values('user_id').annotate(entry_count=Count('user_id')).order_by('-entry_count')
    dr = dailyquestionanswer.objects.values('user_id').annotate(entry_count=Count('user_id')).order_by('-entry_count')
    cr = commonquestionanswer.objects.values('user_id').annotate(entry_count=Count('user_id')).order_by('-entry_count')

    # ✅ Fetch profile image
    try:
        pimage_data = user_detail.objects.get(user_id=user_id)
        if pimage_data.profile_photo:  # ✅ Check if image exists
            profile_image = base64.b64encode(pimage_data.profile_photo).decode('utf-8')
        else:
            profile_image = None  # ✅ No profile image
    except user_detail.DoesNotExist:
        profile_image = None  # ✅ Handle missing user details
  

    # ✅ Fetch user's team & projects
    in_team = InternTeams.objects.filter(
        Q(member1=user_id) | Q(member2=user_id) | Q(member3=user_id) |
        Q(member4=user_id) | Q(member5=user_id)
    ).values_list('team_id', flat=True)

    projects = IdeaSubmission.objects.filter(user_id__in=in_team) if in_team else None

    # ✅ Fetch user's internship details
    userinternship = get_object_or_404(InternRegistartion, user_id=user_id)

    internact = userinternship.ep2
    try:
        internact = json.loads(internact) if isinstance(internact, str) else internact  # Convert string to dict
        internlist = internact.get('intern_history', [])  # Default to empty list
    except json.JSONDecodeError:
        internlist = []  # If parsing fails, default to empty list


    # ✅ Attendance Data for the Last 12 Months
    current_date = now()
    monthly_attendance = (
    Attendance.objects.filter(attendee=user_id, join_time__gte=current_date - timedelta(days=365))  # ✅ Fix here
    .annotate(month=TruncMonth('join_time'))
    .values('month')
    .annotate(
        total_entries=Count('id'),
        total_percentage=Sum('attendance_percentage'),
    )
    .order_by('month')
)

    total_entries = Attendance.objects.filter(attendee=user_id).count()  # ✅ Fix here

    total_attendance_percentage = Attendance.objects.filter(attendee=user_id).aggregate(
        Sum('attendance_percentage')
        )['attendance_percentage__sum'] or 0  # ✅ Fix here

    # Normalize Attendance Data
    chart_labels = []
    chart_data = []
    for month_data in monthly_attendance:
        total_entries = month_data['total_entries']
        total_percentage = month_data['total_percentage']
        normalized_percentage = (total_percentage / (total_entries * 100)) * 100 if total_entries > 0 else 0

        chart_labels.append(month_data['month'].strftime('%b %Y'))  # "Jan 2024"
        chart_data.append(normalized_percentage)
 
    normalized_percentage = (total_attendance_percentage / (total_entries * 100)) * 100 if total_entries > 0 else 0

    context = {
        "id": user.user_id,  # ✅ Ensure `id` is set correctly
        "name": user.student_Name,  # ✅ Ensure `name` is set correctly
        "user": user,
        "profile_image": profile_image,  # ✅ Profile Image Handling
        "token": score,
        "taskcom": fullcom,
        "projects": projects,
        "ds": ds,
        "ws": ws,
        "cs": cs,
        "internlist": internlist,
        "attendance_percentage": normalized_percentage,
        "chart_labels": json.dumps(chart_labels),
        "chart_data": json.dumps(chart_data),
        "banner": bannerupload.objects.all(),
}

    return render(request, "internship/user_profile.html", context)


def college_home(request):
    user_id = request.session.get('user_id', None)
    college = None
    total_intern = 0
    completed_intern = 0
    ongoing_intern = 0
    banner = bannerupload.objects.all()
    
    if user_id: 
        college = collegeRegistartion.objects.filter(user_id=user_id).first()
        if college:
            interns = InternRegistartion.objects.filter(College_name=college.Name)
            total_intern = interns.count()
            completed_intern = interns.filter(status='completed').count()
            ongoing_intern = interns.filter(status='accepted').count()
    
    search_query = request.GET.get('s', '')

    # Get total score (each problem solved is worth 5 points)
    interns_with_scores = InternRegistartion.objects.annotate(
        total_score=(
            Coalesce(Subquery(
                    dailyquestionanswer.objects.filter(user_id=OuterRef('user_id'))
                    .values('user_id')
                    .annotate(count=Count('user_id'))
                    .values('count')[:1]
                ), Value(0)
            ) + 
            Coalesce(
                Subquery(
                    weeklyquestionanswer.objects.filter(user_id=OuterRef('user_id'))
                    .values('user_id')
                    .annotate(count=Count('user_id'))
                    .values('count')[:1]
                ), Value(0)
            ) + 
            Coalesce(
                Subquery(
                    commonquestionanswer.objects.filter(user_id=OuterRef('user_id'))
                    .values('user_id')
                    .annotate(count=Count('user_id'))
                    .values('count')[:1]
                ), Value(0)
            )
        ) * Value(5)  # Multiply total solved problems by 5 to get total score
    )

    # Filter for search
    if search_query:
        interns_with_scores = interns_with_scores.filter(
            Q(student_Name__icontains=search_query) | Q(user_id__icontains=search_query)
        )
    
    # Sort by total score (descending)
    top_participants = interns_with_scores.order_by('-total_score')[:10]  # Top 10 participants
    
    # result = dailyquestionanswer.objects.values('user_id').annotate(entry_count=Count('user_id')).order_by('-entry_count')
    # result2 = weeklyquestionanswer.objects.values('user_id').annotate(entry_count=Count('user_id')).order_by('-entry_count')
    # result3 = commonquestionanswer.objects.values('user_id').annotate(entry_count=Count('user_id')).order_by('-entry_count')

    
    return render(request, 'Internship/college_home.html', {
        'user_id': user_id,
        'college': college,
        'banner': banner,
        # "wr":result2,
        # "dr":result,
        # "cr":result3,
        'top_participants': top_participants,
        'search_query': search_query,
        'total_intern': total_intern,
        'completed_intern': completed_intern,
        'ongoing_intern': ongoing_intern
    })