from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import viewsets, status
from django.http import HttpResponse,JsonResponse, HttpResponseRedirect
from . forms import userRegistration, userLogin
from django.urls import reverse
from django.contrib import messages
import requests, json, psycopg2, collections,jwt
from django.views.decorators.csrf import csrf_exempt

tasks = { }

access_tokens = {}

session = {}

count = 0

def get_next_task_id():
    try:
        db = psycopg2.connect(host='localhost', user='username', password='your_password', dbname='your_dbname')
        cursor = db.cursor()
        sql = "select * from user_table;"
        data = cursor.execute(sql)
        db.commit()
        db.close()
        return int(data)+1
    except:
        return 1
@csrf_exempt
def Home(request):
    return render(request,'modelless_app/home.html')
@csrf_exempt
def get_userList(request):
    r = requests.get('http://127.0.0.1:8000/tasks/')
    json_data = json.loads(r.text)
    id_list = []
    new_json_data = []
    for i in json_data:
        if i['id'] not in id_list:
            id_list.append(i['id'])
            new_json_data.append(i)

    context = {'data':new_json_data}
    #print (context)
    return render(request, 'modelless_app/user_list.html',context)



@csrf_exempt
def user_login(request):
    if request.method == 'POST':
        my_query_dict = request.POST.dict()
        url = 'http://127.0.0.1:8000/user_Login/'
        r = requests.post(url, data=my_query_dict)
        print("login result from rest api",r.text)
        r_dict = {}
        r_list = r.text.split('"')
        print(r_list)
        r_value = ""
        for i in r_list[1::2]:
            if r_value == "token":
                r_dict['token'] = i
                r_value = ""
            elif r_value == "status":
                r_dict['status'] = i
                r_value = ""
            elif r_value == "url":
                r_dict['url'] = i
                r_value = ""
            if i == 'token':
                r_value = "token"
            elif i == 'status':
                r_value = "status"
            elif i == 'url':
                r_value = "url"

        print(r_dict)
        return JsonResponse(r_dict)

    return render(request, "modelless_app/login.html")


@csrf_exempt
def user_loggedin(request):
    if request.method == "GET":

        print("request.COOOKIES->", request.COOKIES)
        print("request.META->", request.META["SESSION_MANAGER"])
        print("\n\n")
        url = 'http://127.0.0.1:8000/login_success/'
        r = requests.post(url, data=request.COOKIES)
        if r.status_code == 201:
            user_name = r.text.split('"')
            user_name = user_name[1]
            print("VALID USERRR>>>>", user_name)
            context_data = {"info": user_name}
            return render(request, "modelless_app/loggedin.html", context_data)

        else:
            print(r.status_code)
            print("Not valid User ")
            return HttpResponse("Please log-in first...!")



@csrf_exempt
def logout(request):
    url = 'http://127.0.0.1:8000/logout_success/'
    r = requests.post(url, data=request.COOKIES)
    if r.status_code == 201:
        messages.success(request, "Successfully logged out")
        return HttpResponseRedirect(reverse('modelless_app:login'))

    else:
        print('Not logged out..')
        return render(request, "modelless_app/loggedin.html")



@csrf_exempt
def user_registration(request):
    form = userRegistration()
    if request.method == 'POST':
        form = userRegistration(request.POST)
        if form.is_valid():
            user_name = form.cleaned_data['user_name']
            password = form.cleaned_data['password1']
            email = form.cleaned_data['email']
            print (user_name,password,email)
            json_data = {}
            json_data['name'] = str(user_name)
            json_data['password'] = str(password)
            json_data['email'] = str(email)
            print(json_data)
            url = 'http://127.0.0.1:8000/tasks/'
            r = requests.post(url, data= json_data)
            print (r.status_code)
            print (r.text)
            try:
                print(type(r.text))
                if r.text.startswith('{"error":"(1062,'):
                    messages.error(request, "User Name exists")
                else:
                    messages.success(request, "Successfully registered")
            except:
                pass
            return HttpResponseRedirect(reverse('modelless_app:home'))
    else:
        form = userRegistration()
    return render(request, 'modelless_app/register.html', {'form': form})

