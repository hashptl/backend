import json
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

# from .models import IntakeForm, Request, Template


@csrf_exempt
def sign_up_api(request):
    if request.method == 'POST':
        data = json.loads(request.body)

        username = data.get('username')
        password = data.get('password')
        email = data.get('email')

        try:
            # Check if the username is already taken
            if User.objects.filter(username=username).exists():
                return JsonResponse({'success': False, 'message': 'Username already exists.'})

            # Create a new user
            user = User.objects.create_user(username=username, password=password, email=email)
            return JsonResponse({'success': True, 'message': 'User registered successfully.'})
        except Exception:
            return JsonResponse({'success': False, 'message': 'An error occurred while creating the user.'})
    else:
        return JsonResponse({'success': False, 'message': 'Invalid request method.'})


@csrf_exempt
def sign_in_api(request):
    if request.method == 'POST':
        data = json.loads(request.body)

        username = data.get('username')
        password = data.get('password')

        # Authenticate the user
        user = authenticate(username=username, password=password)

        if user is not None:
            # Log in the user
            login(request, user)
            return JsonResponse({'success': True, 'message': 'User logged in successfully.'})
        else:
            return JsonResponse({'success': False, 'message': 'Invalid username or password.'})
    else:
        return JsonResponse({'success': False, 'message': 'Invalid request method.'})


@csrf_exempt
def intake_form_api(request):
    if request.method == 'POST':
        # Process the form submission and save the data to the database
        form_data = request.POST
        # Validate and save the form data to the IntakeForm model
        intake_form = IntakeForm.objects.create(
            state=form_data.get('state'),
            requestor_type=form_data.get('requestor_type'),
            request_type=form_data.get('request_type'),
            first_name=form_data.get('first_name'),
            last_name=form_data.get('last_name'),
            email=form_data.get('email'),
            request_details=form_data.get('request_details'),
            last_4_ssn=form_data.get('last_4_ssn'),
            employee_id=form_data.get('employee_id'),
            address=form_data.get('address')
        )
        return JsonResponse({'success': True, 'message': 'Form submitted successfully.'})
    else:
        # Handle GET request for retrieving the form fields dynamically
        # You can define a dictionary of dynamic form fields based on the menu selections
        dynamic_form_fields = {
            'CA': {
                'Customer': ['First Name', 'Last Name', 'Email Address', 'Request Details (Optional)'],
                'Employee': ['First Name', 'Last Name', 'Email Address', 'Request Details (Optional)', 'Last 4 of SSN (Optional)', 'Employee ID (Optional)'],
                'Job Applicant': ['First Name', 'Last Name', 'Email Address', 'Request Details (Optional)', 'Address (Optional)'],
                'Vendor': ['First Name', 'Last Name', 'Email Address', 'Request Details (Optional)']
            },
            'VA': {
                # Define fields for VA state
            },
            'CO': {
                # Define fields for CO state
            },
            'UT': {
                # Define fields for UT state
            }
        }
        state = request.GET.get('state', '')
        requestor_type = request.GET.get('requestor_type', '')
        fields = dynamic_form_fields.get(state, {}).get(requestor_type, [])
        return JsonResponse({'fields': fields})


def requests_api(request):
    if request.method == 'GET':
        # Fetch the requests data from the database based on pagination, sorting, and filtering parameters
        requests = Request.objects.all()  # You can add filters, sorting, and pagination logic here
        data = [{'id': request.id, 'name': request.name, 'request_type': request.request_type} for request in requests]
        return JsonResponse({'requests': data})


def request_details_api(request, request_id):
    if request.method == 'GET':
        # Fetch the request details from the database based on the request ID
        request_obj = Request.objects.get(id=request_id)
        # Fetch associated events for the request
        events = request_obj.events.all()
        event_data = [{'id': event.id, 'name': event.name} for event in events]
        # Prepare the JSON response
        response = {
            'id': request_obj.id,
            'name': request_obj.name,
            'request_type': request_obj.request_type,
            'email': request_obj.email,
            'days_left': request_obj.days_left,
            'events': event_data
        }
        return JsonResponse(response)


def templates_api(request):
    if request.method == 'GET':
        # Fetch the list of templates from the database
        templates = Template.objects.all()
        template_data = [{'id': template.id, 'name': template.name, 'description': template.description, 'date': template.date} for template in templates]
        return JsonResponse({'templates': template_data})