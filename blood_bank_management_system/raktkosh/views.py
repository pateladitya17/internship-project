from ast import Or
from email import message
# import imp
import re
from tokenize import group
from unicodedata import category
from django.contrib.auth import authenticate, login, logout
from .models import *
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.db.models import Sum
from django.shortcuts import render,redirect,reverse
from . import forms,models
from django.db.models import Sum,Q
from django.contrib.auth.models import Group
from django.conf import settings
from datetime import date, timedelta
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from .forms import BloodForm, DonationForm, RequestForm
from django.db.models import Sum
from django.core.mail import send_mail
from django.http import JsonResponse
from .models import Contact
from django.contrib.auth.decorators import login_required


def Home(request):
    return render(request,'index.html')

def About(request):
    return render(request,'about.html')

def contact(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        contact = Contact(
            name=name,
            email=email,
            subject=subject,
            message=message,
        )
        
        subject = subject
        message = message
        email_from = settings.EMAIL_HOST_USER

        send_mail(subject,message,email_from,['up962002@gmail.com'])
        contact.save()
        return redirect('home')
    return render(request,'contact.html')

def Gallery(request):
    return render(request,'gallery.html')

def Login_User(request):
    if request.method == "POST":
        u = request.POST['uname']
        p = request.POST['pwd']
        user = authenticate(username=u, password=p)
        sign = ""
        if not user.is_staff and user:
            login(request, user)
            messages.success(request, "Logged in Successfully")
            return redirect('home')
        else:
            messages.success(request, "Invalid user")
    return render(request, 'login.html')

def admin_login(request):
    if request.method == "POST":
        u = request.POST['uname']
        p = request.POST['pwd']
        user = authenticate(username=u, password=p)
        sign = ""
        if user.is_staff:
            login(request, user)
            messages.success(request, "Logged in Successfully")
            return redirect('admin_home')
        else:
            messages.success(request, "Invalid user")
    return render(request, 'admin_login.html')

def Signup_User(request):
    cat = Category.objects.all()
    if request.method == 'POST':
        f = request.POST['fname']
        l = request.POST['lname']
        u = request.POST['uname']
        e = request.POST['email']
        p = request.POST['pwd']
        d = request.POST['dob']
        con = request.POST['contact']
        add = request.POST['add']
        group = request.POST['group']
        im = request.FILES['image']
        cat = Category.objects.get(id=group)
        user = User.objects.create_user(email=e, username=u, password=p, first_name=f,last_name=l)
        UserProfile.objects.create(user=user,contact=con,address=add,image=im,dob=d, blood_group=cat)
        messages.success(request, "Registration Successful")
        return redirect('login')
    return render(request,'register.html', {'cat':cat})

def Logout(request):
    logout(request)
    return redirect('home')

def Change_Password(request):
    user = User.objects.get(username=request.user.username)
    if request.method=="POST":
        n = request.POST['pwd1']
        c = request.POST['pwd2']
        o = request.POST['pwd3']
        if c == n:
            u = User.objects.get(username__exact=request.user.username)
            u.set_password(n)
            u.save()
            messages.success(request, "Password changed successfully")
        else:
            messages.success(request, "New password and confirm password are not same.")
        return redirect('home')
    return render(request,'change_password.html')

@login_required(login_url='admin_login')
def home_view(request):
    x=models.Stock.objects.all()
    print(x)
    if len(x)==0:
        blood1=models.Stock()
        blood1.bloodgroup="A+"
        blood1.save()

        blood2=models.Stock()
        blood2.bloodgroup="A-"
        blood2.save()

        blood3=models.Stock()
        blood3.bloodgroup="B+"
        blood3.save()        

        blood4=models.Stock()
        blood4.bloodgroup="B-"
        blood4.save()

        blood5=models.Stock()
        blood5.bloodgroup="AB+"
        blood5.save()

        blood6=models.Stock()
        blood6.bloodgroup="AB-"
        blood6.save()

        blood7=models.Stock()
        blood7.bloodgroup="O+"
        blood7.save()

        blood8=models.Stock()
        blood8.bloodgroup="O-"
        blood8.save()

@login_required(login_url='admin_login')
def admin_home(request):
    categories = Category.objects.all()
    stocks = Stock.objects.all()
    total_donors = UserProfile.objects.all().count()
    total_blood_units = Stock.objects.aggregate(total_units=Sum('unit'))['total_units'] or 0
    total_requests = BloodRequest.objects.all().count()
    total_approved_requests = BloodRequest.objects.filter(status='Approved').count()

    if request.method == 'POST':
        form = BloodForm(request.POST)
        if form.is_valid():
            bloodgroup = form.cleaned_data['bloodgroup']
            unit = form.cleaned_data['unit']
            stock, created = Stock.objects.get_or_create(bloodgroup=bloodgroup)
            stock.unit += unit
            stock.save()
            messages.success(request, 'Stock updated successfully.')
            return redirect('admin_home')
        else:
            messages.error(request, 'Error updating stock.')
    else:
        form = BloodForm()

    context = {
        'categories': categories,
        'stocks': stocks,
        'total_donors': total_donors,
        'total_blood_units': total_blood_units,
        'total_requests': total_requests,
        'total_approved_requests': total_approved_requests,
        'form': form,
    }
    return render(request, 'admin_home.html', context)

@login_required(login_url='admin_login')
def request_blood(request):
    requests=models.BloodRequest.objects.all().filter(status='Pending')
    return render(request,'request_blood.html',{'requests':requests})

@login_required(login_url='admin_login')
def update_approve_status_view(request, pk):
    req = get_object_or_404(BloodRequest, id=pk)
    message = None
    bloodgroup = req.bloodgroup
    unit = req.unit
    try:
        stock = Stock.objects.get(bloodgroup=bloodgroup)
        if stock.unit >= unit:
            stock.unit -= unit
            stock.save()
            req.status = "Approved"
        else:
            message = f"Stock does not have enough blood to approve this request. Only {stock.unit} unit(s) available."
    except Stock.DoesNotExist:
        message = "Stock for the requested blood group does not exist."

    req.save()
    if message is None:
        return HttpResponseRedirect('/request_blood')
    else:
        requests = BloodRequest.objects.filter(status='Pending')
        return render(request, 'request_blood.html', {'requests': requests, 'message': message})

@login_required(login_url='admin_login')
def update_reject_status_view(request, pk):
    req = get_object_or_404(BloodRequest, id=pk)
    req.status = "Rejected"
    req.save()
    return HttpResponseRedirect('/request_blood')

@login_required(login_url='admin_login')
def donator_blood(request):
    donations=models.BloodDonate.objects.all()
    return render(request,'donator_blood.html',{'donations':donations})

@login_required(login_url='admin_login')
def approve_donation(request, pk):
    donation = get_object_or_404(BloodDonate, id=pk)
    donation_blood_group = donation.bloodgroup
    donation_blood_unit = donation.unit

    try:
        stock = Stock.objects.get(bloodgroup=donation_blood_group)
    except Stock.DoesNotExist:
        # Handle the case where Stock matching the blood group does not exist
        # Redirect or display an appropriate message
        return HttpResponseRedirect('admin_donation')  # Redirect to admin-donation page

    stock.unit += donation_blood_unit
    stock.save()

    donation.status = 'Approved'
    donation.save()

    return HttpResponseRedirect('/admin_donation')

@login_required(login_url='admin_login')
def reject_donation(request, pk):
    donation = get_object_or_404(BloodDonate, id=pk)
    donation.status = 'Rejected'
    donation.save()

    return HttpResponseRedirect('/admin_donation')

@login_required(login_url='admin_login')
def admin_donation_view(request):
    donations=models.BloodDonate.objects.all()
    return render(request,'admin_donation.html',{'donations':donations})

@login_required(login_url='admin_login')
def history(request):
    requests=models.BloodRequest.objects.all().exclude(status='Pending')
    return render(request,'history.html',{'requests':requests})

@login_required(login_url='admin_login')
def admin_blood(request):
    categories = Category.objects.all()
    stocks = Stock.objects.all()

    # Create a dictionary to map each category to its corresponding stock unit
    stock_dict = {stock.category.name: stock.unit for stock in stocks}

    # Handle form submission
    if request.method == 'POST':
        bloodForm = BloodForm(request.POST)
        if bloodForm.is_valid():
            bloodgroup_name = bloodForm.cleaned_data['bloodgroup']
            unit = bloodForm.cleaned_data['unit']
            category = get_object_or_404(Category, name=bloodgroup_name)

            # Check if the stock entry already exists for the category
            existing_stock = Stock.objects.filter(category=category).first()
            if existing_stock:
                # If the stock entry already exists, update the unit
                existing_stock.unit += unit
                existing_stock.save()
            else:
                # If the stock entry does not exist, create a new one
                Stock.objects.create(bloodgroup=bloodgroup_name, unit=unit, category=category)
            
            return render(request, 'admin_blood.html', {'categories': categories, 'stock_dict': stock_dict, 'bloodForm': BloodForm()})

    else:
        bloodForm = BloodForm()

    return render(request, 'admin_blood.html', {'categories': categories, 'stock_dict': stock_dict, 'bloodForm': bloodForm})

@login_required(login_url='admin_login')
def view_user(request):
    data = UserProfile.objects.all()
    d = {'data':data}
    return render(request,'view_user.html',d)

@login_required(login_url='admin_login')
def delete_user(request, pid):
    data = UserProfile.objects.get(id=pid)
    data.delete()
    messages.success(request, "User deleted successfully")
    return redirect('view_user')

@login_required(login_url='login')
def profile(request):
    pro = UserProfile.objects.get(user=request.user)
    return render(request, "profile.html", {'pro':pro})

def edit_profile(request,pid):
    data = UserProfile.objects.get(id=pid)
    cat = Category.objects.all()
    if request.method == 'POST':
        f = request.POST['fname']
        l = request.POST['lname']
        e = request.POST['email']
        con = request.POST['contact']
        add = request.POST['add']
        cat = request.POST['group']
        try:
            im = request.FILES['image']
            data.image=im
            data.save()
        except:
            pass
        data.user.first_name = f
        data.user.last_name = l
        data.user.email = e
        data.contact = con
        bl = Category.objects.get(id=cat)
        data.blood_group = bl
        data.address = add
        data.user.save()
        data.save()
        messages.success(request, "User Profile updated")
        if request.user.is_staff:
            return redirect('view_user')
        else:
            return redirect('profile')
    d = {'data':data, 'cat':cat}
    return render(request,'edit_profile.html',d)

@login_required(login_url='login')
def request_history(request):
    user= models.UserProfile.objects.get(user_id=request.user.id)
    blood_request=models.BloodRequest.objects.all().filter(user=user)
    return render(request,'request_history.html',{'blood_request':blood_request})

@login_required(login_url='login')
def donation_history(request):
    user = models.UserProfile.objects.get(user_id=request.user.id)
    print(user)  # Check if the user is retrieved correctly
    donations = models.BloodDonate.objects.all().filter(user=user)
    print(donations)  # Check if donations queryset is not empty
    return render(request, 'donation_history.html', {'donations': donations})




def calculate_age(birth_date):
    today = date.today()
    age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
    return age

@login_required(login_url='login')
def donate_blood_view(request):
    # Retrieve the current user's profile
    user_profile = models.UserProfile.objects.get(user=request.user)
    
    if request.method == 'POST':
        donation_form = forms.DonationForm(request.POST)
        if donation_form.is_valid():
            blood_donate = donation_form.save(commit=False)
            blood_donate.user = user_profile
            blood_donate.save()
            return HttpResponseRedirect('donation_history')
    else:
        initial_data = {
            'bloodgroup': user_profile.blood_group.name if user_profile.blood_group else '',  # Assuming UserProfile has a ForeignKey field to blood group
            'age': calculate_age(user_profile.dob), # You can pre-fill other fields similarly
        }
        donation_form = forms.DonationForm(initial=initial_data)  # Pass initial data to pre-fill the form
    
    return render(request, 'donate_blood.html', {'donation_form': donation_form, 'user_profile': user_profile})

@login_required(login_url='login')
def make_request(request):
    user_profile = UserProfile.objects.get(user=request.user)
    user_age = calculate_age(user_profile.dob)  # Assuming dob is the field in UserProfile model
    initial_data = {
        'patient_name': request.user.username,  # Fill patient name with username
        'patient_age': user_age,                # Fill patient age with calculated age
        'bloodgroup': user_profile.blood_group.name if user_profile.blood_group else '',  # Fill blood group with user's blood group from profile
    }
    request_form = forms.RequestForm(initial=initial_data)

    if request.method == 'POST':
        request_form = forms.RequestForm(request.POST)
        if request_form.is_valid():
            blood_request = request_form.save(commit=False)
            blood_request.user = user_profile
            blood_request.save()
            return HttpResponseRedirect('request_history')

    return render(request, 'makerequest.html', {'request_form': request_form})


# def send_email(request):
#     if request.method == 'POST':
#         name = request.POST.get('name')
#         email = request.POST.get('email')
#         subject = request.POST.get('subject')
#         message = request.POST.get('message')

#         # Sender email address
#         sender_email = 'up962002@gmail.com.com'  # Replace with your sender email address

#         # Send email
#         try:
#             send_mail(
#                 subject,
#                 message,
#                 sender_email,  # Use the sender email address here
#                 ['raktkoshbloodbank@gmail.com'],  # Replace with your recipient email address
#                 fail_silently=False,
#             )
#             return JsonResponse({'success': True})
#         except Exception as e:
#             return JsonResponse({'success': False, 'error': str(e)})

#     return JsonResponse({'success': False, 'error': 'Method not allowed'})