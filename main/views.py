from django.shortcuts import render
from .models import *
from django.shortcuts import redirect
from datetime import datetime, timedelta
import requests
from django.contrib.auth import login, authenticate
from calendar import monthrange
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password
from django.http import HttpResponse

# Create your views here.

def LogOut(request):
    logout(request)
    return redirect('login')

def Login_Auth(request):
    print(True)
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            if user.type == 1:
                return redirect('hisobot')
            elif user.type == 2:
                return redirect('pupils_all')
            elif user.type == 3:
                return redirect('groups')
            elif user.type == 4:
                return redirect('hisobot')
        else:
            return redirect('login')



def Login(request):
    if request.user.is_authenticated and request.user.type == 1:
        return redirect('hisobot')
    elif request.user.is_authenticated and request.user.type == 2:
        return redirect('pupils_all')
    elif request.user.is_authenticated and request.user.type == 3:
        return redirect('groups')
    elif request.user.is_authenticated and request.user.type == 4:
        return redirect('hisobot')
    else:
        return render(request, 'login-2.html')



def Index(request):
    phone = 555009010
    location = "Andijan Boburshoh ko'chasi"
    name = "CHINAR"
    if request.user.is_authenticated:
        if request.user.type == 1 or request.user.type == 4:
            payments = Payment_A.objects.all().count()
            pupils = Pupil.objects.all().count()
            teachers = Teacher.objects.all().count()

            payments_today = Payment_A.objects.filter(date_joined=datetime.today()).count()
            pupils_today = Pupil.objects.filter(date_joined=datetime.today()).count()

            pupils_educating = Pupil.objects.filter(status=2).count()
            group = Group.objects.all().count()
            parents = Parents.objects.all().count()

            all_outgoings = Outgoing.objects.all()
            outgoing_balance = 0
            for i in all_outgoings:
                outgoing_balance += i.amount
            outgoing_balance = f"{outgoing_balance:,}"
            

            all_payments = Payment_A.objects.all()
            total_balance = 0
            for i in all_payments:
                total_balance += i.money
            total_balance = f"{total_balance:,}"

            # top_students = Pupil.objects.filter(date_joined=min(date_joined))
            arr = []
            arr2 = []
            for i in Pupil.objects.filter(status=2):
                arr.append(i.date_joined)

            for i in Payment_A.objects.all():
                arr2.append(i.date_joined)

            top_payments = Payment_A.objects.filter(date_joined=arr2[0])
            arr3 = []
            for i in top_payments:
                for i2 in Pupil.objects.all():
                    if i2.id == i.id and i2.status == 2 :
                        arr3.append(i2)
            top_student = Pupil.objects.filter(date_joined=arr[0], status=2)

            balance__payment = 0
            for s in top_student:
                payment = Payment_A.objects.filter(pupil=s)
                for i in payment:
                    balance__payment += i.money

            debtors = []
            payment = Payment_A.objects.all()
            pupil = Pupil.objects.all()
            for i in pupil:
                debtors.append(i)
                for p in payment:
                    if i == p.pupil:
                        if i in debtors:
                            debtors.remove(i)
            debtor_count = 0
            debtors_total_money = 0
            for i in debtors:
                debtor_count += 1
                debtors_total_money += i.group.money

            leaved_students = Pupil.objects.filter(status=3).count()

            # for i in Payment_A.objects.all()
            waiting_students = Pupil.objects.filter(status=1).count()

            todays_number = datetime.today().day
            today = datetime.today()
            yesterday = today - timedelta(days=1)
            before_yesterday = today - timedelta(days=2)
            three_days_ago = today - timedelta(days=3)
            four_days_ago = today - timedelta(days=4)
            five_days_ago = today - timedelta(days=5)
            six_days_ago = today - timedelta(days=6)


            daily_payments_numbers = Payment_A.objects.filter(date_joined=today).count()
            yesterday_payments_numbers = Payment_A.objects.filter(date_joined=yesterday).count()
            before_yesterday_payments_numbers = Payment_A.objects.filter(date_joined=before_yesterday).count()
            three_days_ago_payments_numbers = Payment_A.objects.filter(date_joined=three_days_ago).count()
            four_days_ago_payments_numbers = Payment_A.objects.filter(date_joined=four_days_ago).count()
            five_days_ago_payments_numbers = Payment_A.objects.filter(date_joined=five_days_ago).count()
            six_days_ago_payments_numbers = Payment_A.objects.filter(date_joined=six_days_ago).count()


            today_weekday_num = datetime.today().weekday()
            today_weekday = ''
            if today_weekday_num == 0:
                today_weekday = 'Du'
            elif today_weekday_num == 1:
                today_weekday = 'Se'
            elif today_weekday_num == 2:
                today_weekday = 'Chor'
            elif today_weekday_num == 3:
                today_weekday = 'Pa'
            elif today_weekday_num == 4:
                today_weekday = 'Ju'
            elif today_weekday_num == 5:
                today_weekday = 'Sha'
            elif today_weekday_num == 6:
                today_weekday = 'Yak'
            print(today_weekday)


            yesterday_weekday_num = yesterday.weekday()
            yesterday_weekday = ''
            if yesterday_weekday_num == 0:
                yesterday_weekday = 'Du'
            elif yesterday_weekday_num == 1:
                yesterday_weekday = 'Se'
            elif yesterday_weekday_num == 2:
                yesterday_weekday = 'Chor'
            elif yesterday_weekday_num == 3:
                yesterday_weekday = 'Pa'
            elif yesterday_weekday_num == 4:
                yesterday_weekday = 'Ju'
            elif yesterday_weekday_num == 5:
                yesterday_weekday = 'Sha'
            elif yesterday_weekday_num == 6:
                yesterday_weekday = 'Yak'
            print(yesterday_weekday)



            before_yesterday_weekday_num = before_yesterday.weekday()
            before_yesterday_weekday = ''
            if before_yesterday_weekday_num == 0:
                before_yesterday_weekday = 'Du'
            elif before_yesterday_weekday_num == 1:
                before_yesterday_weekday = 'Se'
            elif before_yesterday_weekday_num == 2:
                before_yesterday_weekday = 'Chor'
            elif before_yesterday_weekday_num == 3:
                before_yesterday_weekday = 'Pa'
            elif before_yesterday_weekday_num == 4:
                before_yesterday_weekday = 'Ju'
            elif before_yesterday_weekday_num == 5:
                before_yesterday_weekday = 'Sha'
            elif before_yesterday_weekday_num == 6:
                before_yesterday_weekday = 'Yak'
            print(before_yesterday_weekday)


            three_days_ago_weekday_num = three_days_ago.weekday()
            three_days_ago_weekday = ''
            if three_days_ago_weekday_num == 0:
                three_days_ago_weekday = 'Du'
            elif three_days_ago_weekday_num == 1:
                three_days_ago_weekday = 'Se'
            elif three_days_ago_weekday_num == 2:
                three_days_ago_weekday = 'Chor'
            elif three_days_ago_weekday_num == 3:
                three_days_ago_weekday = 'Pa'
            elif three_days_ago_weekday_num == 4:
                three_days_ago_weekday = 'Ju'
            elif three_days_ago_weekday_num == 5:
                three_days_ago_weekday = 'Sha'
            elif three_days_ago_weekday_num == 6:
                three_days_ago_weekday = 'Yak'
            print(three_days_ago_weekday)


            four_days_ago_weekday_num = four_days_ago.weekday()
            four_days_ago_weekday = ''
            if four_days_ago_weekday_num == 0:
                four_days_ago_weekday = 'Du'
            elif four_days_ago_weekday_num == 1:
                four_days_ago_weekday = 'Se'
            elif four_days_ago_weekday_num == 2:
                four_days_ago_weekday = 'Chor'
            elif four_days_ago_weekday_num == 3:
                four_days_ago_weekday = 'Pa'
            elif four_days_ago_weekday_num == 4:
                four_days_ago_weekday = 'Ju'
            elif four_days_ago_weekday_num == 5:
                four_days_ago_weekday = 'Sha'
            elif four_days_ago_weekday_num == 6:
                four_days_ago_weekday = 'Yak'
            print(four_days_ago_weekday)


            five_days_ago_weekday_num = five_days_ago.weekday()
            five_days_ago_weekday = ''
            if five_days_ago_weekday_num == 0:
                five_days_ago_weekday = 'Du'
            elif five_days_ago_weekday_num == 1:
                five_days_ago_weekday = 'Se'
            elif five_days_ago_weekday_num == 2:
                five_days_ago_weekday = 'Chor'
            elif five_days_ago_weekday_num == 3:
                five_days_ago_weekday = 'Pa'
            elif five_days_ago_weekday_num == 4:
                five_days_ago_weekday = 'Ju'
            elif five_days_ago_weekday_num == 5:
                five_days_ago_weekday = 'Sha'
            elif five_days_ago_weekday_num == 6:
                five_days_ago_weekday = 'Yak'
            print(five_days_ago_weekday)



            six_days_ago_weekday_num = six_days_ago.weekday()
            six_days_ago_weekday = ''
            if six_days_ago_weekday_num == 0:
                six_days_ago_weekday = 'Du'
            elif six_days_ago_weekday_num == 1:
                six_days_ago_weekday = 'Se'
            elif six_days_ago_weekday_num == 2:
                six_days_ago_weekday = 'Chor'
            elif six_days_ago_weekday_num == 3:
                six_days_ago_weekday = 'Pa'
            elif six_days_ago_weekday_num == 4:
                six_days_ago_weekday = 'Ju'
            elif six_days_ago_weekday_num == 5:
                six_days_ago_weekday = 'Sha'
            elif six_days_ago_weekday_num == 6:
                six_days_ago_weekday = 'Yak'
            print(six_days_ago_weekday)


            # Barchart informations

            pupils_yesterday_accepted = Pupil.objects.filter(date_joined=yesterday, status=1).count()
            pupils_today_accepted = Pupil.objects.filter(date_joined=today, status=1).count()


            lessons_yesterday = Lesson.objects.filter(time=yesterday, status=True).count()
            lessons_today = Lesson.objects.filter(time=today, status=True).count()


            daily_pupils_numbers = Pupil_Copy.objects.filter(pupil__date_joined=today, pupil__status=1).count()
            yesterday_pupils_numbers = Pupil_Copy.objects.filter(pupil__date_joined=yesterday, pupil__status=1).count()
            before_yesterday_pupils_numbers = Pupil_Copy.objects.filter(pupil__date_joined=before_yesterday, pupil__status=1).count()
            three_days_ago_pupils_numbers = Pupil_Copy.objects.filter(pupil__date_joined=three_days_ago, pupil__status=1).count()
            four_days_ago_pupils_numbers = Pupil_Copy.objects.filter(pupil__date_joined=four_days_ago, pupil__status=1).count()
            five_days_ago_pupils_numbers = Pupil_Copy.objects.filter(pupil__date_joined=five_days_ago, pupil__status=1).count()
            six_days_ago_pupils_numbers = Pupil_Copy.objects.filter(pupil__date_joined=six_days_ago, pupil__status=1).count()

            
            weekly_pupils_numbers = daily_pupils_numbers + yesterday_pupils_numbers + before_yesterday_pupils_numbers + three_days_ago_pupils_numbers + four_days_ago_pupils_numbers + five_days_ago_pupils_numbers + six_days_ago_pupils_numbers


            weekly_pupils = []
            daily_pupils = Pupil_Copy.objects.filter(pupil__date_joined=today, pupil__status=1)
            yesterday_pupils = Pupil_Copy.objects.filter(pupil__date_joined=yesterday, pupil__status=1)
            before_yesterday_pupils = Pupil_Copy.objects.filter(pupil__date_joined=before_yesterday, pupil__status=1)
            three_days_ago_pupils = Pupil_Copy.objects.filter(pupil__date_joined=three_days_ago, pupil__status=1)
            four_days_ago_pupils = Pupil_Copy.objects.filter(pupil__date_joined=four_days_ago, pupil__status=1)
            five_days_ago_pupils = Pupil_Copy.objects.filter(pupil__date_joined=five_days_ago, pupil__status=1)
            six_days_ago_pupils = Pupil_Copy.objects.filter(pupil__date_joined=six_days_ago, pupil__status=1)
            print(type(daily_pupils))

            weekly_pupils.append(daily_pupils)
            weekly_pupils.append(yesterday_pupils)
            weekly_pupils.append(before_yesterday_pupils)
            weekly_pupils.append(three_days_ago_pupils)
            weekly_pupils.append(four_days_ago_pupils)
            weekly_pupils.append(five_days_ago_pupils)
            weekly_pupils.append(six_days_ago_pupils)



            # weekly_pupils_added = []
            # daily_pupils = Pupil_Copy.objects.filter(pupil__date_joined=today, pupil__status=2)
            # yesterday_pupils = Pupil_Copy.objects.filter(pupil__date_joined=yesterday, pupil__status=2)
            # before_yesterday_pupils = Pupil_Copy.objects.filter(pupil__date_joined=before_yesterday, pupil__status=2)
            # three_days_ago_pupils = Pupil_Copy.objects.filter(pupil__date_joined=three_days_ago, pupil__status=2)
            # four_days_ago_pupils = Pupil_Copy.objects.filter(pupil__date_joined=four_days_ago, pupil__status=2)
            # five_days_ago_pupils = Pupil_Copy.objects.filter(pupil__date_joined=five_days_ago, pupil__status=2)
            # six_days_ago_pupils = Pupil_Copy.objects.filter(pupil__date_joined=six_days_ago, pupil__status=2)

            # weekly_pupils_added.append(daily_pupils)
            # weekly_pupils_added.append(yesterday_pupils)
            # weekly_pupils_added.append(before_yesterday_pupils)
            # weekly_pupils_added.append(three_days_ago_pupils)
            # weekly_pupils_added.append(four_days_ago_pupils)
            # weekly_pupils_added.append(five_days_ago_pupils)
            # weekly_pupils_added.append(six_days_ago_pupils)


            # lessons_todayy = Lesson.objects.filter(time=today, status=True)
            # lessons_yesterdayy = Lesson.objects.filter(time=yesterday, status=True)
            # lessons_before_yesterday = Lesson.objects.filter(time=before_yesterday, status=True)
            # lessons_three_days_ago = Lesson.objects.filter(time=three_days_ago, status=True)
            # lessons_four_days_ago = Lesson.objects.filter(time=four_days_ago, status=True)
            # lessons_five_days_ago = Lesson.objects.filter(time=five_days_ago, status=True)
            # lessons_six_days_ago = Lesson.objects.filter(time=six_days_ago, status=True)


            # lessons_weekly = []

            # lessons_weekly.append(lessons_todayy)
            # lessons_weekly.append(lessons_yesterdayy)
            # lessons_weekly.append(lessons_before_yesterday)
            # lessons_weekly.append(lessons_three_days_ago)
            # lessons_weekly.append(lessons_four_days_ago)
            # lessons_weekly.append(lessons_five_days_ago)
            # lessons_weekly.append(lessons_six_days_ago)
            # print(lessons_weekly)
            # weekly_added_pupils = 0
            # for i in lessons_weekly:
            #     for p in weekly_pupils_added:
            #         for p2 in p:
            #             p2__pupil = p2.pupil
            #             if i.pupil == p2__pupil:
            #                 weekly_added_pupils += 1


            weekly_pupils2 = Pupil.objects.filter(date_joined__gte=six_days_ago, date_joined__lte=today, status=2)


            weekly_pupils3 = Pupil.objects.filter(date_joined__lte=today, status=3)




            weekly_payments = Payment_A.objects.filter(date_joined__gte=six_days_ago, date_joined__lte=today)
            total_payments = Payment_A.objects.all()
            pupils_paid_all = []
            for i in total_payments:
                pupils_paid_all.append(i.pupil)



            for i in weekly_payments:
                pupil = i.pupil
                for i2 in total_payments:
                    if pupil == i2.pupil and pupil in pupils_paid_all:
                        print(True)
                        pupils_paid_all.remove(pupil)



            context = {
                'payments': payments,
                'pupils': pupils,
                'teachers': teachers,
                'payments_today': payments_today,
                'pupils_today': pupils_today,
                'pupils_educating': pupils_educating,
                'group': group,
                'parents': parents,
                'total_balance':total_balance,
                'top_student': arr3,
                'balance__payment':balance__payment,
                'outgoing_balance':outgoing_balance,
                'debtors_count': debtor_count,
                'leaved_students': leaved_students,
                'branch': Branch.objects.all(),
                'debtors_total_money': debtors_total_money,
                'waiting_students': waiting_students,
                'daily_payments_numbers': daily_payments_numbers,
                'yesterday_payments_numbers': yesterday_payments_numbers,
                'before_yesterday_payments_numbers': before_yesterday_payments_numbers,
                'three_days_ago_payments_numbers': three_days_ago_payments_numbers,
                'four_days_ago_payments_numbers': four_days_ago_payments_numbers,
                'five_days_ago_payments_numbers': five_days_ago_payments_numbers,
                'six_days_ago_payments_numbers': six_days_ago_payments_numbers,
                'today_weekday':today_weekday,
                'yesterday_weekday':yesterday_weekday,
                'before_yesterday_weekday':before_yesterday_weekday,
                'three_days_ago_weekday':three_days_ago_weekday,
                'four_days_ago_weekday':four_days_ago_weekday,
                'five_days_ago_weekday':five_days_ago_weekday,
                'six_days_ago_weekday':six_days_ago_weekday,
                'pupils_yesterday_accepted':pupils_yesterday_accepted,
                'pupils_today_accepted':pupils_today_accepted,
                'lessons_yesterday':lessons_yesterday,
                'lessons_today':lessons_today,
                'weekly_pupils_numbers':weekly_pupils_numbers,
                'weekly_pupils2': len(weekly_pupils2),
                'weekly_pupils3': len(weekly_pupils3),
                'pupils_paid_all': len(pupils_paid_all),
            }


            # Top pupils are here
            return render(request, 'index.html', context)
        else:
            return redirect('pupils_all')




