from .forms import *
import mimetypes
import fitz  # PyMuPDF for PDF processing
from PIL import Image
import filetype
import io
from django.shortcuts import render,get_object_or_404
from django.shortcuts import redirect, get_object_or_404
from .models import AddInvestor,AddVendor,Document,Task,Scheduler,Expense,todolistHistory
from frontend.models import Member
from django.http import HttpResponse, JsonResponse
from django.utils.timezone import now
import base64
from django.utils import timezone

def detect_file_type(binary_data):
    """Detect the MIME type of a file using binary data."""
    kind = filetype.guess(binary_data)
    return kind.mime if kind else "unknown"


def addExpense(request):
    if request.method == 'POST':
        # Initialize the form with POST data and files
        form = ExpenseForm(request.POST, request.FILES)
        
        if form.is_valid():
            # Save the form instance but don't commit to the database yet
            expense = form.save(commit=False)
            # Attach login_id (from session)
            expense.login_id = request.session.get('user_id', None)
            expense.save()

            # Redirect to a success page or expense list after saving
            return redirect('addExpense')  # Replace with your URL name for the list view
        else:
            return render(request, 'AI_Tools/addExpense.html', {'form': form, 'errors': form.errors})
    else:
        form = ExpenseForm()  # Initialize an empty form for GET request
    
    # Fetch and display the list of expenses
    expenses = Expense.objects.filter(login_id=request.session.get('user_id', None)).order_by('date_of_purchase')
    
    return render(request, 'AI_Tools/addExpense.html', {'form': form, 'expenses': expenses})

def delete_expense(request, task_id):
    if request.method == 'POST':
        task = get_object_or_404(Expense, id=task_id)
        task.delete()
    return redirect('addExpense')

def reschedule_meeting(request):
    if request.method == 'POST':
        task_id = request.POST.get('task_id')
        new_due_date = request.POST.get('new_due_date')
        reason = request.POST.get('reason')

        task = get_object_or_404(Scheduler, id=task_id)
        task.due_date = new_due_date
        task.attribute1 = reason  # Assuming `attribute1` is used for storing the reason
        task.attribute2 = 'yes',
        task.save()

    return redirect('scheduler')


def delete_meeting(request, task_id):
    if request.method == 'POST':
        task = get_object_or_404(Scheduler, id=task_id)
        task.delete()
    return redirect('scheduler')

def scheduler(request):
    if request.method == 'POST':
        form = ScheduleForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.login_id = request.session.get('user_id', None)  # Set login_id if necessary
            task.created_at = timezone.now()  # Automatically set the created_at field
            task.save()

            # Redirect to the task list or another page after saving the task
            return redirect('scheduler')  # Or any other URL you want to redirect to

        else:
            # In case the form is not valid, you can return an error message or handle it accordingly
            return JsonResponse({"message": "Form is not valid."}, status=400)

    else:
        # GET request: create an empty form
        form = TaskForm()
        tasks = Scheduler.objects.filter(login_id = request.session.get('user_id',None)).order_by('due_date')
        return render(request, 'AI_Tools/scheduler.html', {'form': form,'tasks':tasks})

def reschedule_task(request):
    if request.method == 'POST':
        task_id = request.POST.get('task_id')
        new_due_date = request.POST.get('new_due_date')
        reason = request.POST.get('reason')

        task = get_object_or_404(Task, id=task_id)
        print(task)
        history = todolistHistory(from_id = request.session.get('user_id',None),to_id = task.attribute1,reason=reason,due_date = new_due_date,startup_id=request.session.get('startup_id',None),attribute1=task_id,attribute2="change in date")
        task.due_date = new_due_date
        task.attribute3 = reason  # Assuming `attribute3` is used for storing the reason
        task.attribute2 = 'yes',
        task.save()
        history.save()
    return redirect('todoList')

def reassign_task(request):
    if request.method == 'POST':
        task_id = request.POST.get('task_id')
        team_member = request.POST.get('attribute1')
        reason = request.POST.get('reason')
        
        task = get_object_or_404(Task, id=task_id)
        print(task)
        date = task.due_date
        history = todolistHistory(from_id = request.session.get('user_id',None),to_id = team_member,reason=reason,due_date = date,startup_id=request.session.get('startup_id',None),attribute1=task_id,attribute2= "change in person")
        task.attribute1 = team_member
        task.attribute3 = reason  # Assuming `attribute1` is used for storing the reason
        task.attribute2 = 'yes',

        task.save()
        history.save()
    return redirect('todoList')


def delete_task(request, task_id):
    if request.method == 'POST':
        task = get_object_or_404(Task, id=task_id)
        task.delete()
    return redirect('todoList')

