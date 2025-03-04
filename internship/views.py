from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
from .models import InternRegistartion
from community.models import user_detail
from .models import dailyquestion, dailyquestionanswer ,weeklyquestion , weeklyquestionanswer ,commonquestion , commonquestionanswer,bannerupload
from django.db.models import Count
import subprocess
import tempfile
from  groq import Groq
import base64
from IdeaSubmission.models import IdeaSubmission

# Assuming 'GroqClient' is the correct class to initialize the API client
groq_client = Groq(api_key="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")


# Create your views here.

def realtimeintern_apply(request):
    pk = request.session.get('user_id', None)

    # Fetch the actual model instance
    try:
        userdata = InternRegistartion.objects.get(user_id=pk)
    except InternRegistartion.DoesNotExist:
        return JsonResponse({"status": "user_not_found"})

    # Check the status and update accordingly
    if userdata.status == 'requested':
        return JsonResponse({"status": "already_applied"})
    else:
        userdata.domain = 'realtime'
        userdata.duration = '6 months'
        userdata.status = "requested"
        userdata.save()  # Save the changes to the database
        return JsonResponse({"status": "success"})



def appintern(request,dom):
    pk=request.session.get('user_id',None)
    try:
        userdata = InternRegistartion.objects.get(user_id=pk)
    except InternRegistartion.DoesNotExist:
        return JsonResponse({"status": "user_not_found"})
    if userdata.status == 'requested':
        return JsonResponse({"status": "already_applied"})
    else:
        userdata.domain = dom
        userdata.duration = '6 months'
        userdata.status = "requested"
        userdata.save()
        return JsonResponse({"status":"success"})


@csrf_exempt
def uploaddq(request):
    qid=request.POST.get('qid')
    question=request.POST.get('question')
    si=request.POST.get('si')
    so=request.POST.get('so')
    ao=request.POST.get('ao')
    posted_on = str(datetime.now().date())
    data = dailyquestion(posted_on = posted_on , question_id=qid,question=question,sample_input=si,sample_output=so,actual_output = ao)
    data.save()
    return JsonResponse({'status':'success'})
    


@csrf_exempt
def uploadwq(request):
    qid=request.POST.get('qid')
    question=request.POST.get('question')
    si=request.POST.get('si')
    so=request.POST.get('so')
    ao=request.POST.get('ao')
    posted_on = str(datetime.now().date())
    data = weeklyquestion(posted_on = posted_on , question_id=qid,question=question,sample_input=si,sample_output=so,actual_output = ao)
    data.save()
    return JsonResponse({'status':'success'})

@csrf_exempt
def uploadcq(request):
    qid=request.POST.get('qid')
    question=request.POST.get('question')
    si=request.POST.get('si')
    so=request.POST.get('so')
    ao=request.POST.get('ao')
    posted_on = str(datetime.now().date())
    data = commonquestion(posted_on = posted_on , question_id=qid,question=question,sample_input=si,sample_output=so,actual_output = ao)
    data.save()
    return JsonResponse({'status':'success'})


def showdq(request):
    time=str(datetime.now().date())
    qdata = list(dailyquestion.objects.filter().values())
    context={
        'qdata':qdata
        }
    return render (request,'internship/dq.html',context)

def showwq(request):
    time=str(datetime.now().date())
    qdata = list(weeklyquestion.objects.filter(posted_on = time).values())
    context={
        'qdata':qdata
        }
    return render (request,'internship/wq.html',context)

def showcq(request):
    time=str(datetime.now().date())
    qdata = list(commonquestion.objects.filter().values())
    context={
        'qdata':qdata
        }
    return render (request,'internship/cq.html',context)


def getdq(request,pk):
    qd = list(dailyquestion.objects.filter(id=pk).values())
    qdata = qd[0]
    context = {'qdata':qdata, 'type':'d'}
    return render(request,'internship/code_editor.html',context)

def getwq(request,pk):
    qd = list(weeklyquestion.objects.filter(id=pk).values())
    qdata = qd[0]
    
    context = {'qdata':qdata, 'type':'w'}
    return render(request,'internship/code_editor.html',context)

def getcq(request,pk):
    qd = list(commonquestion.objects.filter(id=pk).values())
    qdata = qd[0]
    context = {'qdata':qdata, 'type':'c'}
    return render(request,'internship/code_editor.html',context)


