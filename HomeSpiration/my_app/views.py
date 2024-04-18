import json
from django.shortcuts import redirect, render
from .models import NormalUser, ProfessionalDetails, User ,Professional ,Project
from django.contrib import messages
from django.contrib.auth import authenticate ,login,logout, get_user_model
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.hashers import make_password
from .models import Professional
from django.core.exceptions import ValidationError
from django.core.files.storage import FileSystemStorage
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import get_user_model
User = get_user_model()
import logging
logger = logging.getLogger(__name__)
from django.utils import timezone
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.models import User
from .models import User, NormalUser
from .models import Project, User , Layout500to1000,Layout1000to1500,Layout1500to2000
from django.core.mail import EmailMessage
from django.core.mail import send_mail 
logger = logging.getLogger(__name__)  # Add a logger
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.http import JsonResponse
from .models import Ideabook

# # IMAGE GENERATION
# import openai, os, requests
# from dotenv import load_dotenv
# from django.core.files.base import ContentFile
# from my_app.models import Image
# from .models import Image
# load_dotenv()
# api_key = os.getenv("OPENAI_KEY",None)
# openai.api_key = api_key
# from django.shortcuts import render
# from django.conf import settings
# from io import BytesIO
# from PIL import Image as PILImage
# from django.http import HttpResponse

# # views.py or other files
# openai.api_key = settings.OPENAI_API_KEY
# import openai
# openai.api_key = settings.OPENAI_API_KEY
# openai.api_key = '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'
# print(openai.api_key)

# def generate_image_from_txt(request):
#     context = {'image_url': None}

#     if hasattr(settings, 'OPENAI_API_KEY') and settings.OPENAI_API_KEY:
#         openai.api_key = settings.OPENAI_API_KEY
#     else:
#         context['error'] = "API Key is not set in settings."
#         return render(request, 'Design.html', context)

#     if request.method == 'POST':
#         user_input = request.POST.get('user_input')

#         try:
#             # Call the OpenAI API to generate an image
#             response = openai.Image.create(
#                 prompt=user_input,
#                 n=1,
#                 size="1024x1024",
#                 quality="hd",
#             )

#             # Handle response data here...
#             # For example, let's assume response contains a direct URL to the image
#             image_url = response['data'][0]['url']

#             # Download the image content
#             image_response = requests.get(image_url)
#             if image_response.status_code == 200:
#                 # Create a new Image object without saving it to the database
#                 image_content = ContentFile(image_response.content)
#                 filename = f"generated_image.png"
#                 new_image = Image(phrase=user_input)
#                 new_image.ai_image.save(filename, image_content, save=False)

#                 # Add the new image to the context
#                 context['image_url'] = new_image.ai_image.url
#             else:
#                 context['error'] = 'Failed to download the image.'

#         except Exception as e:
#             # Handle any other exceptions
#             context['error'] = 'An error occurred: ' + str(e)

#     # Render the template with the context
#     return render(request, 'Design.html', context)


import os
import openai
import requests
from django.shortcuts import render, redirect
from django.urls import reverse
from django.core.files.base import ContentFile
from my_app.models import Image
from django.conf import settings
from django.http import HttpResponse
from .utilities import remove_background



# Load your API key from an environment variable or Django settings
openai.api_key = os.getenv('OPENAI_API_KEY') or settings.OPENAI_API_KEY

def generate_image_from_txt(request):
    context = {'image_url': None}

    if not openai.api_key:
        context['error'] = "API Key is not set."
        return render(request, 'Design.html', context)

    if request.method == 'POST' and 'user_input' in request.POST:
        user_input = request.POST.get('user_input')

        try:
            # Call the OpenAI API to generate an image
            response = openai.Image.create(
                prompt=user_input,
                n=1,
                size="1024x1024",
                quality="hd",
            )

            # Let's assume the response contains a direct URL to the image
            image_url = response['data'][0]['url']

            # Download the image content
            image_response = requests.get(image_url)
            if image_response.status_code == 200:
                # Create a new Image object and save it to the database
                image_content = ContentFile(image_response.content)
                filename = f"{user_input}_generated_image.png"
                new_image = Image(phrase=user_input)
                new_image.ai_image.save(filename, image_content, save=True)

                # Add the new image to the context
                context['image_url'] = new_image.ai_image.url
            else:
                context['error'] = 'Failed to download the image.'

        except Exception as e:
            # Handle any other exceptions
            context['error'] = f'An error occurred: {str(e)}'

    return render(request, 'Design.html', context)


