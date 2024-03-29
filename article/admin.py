from django.contrib import admin
from django.utils.html import format_html
from jalali_date import datetime2jalali
from jalali_date.fields import JalaliDateField
from jalali_date.widgets import AdminJalaliDateWidget
from django.utils.translation import gettext_lazy as _
from .models import Course, Category, Videos
from .forms import CourseForm




class VideosInline(admin.TabularInline): #admin.TabularInline  #admin.StackedInline
    model = Videos
    ordering = ("position", "-created_at")


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    
    list_display = ("title", "slug", "author", "publish_status", "is_active", "price", "time_of_course","image_tag","jPublish_at")
    inlines = [VideosInline]
    prepopulated_fields = {'slug': ('title',), }
    # form = CourseForm
    
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields['publish_at'] = JalaliDateField(label=_('publish_at'), # date format is  "yyyy-mm-dd"
                                                        widget=AdminJalaliDateWidget )
        form.base_fields['author'].label_from_instance = lambda obj: "%s (%s)" % (obj.get_full_name(), obj.username)
        return form
    
    def image_tag(self, obj):
        return format_html(f'<img src="{obj.image.url}" width="100px" />')
    image_tag.short_description ="تصویر"

    def jPublish_at(self, obj):
        ''' return jalali time'''
        return datetime2jalali(obj.publish_at).strftime('%Y/%m/%d')
    jPublish_at.short_description = "تاریخ انتشار"

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass



   