def Parents_function(request):
    parents = Parents.objects.all()
    context = {
        'parents': parents
    }
    return render(request, 'parents.html', context)



def Pupils_All(request):
    if request.user.is_authenticated:
        if request.user.type == 2:
            teacher = Teacher.objects.get(user=request.user)
            pupil = Pupil.objects.filter(teacher=teacher)
            teacher = Teacher.objects.all()
            group = Group.objects.all()
            branch = Branch.objects.all()
            context = {
                'pupil': pupil,
                'teacher': teacher,
                'group': group,
                'branch': branch,
            }
            return render(request, 'pupils.html', context)
        else:
            pupil = Pupil.objects.all()
            teacher = Teacher.objects.all()
            group = Group.objects.all()
            branch = Branch.objects.all()
            context = {
                'branch': branch,
                'pupil': pupil,
                'teacher': teacher,
                'group': group,
                'branch': branch,
            }
            return render(request, 'pupils.html', context)
    else:
        return redirect('login')



def Payment_Pupil(request, pk):
    pupil = Pupil.objects.get(id=pk)
    money = request.POST['money']
    reception = request.user
    type = request.POST['type']
    Payment_A.objects.create(
        money=money, group=pupil.group, pupil=pupil, reception=reception, type=type
    )

    pupil.debt -= int(money)
    pupil.save()
    id = Parents.objects.all()
    for i in id:
        if i.child1 == pupil or i.child2 == pupil or i.child3 == pupil:
            token = '5705886511:AAHCO9ZSSE6h_I2xYjMdxP515-z___ttc00'
            if pupil.debt > 0 or pupil.debt == 0:
                text = "Assalomu Aleykum" + i.name + "\nTo'lov qilindi!\nGuruh:" + pupil.group.name + 'Fan:\n' + pupil.group.subject.name + 'Sana:\n' + str(datetime.now()) + "O'quvchi\n" + pupil.name + "Qarzdorlik\n" + str(pupil.debt)
                url = 'https://api.telegram.org/bot' + token + '/sendMessage?chat_id='
                requests.get(url + str(i.tg_id) + '&text=' + text)
            else:
                text = "Assalomu Aleykum" + i.name + "\nTo'lov qilindi!\nGuruh:" + pupil.group.name + '\nFan:' + pupil.group.subject.name + '\nSana:' + str(datetime.now()) + "\nO'quvchi:" + pupil.name + "\nBalans:" + str(pupil.debt * -1)
                url = 'https://api.telegram.org/bot' + token + '/sendMessage?chat_id='
                requests.get(url + str(i.tg_id) + '&text=' + text)

    return redirect('payments-history', pk=pk)

