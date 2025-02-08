import base64
from token import OP
from venv import create
from django.shortcuts import redirect, render
from django.http import HttpResponse , JsonResponse
from django.views.decorators import csrf
from .forms import *
from .models import create_community , user_community 
from .models import community_chat_data , post_details , follower , user_detail
import json , random , datetime
from django.views.decorators.csrf import csrf_exempt
import uuid

def generate_unique_community_id():
    return "CM" + str(uuid.uuid4().hex[:8])

# Create your views here.

def community_index(request, pk):
    form = create_communityf()
    if request.method == "POST":
        community_imagedata = request.FILES.get('community_profile')
        community_image = community_imagedata.read()
        form = create_communityf(request.POST, request.FILES)  # Pass both POST and FILES
        if form.is_valid():
            cid = generate_unique_community_id()
            community_name = form.cleaned_data['community_name']
            
            # Save community
            community = create_community(
                community_name=community_name,
                community_image=community_image,
                community_id=cid,
                creator_id=pk
            )
            community.save()

            # Save user-community relation
            user = user_community(user_id=pk, community_id=cid, role="admin")
            user.save()

            return redirect('community:community_home')
        else:
            return HttpResponse("Data not saved. Invalid form.")

    return render(request, 'community/create_communityform.html', {'form': form})



def editprofile(request):
    pk=request.session.get('user_id',None)
    form = edit_profilef()
    if request.method == "POST":
        profile_image = request.FILES.get('Profile').read()
        form = edit_profilef(request.POST, request.FILES)  # Pass both POST and FILES
        if form.is_valid():
           
            bio = form.cleaned_data['Bio']
            

            profile_changes = user_detail.objects.get(user_id=pk)
            profile_changes.bio = bio
            profile_changes.profile_photo = profile_image
            profile_changes.save()
            return redirect('community:community_home')
        else:
            return HttpResponse("Data not saved. Invalid form.")

    return render(request, 'community/editprofile.html', {'form': form})

def create_communityini(request):
    context={'id':request.session.get('user_id',None)}
    
    return render(request,'community/create_communityhome.html',context)


def community_list(request):
   
    pk = request.session.get('user_id',None)
    community = list(user_community.objects.filter(user_id=pk).values())
    print(community)
    entry=[]
    for i in range(len(community)):
        entry.append(create_community.objects.filter(community_id = community[i]['community_id']).values())
    if(len(entry)>0):
        context={
            'data':entry,
            'id':pk
            }
        return render(request,'community/list_of_community.html', context)
    else:
         context={
            'id':pk
            }
         return render(request,'community/create_communityhome.html',context)
    
@csrf_exempt
def community_data(request,pk):
    if request.method == "GET":
        try:
            # Get the community object with the given ID
            data = list(create_community.objects.filter(community_id=pk).values())
            for i in range(len(data)):
                data[i]['community_image'] = base64.b64encode(data[i]['community_image']).decode('utf-8')
            # Convert the QuerySet into a list of dictionaries
            messdata = list(community_chat_data.objects.filter(community_id=pk).values())
            return JsonResponse({'data': data,'messdata':messdata}, safe=False)
        except create_community.DoesNotExist:
            return JsonResponse({'error': 'Community not found'}, status=404)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)

@csrf_exempt
def chat_community(request):
    if request.method == 'POST':
        try:
            # Decode the JSON body
            message = json.loads(request.body.decode('utf-8'))
            sendid=message['send_id']
            print(sendid)
            commid = message['community_id']
            ct = message['contenttype']
            ch = message['chat']
            sd=message['sent_date']
            mesid = message['message_id']
            print(message['community_id'])  # Use 'chat' instead of 'msg' to match the JavaScript code
            # Process the message (e.g., save to database or forward to chat logic)
            data = community_chat_data(message_id=mesid , user_id=sendid, community_id=commid, content_type=ct, messagecontent=ch)
            data.save()
            resdata = list(community_chat_data.objects.filter(message_id=mesid).values())
            return JsonResponse({'data': resdata , 'message': 'Message received!'})
        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'error': 'Invalid JSON format'}, status=400)
    return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=405)


