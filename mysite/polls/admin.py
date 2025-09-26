from django.contrib import admin
from .models import Books
from .models import Questions,Choice

class ChoiceInline(admin.TabularInline):
    model=Choice
    extra=3

class QuestionAdmin(admin.ModelAdmin):
    fieldsets=[
        (None,{'fields':['question_text']}),
        ('Date Information',{'fields':['pub_date']}),
    ]
    inlines=[ChoiceInline]
    list_display=['question_text','pub_date','was_publishedrecently',]
    list_filter=['pub_date']
    search_fields=['question_text']

admin.site.register(Books)
admin.site.register(Questions,QuestionAdmin)