from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User, Group
from django.shortcuts import render, redirect




def custom_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_active:
            login(request, user)

            #  Set role in session
            if user.is_superuser:
                request.session['role'] = 'admin'
                return redirect('admin_dashboard')
            elif user.groups.filter(name='AI Engineer').exists():
                request.session['role'] = 'ai_engineer'
                return redirect('/ai-dashboard/')
            elif user.groups.filter(name='end users').exists():
                request.session['role'] = 'end_user'
                return redirect('/end-user-dashboard/')
            elif user.groups.filter(name='Finance').exists():
                request.session['role'] = 'finance'
                return redirect('/finance-dashboard/')
            else:
                request.session['role'] = 'unknown'
                return render(request, 'login_dashboard/login.html', {'error': 'Access group not assigned. Contact admin.'})
        else:
            return render(request, 'login_dashboard/login.html', {'error': 'Invalid credentials or inactive account'})

    return render(request, 'login_dashboard/login.html')


#  Role-based access control decorators
def is_ai_engineer(user):
    return user.groups.filter(name='AI Engineer').exists()

def is_finance(user):
    return user.groups.filter(name='Finance').exists()

def is_end_user(user):
    return user.groups.filter(name='end users').exists()

def is_admin(user):
    return user.is_superuser


#  Protected dashboards
@user_passes_test(is_admin)
def admin_dashboard(request):
    return render(request, 'admin_dashboard/index.html')


@user_passes_test(is_ai_engineer)
def ai_dashboard(request):
    request.session['role'] = 'ai_engineer'
    return render(request, 'ai_engineer_dashboard/index.html')


@user_passes_test(is_finance)
def finance_dashboard(request):
    request.session['role'] = 'finance'
    return render(request, 'finance_dashboard/financedashboard.html')


@user_passes_test(is_end_user)
def end_user_dashboard(request):
    request.session['role'] = 'end_user'
    return render(request, 'end_user_dashboard/enduserdash.html')


#  Catch-all or shared main dashboard
@login_required
def main_dashboard(request):
    return render(request, 'dashboard/main_dashboard.html')