from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponse

from .utilities import remove_background, generate_3d_model

# Your other imports and code...


import subprocess
def generate_3d_view(request):
    if request.method == 'POST' and 'image_url' in request.POST:
        image_url = request.POST.get('image_url')
        print("Received image URL:", image_url)  # Debug
        
        processed_image = remove_background(image_url)
        print("Processed image path:", processed_image)  # Debug
        
        model_file_path = generate_3d_model(processed_image)
        print("Generated 3D model path:", model_file_path)  # Debug
        
        if model_file_path:
            request.session['model_file_path'] = model_file_path
            print("Model file path set in session:", request.session.get('model_file_path'))  # Debug
            return redirect(reverse('view_3d_model'))
        else:
            print("Model file path not generated")  # Debug
            return HttpResponse("Error: The 3D model could not be generated.")
    else:
        print("POST data did not contain 'image_url'")  # Debug
        return redirect('index')

def view_3d_model(request):
    model_file_path = request.session.get('model_file_path')
    if model_file_path:
        print("Model file path retrieved from session:", model_file_path)  # Debug
    else:
        print("No model file path in session")  # Debug
    context = {'model_file_path': model_file_path}
    return render(request, 'view_3d_model.html', context)



def remove_background(image_url):
    api_key = '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'
    headers = {
        'API-Key': api_key
    }
    data = {
        'image_url': image_url
    }
    response = requests.post('BACKGROUND_REMOVAL_API_ENDPOINT', headers=headers, json=data)
    # ... Existing implementation ...



def user_generate_image_from_txt(request):
    context = {'image_url': None}

    if hasattr(settings, 'OPENAI_API_KEY') and settings.OPENAI_API_KEY:
        openai.api_key = settings.OPENAI_API_KEY
    else:
        context['error'] = "API Key is not set in settings."
        return render(request, 'user_design.html', context)

    if request.method == 'POST':
        user_input = request.POST.get('user_input')

        try:
            # Call the OpenAI API to generate an image
            response = openai.Image.create(
                prompt=user_input,
                n=1,
                size="1024x1024",
                quality="hd",
            )

            # Handle response data here...
            # For example, let's assume response contains a direct URL to the image
            image_url = response['data'][0]['url']

            # Download the image content
            image_response = requests.get(image_url)
            if image_response.status_code == 200:
                # Create a new Image object without saving it to the database
                image_content = ContentFile(image_response.content)
                filename = f"generated_image.png"
                new_image = Image(phrase=user_input)
                new_image.ai_image.save(filename, image_content, save=False)

                # Add the new image to the context
                context['image_url'] = new_image.ai_image.url
            else:
                context['error'] = 'Failed to download the image.'

        except Exception as e:
            # Handle any other exceptions
            context['error'] = 'An error occurred: ' + str(e)

    # Render the template with the context
    return render(request, 'user_design.html', context)


# CHATBOT IMPLEMENTATION
import openai, os, requests
from dotenv import load_dotenv
from django.core.files.base import ContentFile
from my_app.models import Image
from .models import Image
load_dotenv()
api_key = os.getenv("OPENAI_KEY",None)
openai.api_key = api_key
from django.shortcuts import render
from django.conf import settings
from io import BytesIO
from PIL import Image as PILImage
from django.http import HttpResponse

# views.py or other files

openai.api_key = settings.OPENAI_API_KEY
import openai
openai.api_key = settings.OPENAI_API_KEY
openai.api_key = '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'
print(openai.api_key)
# Load environment variables
load_dotenv()
api_key = os.getenv("OPENAI_KEY")
if api_key:
    openai.api_key = api_key
else:
    raise ValueError("No API key found. Make sure your .env file is set up correctly.")

import openai
from django.views.decorators.csrf import csrf_exempt
load_dotenv()
api_key = os.getenv("OPENAI_KEY")
openai.api_key = api_key
from django.views.decorators.http import require_http_methods
import logging
openai.api_key = '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'
logger = logging.getLogger(__name__)

@require_http_methods(["GET", "POST"])
def chatbot(request):
    if request.method == 'POST':
        message = request.POST.get('message')
        response = ask_openai(message)
        return JsonResponse({'message': message, 'response': response})
    else:
        # Handle the GET request
        return render(request, 'chatbot.html')

