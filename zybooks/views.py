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

# @role_required(['admin'])
# def get_chapter(request, chapter_id):
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
        
        textbook_id = data.get("textbook_id")
        chapter_id = data.get("chapter_id")

        # Check if the referenced textbook exists
        try:
            textbook = Textbook.objects.get(textbook_id=textbook_id)
        except Textbook.DoesNotExist:
            return JsonResponse({"detail": "Textbook with this ID does not exist"}, status=400)
        
        # Check if the chapter already exists in that textbook
        if Chapter.objects.filter(chapter_id=chapter_id, textbook=textbook).exists():
            return JsonResponse({"detail": "Chapter with this ID in this textbook already exists"}, status=400)
        
        
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
@role_required(['admin', 'faculty','ta'])  
@require_http_methods(["GET", "PUT", "DELETE"])
def chapter(request, chapter_id):
    data = json.loads(request.body)
    textbook = Textbook.objects.get(textbook_id = data.get('textbook_id'))

    if request.method == "GET":
        if chapter_id:
            try:
                chapter = Chapter.objects.get(chapter_id=chapter_id, textbook=textbook)
                return JsonResponse({
                    "chapter_id": chapter.chapter_id,
                    "title": chapter.title,
                    "textbook_id": chapter.textbook.textbook_id,
                    "hidden": chapter.hidden
                }, status=200)
            except Chapter.DoesNotExist:
                return JsonResponse({"detail": "Chapter not found"}, status=404)
    
    elif request.method == "PUT":
        try:            
            try:
                chapter = Chapter.objects.get(chapter_id=chapter_id, textbook=textbook)
            except Chapter.DoesNotExist:
                return JsonResponse({"detail": "Chapter not found"}, status=404)
            
            chapter.title = data.get("title", chapter.title)
            chapter.hidden = data.get("hidden", chapter.hidden)
            chapter.save()
            
            return JsonResponse({
                "chapter_id": chapter.chapter_id,
                "title": chapter.title,
                "textbook_id": chapter.textbook.textbook_id,
                "hidden": chapter.hidden
            }, status=200)
        
        except Exception as e:
            return JsonResponse({"detail": str(e)}, status=500)
        
    elif request.method == "DELETE":
        try:
            try:
                chapter = Chapter.objects.get(chapter_id=chapter_id, textbook=textbook)
            except Chapter.DoesNotExist:
                return JsonResponse({"detail": "Chapter not found"}, status=404)
            
            chapter.delete()
            return JsonResponse({"message": "Chapter deleted successfully"}, status=200)
        
        except Exception as e:
            return JsonResponse({"detail": str(e)}, status=500)    



# ===========================
# SECTION APIs
# ===========================
@csrf_exempt
@role_required(['admin', 'faculty','ta'])
@require_http_methods(["POST"])
def create_section(request):
    try:
        data = json.loads(request.body)
        
        # Check if the section already exists
        if Section.objects.filter(section_id=data.get("section_id")).exists():
            return JsonResponse({"detail": "Section with this ID already exists"}, status=400)
        
        # Check if the referenced chapter exists
        chapter_id = data.get("chapter_id")
        textbook_id = data.get("textbook_id")
        try:
            chapter = Chapter.objects.get(chapter_id=chapter_id)
            textbook = Textbook.objects.get(textbook_id=textbook_id)
        except Chapter.DoesNotExist:
            return JsonResponse({"detail": "Chapter with this ID does not exist"}, status=400)
        
        
        # Create and save new section
        section = Section.objects.create(
            section_id=data.get("section_id"),
            number=data.get("number"),
            title=data.get("title"),
            chapter=chapter,
            textbook=textbook,
            hidden=data.get("hidden", False)
        )
        return JsonResponse({
            "section_id": section.section_id,
            "number": section.number,
            "title": section.title,
            "chapter_id": section.chapter.chapter_id,
            "textbook_id": section.textbook.textbook_id,
            "hidden": section.hidden
        }, status=200)
    
    except Exception as e:
        return JsonResponse({"detail": str(e)}, status=500)