def Payments_History(request, pk):
    pupil = Pupil.objects.get(id=pk)
    payment = Payment_A.objects.filter(pupil=pupil).order_by('-id')
    context = {
        'payment': payment,
        'pupil': pupil,
    }

    return render(request, 'payments.html', context)


def Payments_All(request):
    payment = Payment_A.objects.all().order_by('-id')
    context = {
        'payment': payment
    }
    return render(request, 'payments_all.html', context)

def Delete_Pupil(request, pk):
    pupil = Pupil.objects.get(id=pk)
    pupil.delete()

    return redirect('pupils_all')

def Delete_Parents(request, pk):
    parents = Parents.objects.get(id=pk)
    parents.delete()

    return redirect('parents')

def Delete_teachers(request, pk):
    teachers = Teacher.objects.get(id=pk)
    teachers.delete()

    return redirect('teachers')

def Delete_groups(request, pk):
    groups = Group.objects.get(id=pk)
    groups.delete()

    return redirect('groups')

def Delete_worker(request, pk):
    worker = User.objects.get(id=pk)
    worker.delete()
    
    return redirect('workers')

def Search_Pupil(request):
    name = request.POST['pupil']
    pupil = Pupil.objects.filter(name__icontains=name)
    context = {
        'pupil': pupil
    }
    return render(request, 'pupils_search.html', context)