@csrf_exempt
def check_answer(request):
    gqid = request.POST.get('qid')
    code = request.POST.get('program')
    user_id = request.POST.get('user_id')
    posted_on = str(datetime.now().date())
    if not gqid or not code:
        return JsonResponse({'status': 'failed', 'message': 'Missing qid or program'})

    try:
        data = dailyquestion.objects.get(id=gqid)
        expected_output = data.actual_output.strip()

        # Save the code to a temporary file
        with tempfile.NamedTemporaryFile(suffix='.py', delete=False) as temp_file:
            temp_file.write(code.encode('utf-8'))
            temp_file.flush()

            # Run the code using subprocess
            result = subprocess.run(
                ['python', temp_file.name],
                capture_output=True,
                text=True
            )

        if result.returncode != 0:
                error_message = result.stderr.strip()
                explanation = get_error_explanation(error_message, code)
                return JsonResponse({'status':'error','output': f"{error_message}\n\n{explanation}", "error" : error_message})
        
        actual_output = result.stdout.strip()
        condition = False

        # Debugging Outputs
        print("Expected Output:", expected_output)
        print("Actual Output:", actual_output)
        if expected_output.isnumeric():
            condition = int(actual_output) == int(expected_output)
        else:
            try:
                condition = float(actual_output) == float(expected_output)
            except ValueError:  # This will handle every datatypes like boolean, string and list.. 
                condition = actual_output.lower() == expected_output.lower()
        
        if condition :
            condition = False # Resetting the flag
            check =list(dailyquestionanswer.objects.filter(user_id=user_id,question_gid = gqid ).values())
            if(len(check)==0):
                entry = dailyquestionanswer(user_id=user_id,question_gid = gqid , submitted_on = posted_on , token = "10")
                entry.save()
                return JsonResponse({'status': 'success', 'output': actual_output})
            else:
                return JsonResponse({'status': 'not allowed', 'message': 'Output mismatch', 'output': actual_output})

        else:
            return JsonResponse({'status': 'failed', 'message': 'Output mismatch', 'output': actual_output})

    except dailyquestion.DoesNotExist:
        return JsonResponse({'status': 'failed', 'message': 'Question not found'})
    except subprocess.TimeoutExpired:
        return JsonResponse({'status': 'failed', 'message': 'Code execution timed out', 'output': actual_output})
    except Exception as e:
        return JsonResponse({'status': 'failed', 'message': f'Error: {str(e)}'})

def get_error_explanation(error, code):
    prompt = f"Explain the following error: {error}\nExplain this in a short paragraph.\nGive ways to correct the error so it goes away. Don't provide corrected code.\nCODE: {code}"

    # Assuming 'groq_client.chat_completions.create' is how you send the request
    response = groq_client.chat.completions.create(
        messages=[
            {"role": "system", "content": "You are a helpful assistant for debugging."},
            {"role": "user", "content": prompt}
        ],
        model="llama3-8b-8192",
        temperature=0.5,
        max_tokens=1024
    )

    # Return the explanation from Groq's response
    return response.choices[0].message.content