@csrf_exempt
@require_http_methods(["GET"])
def read_section(request):
    try:
        # Fetch all sections if no ID is provided
        sections = Section.objects.all().values("section_id", "number", "title", "chapter_id", "hidden")
        return JsonResponse(list(sections), safe=False, status=200)
    
    except Exception as e:
        return JsonResponse({"detail": str(e)}, status=500)

@csrf_exempt
@role_required(['admin', 'faculty'])
@require_http_methods(["GET", "PUT", "DELETE"])
def section(request, section_id):
    section_id = float(section_id)
    if request.method == "GET":        
        if section_id:
            try:
                section = Section.objects.get(section_id=section_id)
                return JsonResponse({
                    "section_id": section.section_id,
                    "number": section.number,
                    "title": section.title,
                    "chapter_id": section.chapter.chapter_id,
                    "hidden": section.hidden
                }, status=200)
            except Section.DoesNotExist:
                return JsonResponse({"detail": "Section not found"}, status=404)
    
    elif request.method == "PUT":
        try:
            data = json.loads(request.body)
            
            try:
                section = Section.objects.get(section_id=section_id)
            except Section.DoesNotExist:
                return JsonResponse({"detail": "Section not found"}, status=404)
            
            section.number = data.get("number", section.number)
            section.title = data.get("title", section.title)
            section.hidden = data.get("hidden", section.hidden)
            section.save()
            
            return JsonResponse({
                "section_id": section.section_id,
                "number": section.number,
                "title": section.title,
                "chapter_id": section.chapter.chapter_id,
                "hidden": section.hidden
            }, status=200)
        
        except Exception as e:
            return JsonResponse({"detail": str(e)}, status=500)
        
    elif request.method == "DELETE":
        try:
            try:
                section = Section.objects.get(section_id=section_id)
            except Section.DoesNotExist:
                return JsonResponse({"detail": "Section not found"}, status=404)
            
            section.delete()
            return JsonResponse({"message": "Section deleted successfully"}, status=200)
        
        except Exception as e:
            return JsonResponse({"detail": str(e)}, status=500)

# ===========================
# Content Block APIs
# ===========================
@csrf_exempt
@role_required(['admin', 'faculty'])
@require_http_methods(["POST"])
def create_content(request):
    try:
        data = json.loads(request.body)
        
        # Validate required fields
        required_fields = ["section_id", "chapter_id", "textbook_id", "content_id"]
        missing_fields = [field for field in required_fields if field not in data]
        
        if missing_fields:
            return JsonResponse(
                {"detail": f"Missing required fields: {', '.join(missing_fields)}"}, 
                status=400
            )
        
        # Fetch Chapter and Textbook objects
        chapter = Chapter.objects.get(chapter_id=data.get("chapter_id"))
        textbook = Textbook.objects.get(textbook_id=data.get("textbook_id"))

        try:
            section = Section.objects.get(section_id=data.get("section_id"), chapter=chapter, textbook=textbook)
        except Section.DoesNotExist:
            return JsonResponse({"detail": "Section with this ID does not exist"}, status=400)
        
        # Create and save new content
        content = Content.objects.create(
            content_id=data.get("content_id"),
            section=section,
            chapter=chapter,
            textbook=textbook,
            hidden=data.get("hidden", False)
        )
        return JsonResponse({
            "textbook_id": content.textbook.textbook_id,
            "chapter_id": content.chapter.id,
            "content_id": content.content_id,
            "section_id": content.section.section_id,
            "hidden": content.hidden
        }, status=200)
    
    except Exception as e:
        return JsonResponse({"detail": str(e)}, status=500)

@csrf_exempt
@require_http_methods(["GET"])
def read_content(request):
    try:
        # Fetch all content blocks
        contents = Content.objects.all().values("content_id", "block_type", "text_data", "image_data", "section_id", "chapter_id", "textbook_id", "hidden")
        return JsonResponse(list(contents), safe=False, status=200)
    
    except Exception as e:
        return JsonResponse({"detail": str(e)}, status=500)