class LoginViewSet(viewsets.ViewSet):
    def list(self, request):
        try:
            my_query_dict = request.POST.dict()
            key = list(my_query_dict.keys())

            if key[0] == 'credentials':
                 json_data = json.loads(my_query_dict['credentials'])
                 db = psycopg2.connect(host='localhost', user='username', password='your_password', dbname='your_dbname')
                 cursor = db.cursor()
                 user_name = json_data['username']
                 passwd = json_data['password']
                 format_str = "select password from user_table where username = '{nm}'"
                 sql = format_str.format(nm=user_name)
                 cursor.execute(sql)
                 data = cursor.fetchall()
                 if data != ():
                     arr = (str(data).split("'"))
                     if arr[1] == passwd:
                         session_cursor = db.cursor()
                         format_str = "select count(*) from session where username = '{nm}'"
                         session_sql = format_str.format(nm=user_name)
                         session_cursor.execute(session_sql)
                         data = session_cursor.fetchall()
                         count = data[0][0]
                         get_data = {}
                         get_data['un'] = user_name
                         get_data['identifier'] = (count + 1)
                         encode_token = jwt.encode(get_data, 'SECRET', algorithm='HS256')
                         sql_token = encode_token.decode("utf-8")
                         insert_cursor = db.cursor()
                         insert_str = 'insert into session (username,jwt) values("{nm}","{tok}");'
                         insert_sql = insert_str.format(nm=user_name, tok=sql_token)
                         insert_cursor.execute(insert_sql)
                         data1 = insert_cursor.fetchall()
                         db.commit()
                         mydict = {"url": "successful_login", "status": "Correct Credentials...!",
                                 "token": str(encode_token)}
                         return Response(mydict, status=status.HTTP_201_CREATED)



                     else:
                         error_dict = {"url": "", "status": "Please Enter Valid Credentials"}
                         return Response(error_dict, status=status.HTTP_400_BAD_REQUEST)

                 else:
                     error_dict = {"url": "", "status": "Please Enter Valid Credentials"}
                     return Response(error_dict, status=status.HTTP_400_BAD_REQUEST)


        except:
            print("Service Not Available")
            error_dict = {"url": "Sorry Service Not Available", "status": "Service Not Available"}
            return Response(error_dict, status=status.HTTP_400_BAD_REQUEST)



class SuccessViewSet(viewsets.ViewSet):
    def list(self, request):
        try:
            cks = request.data
            user = cks['jwt'][2:len(cks['jwt']) - 1].encode("utf-8")
            print(user)
            get_user = jwt.decode(user, 'SECRET', algorithms=['HS256'])
            user_name = get_user['un']
            token = user.decode("utf-8")
            db = psycopg2.connect(host='localhost', user='username', password='your_password', dbname='your_dbname')
            session_cursor = db.cursor()
            format_str = "select count(*) from session where username = '{nm}' and jwt = '{tok}'"
            session_sql = format_str.format(nm=user_name, tok=token)
            session_cursor.execute(session_sql)
            data = session_cursor.fetchall()
            token_count = (data[0][0])
            if token_count == 1:
                context_data = user_name
                return Response(context_data, status=status.HTTP_201_CREATED)
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)

        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class LogoutViewSet(viewsets.ViewSet):
    def list(self, request):
        try:
            cks = request.data
            user = cks['jwt'][2:len(cks['jwt']) - 1].encode("utf-8")
            get_user = jwt.decode(user, 'SECRET', algorithms=['HS256'])
            user_name = get_user['un']
            token = user.decode("utf-8")
            db = psycopg2.connect(host='localhost', user='username', password='your_password', dbname='your_dbname')
            session_cursor = db.cursor()
            format_str = "delete from session where username = '{nm}' and jwt = '{tok}'"
            session_sql = format_str.format(nm=user_name, tok=token)
            session_cursor.execute(session_sql)
            data = session_cursor.fetchall()
            print(data)
            db.commit()
            return Response(status=status.HTTP_201_CREATED)

        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)



class TaskViewSet(viewsets.ViewSet):
    def list(self, request):
        print(request.POST)
        print(request.data)
        db = psycopg2.connect(host='localhost', user='username', password='your_password', dbname='your_dbname')
        psycopg2.connect(host='localhost', user='username', password='your_password', dbname='your_dbname')

        cursor = db.cursor()
        sql = "select * from user_table;"
        print(sql)
        try:
            cursor.execute(sql)
            row_headers = [x[0] for x in cursor.description]
            rv = list(cursor.fetchall())
            ls = []
            for column_header in rv:
                column_header = list(column_header)
                column_header[0] = str(column_header[0])
                column_header = tuple(column_header)
                ls.append(column_header)
            json_data = []
            for result in tuple(ls):
                json_data.append(dict(zip(row_headers, result)))
            default_data = (json.dumps(json_data))
            data = str(default_data)
            print(data)
            ordered_data = json.JSONDecoder(object_pairs_hook=collections.OrderedDict).decode(data)
            print(ordered_data)
        except Exception as e:
            print(e)


        db.close()
        return Response(ordered_data)

    def create(self, request):
        try:
            print(request.data)
            my_query_dict = dict(request.data)
            mydict = {}
            for key in my_query_dict:
                for i in my_query_dict[key]:
                    mydict[key] = i
            mydict['id'] = (get_next_task_id())
            db = psycopg2.connect(host='localhost', user='username', password='your_password', dbname='your_dbname')
            cursor = db.cursor()
            json_data = mydict
            user_id = json_data['id']
            user_name = json_data['name']
            email = json_data['email']
            password = json_data['password']
            format_str = "insert into user_table (id,username,email,password) values({id}, '{nm}', '{em}', '{pw}')"
            sql = format_str.format(id=user_id, nm=user_name, em=email, pw=password)
            cursor.execute(sql)
            data = (cursor.fetchall())
            print(data)
            db.commit()
            db.close()
            return Response(mydict, status=status.HTTP_201_CREATED)
        except Exception as e:
            error_dict = {'error': str(e)}
            return Response(error_dict, status=status.HTTP_400_BAD_REQUEST)


