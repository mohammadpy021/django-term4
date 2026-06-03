from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.db.models.signals import post_delete
from django.core.validators import FileExtensionValidator
from django.dispatch import receiver
from django.db.models.signals import pre_save, post_save
# from moviepy.editor import VideoFileClip
import datetime



def video_path(instance, filename):
    return f'videos/{instance.course.slug}/{filename})'

VIDEO_VALIDATOR = [FileExtensionValidator(allowed_extensions=['mp4', 'mkv'])]

class Videos(models.Model):
    
    def course_slug(self):
        return str(self.course.slug)

    # def video_path(self):
    #     return (str(self.course.slug))
        # return osjoin(str(self.category), filename)
    
    position = models.FloatField(verbose_name=_("ترتیب "), default=1, blank=True, null=True)
    # episode = models.IntegerField(verbose_name=_("قسمت"), default=1, blank=True, null=True)
    # season = models.IntegerField(verbose_name=_("فصل"), default=1, blank=True, null=True)
    title= models.CharField(max_length=255, verbose_name=_("عنوان فیلم"))
    video_description= models.CharField(max_length=500, blank=True, null=True)
    slug = models.SlugField(max_length=255) 
    publish = models.BooleanField(default=False, verbose_name=_(" انتشار")) 
    is_free = models.BooleanField(default=False, verbose_name=_(" رایگان"))
    course = models.ForeignKey("article.Course",verbose_name=_("دوره"), on_delete=models.CASCADE, related_name="videos")
    duration = models.DurationField(_("مدت زمان ویدیو"), null=True, blank=True,help_text = "HH:MM:SS")
    videofile= models.FileField(upload_to=video_path, null=True, verbose_name="ویدیو",help_text=".mp4, .mkv", validators=VIDEO_VALIDATOR)
    video_thumbnail = models.ImageField(upload_to=video_path, blank=True, null=True, verbose_name="تامبنیل")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    type = models.CharField(_("نوع"), default="video", max_length=10, editable=False)
     

    
    # def get_absolute_url(self):
    #     return reverse ("deploy:detail", kwargs={"slug":self.slug})

    class Meta:
        verbose_name =("ویدیو")
        verbose_name_plural = ("ویدیو ها ")
    def __str__(self):
        return self.title
    


# @receiver(post_save, sender=Videos)
# def video_duration(sender, instance, **kwargs):
#     """ create duration for video"""
#     from moviepy.editor import VideoFileClip
#     import datetime
#     # from article.models import Videos
#     # from PIL import Image
    
#     videos = Videos.objects.filter(course = instance.course)
#     for video in videos:
#         clip = VideoFileClip(video.videofile.path)
#         video.duration = datetime.timedelta(seconds=int(clip.duration))
#         # frame_data = clip.get_frame(1)
#         # i.video_thumbnail = Image.fromarray(frame_data, 'RGB')
#         video.save()


# from moviepy.editor import VideoFileClip
# import datetime
# from article.models import Videos
# from PIL import Image

# videos = Videos.objects.all()
# for i in videos:
#     clip = VideoFileClip(i.videofile.path)
#     i.duration = datetime.timedelta(seconds=int(clip.duration))
#     frame_data = clip.get_frame(1)
#     i.video_thumbnail = Image.fromarray(frame_data, 'RGB')
#     i.save()

# from mutagen.mp4 import MP4
# for i in videos:
#     audio = MP4(i.videofile.path)
#     clip = VideoFileClip(i.videofile.path)
#     i.duration = datetime.timedelta(seconds=int(clip.duration))
#     i.save()




# >>> for i in videos:
# ...     clip = VideoFileClip(i.videofile.path)
# ...     i.video_thumbnail = clip.save_frame("thumbnail.jpg",t=1.00)
# ...     i.save()