@csrf_exempt
@role_required(['admin', 'faculty'])
@require_http_methods(["GET", "PUT", "DELETE"])
def content(request, content_id):
    try:
        # Fetch specific content block by ID
        content = Content.objects.get(content_id=content_id)
        
        if request.method == "GET":
            return JsonResponse({
                "content_id": content.content_id,
                "block_type": content.block_type,
                "text_data": content.text_data,
                "image_data": content.image_data.url if content.image_data else None,
                "section_id": content.section.section_id,
                "hidden": content.hidden
            }, status=200)
        
        elif request.method == "PUT":
            data = json.loads(request.body)
            
            # Update fields with validation
            content.block_type = data.get("block_type", content.block_type)
            if content.block_type == 'text':
                content.text_data = data.get("text_data", content.text_data)
                content.image_data = None  # Clear image data for text blocks
            elif content.block_type == 'image':
                content.image_data = data.get("image_data", content.image_data)
                content.text_data = None  # Clear text data for image blocks

            content.hidden = data.get("hidden", content.hidden)
            content.save()
            return JsonResponse({"detail": "Content updated successfully"}, status=200)
        
        elif request.method == "DELETE":
            content.delete()
            return JsonResponse({"detail": "Content deleted successfully"}, status=204)
    
    except Content.DoesNotExist:
        return JsonResponse({"detail": "Content with this ID does not exist"}, status=404)
    
    except Exception as e:
        return JsonResponse({"detail": str(e)}, status=500)

@csrf_exempt
@role_required(['admin', 'faculty','ta'])
def content_text(request, content_id):
    if request.method == "POST":
        try:
            content = Content.objects.get(content_id=content_id)
            data = json.loads(request.body)
            
            content.block_type = 'text' 

            if not data.get("text_data"):
                return JsonResponse({"detail": "Missing 'text_data' for text content block"}, status=400)
            
            content.text_data = data.get("text_data")
            content.save()

            return JsonResponse({"detail": "Text added successfully"}, status=200)
        except Content.DoesNotExist:
            return JsonResponse({"detail": "Content block with this ID does not exist"}, status=404)

        except Exception as e:
            return JsonResponse({"detail": str(e)}, status=500)
    return JsonResponse({"detail": "Only POST request allowed"}, status=500)
    
@csrf_exempt
@role_required(['admin', 'faculty','ta'])
def content_image(request, content_id):
    if request.method == "POST":
        try:
            content = Content.objects.get(content_id=content_id)
            content.block_type = 'image'

            if 'image_data' not in request.FILES:
                return JsonResponse({"detail": "Missing 'image_data' file for image content block"}, status=400)

            content.image_data = request.FILES['image_data']
            content.save()

            return JsonResponse({"detail": "Image added successfully", "image_url": request.build_absolute_uri(content.image_data.url)}, status=200)

        except Content.DoesNotExist:
            return JsonResponse({"detail": "Content block with this ID does not exist"}, status=404)

        except Exception as e:
            return JsonResponse({"detail": str(e)}, status=500)
    return JsonResponse({"detail": "Only POST request allowed"}, status=500)

# ===========================
# Activity APIs
# ===========================
@csrf_exempt
@role_required(['admin', 'faculty', 'ta'])
@require_http_methods(["POST"])
def create_activity(request):
    try:
        data = json.loads(request.body)
        activity_id = data.get("activity_id")
        content_id = data.get("content_id")
        try:
            content = Content.objects.get(content_id=content_id)
            activity = Activity.objects.create(activity_id=activity_id, content=content, hidden=data.get("hidden"))
        except:
            return JsonResponse({"detail": "Activity with the given ID already exists"}, status=500)    
        return JsonResponse({
            "activity_id": activity.activity_id,
            "content_id": activity.content.content_id,
            "question_id": activity.question.question_id if activity.question else None,
            "hidden": activity.hidden
        }, status=201)
    
    except Exception as e:
        return JsonResponse({"detail": str(e)}, status=500)

@csrf_exempt
@require_http_methods(["GET"])
def read_activity(request):
    try:
        activities = Activity.objects.all().values("activity_id", "question_id", "hidden")
        return JsonResponse(list(activities), safe=False, status=200)
    
    except Exception as e:
        return JsonResponse({"detail": str(e)}, status=500)

