from django.utils import timezone
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from College.models import HomeImage, Events_update
from internship.models import weeklyquestion,weeklyquestionanswer,commonquestion,commonquestionanswer,dailyquestionanswer, dailyquestionanswer,bannerupload
from IdeaSubmission.models import statementshowcaseform,statementshowcasecategoryform
from django.db.models import Count
from internship.models import InternTeams
from django.db.models import Q

from AI_tools.views import addInvestorForm
from .models import banneruploadstartup, Question,CostCuttingCategoryMaster, StudentReport, Userauth,TeamCategory,startupscore,startup_individual_score,StartupRegistartion # Assuming you have a model named StudentReport
from community.models import user_detail
from django.views.decorators.csrf import csrf_exempt
import json
from datetime import datetime
from courses.models import Course
import base64
from django.db.models import Sum, F
from django.db.models import IntegerField, F
from django.db.models.functions import Cast
from AI_tools.models import AddInvestor


counters = {
    'member': 0,
}

last_date = None


strength = []
weakness = []
opportunity = []
threat = []

userid=""
password=""

def generate_unique_password(length):
    """
    Generate a unique password of a given length.
    """
    import random
    import string

    characters = string.ascii_letters + string.digits + '!@#$%^&*()_+[]{}|;:,.<>?'
    password = ''.join(random.choices(characters, k=length))

    # Append a unique identifier (e.g., timestamp)
    timestamp = hex(int(datetime.now().timestamp() * 1000))[2:]
    password += timestamp

    return password

def createswot(request):
    latest_report = StudentReport.objects.filter(student_id=request.session.get('user_id',None)).order_by('-timestamp').first()

    context = {
        'strength': latest_report.strengths,
        'weakness': latest_report.weakness,
        'opportunity': latest_report.opportunity,
        'threat': latest_report.threat,
        'new': 'no'
    }

    return render(request, 'swot_analysis/points.html', context)

def strength(request):
    return render(request, 'swot_analysis/strength.html')

def report_detail(request, id):
    report = get_object_or_404(StudentReport, id=id)
    return render(request, 'swot_analysis/viewswot.html', {'report': report})

def viewImprovement(request, id):
    report = get_object_or_404(StudentReport, id=id)
    improvements = report.improvements
    addons = report.addons

    return render(request, 'swot_analysis/viewimprovements.html', {
        'report': report,
        'improvements': improvements,
        'addons': addons
    })

from .models import Member

def member_list(request):
    # Fetch all members from the database
    members = Member.objects.all()

    # Pass the members to the template
    return render(request, 'Teams/members.html', {'members': members})

def swotStartNow(request):
    student_id = request.session.get('user_id',None)
    print(student_id)
    report_count = StudentReport.objects.filter(student_id=student_id).count()

    if report_count == 0:
        return render(request, 'swot_analysis/swot.html')

    elif report_count >= 1:
        search_query = request.GET.get('q', '')

        if search_query:
            reports = StudentReport.objects.filter(student_id=student_id, title__icontains=search_query)
        else:
            reports = StudentReport.objects.filter(student_id=student_id)

        print(f"Reports found: {reports}")

        return render(request, 'swot_analysis/list.html', {'reports': reports, 'search_query': search_query})

@csrf_exempt
def delete_report(request, report_id):
    if request.method == 'POST':
        report = StudentReport.objects.get(id=report_id)
        report.delete()
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'})

def swot(request):
    return render(request, 'swot_analysis/swot.html')

