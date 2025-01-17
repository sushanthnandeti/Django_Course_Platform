import uuid
from django.db import models
import helpers
from cloudinary.models import CloudinaryField
from django.utils.text import slugify

helpers.cloudinary_init()

# Create your models here.

class AccessRequirement(models.TextChoices):
    ANYONE = "any", "Anyone"
    EMAIL_REQUIRED = "email", "Email Required"
  

class PublishStatus(models.TextChoices):
    PUBLISHED = "publish", "PUBLISH"
    COMING_SOON = "soon", "Coming Soon"
    DRAFT = "draft", "DRAFT"

def handle_upload(instance, filename):

    return f"{filename}"

def get_public_id_prefix(instance, *args, **kwargs):
    title = instance.title

    if title:
        slug = slugify(title)
        unique_id = str(uuid.uuid4()).replace("-", "")[:5]
        return f'Courses/{slug}'
    
    if instance.id: 
        return f'courses/{instance.id}'
    
    return 'courses'


def get_display_name(instance, *args, **kwargs):
    title = instance.title

    if title:
       return title 
    return 'Course upload'

class Course(models.Model) :
    title = models.CharField(max_length=120)
    description = models.TextField(blank=True, null=True)
    image= CloudinaryField("image", null = True , 
           public_id_prefix = get_public_id_prefix, 
           display_name = get_display_name,
           tags = ['courses', 'thumbnail']
           )
    access = models.CharField(
        max_length=10,
        choices= AccessRequirement.choices,
        default=AccessRequirement.EMAIL_REQUIRED
    )

    status = models.CharField(
        max_length=10,
        choices= PublishStatus.choices,
        default=PublishStatus.DRAFT
    )

    updated = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    @property 
    def is_published(self):
        return self.status == PublishStatus.PUBLISHED
    
    @property 
    def image_admin_url(self):
        if not self.image: 
            return ""
        image_options = {
            "width" : 200
        }
        url = self.image.build_url(**image_options)
        return url
     
    def get_image_thumbail(self, as_html = False, width = 500):
        if not self.image: 
            return ""
        image_options = {
            "width" : width
        }
        if as_html: 
            # CloudinaryImage(cloudinary_id).image(**image_options)

            return self.image.build_url(**image_options) 
        # CloudinaryImage(cloudinary_id).build_url(**image_options)
        url = self.image.build_url(**image_options)
        return url
    
# Lesson.objects.all() # lesson queryset -> all rows
# Lesson.objects.first()
# course_obj = Course.objects.first()
# course_qs = Course.objects.filter(id=course_obj.id)
# Lesson.objects.filter(course__id=course_obj.id)
# course_obj.lesson_set.all()
# lesson_obj = Lesson.objects.first()
# ne_course_obj = lesson_obj.course
# ne_course_lessons = ne_course_obj.lesson_set.all()
# lesson_obj.course_id
# course_obj.lesson_set.all().order_by("-title")
    
class Lesson(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    title = models.CharField(max_length=120)
    description = models.TextField(blank=True, null=True)
    thumbnail = CloudinaryField("image", blank=True, null=True)
    video = CloudinaryField("video", blank=True, null=True, resource_type = 'video')
    order = models.IntegerField(default=0)
    can_preview = models.BooleanField(default= False, help_text="If a user does not have access to course, can they preview this lesson")

    status = models.CharField(
        max_length=10,
        choices= PublishStatus.choices,
        default=PublishStatus.PUBLISHED
    )

    updated = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta: 
        ordering = ['order', '-updated']