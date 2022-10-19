from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm

def register(request):
    """Register new"""
    if request.method != 'POST':
        form = UserCreationForm() #Blank form
    else:
        form = UserCreationForm(data=request.POST) #Completed form
        if form.is_valid():
            new_user = form.save()
            login(request, new_user)
            return redirect('journals:index')

    #Blank or invalid
    context = {'form':form}
    return render(request, 'registration/register.html', context)