from django.shortcuts import render
from .models import bannerupload
from internship.models import commonquestionanswer,dailyquestionanswer,weeklyquestionanswer
from .models import InternRegistartion
from College.models import collegeRegistartion
from django.db.models import Count, OuterRef, Subquery, Value, IntegerField, Q
from django.db.models.functions import Coalesce

def college_home(request):
    # Retrieve the user_id from session storage
    user_id = request.session.get('user_id', None)
    # Initialize the variables to None or 0
    college = None
    total_intern = 0
    completed_intern = 0
    ongoing_intern = 0
    banner = bannerupload.objects.filter().values()
    # Get the student name from InternRegistartion based on user_id
    if user_id: 
        # Retrieve the college data for the current user
        college = collegeRegistartion.objects.filter(user_id=user_id).first()
        
        if college:
            # Get the total number of interns from the same college
            interns = InternRegistartion.objects.filter(College_name=college.Name)
            total_intern = interns.count()
            
            # Get the number of completed interns
            completed_intern = InternRegistartion.objects.filter(College_name=college.Name, status='completed').count()
            
            # Get the number of ongoing interns (status = accepted)
            ongoing_intern = InternRegistartion.objects.filter(College_name=college.Name, status='accepted').count()
    
    interns = InternRegistartion.objects.values('user_id', 'student_Name')
    search_query = request.GET.get('s', '')
# Subqueries for ranking and score calculations
    daily_rank_subquery = dailyquestionanswer.objects.filter(user_id=OuterRef('user_id')) \
    .values('user_id').annotate(
        entry_count=Count('user_id'),
        score=Count('user_id') * 5  # Each problem = 5 points
    ).values('entry_count', 'score')[:1]

    weekly_rank_subquery = weeklyquestionanswer.objects.filter(user_id=OuterRef('user_id')) \
    .values('user_id').annotate(
        entry_count=Count('user_id'),
        score=Count('user_id') * 5
    ).values('entry_count', 'score')[:1]

    common_rank_subquery = commonquestionanswer.objects.filter(user_id=OuterRef('user_id')) \
    .values('user_id').annotate(
        entry_count=Count('user_id'),
        score=Count('user_id') * 5
    ).values('entry_count', 'score')[:1]

# Get all interns with ranking and scores
    interns_with_rankings = InternRegistartion.objects.annotate(
    entry_count_daily=Coalesce(Subquery(daily_rank_subquery.values('entry_count')), Value(0)),
    score_daily=Coalesce(Subquery(daily_rank_subquery.values('score')), Value(0)),
    entry_count_weekly=Coalesce(Subquery(weekly_rank_subquery.values('entry_count')), Value(0)),
    score_weekly=Coalesce(Subquery(weekly_rank_subquery.values('score')), Value(0)),
    entry_count_common=Coalesce(Subquery(common_rank_subquery.values('entry_count')), Value(0)),
    score_common=Coalesce(Subquery(common_rank_subquery.values('score')), Value(0))
)
    if search_query:
        interns_with_rankings = interns_with_rankings.filter(
            Q(student_Name__icontains=search_query) | Q(user_id__icontains=search_query)
        )
# Assign ranks starting from 1 for each category
    interns_with_rankings = sorted(interns_with_rankings, key=lambda x: -x.entry_count_daily)
    for idx, intern in enumerate(interns_with_rankings):
        intern.rank_daily = idx + 1

    interns_with_rankings = sorted(interns_with_rankings, key=lambda x: -x.entry_count_weekly)
    for idx, intern in enumerate(interns_with_rankings):
        intern.rank_weekly = idx + 11

    interns_with_rankings = sorted(interns_with_rankings, key=lambda x: -x.entry_count_common)
    for idx, intern in enumerate(interns_with_rankings):
        intern.rank_common = idx + 1
    return render(request, 'Internship/college_home.html', {
        'user_id': user_id,
        'college': college,
        'banner' : banner,
        'interns_with_rankings': interns_with_rankings,
        'search_query': search_query,
        'interns': interns,
        'total_intern': total_intern,
        'completed_intern': completed_intern,
        'ongoing_intern': ongoing_intern
    })
