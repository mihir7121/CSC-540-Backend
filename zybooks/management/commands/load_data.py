import json
from django.core.management.base import BaseCommand
from zybooks.models import *

class Command(BaseCommand):
    help = 'Load courses from a JSON file'

    def handle(self, *args, **kwargs):
        # # Load data from JSON file
        with open('zybooks/management/commands/courses.json', 'r') as file:
            courses_data = json.load(file)

        for course_data in courses_data:
            # Fetch faculty and TA users
            faculty = User.objects.get(user_id=course_data['faculty'])
            ta = User.objects.get(user_id=course_data['ta']) if course_data['ta'] else None
            
            # Create Course instance
            Course.objects.create(
                course_id=course_data['course_id'],
                course_name=course_data['course_name'],
                course_token=course_data['course_token'],
                course_type=course_data['course_type'],
                course_capacity=course_data['course_capacity'],
                faculty=faculty,
                ta=ta,
                start_date=course_data['start_date'],
                end_date=course_data['end_date'],
            )
        self.stdout.write(self.style.SUCCESS('Successfully loaded courses'))

        with open('zybooks/management/commands/textbooks.json','r') as file:
            textbook_data = json.load(file)
            for textbook in textbook_data:

                # Create Textbook instance
                Textbook.objects.create(
                        textbook_id=textbook["textbook_id"],
                        title=textbook["title"],
                    )
        self.stdout.write(self.style.SUCCESS('Successfully loaded TextBooks'))
        
        with open('zybooks/management/commands/chapters.json', 'r') as file:
            chapters = json.load(file)
            for chapter in chapters:
                try:
                    # Retrieve the associated textbook
                    textbook = Textbook.objects.get(textbook_id=chapter['textbook'])
                    # Create Chapter instance (id is auto-generated)
                    Chapter.objects.create(
                        chapter_name=chapter['chapter_name'],  # Not unique; it's just a regular field
                        title=chapter['title'],
                        textbook=textbook,
                        hidden=chapter['hidden']  # True or False
                    )
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f'Unexpected error: {e}'))

        self.stdout.write(self.style.SUCCESS('Successfully loaded Chapters'))

        with open('zybooks/management/commands/sections_data.json', 'r') as file:
            sections = json.load(file)
            for section_data in sections:
                try:
                    # Retrieve the associated textbook
                    textbook = Textbook.objects.get(textbook_id=section_data['textbook'])
                    
                    # Retrieve the associated chapter
                    chapter = Chapter.objects.get(chapter_name=section_data['chapter'], textbook=textbook)

                    # Create Section instance
                    Section.objects.create(
                        number=section_data['number'],
                        title=section_data['title'],
                        chapter=chapter,
                        textbook=textbook,
                        hidden=section_data['hidden']
                    )
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f'Unexpected error: {e}'))

        self.stdout.write(self.style.SUCCESS('Successfully loaded Sections'))


        with open('zybooks/management/commands/questions.json', 'r') as file:
                questions = json.load(file)
                for question_data in questions:
                    try:
                        # Create Question instance
                        Question.objects.create(
                            question_name=question_data['question_name'],
                            question_text=question_data['question_text'],
                            option_1_text=question_data['option_1_text'],
                            option_1_explanation=question_data.get('option_1_explanation', ''),
                            option_2_text=question_data['option_2_text'],
                            option_2_explanation=question_data.get('option_2_explanation', ''),
                            option_3_text=question_data['option_3_text'],
                            option_3_explanation=question_data.get('option_3_explanation', ''),
                            option_4_text=question_data['option_4_text'],
                            option_4_explanation=question_data.get('option_4_explanation', ''),
                            answer=question_data['answer']
                        )
                    except Exception as e:
                        self.stdout.write(self.style.ERROR(f'Error inserting question: {e}'))

        self.stdout.write(self.style.SUCCESS('Successfully loaded Questions'))

        with open('zybooks/management/commands/contents.json', 'r') as file:
            contents = json.load(file)
            for content_data in contents:
                try:
                    # Retrieve the associated textbook
                    textbook = Textbook.objects.get(textbook_id=content_data['textbook'])
                    
                    # Retrieve the associated chapter
                    chapter = Chapter.objects.get(chapter_name=content_data['chapter'], textbook=textbook)

                    # Retrieve the associated section
                    section = Section.objects.get(number=content_data['section'], chapter=chapter)

                    # Create Content instance
                    content = Content.objects.create(
                        content_name=content_data['content_name'],
                        section=section,
                        chapter=chapter,
                        textbook=textbook,
                        hidden=content_data.get('hidden', False)
                    )

                    # Check if block_type is 'activities' to create Activity instances
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f'Unexpected error: {e}'))

        self.stdout.write(self.style.SUCCESS('Successfully loaded Contents'))

        with open('zybooks/management/commands/activities.json', 'r') as file:
            activities = json.load(file)
            for activity_data in activities:
                try:
                    # Retrieve the associated textbook
                    textbook = Textbook.objects.get(textbook_id=activity_data['textbook'])

                    # Retrieve the associated chapter
                    chapter = Chapter.objects.get(chapter_name=activity_data['chapter'], textbook=textbook)

                    # Retrieve the associated section
                    section = Section.objects.get(number=activity_data['section'], chapter=chapter)

                    # Retrieve the associated content (assuming Content model exists and is linked with sections)
                    content = Content.objects.get(content_name=activity_data['content_name'], section=section, chapter=chapter, textbook=textbook)

                    # Create Activity instance
                    Activity.objects.create(
                        activity_number=activity_data['activity_number'],
                        content=content,  # Link to Content model
                        hidden=activity_data.get('hidden', False)
                    )

                except Exception as e:
                    self.stdout.write(self.style.ERROR(f'Unexpected error: {e}'))

        self.stdout.write(self.style.SUCCESS('Successfully loaded Activities'))

        with open('zybooks/management/commands/ta.json', 'r') as file:
            ta_data = json.load(file)
            for ta_entry in ta_data:
                try:
                    # Get TA user instance using the ta_id
                    ta_user = User.objects.get(user_id=ta_entry['ta_id'])
                    # Get associated faculty user instance using the associated_faculty_email
                    faculty_user = User.objects.get(user_id=ta_entry['faculty_id'])

                    # Create TA instance and save it to the database
                    TA.objects.create(
                        ta=ta_user,
                        associated_faculty=faculty_user,
                        hourly_pay=ta_entry['hourly_pay'],
                        hours_per_week=ta_entry['hours_per_week']
                    )
                except User.DoesNotExist as e:
                    self.stdout.write(self.style.ERROR(f'User not found: {e}'))
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f'Error inserting TA data: {e}'))

        self.stdout.write(self.style.SUCCESS('Successfully loaded TA data'))


        with open('zybooks/management/commands/enrollments.json', 'r') as file:
                enrollment_data = json.load(file)
                
                for entry in enrollment_data:
                    try:
                        student = User.objects.get(user_id=entry['student_id'])
                        course = Course.objects.get(course_id=entry['course_id'])
                        
                        Enrollment.objects.create(
                            student=student,
                            course=course,
                            status=entry['status']
                        )
                        
                    except Exception as e:
                        self.stdout.write(self.style.ERROR(f"Error inserting enrollment data: {e}"))
                        break
        
        self.stdout.write(self.style.SUCCESS('Successfully loaded enrollment data'))

        with open('zybooks/management/commands/enrolled_students.json', 'r') as file:
                student_data = json.load(file)
                
                for entry in student_data:
                    try:
                        student = User.objects.get(user_id=entry['student_id'])
                        course = Course.objects.get(course_id=entry['course_id'])
                        
                        Student.objects.create(
                            user=student,
                            course_id=course,
                            total_activities=entry['total_activities'],
                            total_points=entry['total_points']
                        )
                        
                    except Exception as e:
                        self.stdout.write(self.style.ERROR(f"Error inserting student data: {e}"))
        

        self.stdout.write(self.style.SUCCESS('Successfully loaded student data'))