from django.contrib import admin
from api.models import Notification, NotificationType, Question, Answer, Profile, AnsweredQuestions

class NotificationTypeAdmin(admin.ModelAdmin):
    pass

class NotificationAdmin(admin.ModelAdmin):
    pass

class QuestionAdmin(admin.ModelAdmin):
    pass

class AnswerAdmin(admin.ModelAdmin):
    pass

class ProfileAdmin(admin.ModelAdmin):
    pass

class AnsweredQuestionsAdmin(admin.ModelAdmin):
    pass

admin.site.register(NotificationType, NotificationTypeAdmin)
admin.site.register(Notification, NotificationAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer, AnswerAdmin)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(AnsweredQuestions, AnsweredQuestionsAdmin)