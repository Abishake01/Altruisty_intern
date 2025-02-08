from django.shortcuts import render
from agora_token_builder import RtcTokenBuilder
import random
import time
from agora_token_builder import RtcTokenBuilder
# from .models import RoomMember
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from .models import RoomMember, Meeting, Attendance
from django.contrib.auth.models import User
from django.utils import timezone
from frontend.models import Userauth
def lobby(request):
    return render(request, 'video_call/lobby.html')  
def lobby2(request):
    return render(request, 'video_call/lobby2.html')  

def room(request):
    num_cards = 1  # You can change this number as needed

    # Generate a list of cards (can be empty or contain data as needed)
    # For demonstration purposes, we'll create a list with placeholders for each card
    cards = [{"id": i, "content": f"Card {i} content"} for i in range(1, num_cards + 1)]

    # Pass num_cards and cards to the template context
    context = {
        'num_cards': num_cards,
        'cards': cards,
        'image_count': range(40)
    }

    return render(request, 'video_call/room.html', context)

def main(request):
    return render(request, 'video_call/main.html')  


def getToken(request):
    appId = "5be627cf59014fd2b76efbaa7eb0760a"
    appCertificate = "f749929763a542fba32b0fbcc1a60a53"
    channelName = request.GET.get('channel')
    uid = random.randint(1, 230)
    expirationTimeInSeconds = 3600
    currentTimeStamp = int(time.time())
    privilegeExpiredTs = currentTimeStamp + expirationTimeInSeconds
    role = 1 #host

    token = RtcTokenBuilder.buildTokenWithUid(appId, appCertificate, channelName, uid, role, privilegeExpiredTs)

    return JsonResponse({'token': token, 'uid': uid}, safe=False)

@csrf_exempt
def createMember(request):
    data = json.loads(request.body)
    member, created = RoomMember.objects.get_or_create(
        name=data['name'],
        uid=data['UID'],
        room_name=data['room_name']
    )

    return JsonResponse({'name': data['name']}, safe=False)

def getMember(request):
    uid = request.GET.get('UID')
    room_name = request.GET.get('room_name')

    if not uid or not room_name:
        return JsonResponse({'error': 'Missing parameters'}, status=400)

    try:
        member = RoomMember.objects.get(uid=uid, room_name=room_name)
        return JsonResponse({'name': member.name})
    except RoomMember.DoesNotExist:
        return JsonResponse({'error': 'Member not found'}, status=404)

@csrf_exempt
def deleteMember(request):
    data = json.loads(request.body)
    try:
        member = RoomMember.objects.get(
            name=data['name'],
            uid=data['UID'],
            room_name=data['room_name']
        )
        member.delete()
        return JsonResponse('Member deleted', safe=False)
    except RoomMember.DoesNotExist:
        return JsonResponse({'error': 'Member not found'}, status=404)

def get_user_details(request):
    user_id = request.session.get('user_id', None) # Retrieve user_id from the session
    print(user_id)   
    try:
        # Query the Userauth model to fetch the username using user_id
        user = Userauth.objects.get(user_id=user_id)
        
        # Return the username and user_id
        return JsonResponse({'username': user.username, 'user_id': user.user_id})
    
    except Userauth.DoesNotExist:
        # Handle the case where the user doesn't exist
        return JsonResponse({'error': 'User not found'}, status=404)
@csrf_exempt
def check_meeting_creator(request):
    try:
        room = request.GET.get('room')
        user = request.GET.get('user')
        
        if not room or not user:
            return JsonResponse({
                'success': False,
                'error': 'Missing room or user parameter',
                'is_creator': False
            })
        
        # Get or create user
        user_obj, _ = User.objects.get_or_create(username=user)
        
        # Get or create meeting
        meeting, created = Meeting.objects.get_or_create(
            room_name=room,
            defaults={
                'creator': user_obj,
                'duration': timezone.timedelta(seconds=0)
            }
        )
        
        is_creator = meeting.creator.username == user
        
        return JsonResponse({
            'success': True,
            'is_creator': is_creator
        })
        
    except Exception as e:
        print(f"Error in check_meeting_creator: {str(e)}")
        return JsonResponse({
            'success': False,
            'error': str(e),
            'is_creator': False
        })

@csrf_exempt
def mark_attendance(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            room_name = data.get('room')
            creator_name = data.get('creator')
            attendees_data = data.get('attendees', [])
            meeting_duration = data.get('meetingDuration', 0)
            
            print(f"Received attendance data: {data}")  # Add debug logging
            
            # Get or create user for creator
            creator, _ = User.objects.get_or_create(username=creator_name)
            
            # Get or create meeting
            meeting, created = Meeting.objects.get_or_create(
                room_name=room_name,
                defaults={
                    'creator': creator,
                    'duration': timezone.timedelta(seconds=meeting_duration)
                }
            )
            
            if not created:
                meeting.duration = timezone.timedelta(seconds=meeting_duration)
                meeting.save()
            
            # Delete existing attendance records for this meeting
            Attendance.objects.filter(meeting=meeting).delete()
            
            # Create new attendance records
            for attendee_data in attendees_data:
                try:
                    member = RoomMember.objects.get(uid=attendee_data['attendee'], room_name=room_name)
                    user, created = User.objects.get_or_create(username=member.name)
                    attendance = Attendance.objects.create(
                        meeting=meeting,
                        attendee=user.username,  # Save the username instead of UID
                        join_time=timezone.now() - timezone.timedelta(seconds=meeting_duration),
                        leave_time=timezone.now(),
                        attendance_percentage=float(attendee_data['percentage']),
                        is_present=attendee_data['isPresent']
                    )
                    attendance.calculate_attendance_percentage()
                    print(f"Created attendance record for {user.username}")  # Add debug logging
                except RoomMember.DoesNotExist:
                    print(f"Error: Member with UID {attendee_data['attendee']} not found in room {room_name}")
                    continue
                except Exception as e:
                    print(f"Error creating attendance for {attendee_data['attendee']}: {str(e)}")
                    continue
            
            return JsonResponse({
                'success': True,
                'message': 'Attendance saved successfully'
            })
            
        except Exception as e:
            print(f"Error in mark_attendance: {str(e)}")  # Add debug logging
            return JsonResponse({
                'success': False,
                'error': str(e)
            })
    
    return JsonResponse({
        'success': False,
        'error': 'Invalid request method'
    })