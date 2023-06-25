from django.contrib import admin
from .models import Question , Answer



class QuestionAdmin(admin.ModelAdmin):
    search_fields = ['content']

class AnswerAdmin(admin.ModelAdmin):
    search_fields = ['author__id']

# Register your models here.
admin.site.register(Question,QuestionAdmin)
admin.site.register(Answer,AnswerAdmin)