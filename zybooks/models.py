from django.db import models
from django.utils import timezone

# Create your models here.
class User(models.Model):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('faculty', 'Faculty'),
        ('ta', 'Teaching Assistant'),
        ('student', 'Student'),
    ]

    user_id = models.CharField(max_length=8, primary_key=True) 
    first_name = models.CharField(max_length=30, null=False)
    last_name = models.CharField(max_length=30, null=False)
    username = models.CharField(max_length=30, unique=True, null=False)
    email = models.EmailField(unique=True, null=False)
    password = models.CharField(max_length=128)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    
    creation_date = models.DateTimeField(default=timezone.now, null = False)

    def save(self, *args, **kwargs):
        if not self.user_id:  # Generate user_id only if it hasn't been set
            month = self.creation_date.strftime("%m")  # Get month in 2 digits
            year = self.creation_date.strftime("%y")    # Get year in 2 digits
            first_part = (self.first_name[:2] + self.last_name[:2]).lower()  # First two letters of first and last names
            self.user_id = f"{first_part}{month}{year}"  # Create user_id
        super().save(*args, **kwargs)  # Call the original save method

    def __str__(self):
        return f"{self.username} ({self.role})"

class Course(models.Model):
    TYPE_CHOICES = [
        ('active', 'Active'),
        ('evaluation', 'Evaluation'),
    ]
    # Primary fields for Course details
    course_id = models.AutoField(primary_key=True)  # Unique identifier for the course
    course_token = models.CharField(max_length=7, unique=True)
    course_name = models.CharField(max_length=100)  # Name of the course
    start_date = models.DateField(default=timezone.now)
    end_date = models.DateField(blank=True, null=True)
    course_type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    course_capacity = models.PositiveIntegerField() 

    # textbook = models.ForeignKey('Textbook', on_delete=models.SET_NULL, blank=True, null=True)  # Textbook used in the course
    # faculty = models.ForeignKey('Faculty', on_delete=models.CASCADE)  # Faculty teaching the course
    # ta = models.ForeignKey('TA', on_delete=models.SET_NULL, blank=True, null=True)  # Teaching Assistant for the course

    def __str__(self):
        return f"{self.course_id} - {self.course_name}"

class Enrollment(models.Model):
    ENROLLMENT_CHOICES = [
        ('pending', 'Pending'),
        ('enrolled', 'Enrolled')
    ]
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=ENROLLMENT_CHOICES, default='pending')

    class Meta:
        unique_together = ('student', 'course')

class Textbook(models.Model):
    textbook_id = models.PositiveIntegerField(primary_key=True)
    title = models.CharField(max_length=100)
    course = models.ForeignKey(Course, on_delete=models.RESTRICT, null=True)

    def __str__(self):
        return self.title
    
class Chapter(models.Model):
    chapter_id = models.PositiveIntegerField(primary_key=True)
    title = models.CharField(max_length=100)
    textbook = models.ForeignKey(Textbook, on_delete=models.CASCADE)
    hidden = models.BooleanField()

class Section(models.Model):
    section_id = models.FloatField(primary_key=True)
    number = models.CharField(max_length=10)
    title = models.CharField(max_length=100)
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE)
    hidden = models.BooleanField()

class Content(models.Model):
    BLOCK_TYPE_CHOICES = [
        ('text', 'Text'),
        ('image', 'Image'),
    ]

    content_id = models.IntegerField(primary_key=True)
    block_type = models.CharField(max_length=5, choices=BLOCK_TYPE_CHOICES, blank=True)
    text_data = models.TextField(blank=True, null=True)  # Field for text content
    image_data = models.ImageField(upload_to='images/', blank=True, null=True)
    section = models.ForeignKey(Section, on_delete=models.CASCADE)
    hidden = models.BooleanField(blank=True)

    class Meta:
        unique_together = ('section', 'content_id')

    def save(self, *args, **kwargs):
        # Validation to ensure only the appropriate field is populated based on block_type
        if self.block_type == 'text':
            if not self.text_data:
                raise ValueError("Text data must be provided for text block type")
            self.image_data = None  # Clear image data for text blocks

        elif self.block_type == 'image':
            if not self.image_data:
                raise ValueError("Image data must be provided for image block type")
            self.text_data = None  # Clear text data for image blocks

        super().save(*args, **kwargs)

class Notification(models.Model):
    notification_id = models.AutoField(primary_key=True)
    message = models.CharField(max_length=500)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    read_status = models.BooleanField()