def Search_Worker(request):
    if request.method == 'POST':
        first_name = request.POST["worker"]
        worker = User.objects.filter(username__icontains=first_name)
        context = {
            'worker': worker,
        }
        return render(request, 'workers_search.html', context)

def Search_Teacher(request):
    name = request.POST['teacher']
    teacher = Teacher.objects.filter(name__icontains=name)
    subject = Subject.objects.all()
    context = {
        'teacher': teacher,
        'subject': subject,
    }
    return render(request, 'teacher_search.html', context)

def Search_Group(request):
    name = request.POST['group']
    group = Group.objects.filter(name__icontains=name)
    level = Level.objects.all()
    context = {
        'group': group,
        'level': level,
    }
    return render(request, 'search_groups.html', context)

def Search_Payments(request):
    date = request.POST['date']
    money = request.POST['money']
    payment = Payment_A.objects.filter(money=money, date_joined=date)
    payment = Payment_A.objects.filter(date_joined=date, money=money)
    context = {
        'payment': payment,
    }
    return render(request, 'payments_all_search.html', context)

def Search_Parents(request):
    name = request.POST['name']
    parents = Parents.objects.filter(name__icontains=name)
    context = {
        'parents': parents
    }
    return render(request, 'parents_search.html', context)

def Teachers(request):
    if request.user.is_authenticated and request.user.type == 1 or request.user.type == 4:
        users = User.objects.filter(type=2)
        context = {
            'teachers': Teacher.objects.all(),
            'subject': Subject.objects.all(),
            'users': users,
        }
        return render(request, 'teachers.html', context)
    else:
        users = User.objects.filter(type=2)
        context = {
            'teachers': Teacher.objects.all(),
            'subject': Subject.objects.all(),
            'users': users,
        }
        return render(request, 'teachers.html', context)

