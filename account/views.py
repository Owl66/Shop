from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from .forms import LoginForm, UserCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserEditForm, ProfileEditForm

def userLogin(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            #Check the user credential(records are in DB).
            user = authenticate(username=cd['username'], password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponse('User Login successfully.')
                else:
                    return HttpResponse('Account disabled.')
            else:
                return HttpResponse('Invalid Login')
    else:
        form = LoginForm()
    return render(request, 'account\sign_in.html', {'form': form})
                    

def register(request):
    if request.method == 'POST':
        user_form = UserCreationForm(request.POST)
        if user_form.is_valid():
             # Create a new user object but avoid saving it yet
            new_user = user_form.save(commit=False)
            # Set the chosen password 
            new_user.set_password(user_form.cleaned_data['password'])
            # Save the User object
            new_user.save()
            messages.success(request, f'Congratulation! Thank you for joining with us.')
            return redirect('account:login')
    else:
        user_form = UserCreationForm()
    return render(request, 'account/register.html', {'user_form': user_form})

@login_required
def deleteAccount(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            request.user.delete()
            return redirect("/")
    return render(request, 'registration/deleteAccount.html')

@login_required
def editProfile(request):
    if request.method == "POST":
        userEditForm = UserEditForm(data=request.POST, instance=request.user)
        profileEditForm = ProfileEditForm(data=request.POST, files=request.FILES, instance=request.user.profile)
        if userEditForm.is_valid() and profileEditForm.is_valid():
            profileEditForm.save()
            userEditForm.save()
    else:
        userEditForm = UserEditForm(instance=request.user)
        profileEditForm = ProfileEditForm(instance=request.user.profile)
    return render(request, 'registration/editProfile.html', {'userEditForm': userEditForm, 'profileEditForm': profileEditForm})     

@login_required
def profile(request):
    return render(request, 'registration/profile.html', )