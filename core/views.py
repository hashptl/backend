import json
import pymongo
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from rest_framework.authtoken.models import Token


# from .models import IntakeForm, Request, Template

# Connect to MongoDB
client = pymongo.MongoClient("mongodb+srv://ptlhiren535:LB0gJ43jzl8gTPJS@ddcna.lvuyy8j.mongodb.net/?retryWrites=true&w=majority")
db = client["ddcna"]
collection = db["IntakeForm"]
userCollection = db["auth_user"]
templateCollection = db["Template"]
requestCollection = db["Request"]

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
        try:
            data = json.loads(request.body)

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
        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'message': 'Invalid JSON payload.'})
    else:
        return JsonResponse({'success': False, 'message': 'Invalid request method.'})


@csrf_exempt
def request_list_api(request):
    if request.method == 'GET':
        try:
            # Retrieve all requests from the collection
            requests = list(requestCollection.find())

            # Convert ObjectId to string for JSON serialization
            for req in requests:
                req['_id'] = str(req['_id'])

            return JsonResponse({'success': True, 'data': requests})
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})
    else:
        return JsonResponse({'success': False, 'message': 'Invalid request method.'})


@csrf_exempt
def request_details_api(request, request_id):
    if request.method == 'GET':
        try:
            # Retrieve the request by ID
            req = requestCollection.find_one({'_id': ObjectId(request_id)})

            if req:
                # Convert ObjectId to string for JSON serialization
                req['_id'] = str(req['_id'])

                return JsonResponse({'success': True, 'data': req})
            else:
                return JsonResponse({'success': False, 'message': 'Request not found.'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})
    else:
        return JsonResponse({'success': False, 'message': 'Invalid request method.'})


    
import json
from bson import ObjectId

@csrf_exempt
def user_list_api(request):
    if request.method == 'GET':
        try:
            users = userCollection.find()
            user_list = []
            for user in users:
                # Convert ObjectId to string
                user['_id'] = str(user['_id'])
                user_list.append(user)
            
            return JsonResponse({'success': True, 'users': user_list})
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})
    else:
        return JsonResponse({'success': False, 'message': 'Invalid request method.'})



@csrf_exempt
def user_add_api(request):
    if request.method == 'POST':
        data = json.loads(request.body)

        username = data.get('username')
        password = data.get('password')
        email = data.get('email')

        # Create a new user
        user = {
            'username': username,
            'password': password,
            'email': email
        }
        userCollection.insert_one(user)

        return JsonResponse({'success': True, 'message': 'User added successfully.'})
    else:
        return JsonResponse({'success': False, 'message': 'Invalid request method.'})


@csrf_exempt
def user_update_api(request, user_id):
    if request.method == 'PUT':
        data = json.loads(request.body)

        # Retrieve the user from the database
        user = userCollection.find_one({'_id': ObjectId(user_id)})

        if user is not None:
            # Update the user details
            user['username'] = data.get('username', user['username'])
            user['password'] = data.get('password', user['password'])
            user['email'] = data.get('email', user['email'])

            # Save the updated user details
            userCollection.update_one({'_id': ObjectId(user_id)}, {'$set': user})

            return JsonResponse({'success': True, 'message': 'User updated successfully.'})
        else:
            return JsonResponse({'success': False, 'message': 'User not found.'})
    else:
        return JsonResponse({'success': False, 'message': 'Invalid request method.'})


@csrf_exempt
def user_delete_api(request, user_id):
    if request.method == 'DELETE':
        # Delete the user from the database
        result = userCollection.delete_one({'_id': ObjectId(user_id)})

        if result.deleted_count > 0:
            return JsonResponse({'success': True, 'message': 'User deleted successfully.'})
        else:
            return JsonResponse({'success': False, 'message': 'User not found.'})
    else:
        return JsonResponse({'success': False, 'message': 'Invalid request method.'})


import json
from bson import ObjectId

@csrf_exempt
def template_list_api(request):
    if request.method == 'GET':
        try:
            templates = templateCollection.find()
            template_list = []
            for template in templates:
                # Convert ObjectId to string
                template['_id'] = str(template['_id'])
                template_list.append(template)
            
            return JsonResponse({'success': True, 'templates': template_list})
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})
    else:
        return JsonResponse({'success': False, 'message': 'Invalid request method.'})


@csrf_exempt
def template_form_api(request):
    if request.method == 'POST':
        data = json.loads(request.body)

        try:
            # Create a new template
            template = {
                'name': data.get('name'),
                'content': data.get('content'),
                'date_created': data.get('date_created')
            }
            template_id = templateCollection.insert_one(template).inserted_id
            return JsonResponse({'success': True, 'message': 'Template created successfully.', 'template_id': str(template_id)})
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})
    else:
        return JsonResponse({'success': False, 'message': 'Invalid request method.'})