def Groups(request):
    if request.user.is_authenticated:
        if request.user.type == 2:
            teacher = Teacher.objects.get(user=request.user)
            debtors = []
            payment = Payment_A.objects.all()
            pupil = Pupil.objects.all()
            for i in pupil:
                debtors.append(i)
                for p in payment:
                    if i == p.pupil:
                        if i in debtors:
                            debtors.remove(i)
            debtor_count = 0
            for i in debtors:
                debtor_count += 1
            teacher = Teacher.objects.all()
            context = {
                'groups': Group.objects.filter(teacher=teacher),
                'level': Level.objects.all(),
                'lesson_days': Lesson_Days.objects.all(),
                'debtors_count': debtor_count,
                'teacher': teacher,
                'subject': Subject.objects.all(),
            }
            return render(request, 'groups.html', context)
        else:
            teacher = Teacher.objects.get(user=request.user)
            debtors = []
            payment = Payment_A.objects.all()
            pupil = Pupil.objects.all()
            for i in pupil:
                debtors.append(i)
                for p in payment:
                    if i == p.pupil:
                        if i in debtors:
                            debtors.remove(i)
            debtor_count = 0
            for i in debtors:
                debtor_count += 1
            context = {
                'groups': Group.objects.all(),
                'level': Level.objects.all(),
                'lesson_days': Lesson_Days.objects.all(),
                'debtors_count': debtor_count,
                'teacher': Teacher.objects.all(),
                'subject': Subject.objects.all(),
            }
            return render(request, 'groups.html', context)
    else:
        return redirect('login')


def Edit_teachers(request):
    if request.method == "POST":
        id = request.POST.get('id')
        name = request.POST.get('name')
        money = request.POST.get('money')
        subject_name = request.POST.get('subject')
        subject = Subject.objects.get(name=subject_name)
        phone = request.POST.get('phone')
        extra_phone = request.POST.get('extra_phone')
        email = request.POST.get('email')
        location = request.POST.get('location')
        teacher = Teacher.objects.get(id=id)
        teacher.name = name
        teacher.money = money
        teacher.subject = subject
        teacher.phone = phone
        teacher.extra_phone = extra_phone
        teacher.email = email
        teacher.location = location
        teacher.save()
        return redirect('teachers')
    return redirect('teachers')

def Edit_Worker(request):
    if request.method == "POST":
        id = request.POST.get('id')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        password = request.POST.get('password')
        workers = User.objects.get(id=id)
        workers.id = id 
        workers.first_name = first_name
        workers.last_name = last_name
        workers.username = username
        workers.password = make_password(password)
        workers.save()
        return redirect('workers')
    return redirect('workers')

def Edit_Parents(request):
    if request.method == "POST":
        id = request.POST.get('id')
        name = request.POST.get('name')
        child1_name = request.POST.get('child1')
        child2_name = request.POST.get('child2')
        child3_name = request.POST.get('child3')
        print(child3_name)
        child1 = Pupil.objects.get(name=child1_name)
        parents = Parents.objects.get(id=id)
        if child2_name != '':
            child2 = Pupil.objects.get(name=child2_name)
            parents.child2 = child2
        else:
            parents.child2 = None
        if child3_name != '':
            child3 = Pupil.objects.get(name=child3_name)
            parents.child3 = child3
        else:
            parents.child3 = None
        tg_id = request.POST.get('tg_id')
        parents.name = name
        parents.tg_id = tg_id
        parents.child1 = child1
        parents.save()
        return redirect('parents')
    return redirect('parents')

