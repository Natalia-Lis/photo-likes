from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import CreateView
from .models import Photo, Comment
from .forms import *
from django.views import View


class IndexView(View): #główna
    def get(self, request):
        photos = Photo.objects.all().order_by('-creation_date')
        users = User.objects.all()
        len_of = len(photos)
        return render(request, 'base.html', {"photos":photos, "users":users, "len_of":len_of})



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


class AddUser(View): #add
    def get(self, request):
        form = AddUserForm()
        return render(request, 'add-user.html', {'form': form})

    def post(self, request):
        form = AddUserForm(request.POST)
        made_mistake = 'Pojawił się błąd - popraw dane'
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
        else:
            return render(request, 'add-user.html', {"made_mistake":made_mistake, 'form': form})


class EditUserView(View): #edit
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


class PasswordView(View): #change password
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



#



class DetailsView(View): #photo details, comments & votes
    def get(self, request, id):
        user = self.request.user
        form = AddCommentToPhotoForm()
        komentarze = Comment.objects.all().filter(about_id=id)
        users = User.objects.all()
        this_photo = Photo.objects.get(pk=id)
        z_vote = Vote.objects.all().filter(voting_photo_id=id).filter(voting_user=user.id)
        moj_if = Vote.objects.all().filter(voting_photo_id=id).filter(voting_user=user.id).exists()
        return render(request, 'photo-details.html', {
            'form': form,
            "komentarze": komentarze,
            "users": users,
            "this_photo": this_photo,
            "z_vote":z_vote,
            "user":user,
            "moj_if": moj_if,
        })
    def post(self, request, id):
        form = AddCommentToPhotoForm(request.POST)
        user = self.request.user
        komentarze = Comment.objects.all().filter(about_id=id)
        done = "Wykonano!"
        users = User.objects.all()

        photo_id = request.POST.get('photo_id') #
        like_or = request.POST.get('like')

        this_photo = Photo.objects.get(pk=id)
        moj_if = Vote.objects.filter(voting_user=user.id).exists()
        z_vote = Vote.objects.all().filter(voting_photo_id=id).filter(voting_user=user.id)

        if like_or == 'Polub to zdjęcie!':
            this_photo.votes += 1
            this_photo.save()
            if z_vote.exists():
                v1=Vote.objects.get(voting_photo_id=id)
                v1.like=True
                v1.save()
            else:
                v1=Vote(voting_photo_id=id)
                v1.like=True
                v1.save()
                v1.voting_user.add(user)
                v1.save()
            # return render(request, 'photo-details.html', {
            #     'form': form,
            #     "komentarze": komentarze,
            #     "done": done,
            #     "users": users,
            #     "this_photo":this_photo,
            #     "z_vote":z_vote,
            #     "user":user,
            #     "moj_if":moj_if,
            # })
            return redirect('photo-details', this_photo.id)

        elif like_or == 'Pokaż, że Ci się nie podoba':
            this_photo.votes -= 1
            this_photo.save()
            if z_vote.exists():
                v1=Vote.objects.get(voting_photo_id=id)
                v1.like=False
                v1.save()
            else:
                v1=Vote(voting_photo_id=id)
                v1.like=False
                v1.save()
                v1.voting_user.add(user)
                v1.save()
            # return render(request, 'photo-details.html', {
            #     'form': form,
            #     "komentarze": komentarze,
            #     "done": done,
            #     "users": users,
            #     "this_photo": this_photo,
            #     "z_vote": z_vote,
            #     "user": user,
            #     "moj_if": moj_if,
            # })
            return redirect('photo-details', this_photo.id)

        if form.is_valid():
            comment = form.cleaned_data['comment']
            komentarz = Comment.objects.create(comment=comment, about_id=this_photo.id, author=user)
            # return render(request, 'photo-details.html', {
            #     'form': form,
            #     "komentarze":komentarze,
            #     "this_photo":this_photo,
            #     "done": done,
            #     "users": users,
            #     "z_vote":z_vote,
            #     "user": user,
            #     "moj_if": moj_if,
            # })
            return redirect('photo-details', this_photo.id)


class AddPhotoView(CreateView): #add img
    model = Photo
    fields = ['path']
    def form_valid(self, form):
        user = self.request.user
        path = form.cleaned_data.get('path')
        create_ph = Photo.objects.create(path=path, photo=user)
        Vote.objects.create(voting_photo_id=create_ph.id)
        return redirect('/')


class UserPhotoView(View): #szczegóły z
    def get(self, request):
        user = self.request.user
        user_photos = Photo.objects.all().filter(photo_id=user.id)
        return render(request, 'user-photos.html', {"user_photos":user_photos})


class UserIdShowView(View): #received user
    def get(self, request,id):
        this_user_photos = Photo.objects.all().filter(photo=id)
        this_user = User.objects.get(id=id)

        return render(request, 'this-user.html', {
            "this_user":this_user,
            "this_user_photos":this_user_photos,
}
            )


class AllUserView(View): #all -list
    def get(self, request):
        all = User.objects.all()
        return render(request, 'all-users.html', {"all":all})




