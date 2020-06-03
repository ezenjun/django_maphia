
from django.contrib import admin

from .models import Question, Choice

# Register your models here.

#admin.site.register(Question)

# inline을 상속받아서 class를 하나 만든다.
# 보여질 모델의 종류, 인라인으로 보여질 모델의 개수를 명시
class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3

# admin을 custumizing하기 위해서 admin을 상속받는 class를 선언
class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['question_text']}),
        ('Date information', {'fields': ['pub_date'],
        'classes': ['collapse']}),
    ]
    inlines = [ChoiceInline] #QuestionAdmin의 Inline으로 ChoiceInline을 등록
    # => questioninline에서 Choice 관리 가능
    # class 내에 우리가 필요로 하는 값을 직접 부여해 custumizing함.
    # field를 변경해서 보여지는 data 순서를 변경할 수 있다.
    # fields = ['pub_date', 'question_text']
    # field가 많아 관리를 필요로 하는 경우에는 fieldsets를 통해 필드를 묶어서 제목을 주는 것도 가능하다.

    #list display를 통해 qestion과 발행일, 최근 발행일 데이터냐는 field도 추가가 가능하다.
    list_display = ('question_text', 'pub_date', 'was_published_recently')

    search_fields=['question_text'] #검색기능 추가

# register의 두번째 인자로 custumizing한 class를 넘겨준다.
admin.site.register(Question, QuestionAdmin)

#admin.site.register(Choice)