def points(request, data):
    print(request.session.get('user_id',None))
    report_count = 0
    if report_count >= 1:
        return render(request, 'swot_analysis/points.html', {"new": "no", "strength": strength, "weakness": weakness, "oppor": opportunity, "threat": threat})
    else:
        student_id = request.session.get('user_id',None)
        objecdata = data
        objedata = objecdata.replace("--", ":")
        objectdata = objedata.replace("-", " ")
        realdata = objectdata.split(",,")
        strength_raw = realdata[0].split(":")
        strength = strength_raw[1].split(",")
        weakness_raw = realdata[1].split(":")
        weakness = weakness_raw[1].split(",")
        opportunity_raw = realdata[2].split(":")
        opportunity = opportunity_raw[1].split(",")
        threat_raw = realdata[3].split(":")
        threat = threat_raw[1].split(",")

        title = 'First analysis'
        savedata = StudentReport(student_id=student_id, title=title, strengths=strength, weakness=weakness, opportunity=opportunity, threat=threat)
        savedata.save()

        return redirect('swot-start-now')

def list(request):
    return render(request, 'swot_analysis/list.html')

def overview(request):
    return render(request, 'swot_analysis/overview.html')

def improvement(request):
    # Filter entries by student_id and order by timestamp
    reports = StudentReport.objects.filter(student_id=request.session.get('user_id',None)).order_by('-timestamp')[:2]
    
    # Initialize an empty dictionary for combined SWOT categories
    combined_swot = {"strength": [], "weakness": [], "opportunity": [], "threat": []}

    if len(reports) >= 2:
        # Define latest and second latest reports
        latest_report = reports[0]
        second_latest_report = reports[1]
        
        # Categories to be compared
        categories = ["strengths", "weakness", "opportunity", "threat"]
        
        for category in categories:
            # Get the list of points in each category for both latest and second latest reports
            latest_points = latest_report.dict.get(category, [])
            second_latest_points = second_latest_report.dict.get(category, [])
            
            # Identify extra points in the latest report that aren't in the second latest
            extra_points = []
            for point in latest_points:
                if point not in second_latest_points:
                    extra_points.append(point)
            
            # Assign the list of extra points to the combined_swot dictionary
            combined_swot[category] = extra_points
    
    return render(request, 'swot_analysis/improve.html', {'combined_swot': combined_swot})

def save_improvements(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            improvements = data.get('improvements', [])
            addons = data.get('addons', {})
            report = StudentReport.objects.filter(student_id=request.session.get('user_id',None)).latest('timestamp')
            report.improvements = improvements
            report.addons = addons
            report.save()

            return JsonResponse({'success': True, 'message': 'Improvements saved successfully.'})

        except StudentReport.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Report not found for this student.'}, status=404)
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)}, status=500)

    return JsonResponse({'success': False, 'message': 'Invalid request method.'}, status=400)

def index(request):
    team_categories = TeamCategory.objects.all()
    members = Member.objects.all()
    context = {'id': request.session.get('user_id',None),
               'categories':team_categories,
               'members':members
               }
    result =[]
    uresult =[]
    top_startups = (
        startupscore.objects
        .values('startup_id')  # Group by startup_id
        .annotate(total_score=Sum(Cast(F('score'), output_field=IntegerField())))  # Convert to int and calculate the sum
        .order_by('-total_score')[:6]  # Order by total_score and limit to top 6
    )
    for entry in top_startups:
        startupname = user_detail.objects.get(user_id=entry['startup_id'])
        entry['name'] = startupname.name
        entry['image']= base64.b64encode(startupname.profile_photo).decode('utf-8')
        result.append(entry)
    print(result)
    top_users = (
        startup_individual_score.objects
        .values('user_id')  # Group by user_id
        .annotate(total_score=Sum(Cast(F('score'), output_field=IntegerField())))  # Convert score to int and calculate sum
        .order_by('-total_score')[:10]  # Order by total_score and limit to top 10
    )

    # Convert QuerySet to a list of dictionaries
    for entry in top_users:
        useridname = user_detail.objects.get(user_id=entry['user_id'])
        entry['name'] = useridname.name
        entry['image']= base64.b64encode(useridname.profile_photo).decode('utf-8')
        uresult.append(entry)
    print(uresult)
    mid = len(uresult) // 2
    firstfive = uresult[:mid]
    nextfive = uresult[mid:]

    context = {'id': request.session.get('user_id',None),
               'categories':team_categories,
               'members':members,
               'results':result,
               'firstfive':firstfive,
               'nextfive':nextfive,
               }

    
    # Convert QuerySet to a list of dictionaries for JSON response
    return render(request, 'index.html',context)

