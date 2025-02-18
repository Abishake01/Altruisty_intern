from django.shortcuts import render,get_object_or_404
from .models import bannerupload
from internship.models import commonquestionanswer,dailyquestionanswer,weeklyquestionanswer
from .models import InternRegistartion
from College.models import collegeRegistartion
from django.db.models import Count, OuterRef, Subquery, Value, IntegerField, Q
from django.db.models.functions import Coalesce

 
def user_profile(request, user_id):
    # Get the student details
    user = get_object_or_404(InternRegistartion, user_id=user_id)

    # Count problems solved in each category using user_id
    daily_solved = dailyquestionanswer.objects.filter(user_id=user.user_id).count()
    weekly_solved = weeklyquestionanswer.objects.filter(user_id=user.user_id).count()
    common_solved = commonquestionanswer.objects.filter(user_id=user.user_id).count()

    # Calculate total score
    total_score = (daily_solved + weekly_solved + common_solved) * 5

    return render(request, 'Internship/user_profile.html', {
        'user': user,
        'daily_solved': daily_solved,
        'weekly_solved': weekly_solved,
        'common_solved': common_solved,
        'total_score': total_score,
    })

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