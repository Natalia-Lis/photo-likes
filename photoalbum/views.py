from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import Photo, Comment
from .forms import *

# Create your views here.
from django.views import View


class IndexView(View): #główna
    def get(self, request):
        photos = Photo.objects.all().order_by('-creation_date')
        users = User.objects.all()
        return render(request, 'base.html', {"photos":photos, "users":users})



class ShowUserView(View): #user zalog. info
    def get(self, request):
        user = self.request.user
        user_info = User.objects.all().filter(email=user.email)
        return render(request, 'show-user.html', {"user_info":user_info})



class LoginView(View): #logow.
    def get(self, request):
        form = LoginForm()
        return render(request, 'login.html', {'form': form})
    def post(self, request):
        form = LoginForm(request.POST)
        msg = "Coś poszło nie tak. Spróbuj zalogować się ponownie"
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(username=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('index')
            else:
                return render(request, 'login.html', {'msg': msg})
        else:
            return redirect('login')


class LogoutView(View): #wylog.
    def get(self, request):
        logout(request)
        return redirect('login')


class AddUser(View): #dodaj użytk.
    def get(self, request):
        form = AddUserForm()
        return render(request, 'add-user.html', {'form': form})

    def post(self, request):
        form = AddUserForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            password2 = form.cleaned_data['password2']
            email = form.cleaned_data['email']
            haslo='Hasło musi być podane dwukrotnie takie samo!'
            spr=User.objects.all().filter(email=email)
            spr2=User.objects.all().filter(username=username)
            already_used='Email zajęty!'
            already_used2='Nazwa użytkownika zajęta!'
            if spr:
                return render(request, 'add-user.html', {"already_used":already_used, 'form': form})
            elif spr2:
                return render(request, 'add-user.html', {"already_used2":already_used2, 'form': form})
            else:
                if password == password2:
                    User.objects.create_user(
                        username=username,
                        email=email,
                        password=password,
                    )
                    return redirect('index')
                else:
                    return render(request, 'add-user.html', {"haslo":haslo, 'form': form})


class EditUserView(View): #edycja
    def get(self, request):
        user = self.request.user
        user_to_change = User.objects.get(email=user.email)
        form = EditUserForm(instance=user_to_change)
        return render(request, 'edit-user.html', {"user_to_change":user_to_change, "form":form})
    def post(self, request):
        user = self.request.user
        user_to_change = User.objects.get(email=user.email)
        form = EditUserForm(request.POST, instance=user_to_change)
        if form.is_valid():
            username = form.cleaned_data['username']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            form.save()
            return redirect('show-user')


class PasswordView(View): #zmiana h.
    def get(self, request):
        user = self.request.user
        user_to_change = User.objects.get(email=user.email)
        form = PasswordViewForm()
        return render(request, 'password.html', {"user_to_change":user_to_change, "form":form})
    def post(self, request):
        user = self.request.user
        user_to_change = User.objects.get(email=user.email)
        form = PasswordViewForm(request.POST)
        if form.is_valid():
            password = form.cleaned_data['password']
            password2 = form.cleaned_data['password2']
            if password == password2:
                user_to_change.set_password(password)
                user_to_change.save()
                return redirect('password-changed')
            else:
                return HttpResponse('hasło musi być podane dwukrotnie takie samo!')


class PasswordChangedView(View): #pass changed, needed login
    def get(self, request):
        changed = "Hasło zmienione. Powinieneś teraz się nim zalogować. Przejdż do strony logowania."
        return render(request, 'test.html', {"changed":changed})


class DeleteUser(View): #deletion
    def get(self, request):
        user = self.request.user
        return render(request, 'user_confirm_delete.html', {"user":user})
    def post(self, request):
            choice_made = request.POST.get('deletion')
            if choice_made == 'YES':
                u = self.request.user
                user_to_delete = User.objects.get(email=u.email)
                user_to_delete.delete()
                return redirect('index')
            elif choice_made != 'YES':
                return redirect('show-user')