def mediaform(request,uid,comid):
    context={
    'userid':uid,
    'comm_id' : comid}
    return render(request,'community/mediaform.html',context)

def joincomm(request,pk):
    return HttpResponse("search")

@csrf_exempt
def mediapostupload(request):
    if request.method == "POST":
        # Extract text fields from request.POST
        caption = request.POST.get('caption')
        mediatype = request.POST.get('mediatype')
        userid = request.POST.get('userid')
        commid = request.POST.get('commid')

        # Extract file from request.FILES
        file = request.FILES.get('file').read()

        # Validate required fields
        if not all([caption, mediatype, userid, commid, file]):
            return JsonResponse({'error': 'Missing required fields'}, status=400)

        # Save to database
        message_id = request.POST.get('message_id')
        entrydata = community_chat_data(
            message_id=message_id,
            user_id=userid,
            community_id=commid,
            content_type=mediatype,
            media_caption=caption,
            media_content=file
        )
        entrydata.save()
        file_path = list(community_chat_data.objects.filter(message_id=message_id).values())
        fp=file_path[0]
        return JsonResponse({'success': 'yes', 'message_id': message_id,"file_path":fp['media_content'],'sent_date':fp['sent_date']}, safe=False)



def community_info(request,pk):
    user = request.session.get('user_id',None)
     
    data = list(create_community.objects.filter(community_id=pk).values())
    userdata = list(user_community.objects.filter(community_id=pk).values())
    data1=data[0]
    data1['community_image'] = base64.b64encode(data1['community_image']).decode('utf-8')
    admin=0
    if data1['creator_id']==user:
        admin=1
        request.session['community_id'] = pk
    print(data)
    context={
        'detail':data1,
        "user":userdata,
        'admin':admin
        }
    return render(request,'community/community_info.html',context)


def community_content_change(request):
    form = change_communityf()
    
    if request.method == "POST":
        Ucommunity_image = request.FILES.get('Updated_community_profile').read()
        form = change_communityf(request.POST, request.FILES)  # Pass both POST and FILES
        if form.is_valid():
            community_id = request.session.get('community_id',None)
            user_id = request.session.get('user_id',None)
            Ucommunity_name = form.cleaned_data['Updated_community_name']
            

            # Save community
            community = create_community.objects.get(community_id=community_id)
         
            
            community.community_name=Ucommunity_name
            community.community_image=Ucommunity_image
            community.save()

            # Save user-community relation
            

            return redirect('community:community_home')
        else:
            return HttpResponse("Data not saved. Invalid form.")

    return render(request, 'community/change_community_content.html', {'form': form})

def edit_chat(request,pk,cd):
    data1 = list(create_community.objects.filter(community_id=cd).values())
    data = list(community_chat_data.objects.filter(community_id=cd,user_id=pk).values())
    data2 = data1[0]
    context = {
        "detail":data,
        "details": data2

        }
    return render(request,'community/edit_chat.html',context)


@csrf_exempt
def edit_content(request):
    if request.method == "POST":
        try:
            message = json.loads(request.body.decode('utf-8'))
            # Extracting data from POST request
            mid = message['mess_id']  # Using POST to get message_id
            nc = message['nc']  # Using POST to get new content

            # Fetching the message object
            messobj = community_chat_data.objects.get(message_id=mid)
            messobj.messagecontent = nc
            messobj.editted = "editted"
            messobj.save()

            return HttpResponse("done")
        except community_chat_data.DoesNotExist:
            return HttpResponse("Message not found", status=404)
        except Exception as e:
            return HttpResponse(f"Error: {str(e)}", status=500)
    else:
        return HttpResponse("Invalid request method", status=405)

def view_media(request,pk,cd):
    print("id is:",pk)
    community = list(user_community.objects.filter(user_id=pk).values())
    print(community)
    entry=[]
    for i in range(len(community)):
        entry.append(create_community.objects.filter(community_id = community[i]['community_id']).values())
    context={
            'data':entry,
            'id':pk
            }
    return render(request,'community/mediaview.html')



def join_community(request):
    return render(request,'community/join_community.html')


