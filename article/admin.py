from django.contrib import admin
from django.utils.html import format_html
from jalali_date import datetime2jalali
from jalali_date.fields import JalaliDateField
from jalali_date.widgets import AdminJalaliDateWidget
from django.utils.translation import gettext_lazy as _
# from moviepy.editor import VideoFileClip
import datetime
from .models import Course, Category, Videos, Question, Quiz, HomePage
from .forms import CourseForm




class QuizInline( admin.TabularInline): #admin.TabularInline  #admin.StackedInline
    model = Quiz
    ordering = ("position",)
    # show_change_link = True
    
class VideosInline(admin.TabularInline): #admin.TabularInline  #admin.StackedInline
    model = Videos
    ordering = ("position", "-created_at")



@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):

    list_display = ("title", "slug", "author", "publish_status", "is_active", "price_or_is_free", "time_of_course","image_tag","jPublish_at")
    inlines = [VideosInline, QuizInline]
    prepopulated_fields = {'slug': ('title',), }
    # form = CourseForm
    def price_or_is_free(self, obj):
        if obj.is_free:
            return _("رایگان")
        return obj.price
    price_or_is_free.short_description ="هزینه دوره"
  
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields['publish_at'] = JalaliDateField(label=_('publish_at'), # date format is  "yyyy-mm-dd"
                                                        widget=AdminJalaliDateWidget )
        form.base_fields['author'].label_from_instance = lambda obj: "%s (%s)" % (obj.get_full_name(), obj.username)
        
        # form.fields['author'].queryset = User.objects.filter(Q(is_author = True)| Q(is_superuser= True))     #way 1
        form.base_fields['author'].queryset  = form.base_fields['author'].queryset.filter(is_superuser= True)  #way 2
        return form
    
    # def save_formset(self, request, form, formset, change):
    #     """ create the duration for videos and save it before the parent model(course)"""
    #     #TODO uncomment this later
    #     formset.save() # this will save the children
    #     form.instance.save() # form.instance is the parent
    #     videos = form.instance.videos.all()
    #     for video in videos:
    #         clip = VideoFileClip(video.videofile.path)
    #         video.duration = datetime.timedelta(seconds=int(clip.duration))
    #         # frame_data = clip.get_frame(1)
    #         # i.video_thumbnail = Image.fromarray(frame_data, 'RGB')
    #         video.save()
   

    def image_tag(self, obj):
        return format_html(f'<img src="{obj.image.url}" width="100px" />')
    image_tag.short_description ="تصویر"

    def jPublish_at(self, obj):
        ''' return jalali time'''
        return datetime2jalali(obj.publish_at).strftime('%Y/%m/%d')
    jPublish_at.short_description = "تاریخ انتشار"




@admin.register(HomePage)
class QuizAdmin(admin.ModelAdmin):
    list_display = ["title" ,  "banner_course" ,  "banner2_course" , ]
    
    def has_add_permission(self, request):
        ''' prevent adding more than 1 post'''
        num_objects = self.model.objects.count()
        if num_objects >= 1:
            return False
        else:
            return True

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass


class QuestionInline( admin.TabularInline): #admin.TabularInline  #admin.StackedInline
    model = Question
    ordering = ("position",)
    # show_change_link = True

@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    inlines = [ QuestionInline]
    list_display = ["title", "course", "position"]
    list_filter = ["course", "position"]
    # readonly_fields=('type',)
    
    

    
    