from .models import Member
def add_member(request):
    if request.method == 'POST':
        initialpart = "ME"
        secondpart = str(get_formatted_timestamp())
        ep1 = str(get_formatted_timestamp())
        add_entry_member()
        thirdpart = str(counters['member'])
        user_id = initialpart+secondpart+thirdpart
        # Extract data from the POST request
        name = request.POST.get('name')
        category = request.POST.get('category')
        college_name = request.POST.get('college_name')
        year = request.POST.get('year')
        domain = request.POST.get('domain')
        profile = request.FILES.get('profile_image').read()
        startup_id = request.session.get('user_id')  # This will be a string
        ep1 = str(get_formatted_timestamp())
        password = generate_unique_password(16)

        # Create a new Member instance and save it to the database
        member = Member(
            name=name,
            category=category,
            college_name=college_name,
            year=year,
            domain=domain,
            startup_id=startup_id,  # Saving as a string
            user_id = user_id,
            ep1=ep1,
        )
        member.save()

        userauth = Userauth(
            user_id = user_id,
            username = name,
            password = password
            )
        userauth.save()

        userprofile = user_detail(user_id = user_id,name=name,profile_photo=profile)
        userprofile.save()

        # Redirect to a success page or another page after saving
        return redirect('startup-home')  # Replace with your desired redirect URL

    return redirect('startup-home')

def login(request):
    return render(request,'login.html')

def verificationlogin(request, udata):
    userdata = udata.split('-')
    usern = userdata[0]
    userid = userdata[0]
    passw = userdata[1]
    
    user = Userauth.objects.filter(user_id=usern, password=passw).first()
    if user:
        if usern == user.user_id and passw == user.password:
            request.session['user_id'] = userid
            request.session['username'] = user.username
            # Set session before returning
            
            if user.user_id[0:2] in ["ST", "MR"]:
                return redirect('mentor_home')
            
            elif user.user_id[0:2] in ["SR", "ME"]:
                if user.user_id[0:2] == "SR":
                    request.session['startup_id'] = usern
                    return redirect('startup-home')
                else:
                    member = Member.objects.get(user_id=usern)
                    request.session['startup_id'] = member.startup_id
                    return redirect('startup-home')

            elif user.user_id[0:2] == "IN":
               return redirect('internship_home')
            
            elif user.user_id[0:2] == "CL":
                return redirect('college_home')
            
            else:
                return redirect('course-list')
    else:
        return HttpResponse("<h1>Provide proper credentials</h1>")

