from django import forms
from .models import *
from frontend.models import Member
from django.utils import timezone

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'due_date']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Task Title', 'class': 'input-field'}),
            'due_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            
        }
    
    # Optionally, you can add custom validation for fields here if needed
    def clean_due_date(self):
        due_date = self.cleaned_data.get('due_date')
        if due_date < timezone.now():
            raise forms.ValidationError("The due date cannot be in the past.")
        return due_date

class ScheduleForm(forms.ModelForm):
    class Meta:
        model = Scheduler
        fields = ['title', 'due_date']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Task Title', 'class': 'input-field'}),
            'due_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }
    
    # Optionally, you can add custom validation for fields here if needed
    def clean_due_date(self):
        due_date = self.cleaned_data.get('due_date')
        if due_date < timezone.now():
            raise forms.ValidationError("The due date cannot be in the past.")
        return due_date


class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ['title', 'document_category', 'document_type', 'party_name', 'description']  # Don't include document_upload here

    # Add document_upload as a separate FileField
    document_upload = forms.FileField(required=True, widget=forms.ClearableFileInput(attrs={'class': 'uploadfile', 'multiple': False}))


class AddVendorForm(forms.ModelForm):
    agreement_upload = forms.FileField(required=True, widget=forms.ClearableFileInput(attrs={'class': 'uploadfile', 'multiple': False}))
    class Meta:
        model = AddVendor  # Specify the model here
        fields = [
            'company_name', 
            'marketing_person_name', 
            'official_contact_number', 
            'official_mail_id', 
            'contact_person_mail_id', 
            'contact_person_contact_number', 
            'company_address', 
            'description'
        ]
        
        widgets = {
            'company_name': forms.TextInput(attrs={'class': 'input-field', 'placeholder': 'Company Name'}),
            'marketing_person_name': forms.TextInput(attrs={'class': 'input-field', 'placeholder': 'Marketing Person Name'}),
            'official_contact_number': forms.TextInput(attrs={'class': 'input-field', 'placeholder': 'Official Contact Number'}),
            'official_mail_id': forms.EmailInput(attrs={'class': 'input-field', 'placeholder': 'Official Mail ID'}),
            'contact_person_mail_id': forms.EmailInput(attrs={'class': 'input-field', 'placeholder': 'Contact Person Mail ID'}),
            'contact_person_contact_number': forms.TextInput(attrs={'class': 'input-field', 'placeholder': 'Contact Person Contact Number'}),
            'company_address': forms.Textarea(attrs={'class': 'input-field', 'placeholder': 'Enter company address', 'rows': 3}),
            'description': forms.Textarea(attrs={'class': 'input-field', 'placeholder': 'Please provide a description', 'rows': 4}),
            
        }


class AddInvestorForm(forms.ModelForm):
    visiting_card = forms.FileField(required=True, widget=forms.ClearableFileInput(attrs={'class': 'uploadfile', 'multiple': False}))
    class Meta:
        model = AddInvestor
        fields = [
            'investor_name', 
            'company_name', 
            'description', 
            'contact_number', 
            'email_id',  
            'purpose', 
            'meeting_date', 
            'meeting_time'
        ]
        
        widgets = {
            'investor_name': forms.TextInput(attrs={'class': 'input-field', 'placeholder': 'Investor Name'}),
            'company_name': forms.TextInput(attrs={'class': 'input-field', 'placeholder': 'Company Name'}),
            'description': forms.Textarea(attrs={'class': 'input-field', 'placeholder': 'Please provide a description', 'rows': 4}),
            'contact_number': forms.TextInput(attrs={'class': 'input-field', 'placeholder': 'Contact Number'}),
            'email_id': forms.EmailInput(attrs={'class': 'input-field', 'placeholder': 'Email ID'}),
            'purpose': forms.TextInput(attrs={'class': 'input-field', 'placeholder': 'Purpose'}),
            'meeting_date': forms.DateInput(attrs={'class': 'input-field', 'type': 'date'}),
            'meeting_time': forms.TimeInput(attrs={'class': 'input-field', 'type': 'time'}),
        }

class ExpenseForm(forms.ModelForm):
    invoice = forms.FileField(required=True, widget=forms.ClearableFileInput(attrs={'class': 'uploadfile', 'multiple': False}))
    class Meta:
        model = Expense
        fields = ['product_name', 'shop_name', 'date_of_purchase', 'amount']
        
        widgets = {
            'product_name': forms.TextInput(attrs={'class': 'input-field', 'placeholder': 'Product name'}),
            'shop_name': forms.TextInput(attrs={'class': 'input-field', 'placeholder': 'Shop name'}),
            'date_of_purchase': forms.DateInput(attrs={'class': 'input-field', 'type': 'date', 'title': 'Date of purchase'}),
            'amount': forms.NumberInput(attrs={'class': 'input-field', 'title': 'Amount'}),
            
        }

   