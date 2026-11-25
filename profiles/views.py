# profiles/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.views.decorators.http import require_POST
from .models import Profile, Post
from .forms import AvatarUpdateForm, CoverPhotoForm, BioUpdateForm, PostForm


def get_active_user():
    user, _ = User.objects.get_or_create(
        username='leah_red',
        defaults={'first_name': 'Leah Mae', 'last_name': 'Red', 'email': 'leah@example.com'}
    )
    return user


def profile_view(request, username=None):
    if username:
        profile_user = get_object_or_404(User, username=username)
    else:
        profile_user = request.user if request.user.is_authenticated else get_active_user()

    profile = profile_user.profile
    posts = profile_user.posts.all()

    if request.method == 'POST' and 'create_post' in request.POST:
        post_form = PostForm(request.POST, request.FILES)
        if post_form.is_valid():
            new_post = post_form.save(commit=False)
            new_post.author = profile_user
            new_post.save()
            return redirect('profile_home')
    else:
        post_form = PostForm()

    context = {
        'profile_user': profile_user,
        'profile': profile,
        'posts': posts,
        'post_form': post_form,
        'bio_form': BioUpdateForm(instance=profile),
    }
    return render(request, 'profiles/profile.html', context)


@require_POST
def update_avatar_ajax(request):
    user = request.user if request.user.is_authenticated else get_active_user()
    form = AvatarUpdateForm(request.POST, request.FILES, instance=user.profile)

    if form.is_valid():
        profile = form.save()
        return JsonResponse({
            'status': 'success',
            'avatar_url': profile.avatar.url,
            'message': 'Profile picture updated!'
        })
    return JsonResponse({'status': 'error', 'errors': form.errors.as_json()}, status=400)


@require_POST
def update_cover_ajax(request):
    user = request.user if request.user.is_authenticated else get_active_user()
    form = CoverPhotoForm(request.POST, request.FILES, instance=user.profile)

    if form.is_valid():
        profile = form.save()
        return JsonResponse({
            'status': 'success',
            'cover_url': profile.cover_photo.url,
            'message': 'Cover photo updated!'
        })
    return JsonResponse({'status': 'error', 'errors': form.errors.as_json()}, status=400)


@require_POST
def update_bio_ajax(request):
    user = request.user if request.user.is_authenticated else get_active_user()
    form = BioUpdateForm(request.POST, instance=user.profile)

    if form.is_valid():
        profile = form.save()
        full_name = profile.user.get_full_name() or profile.user.username
        return JsonResponse({
            'status': 'success',
            'full_name': full_name,
            'first_name': profile.user.first_name,
            'nickname': profile.nickname,
            'tagline': profile.tagline,
            'bio': profile.bio,
            'thought_bubble': profile.thought_bubble,
            'location': profile.location,
            'education': profile.education,
            'social_handle': profile.social_handle,
            'lives_in': profile.lives_in,
            'hometown': profile.hometown,
            'birthday': profile.birthday,
        })
    return JsonResponse({'status': 'error', 'errors': form.errors.as_json()}, status=400)


@require_POST
def toggle_like_ajax(request, post_id):
    user = request.user if request.user.is_authenticated else get_active_user()
    post = get_object_or_404(Post, id=post_id)

    if user in post.likes.all():
        post.likes.remove(user)
        liked = False
    else:
        post.likes.add(user)
        liked = True

    return JsonResponse({
        'status': 'success',
        'liked': liked,
        'total_likes': post.total_likes()
    })