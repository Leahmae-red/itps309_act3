# profiles/forms.py
from django import forms
from .models import Profile, Post


class AvatarUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['avatar']

    def clean_avatar(self):
        avatar = self.cleaned_data.get('avatar')
        if avatar and avatar.size > 5 * 1024 * 1024:
            raise forms.ValidationError("Image file too large (max 5MB).")
        return avatar


class CoverPhotoForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['cover_photo']

    def clean_cover_photo(self):
        cover = self.cleaned_data.get('cover_photo')
        if cover and cover.size > 8 * 1024 * 1024:
            raise forms.ValidationError("Cover image too large (max 8MB).")
        return cover


class BioUpdateForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)

    class Meta:
        model = Profile
        fields = [
            'nickname', 'tagline', 'bio', 'thought_bubble',
            'location', 'education', 'social_handle',
            'lives_in', 'hometown', 'birthday', 'workplace'
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.user:
            self.fields['first_name'].initial = self.instance.user.first_name
            self.fields['last_name'].initial = self.instance.user.last_name

    def save(self, commit=True):
        profile = super().save(commit=False)
        user = profile.user
        user.first_name = self.cleaned_data['first_name'].strip()
        user.last_name = self.cleaned_data['last_name'].strip()
        if commit:
            user.save()
            profile.save()
        return profile


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['content', 'image']