def Edit_Groups(request):
    if request.method == "POST":
        id = request.POST.get('id')
        print(id)
        name = request.POST.get('name')
        level_name = request.POST.get('level')
        level = Level.objects.get(name=level_name)
        subject_name = request.POST.get('subject')
        subject = Subject.objects.get(name=subject_name)
        teacher_name = request.POST.get('teacher')
        teacher = Teacher.objects.get(name=teacher_name)
        money = request.POST.get('money')
        lesson_day1_id = request.POST.get('lesson_day1')
        lesson_day2_id = request.POST.get('lesson_day2')
        lesson_day3_id = request.POST.get('lesson_day3')
        lesson_day1 = Lesson_Days.objects.get(id=lesson_day1_id)
        lesson_day2 = Lesson_Days.objects.get(id=lesson_day2_id)
        lesson_day3 = Lesson_Days.objects.get(id=lesson_day3_id)
        groupss = Group.objects.get(id=id)
        lesson_days_all = Lesson_Days.objects.all()
        for i in lesson_days_all:
            groupss.lesson_days.remove(i)
        groupss.lesson_days.add(lesson_day1, lesson_day2, lesson_day3)
        groupss.name = name
        groupss.level = level
        groupss.subject = subject
        groupss.teacher = teacher
        groupss.money = money
        return redirect('groups')
    return redirect('groups')


def Filter_Pupil(request):
    if request.method == 'POST':
        level = request.POST.get('level')
        # teacher_id = request.POST.get('teacher')
        # teacher = Teacher.objects.get(id=teacher_id)
        # group = Group.objects.filter(teacher=teacher)
        pupil = Pupil.objects.filter(level=level)
        context = {
            'pupil': pupil
        }
    return render(request, 'filter_pupil.html', context)

def Filter_groups(request):
    if request.method == 'POST':
        level__id = request.POST.get('level')
        level = Level.objects.get(id=level__id)
        group = Group.objects.filter(level=level)
        context = {
            'group': group,
            'level': Level.objects.all(),
            'lesson_days': Lesson_Days.objects.all(),
            'teacher': Teacher.objects.all(),
            'subject': Subject.objects.all(),
        }
    return render(request, 'groups_filter.html', context)

def Filter_Teacher(request):
    if request.method == 'POST':
        subject__id = request.POST.get('subject')
        subject = Subject.objects.get(id=subject__id)
        teacher = Teacher.objects.filter(subject=subject)
        context = {
            'teacher': teacher,
            'subject': Subject.objects.all()
        }
    return render(request, 'filter_teachers.html', context)
    
def Edit_Pupil(request):
    if request.method == 'POST':
        id = request.POST.get('id')
        name = request.POST.get('name')
        level = request.POST.get('level')
        phone = request.POST.get('phone')
        extra_phone = request.POST.get('extra_phone')
        group_id = request.POST.get('group')
        status = request.POST.get('status')
        group = Group.objects.get(name=group_id)
        pupil = Pupil.objects.get(id=id)
        pupil.name = name
        pupil.level = level
        pupil.phone = phone
        pupil.extra_phone = extra_phone
        pupil.group = group
        pupil.status = status
        pupil.updated_at = datetime.today()
        pupil.save()
        return redirect('pupils_all')


def Add_Pupil(request):
    name = request.POST['name']
    level = request.POST['level']
    phone = request.POST['phone']
    extra_phone = request.POST['extra_phone']
    group = request.POST['group']
    status = request.POST['status']
    branch_id = request.POST['branch']
    teacher_id = request.POST['teacher']
    teacher = Teacher.objects.get(id=teacher_id)
    branch = Branch.objects.get(id=branch_id)
    group = Group.objects.get(name=group)
    pupil = Pupil.objects.create(
        name=name, level=level, phone=phone, extra_phone=extra_phone, group=group, status=status, branch=branch, teacher=teacher
    )
    Pupil_Copy.objects.create(pupil=pupil)
    return redirect('pupils_all')

def Add_teacher(request):
    name = request.POST['name']
    # money = request.POST['money']
    subject_name = request.POST['subject']
    subject = Subject.objects.get(name=subject_name)
    phone = request.POST['phone']
    # extra_phone = request.POST['extra_phone']
    # email = request.POST['email']
    location = request.POST['location']
    user = request.user
    percent = request.POST['percent']
    Teacher.objects.create(name=name, subject=subject, phone=phone, location=location, user=user, percent=percent)
    return redirect('teachers')

def Add_Parents(request):
    name = request.POST['name']
    child1_name = request.POST['child1']
    child1 = Pupil.objects.get(name=child1_name)
    tg_id = request.POST['tg_id']
    Parents.objects.create(name=name, child1=child1, tg_id=tg_id)
    return redirect('parents')

def Add_groups(request):
    name = request.POST['name']
    level_name = request.POST['level']
    level = Level.objects.get(name=level_name)
    subject_name = request.POST['subject']
    subject = Subject.objects.get(name=subject_name)
    teacher_id = request.POST['teacher']
    teacher = Teacher.objects.get(id=teacher_id)
    money = request.POST['money']
    list = []
    lesson_days = request.POST.get('lesson_days')
    print(type(lesson_days))
    if lesson_days == '1':
        lessonday1 = Lesson_Days.objects.get(dayuz="Du")
        lessonday2 = Lesson_Days.objects.get(dayuz="Chor")
        lessonday3 = Lesson_Days.objects.get(dayuz="Ju")
        room = request.POST['room']
        max_pupil = request.POST['max_pupil']
        time_start = request.POST['time_start']
        time_end = request.POST['time_end']
        group = Group.objects.create(name=name, level=level, subject=subject, teacher=teacher, money=money,
        room=room, max_pupil=max_pupil, time_start=time_start, time_end=time_end)
        group.lesson_days.add(lessonday1, lessonday2, lessonday3)
    elif lesson_days == '2':
        lessonday1 = Lesson_Days.objects.get(dayuz="Se")
        lessonday2 = Lesson_Days.objects.get(dayuz="Pa")
        lessonday3 = Lesson_Days.objects.get(dayuz="Sha")
        room = request.POST['room']
        max_pupil = request.POST['max_pupil']
        time_start = request.POST['time_start']
        time_end = request.POST['time_end']
        group = Group.objects.create(name=name, level=level, subject=subject, teacher=teacher, money=money,
        room=room, max_pupil=max_pupil, time_start=time_start, time_end=time_end)
        group.lesson_days.add(lessonday1, lessonday2, lessonday3)
    return redirect('groups')


