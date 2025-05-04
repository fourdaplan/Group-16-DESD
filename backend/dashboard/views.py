from django.shortcuts import render

def admin_dashboard(request):
    return render(request, 'admin_dashboard/index.html')

def ai_dashboard(request):
    return render(request, 'ai_engineer_dashboard/index.html')

def finance_dashboard(request):
    return render(request, 'finance_dashboard/financedashboard.html')

def end_user_dashboard(request):
    return render(request, 'end_user_dashboard/enduserdash.html')

def main_dashboard(request):
    return render(request, 'dashboard/main_dashboard.html')