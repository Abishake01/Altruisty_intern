from django.shortcuts import render

# Create your views here.
def mentorHome(request):
    return render(request,'Mentor/mentor_home.html')