@csrf_exempt
@require_http_methods(["GET", "PUT", "DELETE"])
@role_required(['admin', 'faculty','ta'])
def activity(request, activity_id):
    try:
        if request.method == "GET":
            try:
                activity = Activity.objects.get(activity_id=activity_id)
                data = {
                    "activity_id": activity.activity_id,
                    "question_id": activity.question.question_id if activity.question else None,
                    "hidden": activity.hidden

                }
                return JsonResponse(data, status=200)
            
            except Activity.DoesNotExist:
                return JsonResponse({"detail": "Activity with this ID does not exist"}, status=404)
        
        elif request.method == "PUT":
            try:
                activity = Activity.objects.get(activity_id=activity_id)
                data = json.loads(request.body)
                
                # Update the question if provided and exists
                activity.hidden = data.get("hidden", activity.hidden)
                question_id = data.get("question_id")
                if question_id:
                    try:
                        question = Question.objects.get(question_id=question_id)
                        activity.question = question
                    except Question.DoesNotExist:
                        return JsonResponse({"detail": "Question with this ID does not exist"}, status=400)
                
                activity.save()
                return JsonResponse({
                    "activity_id": activity.activity_id,
                    "question_id": activity.question.question_id,
                    "hidden": activity.hidden
                }, status=200)
            
            except Activity.DoesNotExist:
                return JsonResponse({"detail": "Activity with this ID does not exist"}, status=404)
        
        elif request.method == "DELETE":
            try:
                activity = Activity.objects.get(activity_id=activity_id)
                activity.delete()
                return JsonResponse({"detail": "Activity deleted successfully"}, status=200)
            
            except Activity.DoesNotExist:
                return JsonResponse({"detail": "Activity with this ID does not exist"}, status=404)
        
    except Exception as e:
        return JsonResponse({"detail": str(e)}, status=500)

# ===========================
# Question APIs
# ===========================
@csrf_exempt
@role_required(['admin', 'faculty', 'ta'])
@require_http_methods(["POST"])
def create_question(request):
    try:
        data = json.loads(request.body)

        if not data.get("activity_id"):
            return JsonResponse({"detail": "Need Activity ID to create question"}, status=400)    
        # Retrieve the associated activity by ID
        activity_id = data.get("activity_id")
        activity = Activity.objects.get(activity_id=activity_id)
        
        # Create and save the new question
        question = Question.objects.create(
            question_id=data.get("question_id"),
            question_text=data.get("question_text"),
            option_1_text=data.get("option_1_text"),
            option_1_explanation=data.get("option_1_explanation"),
            option_1_label=data.get("option_1_label"),
            option_2_text=data.get("option_2_text"),
            option_2_explanation=data.get("option_2_explanation"),
            option_2_label=data.get("option_2_label"),
            option_3_text=data.get("option_3_text"),
            option_3_explanation=data.get("option_3_explanation"),
            option_3_label=data.get("option_3_label"),
            option_4_text=data.get("option_4_text"),
            option_4_explanation=data.get("option_4_explanation"),
            option_4_label=data.get("option_4_label"),
        )
        
        # Associate the question with the activity
        activity.question = question
        activity.save()

        return JsonResponse({
            "question_id": question.question_id,
            "question_text": question.question_text,
            "activity_id": activity.activity_id
        }, status=201)
    
    except Activity.DoesNotExist:
        return JsonResponse({"detail": "Activity with this ID does not exist"}, status=400)
    except Exception as e:
        return JsonResponse({"detail": str(e)}, status=500)

@csrf_exempt
@require_http_methods(["GET"])
def read_questions(request):
    try:
        questions = Question.objects.all().values(
            "question_id", "question_text",
            "option_1_text", "option_1_explanation", "option_1_label",
            "option_2_text", "option_2_explanation", "option_2_label",
            "option_3_text", "option_3_explanation", "option_3_label",
            "option_4_text", "option_4_explanation", "option_4_label"
        )
        return JsonResponse(list(questions), safe=False, status=200)
    
    except Exception as e:
        return JsonResponse({"detail": str(e)}, status=500)
    