@csrf_exempt
def check_answerw(request):
    gqid = request.POST.get('qid')
    code = request.POST.get('program')
    user_id = request.POST.get('user_id')
    posted_on = str(datetime.now().date())
    if not gqid or not code:
        return JsonResponse({'status': 'failed', 'message': 'Missing qid or program'})

    try:
        data = weeklyquestion.objects.get(id=gqid)
        expected_output = data.actual_output.strip()

        # Save the code to a temporary file
        with tempfile.NamedTemporaryFile(suffix='.py', delete=False) as temp_file:
            temp_file.write(code.encode('utf-8'))
            temp_file.flush()

            # Run the code using subprocess
            result = subprocess.run(
                ['python', temp_file.name],
                capture_output=True,
                text=True
            )

        if result.returncode != 0:
                error_message = result.stderr.strip()
                explanation = get_error_explanation(error_message, code)
                return JsonResponse({'status':'error','output': f"{error_message}\n\n{explanation}", "error" : error_message})
        
        actual_output = result.stdout.strip()

        condition = False

        # Debugging Outputs
        print("Expected Output:", expected_output)
        print("Actual Output:", actual_output)
        if expected_output.isnumeric():
            condition = int(actual_output) == int(expected_output)
        else:
            try:
                condition = float(actual_output) == float(expected_output)
            except ValueError:  # This will handle every datatypes like boolean, string and list.. 
                condition = actual_output.lower() == expected_output.lower()
        
        if condition :
            condition = False #Resetting the flag
            check =list(dailyquestionanswer.objects.filter(user_id=user_id,question_gid = gqid ).values())
            if(len(check)==0):
                entry = dailyquestionanswer(user_id=user_id,question_gid = gqid , submitted_on = posted_on , token = "10")
                entry.save()
                return JsonResponse({'status': 'success', 'output': actual_output})
            else:
                return JsonResponse({'status': 'not allowed', 'message': 'Output mismatch', 'output': actual_output})

        else:
            return JsonResponse({'status': 'failed', 'message': 'Output mismatch', 'output': actual_output})

    except dailyquestion.DoesNotExist:
        return JsonResponse({'status': 'failed', 'message': 'Question not found'})
    except subprocess.TimeoutExpired:
        return JsonResponse({'status': 'failed', 'message': 'Code execution timed out', 'output': actual_output})
    except Exception as e:
        return JsonResponse({'status': 'failed', 'message': f'Error: {str(e)}'})

@csrf_exempt
def check_answerc(request):
    gqid = request.POST.get('qid')
    code = request.POST.get('program')
    user_id = request.POST.get('user_id')
    posted_on = str(datetime.now().date())
    if not gqid or not code:
        return JsonResponse({'status': 'failed', 'message': 'Missing qid or program'})

    try:
        data = commonquestion.objects.get(id=gqid)
        expected_output = data.actual_output.strip()

        # Save the code to a temporary file
        with tempfile.NamedTemporaryFile(suffix='.py', delete=False) as temp_file:
            temp_file.write(code.encode('utf-8'))
            temp_file.flush()

            # Run the code using subprocess
            result = subprocess.run(
                ['python', temp_file.name],
                capture_output=True,
                text=True
            )

        if result.returncode != 0:
                error_message = result.stderr.strip()
                explanation = get_error_explanation(error_message, code)
                return JsonResponse({'status':'error','output': f"{error_message}\n\n{explanation}", "error" : error_message})
        
        actual_output = result.stdout.strip()
        condition = False

        # Debugging Outputs
        print("Expected Output:", expected_output)
        print("Actual Output:", actual_output)
        if expected_output.isnumeric():
            condition = int(actual_output) == int(expected_output)
        else:
            try:
                condition = float(actual_output) == float(expected_output)
            except ValueError:  # This will handle every datatypes like boolean, string and list.. 
                condition = actual_output.lower() == expected_output.lower()
        
        if condition :
            condition = False #Resetting
            check =list(dailyquestionanswer.objects.filter(user_id=user_id,question_gid = gqid ).values())
            if(len(check)==0):
                entry = dailyquestionanswer(user_id=user_id,question_gid = gqid , submitted_on = posted_on , token = "10")
                entry.save()
                return JsonResponse({'status': 'success', 'output': actual_output})
            else:
                return JsonResponse({'status': 'not allowed', 'message': 'Output mismatch', 'output': actual_output})

        else:
            return JsonResponse({'status': 'failed', 'message': 'Output mismatch', 'output': actual_output})

    except dailyquestion.DoesNotExist:
        return JsonResponse({'status': 'failed', 'message': 'Question not found'})
    except subprocess.TimeoutExpired:
        return JsonResponse({'status': 'failed', 'message': 'Code execution timed out', 'output': actual_output})
    except Exception as e:
        return JsonResponse({'status': 'failed', 'message': f'Error: {str(e)}'})

