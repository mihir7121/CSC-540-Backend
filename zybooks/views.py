from django.shortcuts import render 
from rest_framework.views import APIView
from . models import *
from rest_framework.response import Response 
from . serializer import *
from django.http import HttpResponse
import datetime
import json
from django.http import JsonResponse
from django.contrib.auth.hashers import check_password, make_password
from .models import User
from .decorators import role_required
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

# Authentication
@csrf_exempt
def login(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')

        user = User.objects.filter(username=username).first()
        if user:
            # Verify password            
            if check_password(password, user.password):
                response = JsonResponse({"message": "success"})
                # Set cookie with username and role
                response.set_cookie('username', user.username)
                response.set_cookie('role', user.role)
                return response
            else:
                return JsonResponse({"error": "Invalid credentials"}, status=400)
        else:
            return JsonResponse({"error": "User does not exist. Please sign up!"}, status=200)
    return JsonResponse({"error": "Only POST method is allowed"}, status=405)

@csrf_exempt
def logout(request):
    response = JsonResponse({"message": "Logged out successfully"})
    response.delete_cookie('username')
    response.delete_cookie('role')
    return response

# User CRUD
@csrf_exempt
def signup(request):
    if request.method == 'POST':
        # Parse request body
        data = json.loads(request.body)
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        role = data.get('role')
        first_name = data.get('first_name')
        last_name = data.get('last_name')

        # Basic validations
        if not all([username, email, password, role, first_name, last_name]):
            return JsonResponse({"error": "All fields are required."}, status=400)

        if User.objects.filter(username=username).exists():
            return JsonResponse({"error": "Username already exists."}, status=400)

        if User.objects.filter(email=email).exists():
            return JsonResponse({"error": "Email already exists."}, status=400)

        # Create and save the new user
        hashed_password = make_password(password)  # Hash the password
        new_user = User(
            username=username,
            email=email,
            password=hashed_password,
            role=role,
            first_name=first_name,
            last_name=last_name
        )

        new_user.save()

        return JsonResponse({"message": "User registered successfully!"}, status=201)
    else:
        return JsonResponse({"message": "Sign Up Today!"}, status=200)

# Admin URLs
@role_required(['admin', 'faculty'])
def add_section(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        section_number = data.get('section_number')
        section_title = data.get('section_title')
        chapter_id = data.get('chapter_id')

        # Validate required fields
        if not all([section_number, section_title, chapter_id]):
            return JsonResponse({"error": "All fields are required."}, status=400)
        
        try:
            chapter = Chapter.objects.get(id=chapter_id)  # Fetch chapter
        except Chapter.DoesNotExist:
            return JsonResponse({"error": "Chapter not found."}, status=404)
        
        # Create the new section
        new_section = Section(
            section_id=Section.objects.count() + 1,  # Random for now
            number=section_number,
            title=section_title,
            chapter=chapter,
            hidden=False 
        )
        new_section.save()
        return JsonResponse({"message": "Section added successfully!"}, status=201)
    return JsonResponse({"error": "Only POST method is allowed."}, status=405)

@role_required(['admin'])
def get_chapter(request, chapter_id):
    try:
        chapter = Chapter.objects.get(chapter_id=chapter_id)
        sections = Section.objects.filter(chapter=chapter)

        chapter_data = {
            "chapter_id": chapter.chapter_id,
            "title": chapter.title,
            "hidden": chapter.hidden,
            "textbook": chapter.textbook.title,  # Assuming the Textbook model has a 'title' field
            "sections": [
                {
                    "section_id": section.section_id,
                    "number": section.number,
                    "title": section.title,
                    "hidden": section.hidden,
                }
                for section in sections
            ]
        }

        return JsonResponse(chapter_data, status=200)  # Return chapter details with sections as JSON

    except Chapter.DoesNotExist:
        return JsonResponse({"error": "Chapter not found."}, status=404)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)  # Handle unexpected errors

# ===========================
# TEXTBOOK APIs
# ===========================
@csrf_exempt
@role_required(['admin', 'faculty'])  
@require_http_methods(["POST"])    
def create_textbook(request):
    data = json.loads(request.body)
    title = data.get("title")
    textbook_id = data.get("textbook_id")

    # Check if the textbook already exists
    if Textbook.objects.filter(title=title, textbook_id=textbook_id).exists():
        return JsonResponse({"detail": "Textbook with this title already exists for the course"}, status=400)

    # Create the textbook
    textbook = Textbook(title=title, textbook_id=textbook_id)
    textbook.save()
    return JsonResponse({
        "textbook_id": textbook.textbook_id,
        "title": textbook.title,
        "course_id": textbook.course_id
    }, status=201)

@csrf_exempt
@role_required(['admin', 'faculty'])
@require_http_methods(["GET"])
def read_textbooks(request):
    textbooks = Textbook.objects.all()
    textbooks_list = [{
        "textbook_id": textbook.textbook_id,
        "title": textbook.title,
        "course_id": textbook.course_id
    } for textbook in textbooks]
    return JsonResponse(textbooks_list, status=200, safe=False)

@csrf_exempt
@role_required(['admin', 'faculty'])
@require_http_methods(["GET", "PUT", "DELETE"])    
def textbook(request, textbook_id):
    if request.method == "GET":
        try:
            textbook = Textbook.objects.get(textbook_id=textbook_id)
        except Textbook.DoesNotExist:
            return JsonResponse({"detail": "Textbook not found"}, status=404)

        return JsonResponse({
            "textbook_id": textbook.textbook_id,
            "title": textbook.title,
            "course_id": textbook.course_id
        }, status=200)
    
    elif request.method == "PUT":
        data = json.loads(request.body)
        updated_title = data.get("title")
        course_id = data.get("course_id")

        try:
            textbook = Textbook.objects.get(textbook_id=textbook_id)
        except Textbook.DoesNotExist:
            return JsonResponse({"detail": "Textbook not found"}, status=404)

        textbook.title = updated_title
        textbook.course_id = course_id
        textbook.save()
        return JsonResponse({
            "textbook_id": textbook.textbook_id,
            "title": textbook.title,
            "course_id": textbook.course_id
        }, status=200)
    
    elif request.method == "DELETE":
        try:
            textbook = Textbook.objects.get(textbook_id=textbook_id)
        except Textbook.DoesNotExist:
            return JsonResponse({"detail": "Textbook not found"}, status=404)

        textbook.delete()
        return JsonResponse({"message": "Textbook deleted successfully"}, status=204)

   
# ===========================
# CHAPTER APIs
# ===========================
@csrf_exempt
@role_required(['admin', 'faculty'])  
@require_http_methods(["POST"])
def create_chapter(request):
    try:
        data = json.loads(request.body)
        
        # Check if the chapter already exists
        if Chapter.objects.filter(chapter_id=data.get("chapter_id")).exists():
            return JsonResponse({"detail": "Chapter with this ID already exists"}, status=400)
        
        # Check if the referenced textbook exists
        textbook_id = data.get("textbook_id")
        try:
            textbook = Textbook.objects.get(textbook_id=textbook_id)
        except Textbook.DoesNotExist:
            return JsonResponse({"detail": "Textbook with this ID does not exist"}, status=400)
        
        # Create and save new chapter
        chapter = Chapter.objects.create(
            chapter_id = data.get("chapter_id"),
            title=data.get("title"),
            textbook=textbook,
            hidden=data.get("hidden", False)
        )
        return JsonResponse({
            "chapter_id": chapter.chapter_id,
            "title": chapter.title,
            "textbook_id": chapter.textbook.textbook_id,
            "hidden": chapter.hidden
        }, status=200)
    
    except Exception as e:
        return JsonResponse({"detail": str(e)}, status=500)

@csrf_exempt
@require_http_methods(["GET"])
def read_chapter(request):
    try:       
        # Fetch all chapters if no ID is provided
        chapters = Chapter.objects.all().values("chapter_id", "title", "textbook", "hidden")
        return JsonResponse(list(chapters), safe=False, status=200)
    
    except Exception as e:
        return JsonResponse({"detail": str(e)}, status=500)

@csrf_exempt
@role_required(['admin', 'faculty'])  
@require_http_methods(["GET", "PUT", "DELETE"])
def chapter(request, chapter_id):
    if request.method == "GET":
        if chapter_id:
            try:
                chapter = Chapter.objects.get(chapter_id=chapter_id)
                return JsonResponse({
                    "chapter_id": chapter.chapter_id,
                    "title": chapter.title,
                    "textbook": chapter.textbook,
                    "hidden": chapter.hidden
                }, status=200)
            except Chapter.DoesNotExist:
                return JsonResponse({"detail": "Chapter not found"}, status=404)
    
    elif request.method == "PUT":
        try:
            data = json.loads(request.body)
            
            try:
                chapter = Chapter.objects.get(chapter_id=chapter_id)
            except Chapter.DoesNotExist:
                return JsonResponse({"detail": "Chapter not found"}, status=404)
            
            chapter.title = data.get("title", chapter.title)
            chapter.hidden = data.get("hidden", chapter.hidden)
            chapter.save()
            
            return JsonResponse({
                "chapter_id": chapter.chapter_id,
                "title": chapter.title,
                "textbook": chapter.textbook,
                "hidden": chapter.hidden
            }, status=200)
        
        except Exception as e:
            return JsonResponse({"detail": str(e)}, status=500)
        
    elif request.method == "DELETE":
        try:
            try:
                chapter = Chapter.objects.get(chapter_id=chapter_id)
            except Chapter.DoesNotExist:
                return JsonResponse({"detail": "Chapter not found"}, status=404)
            
            chapter.delete()
            return JsonResponse({"message": "Chapter deleted successfully"}, status=200)
        
        except Exception as e:
            return JsonResponse({"detail": str(e)}, status=500)    


@role_required(['admin'])        
def landing(request):
    now = datetime.datetime.now()
    html = "<html><body>It is now %s.</body></html>" % now
    return HttpResponse(html)

    