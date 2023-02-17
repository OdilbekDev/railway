from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.



class User(AbstractUser):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    username = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    email = models.EmailField(null=True, blank=True)
    branch = models.ManyToManyField('Branch', default=None, null=True, blank=True)
    age = models.IntegerField(null=True, blank=True)
    gender = models.IntegerField(
        choices=(
            (1, 'Male'),
            (2, 'Female')
        ), null=True, blank=True
    )
    type = models.IntegerField(
        choices=(
            (1, "Director"),
            (2, "Teacher"),
            (3, "Reception"),
            (4, "Manager"),
        ), default=3
    )

class Lesson_Days(models.Model):
    dayuz = models.CharField(max_length=255)
    dayeng = models.BigIntegerField()

    def __str__(self) -> str:
        return self.dayuz

class Subject(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Level(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.name


class Group(models.Model):
    name = models.CharField(max_length=255)
    level = models.ForeignKey(Level, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    teacher = models.ForeignKey('Teacher', on_delete=models.CASCADE)
    money = models.BigIntegerField()
    lesson_days = models.ManyToManyField(Lesson_Days, blank=True, null=True)
    room = models.BigIntegerField()
    max_pupil = models.BigIntegerField()
    time_start = models.CharField(max_length=255)
    time_end = models.CharField(max_length=255)

    # def __str__(self):
    #     return self.name


class Teacher(models.Model):
    name = models.CharField(max_length=255)
    money = models.BigIntegerField(blank=True, null=True)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    phone = models.BigIntegerField(unique=True)
    extra_phone = models.BigIntegerField(null=True, blank=True, unique=True)
    email = models.EmailField(null=True, blank=True, unique=True)
    location = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE, unique=True)
    percent = models.IntegerField()

    def __str__(self):
        return self.name




class Pupil(models.Model):
    name = models.CharField(max_length=255)
    level = models.CharField(max_length=255)
    phone = models.BigIntegerField(unique=True)
    extra_phone = models.BigIntegerField(null=True, blank=True, unique=True)
    debt = models.BigIntegerField(default=0)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    branch = models.ForeignKey('Branch', on_delete=models.CASCADE, related_name="pupil_branch")
    date_joined = models.DateField(auto_now_add=True)
    updated_at = models.DateField(null=True, blank=True, auto_now=True)
    status = models.BigIntegerField(
        choices=(
            (1, "Qabul qilindi"),
            (2, "O'qimoqda"),
            (3, "Tark etgan"),
        )
    )

    # def __str__(self) -> str:
    #     return self.name


class Payment_A(models.Model):
    money = models.BigIntegerField()
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    date_joined = models.DateField(auto_now=True)
    pupil = models.ForeignKey(Pupil, on_delete=models.CASCADE)
    reception = models.ForeignKey(User, on_delete=models.CASCADE)
    type = models.IntegerField(
        choices=(
            (1, 'Cash'),
            (2, 'Card'),
        )
    )


class Payment_B(models.Model):
    money = models.BigIntegerField()
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)


class Lesson(models.Model):
    topic = models.CharField(max_length=255)
    time = models.DateField()
    pupil = models.ForeignKey(Pupil, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    status = models.BooleanField()
    checked = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.topic



class Parents(models.Model):
    name = models.CharField(max_length=255)
    child1 = models.ForeignKey(Pupil, on_delete=models.CASCADE, related_name='child1')
    child2 = models.ForeignKey(Pupil, on_delete=models.CASCADE, related_name='child2', blank=True, null=True)
    child3 = models.ForeignKey(Pupil, on_delete=models.CASCADE, related_name='child3', blank=True, null=True)
    tg_id = models.BigIntegerField()

    def __str__(self) -> str:
        return self.name


class Reason(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class BlockList(models.Model):
    pupil = models.ForeignKey(Pupil, on_delete=models.CASCADE)
    date = models.DateField(auto_now=True)
    reason = models.ForeignKey(Reason, on_delete=models.CASCADE)


class Branch(models.Model):
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=255)
    location = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.name


class Task(models.Model):
    title = models.CharField(max_length=255)
    status = models.BooleanField(default=False)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)


class Task_Result(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    video = models.FileField()
    comment = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.comment


class Notification(models.Model):
    pupil = models.ForeignKey(Pupil, on_delete=models.CASCADE)
    text = models.CharField(max_length=255)
    date = models.DateField()
    status = models.BooleanField(default=False)


class Outgoing(models.Model):
    title = models.CharField(max_length=255)
    amount = models.IntegerField()
    person = models.CharField(max_length=255)
    date = models.DateTimeField(auto_now_add=True)


class Pupil_Copy(models.Model):
    pupil = models.ForeignKey(Pupil, on_delete=models.CASCADE)