@csrf_exempt
@require_http_methods(["GET", "PUT", "DELETE"])
@role_required(['admin', 'faculty','ta'])
def question(request, question_id):
    try:
        # Retrieve specific question by ID
        if request.method == "GET":
            try:
                question = Question.objects.get(question_id=question_id)
                data = {
                    "question_id": question.question_id,
                    "question_text": question.question_text,
                    "option_1_text": question.option_1_text,
                    "option_1_explanation": question.option_1_explanation,
                    "option_1_label": question.option_1_label,
                    "option_2_text": question.option_2_text,
                    "option_2_explanation": question.option_2_explanation,
                    "option_2_label": question.option_2_label,
                    "option_3_text": question.option_3_text,
                    "option_3_explanation": question.option_3_explanation,
                    "option_3_label": question.option_3_label,
                    "option_4_text": question.option_4_text,
                    "option_4_explanation": question.option_4_explanation,
                    "option_4_label": question.option_4_label
                }
                return JsonResponse(data, status=200)
            
            except Question.DoesNotExist:
                return JsonResponse({"detail": "Question with this ID does not exist"}, status=404)

        elif request.method == "PUT":
            try:
                question = Question.objects.get(question_id=question_id)
                data = json.loads(request.body)

                # Update fields
                question.question_text = data.get("question_text", question.question_text)
                question.option_1_text = data.get("option_1_text", question.option_1_text)
                question.option_1_explanation = data.get("option_1_explanation", question.option_1_explanation)
                question.option_1_label = data.get("option_1_label", question.option_1_label)
                question.option_2_text = data.get("option_2_text", question.option_2_text)
                question.option_2_explanation = data.get("option_2_explanation", question.option_2_explanation)
                question.option_2_label = data.get("option_2_label", question.option_2_label)
                question.option_3_text = data.get("option_3_text", question.option_3_text)
                question.option_3_explanation = data.get("option_3_explanation", question.option_3_explanation)
                question.option_3_label = data.get("option_3_label", question.option_3_label)
                question.option_4_text = data.get("option_4_text", question.option_4_text)
                question.option_4_explanation = data.get("option_4_explanation", question.option_4_explanation)
                question.option_4_label = data.get("option_4_label", question.option_4_label)

                # Save the updated question
                question.save()
                return JsonResponse({"detail": "Question updated successfully"}, status=200)
            
            except Question.DoesNotExist:
                return JsonResponse({"detail": "Question with this ID does not exist"}, status=404)

        # Delete specific question by ID
        elif request.method == "DELETE":
            try:
                question = Question.objects.get(question_id=question_id)
                question.delete()
                return JsonResponse({"detail": "Question deleted successfully"}, status=200)
            
            except Question.DoesNotExist:
                return JsonResponse({"detail": "Question with this ID does not exist"}, status=404)
    
    except Exception as e:
        return JsonResponse({"detail": str(e)}, status=500)
    
@role_required(['admin'])        
def landing(request):
    now = datetime.datetime.now()
    html = "<html><body>It is now %s.</body></html>" % now
    return HttpResponse(html)

    
