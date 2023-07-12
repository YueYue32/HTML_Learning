from django.shortcuts import render, redirect
from django.http import HttpResponse
from datetime import datetime
from myapp.models import student
from django.http import Http404
from django.contrib import auth
from django.http import HttpResponseRedirect
from django.utils import timezone
from flask import Flask,render_template,request

# Create your views here.

# def home(request):
#     return HttpResponse("Home page")


def helloworld(request):
    return  HttpResponse("Hello world")


def hiname(request, username):
    return HttpResponse("Hi " + username)


def age(request, year):
    return HttpResponse("Age: " + str(year))


def hello_view(request):
    fourSeason = range(1, 5)
    p1 = {"name": "Amy", "phone": "0912-345678", "age": 20}
    p2 = {"name": "Jack", "phone": "0937-123456", "age": 25}
    p3 = {"name": "Nacy", "phone": "0958-654321", "age": 17}
    persons = [p1, p2, p3]
    return render(request, 'hello_django.html', {
        'title': "樣板使用",
        'data': "Hello Django!",
        'seasons': fourSeason,
        'persons': persons,
        'now': datetime.now()
    })

def getOneByName(request, username):
    title = "顯示一筆資料"
    # unit = get_object_or_404(student, cName=username)
    try:
        unit = student.objects.get(cName=username)
    except student.DoesNotExist:
        raise Http404("查無此學生")
    except:
        raise Http404("讀取錯誤")
    return render(request, 'listone.html', locals() )


def getAll(request):
    title = "顯示全部資料"
    # students = get_list_or_404(student)
    try:
        students = student.objects.all()
    except student.DoesNotExist:
        raise Http404("查無學生資料")
    except:
        raise Http404("讀取錯誤")
    return render(request, 'listall.html', locals() )


