import os
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.core.files.storage import default_storage
from django.dispatch import receiver
from django.db.models.signals import post_delete, pre_save, post_save
from django.core.validators import MinValueValidator, MaxValueValidator
# from moviepy.editor import VideoFileClip
import datetime

from article.models.video import Videos
# from ckeditor.fields import RichTextField
# from ckeditor_uploader.fields import RichTextUploadingField 
from .managers import CourseManager



PERCENTAGE_VALIDATOR = [MinValueValidator(0), MaxValueValidator(100)]

class Course(models.Model):
    C =  "completed"
    I = "inprogress"
    STATUS = [
    (C , "تکمیل شده"),
    (I , "درحال تکمیل"),
]
    title = models.CharField(_("عنوان دوره"), max_length=250)
    description = models.TextField(verbose_name = "توضیحات", blank=True, null=True)

    publish_status = models.CharField(_("وضعیت انتشار دوره"),choices=STATUS, max_length=15, default=I)
    is_active = models.BooleanField(_("دوره منتشر شود"))
    author = models.ForeignKey(get_user_model(),verbose_name=_("مدرس"), on_delete=models.CASCADE, related_name="articles")
    is_free = models.BooleanField(_("دوره رایگان است"), default=False)
    price = models.PositiveIntegerField(_("هزینه دوره"),help_text="به تومان", blank=True, null=True)
    #TODO:discount = models.DecimalField(max_digits=3, decimal_places=0, default=Decimal(0), validators=PERCENTAGE_VALIDATOR, blank=True, null=True)  
    image = models.ImageField(_("تصویر"), upload_to='thumbnails/') # 400 * 225
    slug  =  models.SlugField(_("نامک"), unique=True,  help_text = "slug")
    prerequisite = models.TextField(_("پیش نیاز های دوره"), blank=True, null=True)

    
    time_of_course = models.DurationField(_("مدت زمان دوره"), help_text = "HH:MM:SS")
    category = models.ManyToManyField("Category",  verbose_name=_("دسته بندی"), related_name="articles")
    SuggestedCourses = models.ManyToManyField("self", blank=True, verbose_name=_("دوره پیشنهادی"))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    publish_at = models.DateTimeField(blank=True, default=timezone.now ) 
    #TODO: comments
    
    def get_absolute_url(self):
        return reverse("courses:course-detail", kwargs={"slug": self.slug})
    
       
    objects = CourseManager()
    def __str__(self):
        return self.title
    class Meta:
        verbose_name = 'دوره '
        verbose_name_plural = 'دوره ها'
        
    # def save(self, *args, **kwargs):
    #     """ create duration for video"""
    #     obj = super().save(*args, **kwargs)
    #     if self.id:
    #         videos = self.videos.all()
    #         for video in videos:
    #             clip = VideoFileClip(video.videofile.path)
    #             video.duration = datetime.timedelta(seconds=int(clip.duration))
    #             # frame_data = clip.get_frame(1)
    #             # i.video_thumbnail = Image.fromarray(frame_data, 'RGB')
    #             video.save()
    #     return obj
        

@receiver(post_delete, sender=Course)
def delete_associated_files(sender, instance, **kwargs):
    """Remove all files of an article after deletion."""

    image_path = instance.image.name
    if image_path:
        default_storage.delete(image_path)
        
# @receiver(models.signals.pre_save, sender=Course)
# def auto_delete_file_on_change(sender, instance, **kwargs):
#     """
#     Deletes old file from filesystem
#     when corresponding `MediaFile` object is updated
#     with new file.
#     """
#     if not instance.pk:
#         return False
#     try:
#         old_file = Course.objects.get(pk=instance.pk).image
#     except Course.DoesNotExist:
#         return False
#     new_file = instance.image
#     if not old_file == new_file:
#         if os.path.isfile(old_file.path):
#             os.remove(old_file.path)
            

    
# @receiver(post_save, sender=Course)
# def video_duration(sender, instance, created, *args, **kwargs):
#     """ create duration for video"""
#     # TODO: uncomment this later the error was the library not being installed
#     # from article.models import Videos
#     # from PIL import Image
           
#     videos = instance.videos.all()
#     # videos = Videos.objects.all()
#     for video in videos:
#         clip = VideoFileClip(video.videofile.path)
#         video.duration = datetime.timedelta(seconds=int(clip.duration))
#         # frame_data = clip.get_frame(1)
#         # i.video_thumbnail = Image.fromarray(frame_data, 'RGB')
#         video.save()
#         # instance.save()


 
    
class Category(models.Model):
    title= models.CharField(max_length=255)
    position = models.IntegerField(verbose_name=_("پوزیشن"), default=1)
    slug = models.SlugField(max_length=255, unique=True) 
    status = models.BooleanField(default=False, verbose_name=_("وضعیت انتشار"))

    class Meta:
        verbose_name =("دسته‌بندی")
        verbose_name_plural = ("دسته‌بندی ها ")
        ordering = ["position"]
    def __str__(self):
        return self.title


#TODO:question
    


    