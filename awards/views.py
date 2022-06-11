from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from awards.models import AddProjectForm, Project
# Create your views here.

@login_required(login_url='/accounts/login/')
def homepage(request):
    project=Project.objects.all()
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
    return render(request,'index.html',{'form':form,'projects':project})