def Add_Notification(request, pk):
    print(pk)
    if request.method == 'POST':
        pupil = Pupil.objects.get(id=pk)
        text = request.POST.get('text')
        date = request.POST.get('date')
        Notification.objects.create(
            pupil=pupil, text=text, date=date
        )
    return redirect('pupils_all')


def Send_Notification(request):
    pupil = Pupil.objects.all()
    notification = Notification.objects.filter(date=datetime.today())

    for p in pupil:
        for n in notification:
            # print(n.pupil)
            # print(True)
            # print(pupil)
            print(n.pupil == p)
            if n.pupil == p:
                id = 5643782731
                token = '5705886511:AAHCO9ZSSE6h_I2xYjMdxP515-z___ttc00'

                text = str(n.id) + ' raqamli eslatma' + "\nMatni: " + str(n.text) + "\nO'quvchi: " + p.name + '\nTel raqam ' + str(p.phone) + '\nGuruh: ' + str(p.group.name) + ' ' + str(p.group.level) + ' ' + str(p.group.time_start) + "dan" + str(p.group.time_end) + "gacha" + '\nXona: ' + str(p.group.room)

                url = 'https://api.telegram.org/bot' + token + '/sendMessage?chat_id='
                requests.get(url + str(id) + '&text=' + text)
                print('Muvaffaqiyatli')

    # if notification.pupil == pupil:
    #     print(True)
    #     id = 1645479025
    #     token = '5767824521:AAEjLYdEWI1jieTVgN8YSOPDTiquV0tkQSc'
    #     text = notification.text
    #     url = 'https://api.telegram.org/bot' + token + '/sendMessage?chat_id='  
    #     requests.get(url + str(id) + '&text' + text)
    return redirect('pupils_all')


def Check_Payments_Monthly(request):
    pupils = Pupil.objects.all()
    today = datetime.today()
    res = today.replace(day=1)
    if today == res:
        for p in pupils:
            group = Group.objects.get(pupil=p)
            p.debt = int(group.money)
            p.save()
            print(group.money)
    return redirect('pupils_all')


def Pay_Sallary(request, pk):
    if request.method == 'POST':
        teacher = Teacher.objects.get(id=pk)
        group__id = request.POST['group']
        group = Group.objects.get(id=group__id)
        pupil = Pupil.objects.filter(group=group)
        percent = request.POST['percent']
        money = 0
        money += group.money * len(pupil)
        teacher_money = (int(percent) * int(money)) / 100
        Payment_B.objects.create(
            money=teacher_money,
            group=group,
            teacher=teacher
        )
    return redirect('all-salleries')

def All_Parents(request):
    parents = Parents.objects.all()
    context = {
        'parents': parents
    }
    return render(request, 'parents.html', context)

def All_Salleries(request):
    context = {
        'sallery': Payment_B.objects.all()
    }
    return render(request, 'sallery.html', context)

def Send_Message_Parent(request, pk):
    parent = Parents.objects.get(id=pk)
    message = request.POST.get('message')
    tg_id = parent.tg_id
    token = '5705886511:AAHCO9ZSSE6h_I2xYjMdxP515-z___ttc00'
    text = "Assalomu Aleykum " + parent.name + "\n" + message
    url = 'https://api.telegram.org/bot' + token + '/sendMessage?chat_id='
    requests.get(url + str(tg_id) + '&text=' + text)
    return redirect('parents')

def TimeTables(request):
    group = Group.objects.all().order_by('-id')
    pupils_number = []
    pupil = Pupil.objects.all()
    for p in pupil:
        for g in group:
            print(True)
    context = {
        'group': group,
    }
    return render(request, 'time_tables.html', context)


def All_Tasks(request):
    tasks = Task.objects.all()
    context = {
        'tasks': tasks,
    }
    return render(request, 'tasks.html', context)

def Get_Task_Result(request, pk):
    task = Task.objects.get(id=pk)
    task_result = Task_Result.objects.get(task=task)
    context = {
        'task_result': task_result,
    }
    return render(request, 'task_result.html', context)

def Accept_Task(request):
    pk = request.POST.get('pk')
    task = Task.objects.get(id=pk)
    task.status = True
    task.save()
    return redirect('tasks_all')

def Cancel_Task(request):
    pk = request.POST.get('pk')
    task = Task.objects.get(id=pk)
    task.status = False
    task.save()
    return redirect('task_all')


def Add_Task(request):
    title = request.POST.get('title')
    branch_id = request.POST.get('branch')
    branch = Branch.objects.get(id=branch_id)
    Task.objects.create(title=title, branch=branch)
    return redirect('tasks_all')


def Get_Pupil(request, pk):
    pupil = Pupil.objects.get(id=pk)
    
# All tests are here





def All_Tasks(request):
    tasks = Task.objects.all()
    context = {
        'tasks': tasks,
    }
    return render(request, 'tasks.html', context)

def Debtors(request):
    pupil = Pupil.objects.all()
    payment = Payment_A.objects.all()
    debtors = []

    for i in pupil:
        debtors.append(i)
        for p in payment:
            if i == p.pupil:
                if i in debtors:
                    debtors.remove(i)
    context = {
        'debtors': debtors
    }
    return render(request, 'debtors.html', context)