def save_swot_analysis(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        strengths = request.POST.get('strengths')
        weakness = request.POST.get('weakness')
        opportunity = request.POST.get('opportunity')
        threat = request.POST.get('threat')

        strengths_list = [s.strip() for s in strengths.split(',')]
        weakness_list = [w.strip() for w in weakness.split(',')]
        opportunity_list = [o.strip() for o in opportunity.split(',')]
        threat_list = [t.strip() for t in threat.split(',')]
        uid = request.POST.get('user_id',None)
        student_report = StudentReport(
            student_id=uid,
            title=title,
            timestamp=timezone.now(),
            strengths=strengths_list,
            weakness=weakness_list,
            opportunity=opportunity_list,
            threat=threat_list,
            improvements=None,
            addons=None
        )
        student_report.save()

        return redirect('improvement')

    return render(request, 'swot_analysis/points.html')


def calender(request):
    return render(request,'Internship/calender.html')

def course_video(request):
    return render(request,'courses/course-video.html')

def internship_home(request):
    current_user_id = request.session.get('user_id', None)

    # Query to check if the current_user_id exists in any team
    in_team = InternTeams.objects.filter(
        Q(member1=current_user_id) | Q(member2=current_user_id) | Q(member3=current_user_id) |
        Q(member4=current_user_id) | Q(member5=current_user_id)
    ).exists()

    # Determine if the user is in a team and set the context
    

    idn = request.session.get('user_id', None)
    udt = []
    uwt = []
    uct = []
    courses = Course.objects.all()
    ud = dailyquestionanswer.objects.filter(user_id=idn).values()
    for i in range(len(ud)):
        udt.append(int(ud[i]['token']))
    
    uw = weeklyquestionanswer.objects.filter(user_id=idn).values()
    for i in range(len(uw)):
        uwt.append(int(uw[i]['token']))
    
    uc = commonquestionanswer.objects.filter(user_id=idn).values()
    for i in range(len(uc)):
        uct.append(int(uc[i]['token']))
    
    score = int(sum(udt)) + int(sum(uwt)) + int(sum(uct))
    def add(a, b):
        return (a + b)
    taskcom = add(len(ud), len(uw))
    fullcom = add(taskcom, len(uc))
    banner = bannerupload.objects.all()
    for entry in banner:
        entry.banner1 = base64.b64encode(entry.banner1).decode('utf-8')
        entry.banner2 = base64.b64encode(entry.banner2).decode('utf-8')
        entry.banner3 = base64.b64encode(entry.banner3).decode('utf-8')
    statement = []
    result = dailyquestionanswer.objects.values('user_id').annotate(entry_count=Count('user_id')).order_by('-entry_count')
    result2 = weeklyquestionanswer.objects.values('user_id').annotate(entry_count=Count('user_id')).order_by('-entry_count')
    result3 = commonquestionanswer.objects.values('user_id').annotate(entry_count=Count('user_id')).order_by('-entry_count')
    for entry in result :
        dp = user_detail.objects.get(user_id=entry['user_id'])
        if(dp.profile_photo):
            entry['image'] = base64.b64encode(dp.profile_photo).decode('utf-8')
    for entry in result2 :
        dp = user_detail.objects.get(user_id=entry['user_id'])
        if(dp.profile_photo):
            entry['image'] = base64.b64encode(dp.profile_photo).decode('utf-8')
        
    for entry in result3 :
        dp = user_detail.objects.get(user_id=entry['user_id'])
        if(dp.profile_photo):
            entry['image'] = base64.b64encode(dp.profile_photo).decode('utf-8')
    # Get all categories as a list of dictionaries

    statement_category_list = statementshowcasecategoryform.objects.all().values('statementcategory')
    print(statement_category_list)
    statement = []
    statement_data =[]
    for category in statement_category_list:
        statements = statementshowcaseform.objects.filter(statementcategory=category['statementcategory']).values()
        print(statements)
        for obj in statements:
            statement_data.append(obj)
    statement.append(statement_data)
    print(statement)
    for course in courses:
        course.course_image_list = base64.b64encode(course.course_image_list).decode('utf-8')

    context = {
        "id": idn,
        "name": request.session.get('username', None),
        "wr": result2,
        'banner': banner,
        "dr": result,
        "cr": result3,
        "token": score,
        "taskcom": fullcom,
        'statements': statement,
        'courses':courses,
        'event_image': None,
        'has_images': False,
        'home_image': None,
        'has_image': False,
        'in_team': 'yes' if in_team else 'no'
         # Ensure statement is included here
    }
     # Add home image to context if it exists
    try:
        # Get the latest home image
        latest_home_image = HomeImage.objects.latest('uploaded_at')
        
        # Convert binary data to base64 for HTML display
        if latest_home_image.intern_home:
            home_image = base64.b64encode(latest_home_image.intern_home).decode('utf-8')
            context['home_image'] = home_image
            context['has_image'] = True
        
    except HomeImage.DoesNotExist:
        # Keep default values in context
        pass
    try:
        # Get the latest event image
        latest_Event_image = Events_update.objects.latest('uploaded_at')
        
        # Convert binary data to base64 for HTML display
        if latest_Event_image.events:
            event_image = base64.b64encode(latest_Event_image.events).decode('utf-8')
            context['event_image'] = event_image
            context['has_images'] = True
        
    except Events_update.DoesNotExist:
        # Keep default values in context
        pass
    
    return render(request, 'Internship/internship_home.html', context)


def my_learning(request):
    return render(request,'Internship/my_learning.html')

from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from .models import StudentReport, Question 
from django.views.decorators.csrf import csrf_exempt
import json


def get_questions(request):
    # Query all questions
    questions = Question.objects.all()
    
    # Format the data
    questions_data = []
    for question in questions:
        questions_data.append({
            "question_number": question.question_number,
            "category_name": question.category_name,
            "question": question.question,
            "options": [
                {"text": question.option1, "percentage": question.efficiency_1, "description": question.description_1},
                {"text": question.option2, "percentage": question.efficiency_2, "description": question.description_2},
                {"text": question.option3, "percentage": question.efficiency_3, "description": question.description_3},
                {"text": question.option4, "percentage": question.efficiency_4, "description": question.description_4},
            ],
            "correct_answer": question.correct_option
        })

    # Return as JSON response
    return JsonResponse({"questions": questions_data})

def costover(request):
    return render(request, 'swot_analysis/costover.html')

def costquestions(request,category):
    request.session['category']=category
    return render(request, 'swot_analysis/costquestions.html')

def get_questions(request):
    # Query all questions
    category = request.session.get('category',None)
    questions = Question.objects.filter(category_name=category)
    
    # Format the data
    questions_data = []
    for question in questions:
        questions_data.append({
            "question_number": question.question_number,
            "category_name": question.category_name,
            "question": question.question,
            "options": [
                {"text": question.option1, "percentage": question.efficiency_1, "description": question.description_1},
                {"text": question.option2, "percentage": question.efficiency_2, "description": question.description_2},
                {"text": question.option3, "percentage": question.efficiency_3, "description": question.description_3},
                {"text": question.option4, "percentage": question.efficiency_4, "description": question.description_4},
            ],
            "correct_answer": question.correct_option
        })

    # Return as JSON response
    return JsonResponse({"questions": questions_data})

def costcategory(request):
    categories = CostCuttingCategoryMaster.objects.all()
    for category in categories:
        category.category_image = base64.b64encode(category.category_image).decode('utf-8')
    return render(request, 'swot_analysis/costcategory.html',{'categories':categories})

def startup_dashboard(request):
    result =[]
    uresult =[]
    banner = banneruploadstartup.objects.all()
    for entry in banner:
        entry.banner1 = base64.b64encode(entry.banner1).decode('utf-8')
        entry.banner2 = base64.b64encode(entry.banner2).decode('utf-8')
        entry.banner3 = base64.b64encode(entry.banner3).decode('utf-8')
    investor = AddInvestor.objects.filter(login_id=request.session.get('user_id'))
    top_startups = (
        startupscore.objects
        .filter(startup_id=request.session.get('startup_id',None))
        .values('startup_id')  # Group by startup_id
        .annotate(total_score=Sum(Cast(F('score'), output_field=IntegerField())))  # Convert to int and calculate the sum
        .order_by('-total_score')[:6]  # Order by total_score and limit to top 6
    )
    for entry in top_startups:
        startupname = Userauth.objects.get(user_id=entry['startup_id'])
        entry['name'] = startupname.username
        result.append(entry)
    print(result[0]['total_score'])
    top_users = (
        startup_individual_score.objects
        .filter(startup_id=request.session.get('startup_id',None))
        .values('user_id')  # Group by user_id
        .annotate(total_score=Sum(Cast(F('score'), output_field=IntegerField())))  # Convert score to int and calculate sum
        .order_by('-total_score')[:10]  # Order by total_score and limit to top 10
    )
    print(top_users)
    member = Member.objects.filter(startup_id=request.session.get('startup_id',None))
    for entry in member:
        dp = user_detail.objects.get(user_id=entry.user_id)
        entry.image = base64.b64encode(dp.profile_photo).decode('utf-8')
    print(member)
    # Convert QuerySet to a list of dictionaries
    for entry in top_users:
        useridname = user_detail.objects.get(user_id=entry['user_id'])
        entry['name'] = useridname.name
        entry['image']=base64.b64encode(useridname.profile_photo).decode('utf-8')
        uresult.append(entry)
    print(uresult)
    other_startup = StartupRegistartion.objects.exclude(user_id=request.session.get('startup_id',None))[:4]
    myname = StartupRegistartion.objects.get(user_id=request.session.get('startup_id',None))
    context = {
        "id":request.session.get('user_id',None),
        "name":myname.startup_Name,
        'token':result[0]['total_score'],
        'uresult':uresult,
        "investor":investor,
        'members':member,
        'os':other_startup,
        'banner':banner
        }
    return render(request,'startup_dashboard.html',context)

def logout(request):
    del request.session['user_id']
    return redirect('login')

def get_formatted_timestamp():
    """
    Get the current date formatted as DDMMYYYY.
    """
    now = datetime.now()
    return now.strftime('%d%m%Y')


def add_entry(category):
    """
    Update the counter for the given category, reset if the date changes or counter reaches its limit.
    """
    global last_date

    current_date = get_formatted_timestamp()

    if last_date != current_date or counters[category] == 9999:
        counters[category] = 0  # Reset the counter
        last_date = current_date  # Update the last date
    else:
        ep1 = str(get_formatted_timestamp())
        entrydata = Member.objects.filter(ep1 = ep1).values()
        countd = len(entrydata)
        print(countd)
        if countd>0:
            
                counters[category] = countd
                print("if")
                print(counters[category])
           
        else:
            counters[category] += 1  # Increment the counter
            print('else')
            print(counters[category])
        
    print(f"Category: {category}, Date: {current_date}, Counter: {counters[category]}")

# Usage functions for specific categories
def add_entry_member():
    add_entry('member')

@csrf_exempt
def gamescoreupdatecostcutting(request):
    if request.method == "POST":
        # Get the session data and POST data
        startup_id = request.session.get('startup_id', None)  # Fixed duplicate user_id assignment
        user_id = request.session.get('user_id', None)
        score = int(request.POST.get('score'))  # Ensure score is an integer
        category = request.POST.get('category')
        game = request.POST.get('game')

        print(startup_id)
        print(user_id)
        print(score)
        print(category)
        print(game)

        # Fetch data from the database
        entry1 = startupscore.objects.filter(startup_id=startup_id, game_name=game, category=category)
        entry2 = startup_individual_score.objects.filter(user_id=user_id, startup_id=startup_id, game_name=game, category=category)

        # Update or create for entry1
        if entry1.exists():
            for record in entry1:
                if int(record.score) < score:  # Update the score if it's less than the new score
                    record.score = str(score)
                    record.save()  # Save each updated record
        else:
            # Create a new record if no existing entry
            data = startupscore(startup_id=startup_id, game_name=game, category=category, score=str(score))
            data.save()

        # Update or create for entry2
        if entry2.exists():
            for record in entry2:
                if int(record.score) < score:  # Update the score if it's less than the new score
                    record.score = str(score)
                    record.save()  # Save each updated record
        else:
            # Create a new record if no existing entry
            data = startup_individual_score(user_id=user_id, startup_id=startup_id, game_name=game, category=category, score=str(score))
            data.save()

        # Return a JSON response to the frontend
        return JsonResponse({'status': 'success'})

    # Return error for non-POST methods
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)