def ask_openai(user_message):
    try:
        # Construct the chat history for context
        # You'll need to manage and store this context based on the user session or some database
        chat_history = [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": user_message}
            # ... include other messages to maintain the context ...
        ]
        
        # Make the API call to OpenAI's Chat Completion
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # Make sure you're using the correct model name
            messages=chat_history
        )
        
        # Extract the AI's response from the list of messages
        # The response structure may vary, so adjust the following line if needed
        ai_message = response.choices[0].message['content']
        return ai_message.strip()
    except openai.error.OpenAIError as e:
        # Handle specific OpenAI errors here
        logger.error(f"OpenAI API error: {e}")
        return "There was an OpenAI error: " + str(e)
    except Exception as e:
        # Handle other exceptions
        logger.error(f"An unexpected error occurred: {e}")
        return "There was an unexpected error: " + str(e)


@require_http_methods(["GET", "POST"])
def user_chatbot(request):
    if request.method == 'POST':
        message = request.POST.get('message')
        response = ask_openai(message)
        return JsonResponse({'message': message, 'response': response})
    else:
        # Handle the GET request
        return render(request, 'user_chatbot.html')

def ask_openai(user_message):
    try:
        # Construct the chat history for context
        # You'll need to manage and store this context based on the user session or some database
        chat_history = [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": user_message}
            # ... include other messages to maintain the context ...
        ]
        
        # Make the API call to OpenAI's Chat Completion
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # Make sure you're using the correct model name
            messages=chat_history
        )
        
        # Extract the AI's response from the list of messages
        # The response structure may vary, so adjust the following line if needed
        ai_message = response.choices[0].message['content']
        return ai_message.strip()
    except openai.error.OpenAIError as e:
        # Handle specific OpenAI errors here
        logger.error(f"OpenAI API error: {e}")
        return "There was an OpenAI error: " + str(e)
    except Exception as e:
        # Handle other exceptions
        logger.error(f"An unexpected error occurred: {e}")
        return "There was an unexpected error: " + str(e)


# Remember to replace 'your-openai-api-key' with your actual OpenAI API key.

# Create your views here.
def index(request):
    return render(request,'index.html')

def adminpage(request):
    return render(request,'adminpage.html')

def professional_dashboard(request):
    professional = None
    if hasattr(request.user, 'professional'):
        professional = request.user.professional
    return render(request, 'professional_home.html', {'professional': professional})

def signup(request):
    return render(request,'signup.html')

def about(request):
    return render(request,'about.html')

# @csrf_protect
def register_normal_user(request):

    error_messages = {}
    if request.method == 'POST':
        fname = request.POST['fname']
        lname = request.POST['lname']
        uname = request.POST['uname']
        email = request.POST['email']
        phone = request.POST['phone']
        password = request.POST['pass']
        cpassword = request.POST['cpass']

        if User.objects.filter(username=uname).exists():
            error_messages['uname'] = 'Username already taken'  
        if User.objects.filter(email=email).exists():
            error_messages['email'] = 'Email already taken'  

        if not error_messages:
            user = User(username=uname, email=email, is_user=True)
            user.set_password(password)
            user.save()

            normal_user = NormalUser(user=user, first_name=fname, last_name=lname, phone_number=phone)
            normal_user.save()

            return redirect('loginnew')

    return render(request, 'signup.html')


def register_normal_user(request):

    error_messages = {}
    if request.method == 'POST':
        fname = request.POST['fname']
        lname = request.POST['lname']
        uname = request.POST['uname']
        email = request.POST['email']
        phone = request.POST['phone']
        password = request.POST['pass']
        cpassword = request.POST['cpass']

        if User.objects.filter(username=uname).exists():
            error_messages['uname'] = 'Username already taken'  
        if User.objects.filter(email=email).exists():
            error_messages['email'] = 'Email already taken'  

        if not error_messages:
            user = User(username=uname, email=email, is_user=True)
            user.set_password(password)
            user.save()

            normal_user = NormalUser(user=user, first_name=fname, last_name=lname, phone_number=phone)
            normal_user.save()

            return redirect('login')

    return render(request, 'signup.html')

def user_signup(request):
    return render(request,'user_signup.html')