def Attendance(request, pk):
    lesson = Lesson.objects.filter(time=datetime.today())
    pupils1 = []
    for i in lesson:
        pupils1.append(i.pupil)
    print(pupils1)
    
    
    group = Group.objects.get(id=pk)
    a = datetime.today().month
    b = datetime.today().year
    days =  monthrange(b,a)[1]
    today = datetime.today()
    context = {
        'group': group,
        'pupil': pupils1,
        'days': days,
        'today': today,
        'lesson':lesson,
    }
    return render(request, 'attendance.html', context)


def Davomat(request, pk):
    pupil = Pupil.objects.get(id=pk)
    group = pupil.group
    lesson = Lesson.objects.get(pupil=pupil, group=group, time=datetime.today())
    lesson.status = True
    lesson.save()
    return redirect('attendance', pk=Pupil.objects.get(id=pk).group.id)


def Davomat_False(request, pk):
    pupil = Pupil.objects.get(id=pk)
    group = pupil.group
    lesson = Lesson.objects.get(pupil=pupil, group=group, time=datetime.today())
    lesson.status = False
    lesson.save()
    return redirect('attendance', pk=Pupil.objects.get(id=pk).group.id)


# def Davomat_False(request, pk):
#     pupil = Pupil.objects.get(id=pk)
#     pupil.status = False
#     pupil.save()
#     return redirect('attendance', pk=Pupil.objects.get(id=pk).group.id)


def All_Outgoings(request):
    outgoings = Outgoing.objects.all()
    context = {
        'outgoings': outgoings,
    }
    return render(request, 'outgoings.html', context)


def Send_All_Parents(request):
    message = request.POST['message']
    parent = Parents.objects.all()
    for i in parent:
        tg_id = i.tg_id
        token = '5705886511:AAHCO9ZSSE6h_I2xYjMdxP515-z___ttc00'
        text = "Assalomu Aleykum " + i.name + "\n" + message
        url = 'https://api.telegram.org/bot' + token + '/sendMessage?chat_id='
        requests.get(url + str(tg_id) + '&text=' + text)
    return redirect('parents')



def Attendance_Monthly(request, pk):
    group = Group.objects.get(id=pk)
    pupil = Pupil.objects.filter(group=group)
    lesson = Lesson.objects.filter(time__gte=datetime.today().replace(day=1), time__lte=datetime.today()).order_by('time')
    lessons = []
    pupils = []
    for p in pupil:
        for l in lesson:
            if l not in lessons:
                lessons.append(l)
            if p == l.pupil and p not in pupils:
                pupils.append(p)
    lesson_days = []
    for i in lessons:
        if i.time.day not in lesson_days:
            lesson_days.append(i.time.day)
    context = {
        'group': group,
        'pupils': pupils,
        'lessons': lessons,
        'lesson_days':lesson_days,
    }
    return render(request, 'attendance_monthly.html', context)



def Waiting_Pupils(request):
    waiting_students = Pupil.objects.filter(status=1)
    branch = Branch.objects.all()
    context = {
        'pupil': waiting_students,
    }
    return render(request, 'waiting_pupils.html', context)


def Workers(request):
    context = {
        'workers': User.objects.all()
    }
    return render(request, 'workers.html', context)

def Add_Worker(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        password1 = request.POST['password']
        password = make_password(password1)
        type = request.POST['type']
        User.objects.create(
            first_name=first_name, last_name=last_name, username=username, password=password, type=type
        )
        return redirect('workers')


def Check_Missed_Lesson(request, pk):
    pupil = Pupil.objects.get(id=pk)
    lesson = Lesson.objects.filter(time__gte=datetime.today().replace(day=1), time__lte=datetime.today(), status=False, pupil=pupil).count()
    context = {
        'pupil': pupil,
        'lessons':lesson,
    }
    return render(request, 'missed.html', context)


def Work_Plan(request, pk):
    group = Group.objects.get(id=pk)
    teacher = group.teacher
    lesson = Lesson.objects.filter(group=group).order_by('time')
    lessons = []
    lesson_topics = []
    for i in lesson:
        if i.topic not in lesson_topics:
            lessons.append(i)
            lesson_topics.append(i.topic)
    context = {
        'lesson':lessons,
        'teacher': teacher,
        'group':group,
    }
    return render(request, 'workplan.html', context)


def Add_Workplan(request):
    if request.method == 'POST':
        id = request.POST.get('group')
        group = Group.objects.get(id=id)
        topic = request.POST.get('topic')
        time = request.POST.get('time')
        pupil = Pupil.objects.filter(group=group)
        for i in pupil:
            Lesson.objects.create(
                group=group, topic=topic, time=time, status=True, pupil=i
            )       
        return redirect('work-plan', pk=id)


def Get_Chekout(request, pk):
    payment = Payment_A.objects.get(id=pk)
    month = payment.date_joined.month
    money =  f"{payment.money:,}"
    context = {
        'payment': payment,
        'month': month,
        'money': money,
    }
    return render(request, 'checkout.html', context)


def My_Profile(request, username):
    if request.user.is_authenticated:
        user = User.objects.get(username=username)
        if request.user.type == 2:
            teacher = Teacher.objects.get(user=request.user)
            group = Group.objects.filter(teacher=teacher)
            pupils = []
            for i in group:
                pupils.append(i)
            pupils = Pupil.objects.filter(teacher=teacher)
            context = {
                'user': user,
                'group': group.count(),
                'pupils': pupils,
            }
            return render(request, 'profile.html', context)
        else:
            return redirect('pupils_all')


#All tests are here


def Buttons_Test(request):
    return render(request, 'buttons.html')



def Pupil_Test(request):
    return render(request, 'pupils2.html')