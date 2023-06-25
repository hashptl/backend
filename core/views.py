import json
import pymongo
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

# from .models import IntakeForm, Request, Template

# Connect to MongoDB
client = pymongo.MongoClient("mongodb+srv://ptlhiren535:LB0gJ43jzl8gTPJS@ddcna.lvuyy8j.mongodb.net/?retryWrites=true&w=majority")
db = client["ddcna"]
collection = db["IntakeForm"]

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


"""
Intake Form API
"""
@csrf_exempt
def intake_form_api(request):
    if request.method == 'POST':
        data = request.POST

        # Basic validation for required fields
        state = data.get('state')
        requestor_type = data.get('requestor_type')
        request_type = data.get('request_type')
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        email = data.get('email')

        if not state or not requestor_type or not request_type or not first_name or not last_name or not email:
            return JsonResponse({'success': False, 'message': 'Required fields are missing.'})

        # Perform additional validation based on the selected requestor type
        if requestor_type == 'Customer':
            request_details = data.get('request_details')
            if not request_details:
                return JsonResponse({'success': False, 'message': 'Request details are required for customers.'})

        elif requestor_type == 'Employee':
            request_details = data.get('request_details')
            ssn_last_4 = data.get('ssn_last_4')
            employee_id = data.get('employee_id')

            if not request_details:
                return JsonResponse({'success': False, 'message': 'Request details are required for employees.'})

            # Additional validation for optional fields
            if ssn_last_4 and len(ssn_last_4) != 4:
                return JsonResponse({'success': False, 'message': 'Invalid SSN last 4 digits.'})

        elif requestor_type == 'Job Applicant':
            request_details = data.get('request_details')
            address = data.get('address')

            if not request_details:
                return JsonResponse({'success': False, 'message': 'Request details are required for job applicants.'})

        elif requestor_type == 'Vendor':
            request_details = data.get('request_details')

            if not request_details:
                return JsonResponse({'success': False, 'message': 'Request details are required for vendors.'})

        else:
            return JsonResponse({'success': False, 'message': 'Invalid requestor type.'})

        # Check for duplicate entry in the collection
        existing_entry = collection.find_one({'email': email})
        if existing_entry:
            return JsonResponse({'success': False, 'message': 'Duplicate entry. Form already submitted.'})

        # Save the form data to the database
        form_data = {
            'state': state,
            'requestor_type': requestor_type,
            'request_type': request_type,
            'first_name': first_name,
            'last_name': last_name,
            'email': email,
            'request_details': request_details,
            'ssn_last_4': data.get('ssn_last_4'),
            'employee_id': data.get('employee_id'),
            'address': data.get('address'),
        }
        collection.insert_one(form_data)

        return JsonResponse({'success': True, 'message': 'Form submitted successfully.'})
    else:
        return JsonResponse({'success': False, 'message': 'Invalid request method.'})


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