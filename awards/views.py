from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UpdateUserForm, UpdateUserProfileForm
from .models import AddProjectForm, Project, Rating, RatingForm, UpdateProfileForm
from django.contrib.auth.models import User
# Create your views here.

@login_required(login_url='/accounts/login/')
def homepage(request):
    project=Project.objects.all()

    return render(request,'index.html',{'projects':project})

@login_required(login_url='/accounts/login/')
def add_project(request):
  if request.method=='POST':
        current_user=request.user
        form=AddProjectForm(request.POST,request.FILES)
        if form.is_valid():
            project=form.save(commit=False)
            project.user=current_user
            project.save()
            messages.success(request,('Project was posted successfully!'))
            return redirect('landing')
  else:
            form=AddProjectForm()
  return render(request,'add_project.html',{'form':form})  

@login_required(login_url='login')
def profile(request, username):
    return render(request, 'profile.html')


def user_profile(request, username):
    user_prof = get_object_or_404(User, username=username)
    if request.user == user_prof:
        return redirect('profile', username=request.user.username)
    params = {
        'user_prof': user_prof,
    }
    return render(request, 'userprofile.html', params)


@login_required(login_url='login')
def edit_profile(request, username):
    user = User.objects.get(username=username)
    if request.method == 'POST':
        user_form = UpdateUserForm(request.POST, instance=request.user)
        prof_form = UpdateProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if user_form.is_valid() and prof_form.is_valid():
            user_form.save()
            prof_form.save()
            return redirect('profile', user.username)
    else:
        user_form = UpdateUserForm(instance=request.user)
        prof_form = UpdateUserProfileForm(instance=request.user.profile)
    params = {
        'user_form': user_form,
        'prof_form': prof_form
    }
    return render(request, 'editprofile.html', params)


@login_required(login_url='/accounts/login/')
def project_details(request, project_id):
  
  form = RatingForm(request.POST)
  try:
    project_details = Project.objects.get(pk = project_id)
    project_rates = Rating.objects.filter(project__id=project_id).all()
  except Project.DoesNotExist:
    raise Http404
  
  return render(request, 'pro_details.html', {"details":project_details, "rates":project_rates, "form":form})




@login_required(login_url='/accounts/login/')
def submit_rates(request, project_id):
  url = request.META.get('HTTP_REFERER')
  if request.method == 'POST':
    try:
      rating = Rating.objects.get(user__id=request.user.id, project__id=project_id)
      form = RatingForm(request.POST, instance=rating)
      form.save()
      messages.success(request, 'Your rating has been updated')
      return redirect(url)
    except Rating.DoesNotExist:
      form = RatingForm(request.POST)
      if form.is_valid():
        # rating_data = Votes()
        design = form.cleaned_data.get('design')
        userbility = form.cleaned_data.get('userbility')
        content = form.cleaned_data.get('content')
        # form.instance.Avg_score = design_score
        form.instance.project_id=project_id
        form.instance.user_id = request.user.id
        form.save()
        messages.success(request, 'Your rating has been posted')
        
        return redirect(url)
      
      
@login_required(login_url='/accounts/login/')
def search_results(request):
  form=AddProjectForm()
  if 'search' in request.GET and request.GET['search']:
    
    title_search = request.GET.get('search')
    print(title_search)
    searched_projects = Project.search_by_title(title_search)
  
    message = f"{title_search}"
    return render(request, 'search.html', {"message":message, "projects":searched_projects,"form":form})
  else:
    message = "You have not yet made a search"

    return render(request, 'search.html', {"message":message})
      