from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from .models import IdeaSubmission
from django.http import JsonResponse
from datetime import datetime


def idea_submission_form(request):
    return render(request, 'IdeaSubmission/ideaSubmissionForm.html')


@csrf_exempt  # Not recommended for production
def submitidea(request):
    if request.method == 'POST':
        try:
            # Collect form data
            idea_id = "IDEA" + datetime.now().strftime('%Y%m%d%H%M%S')
            statement_id = request.POST.get('statement_id')
            user_id = request.session.get('user_id', None)
            name_of_innovator = request.POST.get('innovator_name')
            age = request.POST.get('age')
            gender = request.POST.get('gender')
            dob = request.POST.get('dob')
            highest_education_qualification = request.POST.get('highest_education_qualification')
            title_of_project = request.POST.get('title_of_project')
            name_of_product = request.POST.get('product_name')
            description = request.POST.get('description')
            uniqueness = request.POST.get('uniqueness')
            innovation_type = request.POST.get('innovation_type')
            existing_product_upgrade = request.POST.get('existing_product_upgrade')  # Can be None if not provided
            need = request.POST.get('need')
            budget = request.POST.get('budget')
            price_advantage = request.POST.get('price_advantage')
            social_impact = request.POST.get('social_impact')
            proposal_file = request.FILES.get('proposal_file').read()  # Avoid reading large files into memory

            # Validate required fields
            if not all([statement_id, name_of_innovator, age, gender, dob, title_of_project, name_of_product, description]):
                return JsonResponse({'error': 'Missing required fields'}, status=400)

            # Ensure user is logged in
            if user_id is None:
                return JsonResponse({'error': 'User not logged in'}, status=403)

            # Parse date of birth
            dob = datetime.strptime(dob, '%Y-%m-%d').date()

            # Convert budget to float
            try:
                budget = float(budget)
            except ValueError:
                return JsonResponse({'error': 'Invalid budget value'}, status=400)

            # Save the data to the database
            idea = IdeaSubmission(
                user_id=user_id,
                idea_id=idea_id,
                statement_id=statement_id,
                name_of_innovator=name_of_innovator,
                age=int(age),
                gender=gender,
                dob=dob,
                highest_education_qualification=highest_education_qualification,
                title_of_project=title_of_project,
                name_of_product=name_of_product,
                description=description,
                uniqueness=uniqueness,
                innovation_type=innovation_type,
                existing_product_upgrade=existing_product_upgrade,
                need=need,
                budget=budget,
                price_advantage=price_advantage,
                social_impact=social_impact,
                proposal_file=proposal_file,
            )
            idea.save()

            return redirect('idea_submission')  # Replace with the correct URL name
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Invalid request method'}, status=405)
