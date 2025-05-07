from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required

def custom_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)

            # Role-based redirection
            if user.is_superuser:
                return redirect('admin_dashboard')
            elif user.groups.filter(name='AI Engineer').exists():
                return redirect('/ai-dashboard/')
            elif user.groups.filter(name='end users').exists():
                return redirect('/end-user-dashboard/')
            elif user.groups.filter(name='Finance').exists():
                return redirect('/finance-dashboard/')
            else:
                return redirect('/main-dashboard/')

        else:
            return render(request, 'login_dashboard/login.html', {'error': 'Invalid credentials'})

    return render(request, 'login_dashboard/login.html')



# Existing dashboard views
@login_required
def admin_dashboard(request):
    return render(request, 'admin_dashboard/index.html')

@login_required
def ai_dashboard(request):
    return render(request, 'ai_engineer_dashboard/index.html')

@login_required
def finance_dashboard(request):
    return render(request, 'finance_dashboard/financedashboard.html')

@login_required
def end_user_dashboard(request):
    return render(request, 'end_user_dashboard/enduserdash.html')

@login_required
def main_dashboard(request):
    return render(request, 'dashboard/main_dashboard.html')
