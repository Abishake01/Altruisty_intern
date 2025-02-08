from django.urls import path
from . import views


urlpatterns = [
    path('ai_tools/',views.aiToolsMainPage,name="ai_tools"),
    path('investor_form/',views.addInvestorForm,name="investor_form"),
    path('delete_investor/<int:task_id>/', views.delete_investor, name='delete_investor'),
    path('vendor_form/',views.addVendor,name="vendor_form"),
    path('delete_vendor/<int:task_id>/', views.delete_vendor, name='delete_vendor'),
    path('document-form/', views.document_form, name='document_form'),
    path('delete_document/<int:task_id>/', views.delete_document, name='delete_document'),
    path('todoList/',views.todoList,name='todoList'),
    path('delete_task/<int:task_id>/', views.delete_task, name='delete_task'),
    path('reschedule_task/', views.reschedule_task, name='reschedule_task'),
    path('reassign_task/', views.reassign_task, name='reassign_task'),
    path('scheduler/',views.scheduler,name='scheduler'),
    path('delete_scheduler/<int:task_id>/', views.delete_meeting, name='delete_scheduler'),
    path('reschedule_scheduler/', views.reschedule_meeting, name='reschedule_scheduler'),
    path('addExpense/',views.addExpense,name='addExpense'),
    path('delete_expense/<int:task_id>/', views.delete_expense, name='delete_expense'),
    path('history/<int:taskid>', views.history, name='history'),
]

