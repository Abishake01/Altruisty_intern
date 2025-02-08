import datetime
import logging
from django.http import HttpResponse
from io import BytesIO
from groq import Groq
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from docx import Document
from django.http import JsonResponse
from django.shortcuts import render
from django.http import HttpResponse
from reportlab.pdfgen import canvas 
from docx import Document
from AI_tools.models import Document as dmodel
from datetime import datetime

# Get the current date and time
daten = datetime.now()
# Initialize Groq client
idn=""
import io
from django.views.decorators.csrf import csrf_exempt
client = Groq(api_key="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")
logger = logging.getLogger(__name__)
def groq_chatbot_response(user_message):
    """Get a response from the Groq LLaMA model."""
    chat_completion = client.chat.completions.create(
        messages=[{"role": "user", "content": user_message}],
        model="llama3-8b-8192",
    )
    return chat_completion.choices[0].message.content

def chatbot(request):
    if request.method == "POST":
        user_message = request.POST.get('message')  # or request.body for JSON data
        logging.info(f"Received message: {user_message}")  # Log the received message for debugging

        # Generate a response based on the user's message
        response_message = groq_chatbot_response(user_message)
        logging.info(f"Sending response: {response_message}")  # Log the response for debugging

        return JsonResponse({'response': response_message})
    
    return render(request, 'chatbot/index.html')


def chat_view(request):
    if request.method == "POST":
        user_message = request.POST.get('message')  # or request.body for JSON data
        logging.info(f"Received message: {user_message}")  # Log the received message for debugging

        # Generate a response based on the user's message
        response_message = groq_chatbot_response(user_message)
        logging.info(f"Sending response: {response_message}")  # Log the response for debugging

        return JsonResponse({'response': response_message})
    return JsonResponse({'error': 'Invalid request'}, status=400)

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import logging
import io

logger = logging.getLogger(__name__)

from datetime import datetime
from django.http import JsonResponse
from django.core.files.base import ContentFile
import os
from django.http import JsonResponse
from django.core.files.base import ContentFile
from datetime import datetime

@csrf_exempt
def documentdbsave(request):
    if request.method == "POST":
        # Check if the file is being uploaded correctly
        uploaded_file = request.FILES.get('file')
        
        if uploaded_file is None:
            return JsonResponse({'status': "error", 'message': "No file uploaded"})
        
        try:
            # Read the uploaded file content (binary data)
            file_content = uploaded_file.read()
            print(file_content)

            # Debugging: log the file's name and size
            print(f"File name: {uploaded_file.name}")
            print(f"File size: {len(file_content)} bytes")
            
            # Optionally, validate file size or type here

            # Get the current timestamp for the document
            daten = datetime.now()
            daten_str = daten.strftime("%Y-%m-%d %H:%M:%S")

            # Create a new document instance and save it to the database
            document = dmodel(
                login_id=request.session.get('user_id', None),  # Get the user ID from session
                title="AI_document_" + daten_str,
                document_category="AI",
                document_type="AI",
                description="AI generated document created on: " + daten_str,
                document_upload= file_content  # Save file with its name
            )
            document.save()

            # Return success response
            return JsonResponse({'status': "success", 'message': "File uploaded successfully"})
        
        except Exception as e:
            # Catch any exception and return the error message
            print(f"Error while processing the file: {str(e)}")
            return JsonResponse({'status': "error", 'message': f"Error while processing the file: {str(e)}"})
    
    # If the method is not POST, return an error
    return JsonResponse({'status': "error", 'message': "Invalid request method"})



@csrf_exempt
def download(request):
    print("Download function called")  # Debug print statement
    if request.method == "POST":
        message = request.POST.get("message", "").strip()
        file_format = request.POST.get("format", "").strip()

        print(f"Received message: {message}")  # Debug print statement

        if not message or not file_format:
            return JsonResponse({"error": "Invalid input"}, status=400)

        if file_format == 'pdf':
            file_content = generate_pdf(message, request.session.get('user_id', None))
            return HttpResponse(file_content, content_type='application/pdf')

        elif file_format == 'docx':
            file_content = generate_docx(message, request.session.get('user_id', None))
            return HttpResponse(file_content, content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')

        else:
            return JsonResponse({"error": "Unsupported format"}, status=400)
    else:
        print("Invalid request method")  # Debug print statement
        return JsonResponse({"error": "Invalid request method"}, status=405)

logger = logging.getLogger(__name__)
def generate_pdf(message, idn):
    daten = datetime.now()
    daten_str = daten.strftime("%Y-%m-%d %H:%M:%S")

    print("Entering generate_pdf function...")  # Debug print statement
    
    # Create the PDF in memory using reportlab
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    c.drawString(100, 750, message)
    c.showPage()
    c.save()

    # Get the binary content of the generated PDF
    pdf_content = buffer.getvalue()
    if not pdf_content:
        print("Generated PDF content is empty.")  # Debug print statement
        logger.error("Generated PDF content is empty.")
        return JsonResponse({"error": "Failed to generate PDF"}, status=500)

    print("Generated PDF content...")  # Debug print statement
    
    # Try saving the document to the database
    try:
        document = dmodel(
            login_id=idn,
            title="AI_document_" + daten_str,
            document_category="AI",
            document_type="AI",
            description="AI generated document created on: " + daten_str,
        )

        # Save the PDF binary content to the BinaryField
        document.document_upload = pdf_content
        document.save()

        print(f"Document saved with title: {document.title}")  # Debug print statement
        logger.info(f"Document saved successfully with title: {document.title}")
        return pdf_content  # Return the binary content for download
    except Exception as e:
        print(f"Error during save: {str(e)}")  # Debug print statement
        logger.error(f"Error saving document: {str(e)}")
        return JsonResponse({"error": "Failed to save document"}, status=500)
