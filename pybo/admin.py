from django.contrib import admin
from .models import Question, Answer

class QuestionAdmin(admin.ModelAdmin):
    search_fields = ['subject']
    list_display = ['id', 'subject', 'create_date']
    ordering = ['-id']


admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer)
