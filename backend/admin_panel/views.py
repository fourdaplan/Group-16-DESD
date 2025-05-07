from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import User, Group
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from rest_framework import viewsets, permissions
from .models import ActivityLog
from .serializers import ActivityLogSerializer
from .utils import log_activity
from model_manager.models import UploadedModel, Interaction

# ✅ Permissions for DRF
class IsAdminUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_staff

# ✅ DRF ViewSet for logs API
class ActivityLogViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ActivityLog.objects.all().order_by('-timestamp')
    serializer_class = ActivityLogSerializer
    permission_classes = [IsAdminUser]

    def list(self, request, *args, **kwargs):
        log_activity(request.user, "Viewed activity logs via API")
        return super().list(request, *args, **kwargs)

# ✅ Admin Dashboard View
@user_passes_test(lambda u: u.is_superuser)
def admin_dashboard(request):
    try:
        engineers_group = Group.objects.get(name='AI Engineer')
        pending_engineers = User.objects.filter(groups=engineers_group, is_active=False)
    except Group.DoesNotExist:
        pending_engineers = []

    recent_uploads = UploadedModel.objects.select_related('user') \
        .filter(user__isnull=False) \
        .order_by('-uploaded_at')

    print("🟢 DEBUG: recent_uploads count =", recent_uploads.count())
    for model in recent_uploads:
        if model.user:
            print(f" - {model.name} by {model.user.username} at {model.uploaded_at}")
        else:
            print(f" - {model.name} with NO USER ❌")

    recent_predictions = Interaction.objects.all().order_by('-timestamp')[:5]
    logs = ActivityLog.objects.all().order_by('-timestamp')[:10]

    log_activity(request.user, "Accessed admin dashboard")

    return render(request, 'admin_dashboard/index.html', {
        'pending_engineers': pending_engineers,
        'recent_uploads': recent_uploads,
        'recent_predictions': recent_predictions,
        'logs': logs,
    })

# ✅ Approve AI Engineer
@user_passes_test(lambda u: u.is_superuser)
def approve_engineer(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user.is_active = True
    user.save()
    log_activity(request.user, f"Approved AI Engineer: {user.username}")
    return redirect('admin_dashboard')

# ✅ View Activity Logs in HTML
@user_passes_test(lambda u: u.is_superuser)
def view_activity_logs(request):
    logs = ActivityLog.objects.all().order_by('-timestamp')[:50]
    log_activity(request.user, "Viewed activity logs (HTML)")
    return render(request, 'admin_panel/activity_logs.html', {'logs': logs})

# ✅ View All Users
@user_passes_test(lambda u: u.is_superuser)
def user_list(request):
    users = User.objects.all()
    return render(request, 'admin_dashboard/user_list.html', {'users': users})

# ✅ Add New User
@user_passes_test(lambda u: u.is_superuser)
def add_user(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            log_activity(request.user, f"Created user: {new_user.username}")
            return redirect('user_list')
    else:
        form = UserCreationForm()
    return render(request, 'admin_dashboard/add_user.html', {'form': form})

# ✅ Edit Existing User
@user_passes_test(lambda u: u.is_superuser)
def edit_user(request, user_id):
    user_obj = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        form = UserChangeForm(request.POST, instance=user_obj)
        if form.is_valid():
            form.save()
            log_activity(request.user, f"Updated user: {user_obj.username}")
            return redirect('user_list')
    else:
        form = UserChangeForm(instance=user_obj)
    return render(request, 'admin_dashboard/edit_user.html', {'form': form, 'user_obj': user_obj})

# ✅ Delete User
@user_passes_test(lambda u: u.is_superuser)
def delete_user(request, user_id):
    user_obj = get_object_or_404(User, id=user_id)
    log_activity(request.user, f"Deleted user: {user_obj.username}")
    user_obj.delete()
    return redirect('user_list')