def main(request):
    # 除了網頁名稱，其他都先註解掉，不要增加版面複雜程度
    pageTitle="子網頁繼承"
    # mainTitle="段落標題"
    # mainContent="段落內文"
    # artitle1={"aTitle":"人名","aContent":"資料"}
    # artitle2={"aTitle":"文章標題","aContent":"文章2內文"}
    # artitles=[artitle1]

    # =============================================================================================

    # 4個篩選器，主要用於篩選判斷出有沒有輸入資料、是否輸入完整資料，變數如果轉換成True，那index.html內會收到回傳值，並做出不同的反應

    # search_check，用於判斷查詢框內輸入的人名是否存在於資料庫中
    # 人名如果存在於資料庫中，search_check = ""(沒值)
    # 人名如果不存在於資料庫中，search_check = True，對應到index.html的
    # {% if search_check %}
    # <p>{{username_search}}，沒這個人</p>
    # {% endif %}
    # 因為search_check = True(有值)，所以會跳出{{username_search}}，沒這個人的訊息，{{username_search}}是user輸入的人名
    search_check = ""


    # data_check，用於判斷建立資料框內輸入的資料是否建立成功
    # 如果確實輸入了全部資料，並且按下"送出資料"按鈕，data_check = True，對應到index.html的
    # {% if data_check %}
    # <p>{{username_insert}}的資料建立成功</p>
    # {% endif %}
    # 因為data_check = True(有值)，所以會跳出{{username_insert}}的資料建立成功的訊息，{{username_search}}是user輸入的人名
    data_check = ""


    # one_check，用於判斷查詢框框內是否有輸入文字
    # 如果搜尋框框內沒輸入文字就按"送出查詢"按鈕，one_check = True，對應到index.html的
    # {% if one_check %}
    # <p>你沒輸入人名資料</p>
    # {% endif %}
    # 因為one_check = True(有值)，所以會跳出你沒輸入人名資料的訊息
    one_check = ""


    # full_check，用於判斷建立資料框框中的資料是否齊全
    # 如果輸入的資料不齊全，full_check = True，對應到index.html的
    # {% if full_check %}
    # <p>你資料沒輸入完全</p>
    # {% endif %}
    # 因為full_check = True(有值)，所以會跳出你資料沒輸入完全的訊息
    full_check = ""

    # 請求資料的方法，不選用"GET"，因為會改變網址，"POST"則不會
    if request.method == "POST":

        # 判斷user按下哪個按鈕，如果button_search有回傳值(不是None)，代表user按下的是"送出查詢"按鈕
        # 反之，如果回傳值是None，代表user按下的是"送出資料"按鈕
        button_search = request.POST.get("sendsearch")

        # 如果button_search有回傳值(代表按下"送出查詢"按鈕)，底下執行查詢功能
        if button_search:

            # 找name = "ccName"的POST回傳值，也就是user輸入的人名(故意不設計成cName，會跟後面建立資料中的人名衝突)
            username_search = request.POST['ccName']

            # 如果name = "ccName"的POST回傳值不是空白的(代表有輸入文字)
            if username_search != "":

                # 找尋資料庫中的資料，看看是否有這筆資料(objects.filter(條件))
                check = student.objects.filter(cName__exact=username_search)

                # 如果check成立，代表資料庫中有這筆資料
                if check:

                    # 提取出該筆資料
                    unit = student.objects.get(cName=username_search)

                # 如果check不成立，代表資料庫中沒有這筆資料
                else:
                    search_check = True

            # else，表示name = "ccName"的POST回傳值是空白的(代表沒有輸入文字)
            else:
                one_check = True

        # 如果button_search沒有回傳值(代表按下"送出資料"按鈕)，底下執行建立資料功能
        else:

            # 取得各項"POST"回傳值
            username_insert = request.POST['cName']
            usersex_insert = request.POST['cSex']
            userbirthday_insert = request.POST['cBirthday']
            useremail_insert = request.POST['cEmail']
            userphone_insert = request.POST['cPhone']
            useraddr_insert = request.POST['cAddr']

            # 防呆機制，確保user輸入齊全的資料，只要有一項資料是空白，就會進入else(跳出"你資料沒輸入完全"的訊息)
            if username_insert !="" and usersex_insert !="" and userbirthday_insert !="" and useremail_insert !="" and userphone_insert !="" and useraddr_insert !="":
                stu = student(cName=username_insert, cSex=usersex_insert, cBirthday=userbirthday_insert, cEmail=useremail_insert, cPhone=userphone_insert, cAddr=useraddr_insert, last_modified=timezone.now(),created=timezone.now())
                stu.save() # 記得存檔，不然不會寫進資料庫
                data_check = True
            else:
                full_check = True
    return render(request, 'index.html', locals())



#
# def query(request):
#     search = request.GET
#     username = search.get('cName')
#
#     check = student.objects.filter(cName__exact=username)
#     if check:

#         unit = student.objects.get(cName=username)

#         # return render(request, 'index.html', locals())

#     else:
#         # return render(request, 'index_n.html', locals())
#         return HttpResponse("沒這個人")

    # if unit:
        # return HttpResponse(unit)
        # return render(request, 'index.html', locals())
    # else:
    #     return
    # try:
    #     unit = student.objects.get(cName=username)
    # except student.DoesNotExist:
    #     raise Http404("查無此學生")
    # except:
    #     raise Http404("讀取錯誤")
    # return render(request, 'index.html', locals() )






def login(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    elif request.method == 'POST':
        uName = request.POST.get('uName')  # login.html 傳來的變數
        uPass = request.POST.get('uPass')  # login.html 傳來的變數
        # 直接判斷帳密有效性
        # if uName=='Peter' and uPass=='591026':
        #     return HttpResponse("已登入")
        # else:
        #     return redirect('/login/')

        # 以 Django 內建的管理者帳密判斷有效性
        user = auth.authenticate(username=uName, password=uPass)
        if user is not None:
            auth.login(request, user)
            return HttpResponse("已登入")
        else:
            return redirect('/login/')