# ===========================
# Courses APIs
# ===========================
@csrf_exempt
@role_required(['admin'])
@require_http_methods(["POST"])
def create_course(request):
    try:
        data = json.loads(request.body)
        
        course_token = data.get("course_token")
        course_name = data.get("course_name")
        start_date = data.get("start_date")
        end_date = data.get("end_date")
        course_type = data.get("course_type")
        course_capacity = data.get("course_capacity")
        textbook_id = data.get("textbook_id")
        faculty_id = data.get("faculty_id")
        # Validate required fields
        if not course_token or not course_name or not course_type or not course_capacity:
            return JsonResponse({"detail": "Missing required fields"}, status=400)

        # Check if the course with the given token already exists
        if Course.objects.filter(course_token=course_token).exists():
            return JsonResponse({"detail": "Course with this token already exists"}, status=400)

        # Check if faculty_id exists
        try:
            faculty = User.objects.get(user_id=faculty_id)
        except User.DoesNotExist:
            return JsonResponse({"detail": "Faculty with this ID does not exist"}, status=400)

        # Check if textbook_id exists (if provided)
        textbook = None
        if textbook_id:
            try:
                textbook = Textbook.objects.get(textbook_id=textbook_id)
            except Textbook.DoesNotExist:
                return JsonResponse({"detail": "E-textbook with this ID does not exist"}, status=400)

        
        # Create the course
        course = Course(
            course_token=course_token,
            course_name=course_name,
            start_date=start_date,
            end_date=end_date,
            course_type=course_type,
            course_capacity=course_capacity,
            faculty=faculty
        )
        textbook.course = course
        
        # Save the course instance
        course.save()
        textbook.save()

        # Return response with course details
        return JsonResponse({
            "course_id": course.course_id,
            "course_token": course.course_token,
            "course_name": course.course_name,
            "start_date": course.start_date,
            "end_date": course.end_date,
            "course_type": course.course_type,
            "course_capacity": course.course_capacity
        }, status=201)

    except json.JSONDecodeError:
        return JsonResponse({"detail": "Invalid JSON"}, status=400)
    except Exception as e:
        return JsonResponse({"detail": str(e)}, status=500)

@csrf_exempt
@require_http_methods(["GET"])
def read_courses(request):
    try:
        courses = Course.objects.all().values(
            "course_id", "course_token", "course_name", "start_date", 
            "end_date", "course_type", "course_capacity", 
            "faculty", "ta"
        )
        return JsonResponse(list(courses), safe=False, status=200)
    except Exception as e:
        return JsonResponse({"detail": str(e)}, status=500)

@csrf_exempt
@role_required(['admin', 'faculty'])
@require_http_methods(["GET", "PUT", "DELETE"])
def course(request, course_id):
    if request.method == "GET":
        try:
            course = Course.objects.filter(course_id=course_id).values(
                "course_id", "course_token", "course_name", "start_date", 
                "end_date", "course_type", "course_capacity", 
                "faculty", "ta"
            ).first()
            
            if not course:
                return JsonResponse({"detail": "Course not found"}, status=404)
            
            return JsonResponse(course, status=200)
        except Exception as e:
            return JsonResponse({"detail": str(e)}, status=500)
    
    elif request.method == "PUT":
        try:
            data = json.loads(request.body)
            course = Course.objects.get(course_id=course_id)

            course.course_token = data.get("course_token", course.course_token)
            course.course_name = data.get("course_name", course.course_name)
            course.start_date = data.get("start_date", course.start_date)
            course.end_date = data.get("end_date", course.end_date)
            course.course_type = data.get("course_type", course.course_type)
            course.course_capacity = data.get("course_capacity", course.course_capacity)

            course.save()
            return JsonResponse({
                "course_id": course.course_id,
                "course_token": course.course_token,
                "course_name": course.course_name,
                "start_date": course.start_date,
                "end_date": course.end_date,
                "course_type": course.course_type,
                "course_capacity": course.course_capacity
            }, status=200)
        except Course.DoesNotExist:
            return JsonResponse({"detail": "Course not found"}, status=404)
        except Exception as e:
            return JsonResponse({"detail": str(e)}, status=500)
        
    elif request.method == "DELETE":
        try:
            course = Course.objects.get(course_id=course_id)
            course.delete()
            return JsonResponse({"detail": "Course deleted successfully"}, status=204)
        except Course.DoesNotExist:
            return JsonResponse({"detail": "Course not found"}, status=404)
        except Exception as e:
            return JsonResponse({"detail": str(e)}, status=500)

