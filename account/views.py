from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from .forms import LoginForm, UserCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserEditForm, ProfileEditForm
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from shop.utils import ajax_required
from .models import Contact
from actions.utils import create_action

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
            create_action(new_user, 'has created an account')
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
            create_action(request.user, 'has edited their profile.')
    else:
        userEditForm = UserEditForm(instance=request.user)
        profileEditForm = ProfileEditForm(instance=request.user.profile)
    return render(request, 'registration/editProfile.html', {'userEditForm': userEditForm, 'profileEditForm': profileEditForm})     

@login_required
def profile(request):
    return render(request, 'registration/profile.html', )

def userList(request):
    users = User.objects.filter(is_active=True)
    return render(request, 'user/list.html', {'section':'people', 'users':users})

def userDetail(request, username):
    user = get_object_or_404(User, username=username, is_active=True)
    return render(request, 'user/detail.html', {'section':'people', 'user':user})

@ajax_required
@require_POST
@login_required
def userFollow(request):
    user_id = request.POST.get('id')
    action = request.POST.get('action')
    if user_id and action:
        try:
            user = User.objects.get(id=user_id)
            if action == 'follow':
                Contact.objects.get_or_create(userFrom=request.user, userTo=user)
                create_action(request.user, 'is following', user)
            else:
                Contact.objects.filter(userFrom=request.user, userTo=user).delete()
            return JsonResponse({'status':'ok'})
        except User.DoesNotExist:
            return JsonResponse({'status':'ko'})
    return JsonResponse({'status':'ko'})