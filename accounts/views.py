from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import CreateUserForm
from django.contrib import messages

# Create your views here.

def register(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        form = CreateUserForm()
        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            print('____________________salom_____________________')
            if form.is_valid():
                print('_________________alik____________________')
                user = form.cleaned_data.get('username')
                messages.success(request, 'Account was created for ' + user)
                form.save()
                return redirect('login')

        context = {'form':form}
        return render(request=request, template_name='register.html', context=context)



def loginPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == 'POST':
            print(request.session.test_cookie_worked(), '      ----------------')
            print(request.session.set_test_cookie(), '-------------------------------------------------')
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username = username, password = password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.info(request, 'Username OR Password is incorrect')

        context = {}
        return render(request=request, template_name='login.html', context=context)


def logoutPage(request):
    logout(request)
    return redirect('home')

def account(request):
    return render(request=request, template_name='my-account.html')