@csrf_exempt
@require_http_methods(["POST"])
def enroll_in_course(request, course_id):
    try:
        user_id = request.COOKIES.get('username') 

        if not user_id:
            return JsonResponse({"detail": "Missing required fields"}, status=400)

        try:
            student = User.objects.get(username=user_id, role='student')
        except User.DoesNotExist:
            return JsonResponse({"detail": "Student not found or invalid role"}, status=404)

        try:
            course = Course.objects.get(course_id=course_id)
        except Course.DoesNotExist:
            return JsonResponse({"detail": "Course not found"}, status=404)

        if Enrollment.objects.filter(student=student, course=course).exists():
            return JsonResponse({"detail": "Student is already enrolled in this course"}, status=400)

        enrollment = Enrollment(student=student, course=course, status='pending')
        enrollment.save()

        return JsonResponse({
            "message": "Enrollment successful",
            "student_id": student.user_id,
            "course_id": course.course_id,
            "status": enrollment.status
        }, status=201)

    except json.JSONDecodeError:
        return JsonResponse({"detail": "Invalid JSON"}, status=400)
    except Exception as e:
        return JsonResponse({"detail": str(e)}, status=500)

@csrf_exempt
@role_required(['faculty'])
@require_http_methods(["GET"])
def course_worklist(request, course_id):
    try:
        faculty_username = request.COOKIES.get('username')  # Assuming 'username' refers to faculty's username
        if not faculty_username:
            return JsonResponse({"detail": "Missing faculty identifier in cookies"}, status=400)

        try:
            faculty = User.objects.get(username=faculty_username, role='faculty')
        except User.DoesNotExist:
            return JsonResponse({"detail": "Faculty not found or invalid role"}, status=404)
        try:
            course = Course.objects.get(course_id=course_id, faculty=faculty)  
        except Course.DoesNotExist:
            return JsonResponse({"detail": "Course not found for the specified faculty"}, status=404)

        pending_enrollments = Enrollment.objects.filter(course=course, status="pending")

        pending_students = [
            {
                "student_id": enrollment.student.user_id,
                "student_name": f"{enrollment.student.first_name} {enrollment.student.last_name}",
                "status": enrollment.status
            }
            for enrollment in pending_enrollments
        ]

        return JsonResponse({"pending_students": pending_students}, status=200)

    except json.JSONDecodeError:
        return JsonResponse({"detail": "Invalid JSON"}, status=400)
    except Exception as e:
        return JsonResponse({"detail": str(e)}, status=500)


@csrf_exempt
@role_required(['admin', 'faculty'])
@require_http_methods(["GET"])
def course_students(request, course_id):
    try:
        faculty_username = request.COOKIES.get('username')  
        if not faculty_username:
            return JsonResponse({"detail": "Missing faculty identifier in cookies"}, status=400)

        try:
            faculty = User.objects.get(username=faculty_username, role='faculty')
        except User.DoesNotExist:
            return JsonResponse({"detail": "Faculty not found or invalid role"}, status=404)

        try:
            course = Course.objects.get(course_id=course_id, faculty=faculty)  
        except Course.DoesNotExist:
            return JsonResponse({"detail": "Course not found for the specified faculty"}, status=404)

        enrolled_students = Enrollment.objects.filter(course=course, status="enrolled")

        enrolled_students = [
            {
                "student_id": enrollment.student.user_id,
                "student_name": f"{enrollment.student.first_name} {enrollment.student.last_name}",
                "status": enrollment.status
            }
            for enrollment in enrolled_students
        ]

        return JsonResponse({"enrolled_students": enrolled_students}, status=200)

    except json.JSONDecodeError:
        return JsonResponse({"detail": "Invalid JSON"}, status=400)
    except Exception as e:
        return JsonResponse({"detail": str(e)}, status=500)