def search_community(request,pk,query):
        qd = query.replace("%20"," ")   
        uid = pk
        print(qd)
        data = list(create_community.objects.filter(community_name__icontains=qd).values())
        for entry in data:
            entry['community_image'] = base64.b64encode(entry['community_image']).decode('utf-8')
        if(len(data)>0):
            context = {
                "data": data  ,
                "id":uid
                }
            return render(request,'community/join_community.html',context)
        else:
            return JsonResponse({"data":"no data found"})
@csrf_exempt
def add_member(request):
    if request.method == "POST":
        comm_id = request.POST.get("community_id")
        uid = request.POST.get("uid")
        data = user_community(user_id = uid,community_id = comm_id, role="follower")
        data.save()
        return HttpResponse("done")

@csrf_exempt
def delete_member(request):
    if request.method == "POST":
        comm_id = request.POST.get("community_id")
        uid = request.POST.get("uid")
        data = user_community.objects.get(user_id = uid,community_id = comm_id, role="follower")
        data.delete()
        return HttpResponse("done")

@csrf_exempt
def follow_member(request):
    if request.method == "POST":
        to_id = request.POST.get("to_id")
        uid = request.POST.get("uid")
        data = follower(from_id = uid, to_id = to_id)
        data.save()
        return HttpResponse("done")

@csrf_exempt
def unfollow_member(request):
    if request.method == "POST":
        to_id = request.POST.get("to_id")
        uid = request.POST.get("uid")
        data = follower.objects.get(from_id = uid, to_id = to_id)
        data.delete()
        return HttpResponse("done")


def community_home(request):
    pk = request.session.get('user_id',None)
    following_ids = follower.objects.filter(from_id=pk).values_list('to_id', flat=True)
    
    # Fetch all posts from users in the following_ids list in one query
    posts = post_details.objects.filter(posted_by__in=following_ids).values()

    # Process and encode media for each post
    postd = []
    for post in posts:
        if post['media']:  # Check if media is not None
            post['media'] = base64.b64encode(post['media']).decode('utf-8')
        postd.append(post)
    for entry in postd:
        profileimage = user_detail.objects.get(user_id=entry['posted_by'])
        entry['profile_image']=base64.b64encode(profileimage.profile_photo).decode('utf-8')
    user = list(user_detail.objects.filter(user_id = pk).values())
    userd = user[0]
    community_id=[]
    cd=[]
    ccd=[]
    uc_details = list(user_community.objects.filter(user_id=pk).values())
    for i in range(len(uc_details)):
       community_id.append( uc_details[i]['community_id'])
    print(community_id)
    for i in range (len(community_id)):
        community_details=list(create_community.objects.filter(community_id=community_id[i]).values())
        community_details[0]['community_image'] = base64.b64encode(community_details[0]['community_image']).decode('utf-8')
        cd.append(community_details[0])
    print(postd)
    common_community_details=list(create_community.objects.filter().values())
    for community in common_community_details[:]:  # Iterate over a copy of the list
       if any(community['community_id'] == c['community_id'] for c in cd):
          common_community_details.remove(community)
    for community in common_community_details:
        community['community_image']= base64.b64encode(community['community_image']).decode('utf-8')
    user_profile_image = user_detail.objects.get(user_id=request.session.get('user_id',None))
    pimage = base64.b64encode(user_profile_image.profile_photo).decode('utf-8')
    context = {
        "id":pk,
        "userd":userd,
        "community_details":cd,
        "ccd":common_community_details,
        "pd":postd,
        "profile_image":pimage,   
        }
    return render(request,'community/community_home.html',context)


@csrf_exempt
def generalpostupload(request):
    if request.method == "POST":
        # Extract text fields from request.POST
        caption = request.POST.get('caption')
        posted_by = request.POST.get('userid')
        post_id = request.POST.get('post_id')
        print(post_id)
        # Extract file from request.FILES
        file = request.FILES.get('file').read()

        # Validate required fields
        if not all([caption,post_id , posted_by, file]):
            return JsonResponse({'error': 'Missing required fields'}, status=400)

        # Save to database
       
        entrydata = post_details(
            post_id=post_id,
            posted_by=posted_by,
            caption=caption,
            media=file
        )
        entrydata.save()
       
        return JsonResponse({'success': 'yes'}, safe=False)


