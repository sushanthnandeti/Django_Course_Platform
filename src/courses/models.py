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

def generate_public_id(instance, *args, **kwargs):
    title = instance.title
    unique_id = str(uuid.uuid4()).replace("-", "")
    if not title:
        return unique_id
    slug = slugify(title)
    unique_id_short = unique_id[:5]
    return f'Courses/{slug} - {unique_id_short}'


def get_public_id_prefix(instance, *args, **kwargs):
    if hasattr(instance, 'path'):
        path = instance.path 
        if path.startswith("/"):
            path = path[1:]
        if path.endswith("/"):
            path = path[:-1]
        return path
    public_id = instance.public_id
    model_class = instance.__class__
    model_name = model_class.__name__
    model_name_slug = slugify(model_name)
    if not public_id:
        return f"{model_name_slug}"
    return f'{model_name_slug}/{public_id}'

def get_display_name(instance, *args, **kwargs):

    if hasattr(instance, 'get_display_name'):
        return instance.get_display_name()
    elif hasattr(instance, 'title'): 
        return instance.title
    model_class = instance.__class__
    model_name = model_class.__name__
    return f"{model_name} Upload" 

class Course(models.Model) :
    title = models.CharField(max_length=120)
    description = models.TextField(blank=True, null=True)
    public_id = models.CharField(max_length=130, blank=True, null=True)
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

    def save(self, *args, **kwargs):
        # before save 
        if self.public_id == "" or self.public_id is None: 
            self.public_id = generate_public_id(self)
        super().save(*args, **kwargs)
        # after save

    def get_absolute_url(self):
        return self.path

    @property
    def path(self):
        return f"/courses/{self.public_id}"
    
    def get_display_name(self):
        return f'{self.title} - Course'

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
    public_id = models.CharField(max_length=130, blank=True, null=True)
    thumbnail = CloudinaryField("image", 
                                public_id_prefix = get_public_id_prefix, 
                                display_name = get_display_name,    
                                blank=True, null=True,
                                tags = ['image', 'thumbnail', 'lesson'])
    video = CloudinaryField("video", 
                                public_id_prefix = get_public_id_prefix, 
                                display_name = get_display_name,
                                blank=True, null=True, resource_type = 'video',
                                tags = ['video', 'thumbnail', 'lesson'])
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

    
    def save(self, *args, **kwargs):
        # before save 
        if self.public_id == "" or self.public_id is None: 
            self.public_id = generate_public_id(self)
        super().save(*args, **kwargs)
        # after save

    def get_absolute_url(self):
        return self.path

    @property
    def path(self):
        course_path = self.course.path
        if course_path.endswith("/"):
            course_path = course_path[:-1]
        return f'{course_path}/lessons/{self.public_id}'
    
    def get_display_name(self):
        return f'{self.title} - {self.course.get_display_name()}'