@csrf_exempt
@require_http_methods(["PUT"])
def update_enrollment_status(request, course_id):
    try:
        data = json.loads(request.body)
        student_id = data.get('student-id')
        if not student_id:
            return JsonResponse({"detail": "Missing required fields"}, status=400)

        faculty_username = request.COOKIES.get('username') 
        if not faculty_username:
            return JsonResponse({"detail": "Missing faculty identifier in cookies"}, status=400)

        try:
            faculty = User.objects.get(username=faculty_username, role='faculty')
        except User.DoesNotExist:
            return JsonResponse({"detail": "Faculty not found or invalid role"}, status=404)

        try:
            course = Course.objects.get(course_id=course_id, faculty=faculty) 
        except Course.DoesNotExist:
            return JsonResponse({"detail": "Course not found for the specified faculty"}, status=404)

        try:
            student = User.objects.get(user_id=student_id, role='student')
            enrollment = Enrollment.objects.get(student=student, course=course, status="pending")
        except User.DoesNotExist:
            return JsonResponse({"detail": "Student not found or invalid role"}, status=404)
        except Enrollment.DoesNotExist:
            return JsonResponse({"detail": "Pending enrollment not found for the specified student and course"}, status=404)

        enrolled_count = Enrollment.objects.filter(course=course, status="enrolled").count()
        if enrolled_count >= course.course_capacity:
            return JsonResponse({"detail": "Course capacity has been reached"}, status=400)

        enrollment.status = "enrolled"
        enrollment.save()

        return JsonResponse({
            "message": "Enrollment status updated to enrolled",
            "student_id": student.user_id,
            "course_id": course.course_id,
            "status": enrollment.status
        }, status=200)

    except json.JSONDecodeError:
        return JsonResponse({"detail": "Invalid JSON"}, status=400)
    except Exception as e:
        return JsonResponse({"detail": str(e)}, status=500)

# ===========================
# ADD TA
# ===========================  
@csrf_exempt
@role_required(['faculty'])
@require_http_methods(["POST"])
def create_ta(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        first_name = data.get('username')
        last_name = data.get('password')
        email_id = data.get('email')
        default_password = data.get('password')
        course_id = data.get('course_id')
        username = request.COOKIES.get('username')
        faculty_id = User.objects.get(username=username).user_id
        user = User.objects.filter(first_name=first_name, last_name=last_name,email=email_id).first()
        if user:
            return JsonResponse({"error": "TA Already Exists"}, status=400)
        else:
            # Create and save a new TA instance
            new_user = User(first_name=first_name, last_name=last_name, email=email_id, password=default_password)
            new_user.save()
            # faculty_id = request.COOKIES.get('user_id')
            try:
                course_selected = Course.objects.get(course_id=course_id)
            except Course.DoesNotExist:
                return JsonResponse({'error': 'Course ID does not exist'}, status=404)
            course_selected.ta = new_user
            course_selected.save()
            ta = TA(ta_username = new_user,faculty_id=User.objects.get(user_id=faculty_id))
            ta.save()
            return JsonResponse({"success": "TA created successfully"}, status=201)

    return JsonResponse({"error": "Only POST method is allowed"}, status=405)

# ================
# Change Password
# ================
@csrf_exempt
@require_http_methods(["POST"])
def change_password(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError as e:
            return JsonResponse({'error': 'Invalid JSON: ' + str(e)}, status=400)

        old_password = data.get("old_password")
        new_password = data.get("new_password")
        username = request.COOKIES.get('username')

        # Fetch the user by username
        user = User.objects.filter(username=username).first()
        if user.DoesNotExist:
            return JsonResponse({'error': 'User not found'}, status=404)

        # Update the password
        user.password = make_password(new_password)  # Hash the new password
        user.save()
        return JsonResponse({'success': 'Password Changed'}, status=200)

    return JsonResponse({'error': 'Only POST method is allowed'}, status=405)

# =============
# TA API's
# =============
@csrf_exempt
@require_http_methods(["GET"])
# @role_required(['ta'])
def all_students(request):
    if request.method == "GET":
        try:
            # Attempt to get all users with the role 'student'
            all_students = User.objects.filter(role='student')
            # Check if any students exist
            if not all_students.exists():
                return JsonResponse({"error": "No students found."}, status=404)
            # Convert QuerySet to a list of dictionaries for JSON serialization
            students_list = list(all_students.values('user_id', 'first_name', 'last_name', 'username', 'email'))
            return JsonResponse({"students": students_list}, status=200)
        except Exception as e:
            # Handle any unexpected exceptions
            return JsonResponse({"error": f"An error occurred: {str(e)}"}, status=500)
    return JsonResponse({"error": "Only GET method is allowed"}, status=405)