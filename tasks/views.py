import datetime

from django.shortcuts import HttpResponse, render
from django.views.decorators.http import require_POST

from lms.models import StudentLessonRelation
from nodes.models import Lesson
from tasks.models import LessonTask
from users.models import User


def tasks_view(request):
    tasks = LessonTask.objects.filter(student=request.user, is_finished=False)
    args = {'tasks': tasks}
    return render(request, 'teaching/tasks.html', args)


# =======
# For API
# =======
@require_POST
# Create your views here.
def lesson_task_create(request):
    if request.is_ajax():
        lesson_id = request.POST["lesson_id"]
        lesson = Lesson.objects.get(id=lesson_id)

        student_id = request.POST["student_id"]
        student = User.objects.get(id=student_id)

        days = request.POST["days"]
        days = int(days)
        datetime_to = datetime.datetime.now() + datetime.timedelta(days=days)

        teacher = request.user

        try:
            student_lesson = StudentLessonRelation.objects.get(lesson=lesson, student=student)
            student_lesson.has_perm = True
        except StudentLessonRelation.DoesNotExist:
            student_lesson = StudentLessonRelation.objects.create(lesson=lesson, student=student, has_perm=True)
        student_lesson.save()

        lesson_task = LessonTask.objects.create(
            student=student,
            teacher=teacher,
            datetime_to=datetime_to,
            datetime=datetime.datetime.now(),
            lesson=lesson
        )
        lesson_task.save()

    return HttpResponse('OK')
