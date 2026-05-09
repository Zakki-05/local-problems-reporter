from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.http import JsonResponse
from .models import Issue, UserProfile
from .forms import IssueForm, UserRegistrationForm

def home(request):
    recent_issues = Issue.objects.select_related('user').order_by('-created_at')[:6]
    return render(request, 'issues/home.html', {'recent_issues': recent_issues})

@login_required
def report_issue(request):
    if request.method == 'POST':
        form = IssueForm(request.POST, request.FILES)
        if form.is_valid():
            issue = form.save(commit=False)
            issue.user = request.user
            issue.save()
            return redirect('issues_list')
    else:
        form = IssueForm()
    return render(request, 'issues/report.html', {'form': form})

def issues_list(request):
    issues = Issue.objects.select_related('user').order_by('-created_at')
    
    category = request.GET.get('category')
    if category:
        issues = issues.filter(category=category)
        
    status = request.GET.get('status')
    if status:
        issues = issues.filter(status=status)
        
    return render(request, 'issues/list.html', {'issues': issues})

def map_view(request):
    return render(request, 'issues/map.html')

def map_data(request):
    issues = Issue.objects.all()
    data = []
    for issue in issues:
        data.append({
            'id': issue.id,
            'title': issue.title,
            'category': issue.category,
            'status': issue.status,
            'lat': issue.latitude,
            'lng': issue.longitude,
            'url': f"/issue/{issue.id}/",
        })
    return JsonResponse(data, safe=False)

def issue_detail(request, pk):
    issue = get_object_or_404(Issue, pk=pk)
    return render(request, 'issues/detail.html', {'issue': issue})

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            phone = form.cleaned_data.get('phone_number')
            UserProfile.objects.create(user=user, phone_number=phone)
            login(request, user)
            return redirect('home')
    else:
        form = UserRegistrationForm()
    return render(request, 'registration/register.html', {'form': form})

@login_required
def dashboard(request):
    user_issues = Issue.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'issues/dashboard.html', {'user_issues': user_issues})

@login_required
def official_dashboard(request):
    if not request.user.is_staff:
        return redirect('home')
        
    if request.method == 'POST':
        issue_id = request.POST.get('issue_id')
        new_status = request.POST.get('status')
        if issue_id and new_status:
            issue = get_object_or_404(Issue, pk=issue_id)
            issue.status = new_status
            issue.save()
            return redirect('official_dashboard')
            
    issues = Issue.objects.select_related('user').order_by('-created_at')
    registered_users = User.objects.all().order_by('username')
    
    # Counting based on matching keys or bilingual strings
    pending_count = sum(1 for i in issues if i.status and 'Pending' in i.status)
    progress_count = sum(1 for i in issues if i.status and 'In Progress' in i.status)
    resolved_count = sum(1 for i in issues if i.status and 'Resolved' in i.status)
    
    context = {
        'issues': issues,
        'registered_users': registered_users,
        'pending_count': pending_count,
        'progress_count': progress_count,
        'resolved_count': resolved_count
    }
    return render(request, 'issues/official_dashboard.html', context)

def contact(request):
    return render(request, 'issues/contact.html')
def about(request):
    return render(request, 'issues/about.html')