def progress(request):
    idn = request.session.get('user_id', None)
    udt = []
    uwt = []
    uct = []
    
    ud = dailyquestionanswer.objects.filter(user_id=idn).values()
    for i in range(len(ud)):
        udt.append(int(ud[i]['token']))
    
    uw = weeklyquestionanswer.objects.filter(user_id=idn).values()
    for i in range(len(uw)):
        uwt.append(int(uw[i]['token']))
    
    uc = commonquestionanswer.objects.filter(user_id=idn).values()
    for i in range(len(uc)):
        uct.append(int(uc[i]['token']))
    ds,ws,cs = int(sum(udt)) , int(sum(uwt)) , int(sum(uct))
    score = int(sum(udt)) + int(sum(uwt)) + int(sum(uct))
    def add(a, b):
        return (a + b)
    taskcom = add(len(ud), len(uw))
    fullcom = add(taskcom, len(uc))
    banner = bannerupload.objects.filter().values()
    
    result = dailyquestionanswer.objects.values('user_id').annotate(entry_count=Count('user_id')).order_by('-entry_count')
    result2 = weeklyquestionanswer.objects.values('user_id').annotate(entry_count=Count('user_id')).order_by('-entry_count')
    result3 = commonquestionanswer.objects.values('user_id').annotate(entry_count=Count('user_id')).order_by('-entry_count')

    # Get all categories as a list of dictionaries
    pimage_data = user_detail.objects.get(user_id=request.session.get('user_id',None))
    if pimage_data.profile_photo: 
        profile_image = base64.b64encode(pimage_data.profile_photo).decode('utf-8')
    else:
        profile_image = None

    userinternship = InternRegistartion.objects.get(user_id=request.session.get("user_id",None))
    internact = userinternship.ep2
    internlist=internact.get('intern_history')
    context = {
        "id": idn,
        "name": request.session.get('username', None),
        "wr": result2,
        'banner': banner,
        "dr": result,
        "cr": result3,
        "token": score,
        "taskcom": fullcom,
        'ds':ds,
        'ws':ws,
        'cs':cs,
        'profile_image':profile_image,
        'internlist':internlist
         # Ensure statement is included here
    }
    return render (request,'internship/internshipprogress.html',context)


def request_teammate(request):
    # Get the statement_id from the request
    statement_id = request.GET.get('statement_id')
    user_id = request.session.get('user_id',None)

    # Fetch all IdeaSubmission entries with the given statement_id
    ideas = IdeaSubmission.objects.filter(statement_id=statement_id)

    # Prepare a list to hold the final data
    
    # Pass the data to the template
    context = {'teammates': ideas,'user_id':user_id}
    return render(request, 'Internship/request_teammate.html', context)


from django.contrib import messages
from .models import InternTeams  # Assuming InternTeams is the model for the teams table
from django.db.models import Q

def connect_user(request, user_id):
    # Get the current user who clicked "Connect"
    current_user_id = request.session.get('user_id', None)
    
    
    # Check if the user is already in a team with the current_user_id
    existing_team = InternTeams.objects.filter(
        Q(member1=current_user_id) | Q(member2=current_user_id) | Q(member3=current_user_id) |
        Q(member4=current_user_id) | Q(member5=current_user_id)
    ).first()

    if existing_team:
        # Check if the user_id is already in the team with current_user_id
        if user_id in [existing_team.member1, existing_team.member2, existing_team.member3, existing_team.member4, existing_team.member5]:
            messages.error(request, "This user is already your teammate.")
            return redirect('internship_home')  # Redirect to the appropriate page
        
        # Check if the team is full
        if None not in [existing_team.member1, existing_team.member2, existing_team.member3, existing_team.member4, existing_team.member5]:
            messages.error(request, "Team is full.")
            return redirect('internship_home')  # Redirect to the appropriate page
        
        # Assign user to the next available slot in the existing team
        if existing_team.member1 is None:
            existing_team.member1 = user_id
        elif existing_team.member2 is None:
            existing_team.member2 = user_id
        elif existing_team.member3 is None:
            existing_team.member3 = user_id
        elif existing_team.member4 is None:
            existing_team.member4 = user_id
        elif existing_team.member5 is None:
            existing_team.member5 = user_id
        
        existing_team.save()
        messages.success(request, "You have been added to the team.")
        return redirect('internship_home')  # Redirect to the appropriate page
    
    else:
        # No team exists for the user, create a new team and assign them to member2
        new_team = InternTeams.objects.create(
            member1=current_user_id,  # Assign member1 to the current user
            member2=user_id,  # Assign the current user to member2
            member3=None,
            member4=None,
            member5=None
        )
        messages.success(request, "New team created and you have been assigned as member2.")
        return redirect('internship_home')
    
    