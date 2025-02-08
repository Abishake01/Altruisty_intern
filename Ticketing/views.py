from django.shortcuts import render, redirect
from django.utils.timezone import now
from .models import Ticket  # Import the Ticket model

def ticketing(request):
    if request.method == "POST":
        title = request.POST.get("title")
        issue_type = request.POST.get("issue_type")
        description = request.POST.get("description")
        attachment = request.FILES.get("agreement_upload")  # For file uploads
        created_date = now().date()
        created_time = now().time()

        # Save the data to the database with nullable fields explicitly set to None
        ticket = Ticket(
            title=title,
            issue_type=issue_type,
            description=description,
            attachment=attachment.read() if attachment else None,  # Save file as binary
            created_date=created_date,
            created_time=created_time,
            login_id=request.session.get('user_id',None),
            closed_date=None,
            closed_time=None,
            assigned_to=None,
            company_name=None,
            levels=1,
            attribute1=None,
            attribute2=None,
            attribute3=None,
            attribute4=None,
            attribute5=None,
        )
        ticket.save()

        return redirect("ticketing")  # Redirect to the same page or a confirmation page

    # Retrieve tickets and order by latest created_date and created_time
    tickets = Ticket.objects.filter(login_id = request.session.get('user_id',None)).order_by('-created_date', '-created_time')

    return render(request, "Ticketing/ticketing.html", {"tickets": tickets})