def userinfo(request,pk):
    data = list(user_detail.objects.filter(user_id=pk).values())
    userdata = list(user_community.objects.filter(user_id=pk).values())
    for entry in data:
            entry['profile_photo'] = base64.b64encode(entry['profile_photo']).decode('utf-8')
    print(data)
    data1=data[0]
    context={
        'detail':data1,
        "user":userdata
        }
    return render(request,'community/user_info.html',context)
 
def search_info(request,pk):
        content = pk.replace("%20"," ")   
        data = list(user_detail.objects.filter(name__icontains=content).values())
        for entry in data:
            entry['profile_photo'] = base64.b64encode(entry['profile_photo']).decode('utf-8')
        if(len(data)>0):
            context = {
                "data": data  
                }
            return render(request,'community/search_user.html',context)
        else:
            return JsonResponse({"data":"no data found"})

def following_info(request,pk):
        fid=[]
        fd = []
        data = list(follower.objects.filter(from_id=pk).values())
        for i in range(len(data)):
            fid.append(data[i]['to_id'])
        for i in range(len(fid)):
            datad = list(user_detail.objects.filter(user_id = fid[i]).values())
            dd=datad[0]
            dd['profile_photo']=base64.b64encode(dd['profile_photo']).decode('utf-8')
            fd.append(dd)
        if(len(data)>0):
            context = {
                "data": fd  
                }
            return render(request,'community/following_user.html',context)
        else:
            return JsonResponse({"data":"no data found"})

def invlvedcommunity_info(request,pk):
        cid=[]
        cd = []
        data = list(user_community.objects.filter(user_id=pk,role="follower").values())
        for i in range(len(data)):
            cid.append(data[i]['community_id'])
        for i in range(len(cid)):
            datad = list(create_community.objects.filter(community_id = cid[i]).values())
            dd=datad[0]
            dd['community_image']=base64.b64encode(dd['community_image']).decode('utf-8')
            cd.append(dd)
        if(len(data)>0):
            context = {
                "data": cd  
                }
            return render(request,'community/joined_community.html',context)
        else:
            return JsonResponse({"data":"no data found"})


def community_myfeed(request,pk):
    following_ids = follower.objects.filter(from_id=pk).values_list('to_id', flat=True)

# Retrieve all posts by users in 'following_ids'
    posts = post_details.objects.filter(posted_by__in=following_ids).values()

# Convert QuerySet to a list
    postd = list(posts)
    
    user = list(user_detail.objects.filter(user_id = pk).values())
    userd = user[0]
    community_id=[]
    cd=[]
    ccd=[]
    uc_details = list(user_community.objects.filter(user_id=pk).values())
    for i in range(len(uc_details)):
       community_id.append( uc_details[i]['community_id'])
    print(community_id)
    for i in range (len(community_id)):
        community_details=list(create_community.objects.filter(community_id=community_id[i]).values())
        community_details[0]['community_image'] = base64.b64encode(community_details[0]['community_image']).decode('utf-8')
        cd.append(community_details[0])
    print(postd)
    common_community_details=list(create_community.objects.filter().values())
    for community in common_community_details[:]:  # Iterate over a copy of the list
       if any(community['community_id'] == c['community_id'] for c in cd):
          common_community_details.remove(community)
    for community in common_community_details:
        community['community_image']= base64.b64encode(community['community_image']).decode('utf-8')
    postdd = list(post_details.objects.filter(posted_by=pk).values())
    for entry in postdd:
        entry['media']= base64.b64encode(entry['media']).decode('utf-8')
    for entry in postdd:
        profileimage = user_detail.objects.get(user_id=entry['posted_by'])
        entry['profile_image']=base64.b64encode(profileimage.profile_photo).decode('utf-8')
    user_profile_image = user_detail.objects.get(user_id=request.session.get('user_id',None))
    pimage = base64.b64encode(user_profile_image.profile_photo).decode('utf-8')
    context = {
        "id":pk,
        "userd":userd,
        "community_details":cd,
        "ccd":common_community_details,
        "pd":postdd,
        'profile_image':pimage
        }
    return render(request,'community/community_myfeed.html',context)

def calender(request):
    return render(request,'calender/calender.html')