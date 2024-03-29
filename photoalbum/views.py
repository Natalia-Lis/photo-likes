from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import CreateView
from django.views import View

from .models import Photo, Comment, Vote
from .forms import LoginForm, AddUserForm, EditUserForm, PasswordViewForm, AddCommentToPhotoForm, AddPhotoOnMainSiteForm


class IndexView(LoginRequiredMixin, View):

    def get(self, request):
        form = AddPhotoOnMainSiteForm()
        photos = Photo.objects.all().order_by('-creation_date')
        users = User.objects.all()
        len_of = len(photos)
        return render(request, 'base.html', {"photos":photos, "users":users,
                                             "len_of":len_of, "form":form})

    def post(self, request):
        form = AddPhotoOnMainSiteForm(request.POST)
        user = self.request.user
        if form.is_valid():
            path = form.cleaned_data['path']
            Photo.objects.create(path=path, photo_id=user.id)
            return redirect('/')


class ShowUserView(LoginRequiredMixin, View):

    def get(self, request):
        user = self.request.user
        user_info = User.objects.filter(email=user.email)
        return render(request, 'show-user.html', {"user_info":user_info})


class AddUser(View):

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
            password_message = 'Hasło musi być podane dwukrotnie takie samo!'
            check_if_used = User.objects.filter(email=email)
            check_if_used_2 = User.objects.filter(username=username)
            already_used = 'Email zajęty!'
            already_used2 = 'Nazwa użytkownika zajęta!'
            if check_if_used:
                return render(request, 'add-user.html', {"already_used":already_used, 'form':form})
            elif check_if_used_2:
                return render(request, 'add-user.html', {"already_used2":already_used2, 'form':form})
            else:
                if password == password2:
                    User.objects.create_user(
                        username=username,
                        email=email,
                        password=password,
                    )
                    return redirect('index')
                else:
                    return render(request, 'add-user.html', {"password_message":password_message,
                                                             'form':form})
        else:
            return render(request, 'add-user.html', {"made_mistake":made_mistake, 'form':form})


class EditUserView(LoginRequiredMixin, View):

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
            form.save()
            return redirect('show-user')


class PasswordView(LoginRequiredMixin, View):

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
                return HttpResponse('Hasło musi być podane dwukrotnie takie samo!')


class PasswordChangedView(View): #pass changed, needed login

    def get(self, request):
        changed = "Hasło zmienione. Powinieneś teraz się nim zalogować. Przejdż do strony logowania."
        return render(request, 'test.html', {"changed":changed})


class DeleteUser(LoginRequiredMixin, View):

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


class DetailsView(LoginRequiredMixin, View): #photo details, comments & votes

    def get(self, request, id):
        user = self.request.user
        form = AddCommentToPhotoForm()
        comments = Comment.objects.filter(about_id=id).order_by('when')
        users = User.objects.all()
        this_photo = Photo.objects.get(pk=id)
        z_vote = Vote.objects.filter(voting_photo_id=id).filter(voting_user=user.id)
        mine_if = Vote.objects.filter(voting_photo_id=id).filter(voting_user=user.id).exists()
        return render(request, 'photo-details.html', {"mine_if": mine_if, "comments": comments,
                                                      "users": users, "this_photo": this_photo,
                                                      "z_vote":z_vote, "user":user, 'form': form,
                                                     })

    def post(self, request, id):
        form = AddCommentToPhotoForm(request.POST)
        user = self.request.user
        comments = Comment.objects.filter(about_id=id)
        done = "Wykonano!"
        users = User.objects.all()
        photo_id = request.POST.get('photo_id')
        like_or = request.POST.get('like')
        this_photo = Photo.objects.get(pk=id)
        mine_if = Vote.objects.filter(voting_user=user.id).exists()
        z_vote = Vote.objects.filter(voting_photo_id=id).filter(voting_user=user.id)

        if like_or == 'Polub to zdjęcie!':
            this_photo.votes += 1
            this_photo.save()
            if z_vote.exists():
                v1 = Vote.objects.get(voting_photo_id=id, voting_user=user)
                v1.like = True
                v1.save()
            else:
                v1 = Vote.objects.create(voting_photo_id=id)
                v1.like = True
                v1.save()
                v1.voting_user.add(user)
                v1.save()
            return redirect('photo-details', this_photo.id)
        elif like_or == 'Pokaż, że Ci się nie podoba':
            this_photo.votes -= 1
            this_photo.save()
            if z_vote.exists():
                v1 = Vote.objects.get(voting_photo_id=id, voting_user=user)
                v1.like = False
                v1.save()
            else:
                v1 = Vote.objects.create(voting_photo_id=id)
                v1.like = False
                v1.save()
                v1.voting_user.add(user)
                v1.save()
            return redirect('photo-details', this_photo.id)
        if form.is_valid():
            comment = form.cleaned_data['comment']
            Comment.objects.create(comment=comment, about_id=this_photo.id, author=user)
            return redirect('photo-details', this_photo.id)


class AddPhotoView(LoginRequiredMixin, CreateView):
    model = Photo
    fields = ['path']

    def form_valid(self, form):
        user = self.request.user
        path = form.cleaned_data.get('path')
        create_ph = Photo.objects.create(path=path, photo=user)
        Vote.objects.create(voting_photo_id=create_ph.id)
        return redirect('/')


class UserPhotoView(LoginRequiredMixin, View):

    def get(self, request):
        user = self.request.user
        user_photos = Photo.objects.filter(photo_id=user.id)
        return render(request, 'user-photos.html', {"user_photos":user_photos})


class UserIdShowView(LoginRequiredMixin, View):

    def get(self, request, id):
        this_user_photos = Photo.objects.filter(photo=id)
        this_user = User.objects.get(id=id)
        return render(request, 'this-user.html', {"this_user":this_user,
                                                  "this_user_photos":this_user_photos,
                                                  })


class AllUserView(LoginRequiredMixin, View):

    def get(self, request):
        all = User.objects.all()
        return render(request, 'all-users.html', {"all":all})


class DeletePhoto(LoginRequiredMixin, View):

    def get(self, request, id):
        user = self.request.user
        return render(request, 'photo_confirm_delete.html', {"user":user})

    def post(self, request, id):
        choice_made = request.POST.get('deletion')
        if choice_made == 'YES':
            delete_photo = Photo.objects.get(id=id)
            delete_photo.delete()
            return redirect('user-photos')
        elif choice_made != 'YES':
            return redirect('user-photos')