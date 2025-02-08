from django.shortcuts import render
from .models import bannerupload
from internship.models import commonquestionanswer,dailyquestionanswer,weeklyquestionanswer
from .models import InternRegistartion
from College.models import collegeRegistartion
from django.db.models import Count

def college_home(request):
    # Retrieve the user_id from session storage
    user_id = request.session.get('user_id', None)
    
    # Initialize the variables to None or 0
    college = None
    total_intern = 0
    completed_intern = 0
    ongoing_intern = 0

    banner = bannerupload.objects.filter().values()
    
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
    
    # Pass the user_id, college data, and intern counts to the template
    result = dailyquestionanswer.objects.values('user_id').annotate(entry_count=Count('user_id')).order_by('-entry_count')
    result2 = weeklyquestionanswer.objects.values('user_id').annotate(entry_count=Count('user_id')).order_by('-entry_count')
    result3 = commonquestionanswer.objects.values('user_id').annotate(entry_count=Count('user_id')).order_by('-entry_count')

    return render(request, 'Internship/college_home.html', {
        'user_id': user_id,
        'college': college,
        'banner' : banner,
        "wr":result2,
        "dr":result,
        "cr":result3,
        'interns': interns,
        'total_intern': total_intern,
        'completed_intern': completed_intern,
        'ongoing_intern': ongoing_intern
    })