def register_professional(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        company_name = request.POST.get('company_name')
        phone_number = request.POST.get('phone_number')
        country = request.POST.get('country')
        state = request.POST.get('state')
        city = request.POST.get('city')
        pincode = request.POST.get('pincode')
        license_number = request.POST.get('license_number')
        # Assuming you're handling file uploads with Django's default storage system
        license_document = request.FILES.get('license_document')

        print(username, email, password, company_name, phone_number, country, state, city, pincode, license_number,license_document)

        # Basic validation
        if not all([username, email, password, company_name, phone_number, country, state, city, pincode, license_number, license_document]):
            return HttpResponse("All fields are required.", status=400)
        
        if User.objects.filter(username=username).exists():
            return HttpResponse("Username already taken.", status=400)
        
        if User.objects.filter(email=email).exists():
            return HttpResponse("Email already exists.", status=400)
        
        # Create User
        user = User(username=username, email=email ,is_professional=True)
        user.set_password(password)# Hash the password
        user.save()

        # Save license_document
        fs = FileSystemStorage()
        filename = fs.save(license_document.name, license_document)
        uploaded_file_url = fs.url(filename)
        
        # Create Professional
        professional = Professional(
            user=user,
            company_name=company_name,
            phone_number=phone_number,
            country=country,
            state=state,
            city=city,
            pincode=pincode,
            license_document=uploaded_file_url,
            license_number=license_number,
            company_verified=False 
        )
        professional.save()

        return redirect('login')  
    else:
        return render(request, 'professional_signup.html')

def loginnew(request):
    if request.method == 'POST':
        username = request.POST['uname']
        password = request.POST['pass']
        
        user = authenticate(request, username=username, password=password)
        print(user)
        
        if user is not None:
            login(request, user)
            if user.is_user:
                messages.success(request, 'You successfully signed in as a normal user.')
                return redirect('user_signup')
            elif user.is_professional:
                try:
                    professional = Professional.objects.get(user=user)
                    if professional.company_verified:
                        login(request, user)
                        return redirect('professional_dashboard')
                    else:
                        messages.error(request, 'Your company has not been verified yet.')
                        return redirect('login')
                except Professional.DoesNotExist:
                    messages.error(request, 'Professional profile not found.')
                    return redirect('login')
            elif user.is_superuser:
                return redirect('admin_home')
        else:
            return render(request, 'login.html', {'error_message': 'Username or password is incorrect'})
            

    return render(request, 'login.html')

@login_required
@require_POST
def submit_professional_type_services(request):
    user = request.user
    company_type = request.POST.getlist('company_type')
    services_offered = request.POST.getlist('services_offered')
    try:
        professional, created = Professional.objects.get_or_create(user=user)
        professional.company_type = company_type[0] if company_type else ''
        professional.save()
        professional_details, created = ProfessionalDetails.objects.get_or_create(professional=professional)
        professional_details.services_offered = services_offered[0] if company_type else ''
        professional_details.save()
        # Successfully saved, instruct the client to open the next modal
        return JsonResponse({"success": True, "nextModal": "modal2"}, status=200)
    except Exception as e:
        # Error handling
        return JsonResponse({"success": False, "error": str(e)}, status=400)

@login_required
@require_POST
def submit_professional_website_info(request):
    user = request.user
    website_link = request.POST.get('website_link')
    professional_info = request.POST.get('professional_info')
    business_description = request.POST.get('business_description')
    certifications = request.POST.get('certifications')

    try:
        professional = Professional.objects.get(user=user)
        professional_details, created = ProfessionalDetails.objects.get_or_create(professional=professional)
        professional_details.website_link = website_link
        professional_details.professional_information = professional_info
        professional_details.business_description = business_description
        professional_details.certifications_and_awards = certifications
        professional_details.save()
        # Successfully saved, instruct the client to open the next modal
        return JsonResponse({"success": True, "nextModal": "modal3"}, status=200)
    except Exception as e:
        # Error handling
        return JsonResponse({"success": False, "error": str(e)}, status=400)

@login_required
@require_POST
def submit_professional_final_details(request):
    user = request.user
    typical_job_cost = request.POST.get('typical_job_cost')
    number_of_projects = request.POST.get('number_of_projects')
    profile_picture = request.FILES.get('profile_picture')
    cover_photo = request.FILES.get('cover_photo')

    try:
        professional, created = Professional.objects.get_or_create(user=user)

        fs = FileSystemStorage()
        filename = fs.save(profile_picture.name, profile_picture)
        uploaded_profile_picture = fs.url(filename)

        fs = FileSystemStorage()
        filenamee = fs.save(cover_photo.name, cover_photo)
        uploaded_cover_photo = fs.url(filenamee)

        professional.profile_photo = uploaded_profile_picture
        professional.cover_photo = uploaded_cover_photo
        professional.save()
        professional_details = ProfessionalDetails.objects.get(professional=professional)
        professional_details.typical_job_cost = typical_job_cost
        professional_details.number_of_projects = number_of_projects
        professional_details.save()
        # Final step completed, you can instruct the client to redirect or display a success message
        return JsonResponse({"success": True, "message": "Final details submitted successfully!"}, status=200)
    except Exception as e:
        # Error handling
        return JsonResponse({"success": False, "error": str(e)}, status=400)
    
# @login_required
# @require_POST
# def submit_professional_final_details(request):
#     user = request.user
#     typical_job_cost = request.POST.get('typical_job_cost')
#     number_of_projects = request.POST.get('number_of_projects')
    
#     # The following lines handle file uploads and should be within the try block
#     # to properly handle exceptions if the files are not provided
#     try:
#         professional = Professional.objects.get(user=user)
        
#         if 'profile_picture' in request.FILES:
#             profile_picture = request.FILES['profile_picture']
#             fs = FileSystemStorage()
#             filename = fs.save(profile_picture.name, profile_picture)
#             uploaded_profile_picture = fs.url(filename)
#             professional.profile_photo = uploaded_profile_picture

#         if 'cover_photo' in request.FILES:
#             cover_photo = request.FILES['cover_photo']
#             fs = FileSystemStorage()
#             filenamee = fs.save(cover_photo.name, cover_photo)
#             uploaded_cover_photo = fs.url(filenamee)
#             professional.cover_photo = uploaded_cover_photo

#         professional.save()
        
#         # Get or create ProfessionalDetails instance
#         professional_details, created = ProfessionalDetails.objects.get_or_create(professional=professional)
        
#         # Update fields from the form
#         professional_details.typical_job_cost = typical_job_cost
#         professional_details.number_of_projects = number_of_projects
        
#         # Handle other fields such as company_type, services_offered, etc.
#         if not created:
#             professional_details.company_type = request.POST.get('company_type')
#             # Assuming services_offered is a list of services, e.g. ['Masons', 'Electricals']
#             professional_details.services_offered = request.POST.getlist('services_offered')
#             professional_details.website_link = request.POST.get('website_link')
#             professional_details.professional_information = request.POST.get('professional_info')
#             professional_details.business_description = request.POST.get('business_description')
#             professional_details.certifications_and_awards = request.POST.get('certifications')
#             # ... handle other fields as necessary ...

#         professional_details.save()
#         return render(request, 'professional_home.html')


    #     # Final step completed, you can instruct the client to redirect or display a success message
    #     return JsonResponse({"success": True, "message": "Final details submitted successfully!"}, status=200)
    # except Exception as e:
    #     # Error handling
    #     return JsonResponse({"success": False, "error": str(e)}, status=400)



def addprojects(request):
    return render(request,'addprojects.html')

def logoutp(request):
    logout(request)
    return redirect('login')

# def logout(request):
#     logout(request)
#     return redirect('professional_home')

# Add Projects
@login_required
def add_project(request):
    # Ensure the user is an employee and has a company associated
    if not hasattr(request.user, 'is_professional') or not request.user.is_professional:
        return HttpResponse("Unauthorized", status=401)

    # Ensure the employee has an associated company
    try:
        company = request.user.professional
    except Professional.DoesNotExist:
        messages.error(request, "You need to create a company before adding a project.")
        return redirect('add_company')

    if request.method == 'POST':
        try:
            # Process form data
            project_name = request.POST.get('project_name')
            client_name = request.POST.get('client_name')
            address = request.POST.get('address')
            start_date = request.POST.get('start_date')
            expected_end_date = request.POST.get('expected_end_date')
            total_expected_duration = request.POST.get('total_expected_duration')
            cost_of_construction = request.POST.get('cost_of_construction')
            square_feet = request.POST.get('square_feet')
            engineer_name = request.POST.get('engineer_name')
            contact_number = request.POST.get('contact_number')
            status = request.POST.get('status')

            # Create a new project instance
            project = Project(
                professional=company,
                client_name=client_name,
                project_name=project_name,
                address=address,
                start_date=start_date,
                expected_end_date=expected_end_date,
                total_expected_duration=timezone.timedelta(days=int(total_expected_duration)),
                cost_of_construction=cost_of_construction,
                square_feet=square_feet,
                engineer_name=engineer_name,
                contact_number = contact_number,
                status=status
            )

            # Handle uploaded files if any
            if 'image_of_building' in request.FILES:
                project.image_of_building = request.FILES['image_of_building']
            if 'image_of_map' in request.FILES:
                project.image_of_map = request.FILES['image_of_map']

            # Save the project instance
            project.save()
            messages.success(request, "Project added successfully.")
            return redirect('professional_dashboard')
        except Exception as e:
            messages.error(request, f"An error occurred while adding the project: {e}")
            return render(request, 'add_project.html')

    # If the request method is not POST, render the add project form
    return render(request, 'add_project.html')

# def show_projects(request):
#     projects = Project.objects.all()
#     return render(request, 'show_projects.html', {'projects': projects})

# views.py

# views.py

def show_projects(request):
    projects = Project.objects.all()
    return render(request, 'show_projects.html', {'projects': projects})

# def user_project_view(request):
#     projects = Project.objects.all()
#     return render(request, 'user_project_view.html', {'projects': projects})

def user_project_view(request):
    # This assumes that every project has a professional associated with it
    projects = Project.objects.filter(professional__isnull=False)
    return render(request, 'user_project_view.html', {'projects': projects})







def project_detail(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    return render(request, 'project_detail.html', {'project': project})

@login_required
def edit_professional_details(request):
    try:
        professional = request.user.professional
        professional_details = ProfessionalDetails.objects.get(professional=professional)
        # Pass the professional details to the template
        return render(request, 'edit_professional_details.html', {'professional': professional, 'professional_details': professional_details})
    except Professional.DoesNotExist:
        # Handle the case where the professional details do not exist
        messages.error(request, "Professional details not found.")
        return redirect('some_error_page')
    

#view function to add layout 500 to 1000
def add_layout500to1000(request):
    if request.method == 'POST':
        description = request.POST['description']
        num_rooms = int(request.POST['num_rooms'])
        num_halls = int(request.POST['num_halls'])
        num_kitchens = int(request.POST['num_kitchens'])
        num_bathrooms = int(request.POST['num_bathrooms'])
        cost = float(request.POST['cost'])
        num_storeys = int(request.POST['num_storeys'])
        layout_image = request.FILES['layout_image']
        design_image = request.FILES['design_image']
        sqr_ft=int(request.POST['sqr_ft'])
        
        # You should add your own validation logic here
        
        layout_instance = Layout500to1000(
            description=description,
            num_rooms=num_rooms,
            num_halls=num_halls,
            num_kitchens=num_kitchens,
            num_bathrooms=num_bathrooms,
            cost=cost,
            num_storeys=num_storeys,
            layout_image=layout_image,
            design_image=design_image,
            sqr_ft=sqr_ft,
        )
        layout_instance.save()
        
        # Redirect to a new URL:
        return HttpResponse("Layout added successfully")
    
    # If this is a GET (or any other method) create the blank form.
    return render(request, 'add_layout500to1000.html')


#view function to add layout 1000 to 1500
def add_layout1000to1500(request):
    if request.method == 'POST':
        description = request.POST['description']
        num_rooms = int(request.POST['num_rooms'])
        num_halls = int(request.POST['num_halls'])
        num_kitchens = int(request.POST['num_kitchens'])
        num_bathrooms = int(request.POST['num_bathrooms'])
        cost = float(request.POST['cost'])
        num_storeys = int(request.POST['num_storeys'])
        layout_image = request.FILES['layout_image']
        design_image = request.FILES['design_image']
        sqr_ft=int(request.POST['sqr_ft'])
        
        # You should add your own validation logic here
        
        layout_instance = Layout1000to1500(
            description=description,
            num_rooms=num_rooms,
            num_halls=num_halls,
            num_kitchens=num_kitchens,
            num_bathrooms=num_bathrooms,
            cost=cost,
            num_storeys=num_storeys,
            layout_image=layout_image,
            design_image=design_image,
            sqr_ft=sqr_ft
        )
        layout_instance.save()
        
        # Redirect to a new URL:
        return HttpResponse("Layout added successfully")
    
    # If this is a GET (or any other method) create the blank form.
    return render(request, 'add_layout1000to1500.html')


#view function to add layout 1500 to 2000
def add_layout1500to2000(request):
    if request.method == 'POST':
        description = request.POST['description']
        num_rooms = int(request.POST['num_rooms'])
        num_halls = int(request.POST['num_halls'])
        num_kitchens = int(request.POST['num_kitchens'])
        num_bathrooms = int(request.POST['num_bathrooms'])
        cost = float(request.POST['cost'])
        num_storeys = int(request.POST['num_storeys'])
        layout_image = request.FILES['layout_image']
        design_image = request.FILES['design_image']
        sqr_ft=int(request.POST['sqr_ft'])
        
        # You should add your own validation logic here
        
        layout_instance = Layout1500to2000(
            description=description,
            num_rooms=num_rooms,
            num_halls=num_halls,
            num_kitchens=num_kitchens,
            num_bathrooms=num_bathrooms,
            cost=cost,
            num_storeys=num_storeys,
            layout_image=layout_image,
            design_image=design_image,
            sqr_ft=sqr_ft
        )
        layout_instance.save()
        
        # Redirect to a new URL:
        return HttpResponse("Layout added successfully")
    
    # If this is a GET (or any other method) create the blank form.
    return render(request, 'add_layout1500to2000.html')


#view function to search layouts
def search_layouts(request):
    # Initialize an empty context
    context = {'layouts': None}

    # Check if this is a GET request with parameters
    if request.method == 'GET' and request.GET:
        # Extract search parameters from the GET request
        sqr_ft_range = request.GET.get('sqr_ft_range', '')
        num_rooms = request.GET.get('num_rooms', '')
        num_halls = request.GET.get('num_halls', '')
        num_kitchens = request.GET.get('num_kitchens', '')
        num_bathrooms = request.GET.get('num_bathrooms', '')
        num_storeys = request.GET.get('num_storeys', '')

        # Initialize an empty query
        query = None

        # Determine which model to search based on sqr_ft_range
        if sqr_ft_range == '500to1000':
            query = Layout500to1000.objects.all()
        elif sqr_ft_range == '1000to1500':
            query = Layout1000to1500.objects.all()
        elif sqr_ft_range == '1500to2000':
            query = Layout1500to2000.objects.all()

        # Apply additional filters if fields are given
        if num_rooms:
            query = query.filter(num_rooms=num_rooms)
        if num_halls:
            query = query.filter(num_halls=num_halls)
        if num_kitchens:
            query = query.filter(num_kitchens=num_kitchens)
        if num_bathrooms:
            query = query.filter(num_bathrooms=num_bathrooms)
        if num_storeys:
            query = query.filter(num_storeys=num_storeys)

        # Update the context with the query results
        context['layouts'] = query

    # Render the search page with the context containing the search results
    return render(request, 'search_results.html', context)

def send_email(request):
    if request.method == 'POST':
        recipient = request.POST.get('recipient')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        image_url = request.POST.get('image_url')

        try:
            # Render the HTML template for the email body
            html_content = render_to_string('email_template.html', {'message': message, 'image_url': image_url})

            # Create an EmailMultiAlternatives object
            email = EmailMultiAlternatives(subject, strip_tags(html_content), None, [recipient])
            email.attach_alternative(html_content, "text/html")

            # Send email with image
            email.send()

            return JsonResponse({'success': True})  # Return success response
        except Exception as e:
            logging.error(f"Error sending email: {e}")
            return JsonResponse({'success': False, 'error': str(e)}, status=500)  # Return failure response
    else:
        return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=400)


def ideabook(request):
    ideabook_projects = Ideabook.objects.filter(user=request.user)
    return render(request, 'ideabook.html', {'ideabook_projects': ideabook_projects})

def save_to_ideabook(request):
    if request.method == 'POST':
        # Extract data from the POST request
        project_id = request.POST.get('project_id')
        image_url = request.POST.get('image_url')
        project_name = request.POST.get('project_name')

        # Save the project to the ideabook
        ideabook_entry = Ideabook.objects.create(
            user=request.user,
            project_name=project_name,
            image_url=image_url
        )
        ideabook_entry.save()

        # Return a JSON response indicating success
        return JsonResponse({'message': 'Project saved to ideabook successfully'})

    # Handle GET requests (optional)
    return JsonResponse({'error': 'Invalid request method'}, status=400)

def dashboard(request):
    return render(request, 'dashboard.html')

def videocall(request):
    return render(request, 'videocall.html')

def join_room(request):
    if request.method == 'POST':
        roomID = request.POST['roomID']
        return redirect("/meeting/?roomID=" + roomID)
    return render(request, 'joinroom.html')










