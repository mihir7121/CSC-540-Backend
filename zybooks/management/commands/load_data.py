import json
from django.core.management.base import BaseCommand
from zybooks.models import Course, User,Textbook,Chapter 

class Command(BaseCommand):
    help = 'Load courses from a JSON file'

    def handle(self, *args, **kwargs):
        # Load data from JSON file
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
                course =  Course.objects.get(course_id=textbook['course_id'])

                # Create Textbook instance
                Textbook.objects.create(
                        textbook_id=textbook["textbook_id"],
                        title=textbook["title"],
                        course=course
                    )
        self.stdout.write(self.style.SUCCESS('Successfully loaded TextBooks'))
        
        with open('zybooks/management/commands/chapters.json', 'r') as file:
            chapters = json.load(file)
            for chapter in chapters:
                try:
                    # Retrieve the associated textbook
                    textbook = Textbook.objects.get(textbook_id=chapter['textbook_id'])
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