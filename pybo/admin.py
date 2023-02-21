from django.contrib import admin
from .models import Question, Answer
# .models : 현재 패키지(pybo)에 있는 models 패키지(모듈)
# from pybo.models import admin과 같음

# Register your models here.

class QuestionAdmin(admin.ModelAdmin):
    search_fields = ['subject']
    list_display = ['id', 'subject', 'create_date']
    ordering = ['id']   # -id라고 하면 내림차순 정렬

admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer)










