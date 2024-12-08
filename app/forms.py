from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import UploadedFile

from app.models import Profile, Question, Tag


class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your username'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter your password'})
    )
    confirm = forms.BooleanField(widget=forms.CheckboxInput)

    def clean_username(self):
        return self.cleaned_data['username'].strip()


class SignupForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your username'}),
        min_length=3,
        max_length=50
    )
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter your email'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter your password'}),
        min_length=8
    )
    password_confirmation = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Repeat your password'})
    )
    avatar = forms.ImageField(required=False)

    def clean_username(self):
        username = self.cleaned_data['username'].strip()
        if User.objects.filter(username=username).exists():
            raise ValidationError('User with that username already exists.')
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise ValidationError('User with that email already exists.')
        return email

    def clean_password_confirmation(self):
        password = self.cleaned_data.get('password')
        password_confirmation = self.cleaned_data.get('password_confirmation')
        if password and password_confirmation and password != password_confirmation:
            raise ValidationError('Passwords do not match.')
        return password_confirmation

    def clean_avatar(self):
        avatar = self.cleaned_data.get('avatar')
        if avatar and isinstance(avatar, UploadedFile):
            if avatar.size > 5 * 1024 * 1024:
                raise ValidationError('Image file too large ( > 5mb )')
        return avatar

    def save(self):
        user = User.objects.create_user(
            username=self.cleaned_data['username'],
            email=self.cleaned_data['email'],
            password=self.cleaned_data['password']
        )
        avatar = self.cleaned_data.get('avatar')
        Profile.objects.create(user=user, avatar=avatar)
        return user


class ProfileForm(forms.ModelForm):
    username = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your new username'}),
        min_length=3,
        max_length=50
    )
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter your new email'})
    )
    password = forms.CharField(
        required=False,
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter your new password'}),
        min_length=8
    )
    password_confirmation = forms.CharField(
        required=False,
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Repeat your password'})
    )

    avatar = forms.ImageField(required=False, widget=forms.FileInput)

    class Meta:
        model = Profile
        fields = ['username', 'email', 'password', 'password_confirmation', 'avatar']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if self.user:
            self.fields['email'].initial = self.user.email
            self.fields['username'].initial = self.user.username
            # if self.user.profile.avatar:
            #     self.fields['avatar'].initial = self.user.profile.avatar

    def clean_username(self):
        username = self.cleaned_data.get('username').strip()
        if User.objects.filter(username=username).exclude(pk=self.user.pk).exists():
            raise ValidationError('User with that username already exists.')
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email and User.objects.filter(email=email).exclude(pk=self.user.pk).exists():
            raise ValidationError('User with that email already exists.')
        return email

    def clean_avatar(self):
        avatar = self.cleaned_data.get('avatar')
        if avatar and isinstance(avatar, UploadedFile):
            if avatar.size > 5 * 1024 * 1024:
                raise ValidationError('Image file too large ( > 5mb )')
        return avatar

    def clean_password_confirmation(self):
        password = self.cleaned_data.get('password')
        password_confirmation = self.cleaned_data.get('password_confirmation')

        if password and not password_confirmation:
            raise ValidationError('Please confirm your password.')
        elif password_confirmation and not password:
            raise ValidationError('Please enter a new password.')
        elif password and password_confirmation and password != password_confirmation:
            raise ValidationError('Passwords do not match.')

        return password_confirmation

    def save(self, commit=True):
        profile = super().save(commit=False)
        user = self.user

        user.username = self.cleaned_data.get('username')
        user.email = self.cleaned_data.get('email')

        if self.cleaned_data.get('password'):
            user.set_password(self.cleaned_data.get('password'))

        new_avatar = self.cleaned_data.get('avatar')
        if new_avatar:
            profile.avatar = new_avatar

        if commit:
            user.save()
            profile.save()

        return profile


class AskForm(forms.ModelForm):
    title = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter question title'})
    )
    content = forms.CharField(
        required=True,
        widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter question content', 'rows': '5'})
    )
    tags = forms.CharField(
        help_text="Enter up to 5 tags, separated by commas. Example: python, django, forms",
        required=False
    )

    class Meta:
        model = Question
        fields = ['title', 'content', 'tags']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

    def clean_title(self):
        title = self.cleaned_data.get('title')
        if len(title) < 10:
            raise ValidationError("Title must be at least 10 characters long.")
        return title

    def clean_content(self):
        content = self.cleaned_data.get('content')
        if len(content) < 30:
            raise ValidationError("Content must be at least 30 characters long.")
        return content

    def clean_tags(self):
        tags = self.cleaned_data.get('tags')
        if tags:
            tags = [tag.strip() for tag in tags.split(',') if tag.strip()]
            if len(tags) > 5:
                raise ValidationError("You can specify at most 5 tags.")
            for tag in tags:
                if len(tag) > 100:
                    raise ValidationError(f"Tag '{tag}' is too long (max 100 characters).")
            return tags
        return []

    def save(self, commit=True):
        question = Question(
            author=self.user,
            title=self.cleaned_data['title'],
            content=self.cleaned_data['content']
        )
        if commit:
            question.save()
            tags = set(self.cleaned_data.get('tags', []))
            print(f"tags: {tags}")
            for tag_name in tags:
                tag, created = Tag.objects.get_or_create(name=tag_name)
                question.tags.add(tag)
        return question
