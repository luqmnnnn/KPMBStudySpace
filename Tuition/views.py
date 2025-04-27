from django.shortcuts import render, redirect
from Tuition.models import User, TuitionPackage, Registration, Suggestion
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import logout

u_ID = ''

def login(request):  # GET 1
    global u_ID
    if request.method == 'GET':
        u_ID = request.GET.get('userid')
        u_password = request.GET.get('u_password')
        try:
            data = User.objects.get(userID=u_ID)
        except User.DoesNotExist:
            dict = {
                'message': ''
            }
            return render(request, 'login.html', dict)
        if u_password != data.password1:
            dict = {
                'message': 'Password doesn\'t match with userID'
            }
            return render(request, 'login.html', dict)
        else:
            return redirect('homepage')
    else:
        dict = {}
    return render(request, 'login.html', dict)

def forgot_password(request):  # GET 2
    return render(request, 'forgot_password.html')

def password_reset(request):  # PUT 1
    userid = request.POST['userid']
    u_password1 = request.POST['u_password1']
    u_password2 = request.POST['u_password2']
    data = User.objects.get(userID=userid)
    data.password1 = u_password1
    data.password2 = u_password2
    data.save()
    return HttpResponseRedirect(reverse('login'))

def logout_view(request):  # GET 3
    logout(request)
    return redirect('login')

def homepage(request):  # GET 4
    global u_ID
    data = User.objects.filter(userID=u_ID)
    dict = {
        'data': data
    }
    return render(request, 'homepage.html', dict)

def tuitionpackage(request):  # GET 5 / POST 1
    global u_ID
    data = User.objects.filter(userID=u_ID)
    data2 = TuitionPackage.objects.values('packageCategory').distinct()
    
    selected_category = request.GET.get('i_category')

    if 'cart' not in request.session:
        request.session['cart'] = []
        request.session['cart_details'] = []

    if request.method == 'POST':  # POST 1
        item_id = request.POST.get('tuitionPackageID')
        
        if item_id not in request.session['cart']:
            request.session['cart'].append(item_id)
        
            package = TuitionPackage.objects.get(tuitionPackageID=item_id)
            package_details = {
                'tuitionPackageID': package.tuitionPackageID,
                'userID': u_ID,
                'packageCategory': package.packageCategory,
                'packageDescription': package.packageDescription,
                'packagePrice': float(package.packagePrice),
                'subjects': package.subjects
            }
            request.session['cart_details'].append(package_details)
            request.session.modified = True

    cart_items = request.session.get('cart', [])
    cart_details = request.session.get('cart_details', [])

    total_price = sum(item['packagePrice'] for item in cart_details)

    if selected_category and selected_category != 'Choose preferred tuition package categories':
        data3 = TuitionPackage.objects.filter(packageCategory=selected_category)
    else:
        data3 = TuitionPackage.objects.all()

    context = {
        'data': data,
        'data2': data2,
        'data3': data3,
        'cart_items': cart_items,
        'cart_details': cart_details,
        'total_price': total_price 
    }
    return render(request, 'tuitionpackage.html', context)

def registration(request):  # GET 6
    global u_ID
    data = User.objects.filter(userID=u_ID)
    data2 = Registration.objects.filter(userID=u_ID).values('registrationID').distinct()
    filter = Registration.objects.filter(userID=u_ID, registrationID=request.GET.get('i_id'))
    
    if request.method == 'GET':
        if filter:
            data3 = Registration.objects.filter(userID=u_ID, registrationID=request.GET.get('i_id'))
        else:
            data3 = Registration.objects.filter(userID=u_ID)
        return render(request, 'registration.html', {
            'data': data,
            'data2': data2,
            'data3': data3,
            'user_id': u_ID
        })

def update_registration(request, id):  # POST 2
    global u_ID
    data = User.objects.filter(userID=u_ID)
    try:
        registration = Registration.objects.get(userID=u_ID, registrationID=id)
    except Registration.DoesNotExist:
        return redirect('registration')  

    if request.method == 'POST':
        selected_status = request.POST.get('status')
        selected_session = request.POST.get('session')

        if selected_status and selected_session:
            registration.status = selected_status
            registration.session = selected_session
            registration.save()
            cart_details = request.session.get('cart_details', [])
            for item in cart_details:
                if item.get('registrationID') == registration.registrationID:
                    item['status'] = selected_status
                    item['session'] = selected_session
                    break

            request.session['cart_details'] = cart_details
            request.session.modified = True

            return redirect('registration')
    return render(request, 'update_registration.html', {'data': data, 'registration': registration})

def save_update_registration(request, id):  # PUT 2
    try:
        registration = Registration.objects.get(userID=u_ID, registrationID=id)
    except Registration.DoesNotExist:
        return HttpResponseRedirect(reverse('registration')) 

    if request.method == 'POST':
        selected_status = request.POST.get('status')
        selected_session = request.POST.get('session')
        registration.status = selected_status
        registration.session = selected_session
        registration.save()
        cart_details = request.session.get('cart_details', [])
        for item in cart_details:
            if 'registrationID' in item and item['registrationID'] == registration.registrationID:
                item['status'] = selected_status
                item['session'] = selected_session
                break
        
        request.session['cart_details'] = cart_details
        request.session.modified = True

        return HttpResponseRedirect(reverse('registration'))

def clear_registration(request):  # DELETE 1
    global u_ID
    Registration.objects.filter(userID=u_ID).delete()  
    return redirect('registration')

def suggestion(request):  # GET 7
    global u_ID
    user = User.objects.filter(userID=u_ID)
    allsuggestion = Suggestion.objects.all()
    dict = {
        'user': user,
        'allsuggestion': allsuggestion
    }
    return render(request, 'suggestion.html', dict)

def new_suggestion(request):  # POST 3
    global u_ID
    user = User.objects.filter(userID=u_ID)
    if request.method == 'POST':
        s_userid = User.objects.get(userID=u_ID)
        u_title = request.POST['u_title']
        u_forum = request.POST['u_forum']
        data2 = Suggestion(userID=s_userid, title=u_title, forum=u_forum)
        data2.save()
        dict = {
            'user': user,
            'message': 'Thank you for your suggestion!'
        }
        return render(request, 'new_suggestion.html', dict)
    else:
        return render(request, 'new_suggestion.html', {'user': user})

def delete_suggestion(request, suggestion_id):  # DELETE 2
    if request.method == 'POST':
        try:
            suggestion = Suggestion.objects.get(id=suggestion_id)
            suggestion.delete()
            return redirect('suggestion')
        except Suggestion.DoesNotExist:
            return render(request, 'error.html', {'message': 'Suggestion not found.'})

def my_account(request):  # GET 8
    global u_ID
    data = User.objects.filter(userID=u_ID)
    return render(request, 'my_account.html', {'data': data})

def update_my_account(request):  # PUT 3
    global u_ID
    username = request.POST['u_name']
    useremail = request.POST['u_email']
    usermobile = request.POST['u_mobile']
    data = User.objects.get(userID=u_ID)
    data.userName = username
    data.userEmail = useremail
    data.userMobile = usermobile
    data.save()
    return redirect('my_account')