def todoList(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        attribute1 = request.POST.get('attribute1')
        if form.is_valid() and attribute1 :
            form.instance.attribute1 = attribute1
            task = form.save(commit=False)
            task.login_id = request.session.get('user_id', None)  # Set login_id if necessary
            task.created_at = timezone.now()  # Automatically set the created_at field
            print(task)
            task.save()
            
            # Redirect to the task list or another page after saving the task
            return redirect('todoList')  # Or any other URL you want to redirect to

        else:
            # In case the form is not valid, you can return an error message or handle it accordingly
            print("Form Errors:", form.errors)  # Debugging
            print("POST Data:", request.POST) 
            return JsonResponse({"message": "Form is not valid."}, status=400)

    else:
        # GET request: create an empty form
        form = TaskForm()
        idn = request.session.get('user_id', None)
        if idn[0:2] == "SR":
            team_id = []
            team_id.append(idn)
            print(idn,team_id)
            members = Member.objects.filter(startup_id = request.session.get('startup_id',None))
            for member in members:
                team_id.append(member.user_id)
        
            print(team_id)
            current_date = timezone.now()
            tasks = Task.objects.filter(login_id__in=team_id, due_date__gte=current_date).order_by('due_date')
            return render(request, 'AI_Tools/todolist.html', {'form': form,'tasks':tasks,'members':members})

        else:
            members = Member.objects.filter(startup_id = request.session.get('startup_id',None))
            for member in members:
                team_id.append(member.user_id)
        
            print(team_id)
            current_date = timezone.now()
            tasks = Task.objects.filter(login_id__in=team_id, due_date__gte=current_date).order_by('due_date')
            return render(request, 'AI_Tools/todolist.html', {'form': form,'tasks':tasks,'members':members})


    
def document_form(request):
    if request.method == "POST":
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            # Save the form data
            upload_file = request.FILES['document_upload'].read()
            document = form.save(commit=False)
            document.document_upload = upload_file
            document.login_id = request.session.get('user_id', None)  # Set login_id from session
            document.save()

            return redirect('document_form')  # Redirect after successful form submission

        else:
            # Handle form errors
            return JsonResponse({"error": "Form is not valid.", "details": form.errors}, status=400)

    # Handle GET request
    form = DocumentForm()
    documents = Document.objects.filter(login_id=request.session.get('user_id', None))

    return render(request, "AI_Tools/addDocument.html", {'form': form, 'documents': documents})



def delete_document(request, task_id):
    if request.method == 'POST':
        task = get_object_or_404(Document, id=task_id)
        task.delete()
    return redirect('document_form')

def addVendor(request):
    if request.method == "POST":
        form = AddVendorForm(request.POST, request.FILES)
        if form.is_valid():
            # Save form data to the database
            vendor = form.save(commit=False)
            vendor.login_id = request.session.get('user_id', None)  # Set login_id from session
            vendor.save()

            return redirect('vendor_form')  # Redirect after successful form submission
        else:
            # Handle form errors
            return JsonResponse({"error": "Form is not valid.", "details": form.errors}, status=400)
    else:
        form = AddVendorForm()  # Initialize the empty form

        vendors = AddVendor.objects.filter(login_id=request.session.get('user_id', None))
        return render(request, "AI_Tools/addVendor.html", {'form': form, 'vendors': vendors})

def delete_vendor(request, task_id):
    if request.method == 'POST':
        task = get_object_or_404(AddVendor, id=task_id)
        task.delete()
    return redirect('vendor_form')




def aiToolsMainPage(request):
    # Fetch documents for the logged-in user
    idn = request.session.get('user_id', None)
    documents = Document.objects.filter(login_id=idn)
    print(idn)
    # Prepare documents with Base64 data
   
    for document in documents:
        
            # Detect file type using mimetypes
            binary_data = document.document_upload  # Adjust based on your storage field
            mime_type = detect_file_type(binary_data)
            print(f"Detected MIME type: {mime_type}")
            if mime_type == 'application/pdf':
                print('Processing PDF')
                # Open PDF and extract the first image
                pdf_document = fitz.open(stream=document.document_upload, filetype="pdf")
                for page in pdf_document.pages():
                    images = page.get_images(full=True)
                    if images:
                        xref = images[0][0]  # Get the xref of the first image
                        base_image = pdf_document.extract_image(xref)
                        image_bytes = base_image["image"]
                        document.document_upload = image_bytes
                        document.document_upload = base64.b64encode(document.document_upload).decode('utf-8')
                        print(document.document_upload)
                        break
                pdf_document.close()
            else:
               print('looping')
               document.document_upload = base64.b64encode(document.document_upload).decode('utf-8')
               print(document.document_upload)
        
   
    # Render the template with the processed documents
    
    return render(request, 'AI_tools/ai_tools.html', {'documents': documents})


def addInvestorForm(request):
    if request.method == 'POST':
        # Initialize the form with POST data and uploaded files
        form = AddInvestorForm(request.POST, request.FILES)
        
        if form.is_valid():
            # Save the form but do not commit to the database yet
            investor = form.save(commit=False)
            # Attach login_id (from session)
            investor.login_id = request.session.get('user_id', None)
            investor.save()
            return redirect('investor_form')  # Redirect to the form page after submission
            
        else:
            return render(request, 'AI_Tools/addInvestorForm.html', {'form': form, 'errors': form.errors})

    else:
        form = AddInvestorForm()  # GET request: initialize an empty form

    # Fetch and display the existing investor data
    investors = AddInvestor.objects.filter(login_id=request.session.get('user_id', None))
    return render(request, 'AI_Tools/addInvestorForm.html', {'form': form, 'investors': investors})

def delete_investor(request, task_id):
    if request.method == 'POST':
        task = get_object_or_404(AddInvestor, id=task_id)
        task.delete()
    return redirect('investor_form')

def history(request,taskid):
    tasks = todolistHistory.objects.filter(attribute1=str(taskid)).order_by('reassign_at')
    return render(request, 'AI_Tools/history.html',{'tasks':tasks})
