// static/js/profile.js
document.addEventListener('DOMContentLoaded', () => {
    const avatarModal = document.getElementById('avatarModal');
    const bioModal = document.getElementById('bioModal');
    const fileInput = document.getElementById('id_avatar');
    const previewImg = document.getElementById('avatarPreviewImg');
    const avatarForm = document.getElementById('avatarUploadForm');
    const bioForm = document.getElementById('bioUpdateForm');
    const errorMsg = document.getElementById('uploadErrorMsg');
    const coverInput = document.getElementById('coverFileInput');
    const coverImg = document.getElementById('coverPhotoImg');

    document.getElementById('openAvatarModalBtn').addEventListener('click', () => {
        errorMsg.textContent = '';
        avatarModal.classList.add('show');
    });

    const openBioModal = () => bioModal.classList.add('show');
    document.getElementById('openBioModalBtn').addEventListener('click', openBioModal);
    document.getElementById('editDetailsIconBtn').addEventListener('click', openBioModal);

    document.getElementById('focusPostBtn').addEventListener('click', () => {
        const input = document.getElementById('postInputBox');
        input.scrollIntoView({ behavior: 'smooth', block: 'center' });
        input.focus();
    });

    document.querySelectorAll('[data-close]').forEach(btn => {
        btn.addEventListener('click', () => {
            document.getElementById(btn.dataset.close).classList.remove('show');
        });
    });

    // Cover photo upload
    document.getElementById('openCoverBtn').addEventListener('click', () => coverInput.click());

    coverInput.addEventListener('change', async (e) => {
        const file = e.target.files[0];
        if (!file) return;

        const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
        const formData = new FormData();
        formData.append('cover_photo', file);

        const response = await fetch(COVER_UPLOAD_URL, {
            method: 'POST',
            headers: { 'X-CSRFToken': csrfToken },
            body: formData,
        });
        const data = await response.json();

        if (response.ok && data.status === 'success') {
            coverImg.src = `${data.cover_url}?t=${Date.now()}`;
            coverImg.classList.remove('is-hidden');
            showToast(data.message);
        } else {
            showToast('Could not upload cover photo.');
        }
    });

    // Avatar preview & upload
    fileInput.addEventListener('change', (e) => {
        const file = e.target.files[0];
        if (!file) return;
        const reader = new FileReader();
        reader.onload = (event) => {
            previewImg.src = event.target.result;
        };
        reader.readAsDataURL(file);
    });

    avatarForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const saveBtn = document.getElementById('saveAvatarBtn');
        saveBtn.disabled = true;
        saveBtn.textContent = 'Saving...';

        const formData = new FormData(avatarForm);

        try {
            const response = await fetch(AVATAR_UPLOAD_URL, {
                method: 'POST',
                body: formData,
            });
            const data = await response.json();

            if (response.ok && data.status === 'success') {
                const newUrl = `${data.avatar_url}?t=${Date.now()}`;
                document.querySelectorAll('.js-avatar-sync').forEach(img => {
                    img.src = newUrl;
                });
                avatarModal.classList.remove('show');
                showToast(data.message);
            } else {
                const parsedErrors = JSON.parse(data.errors);
                errorMsg.textContent = parsedErrors.avatar[0].message;
            }
        } catch (err) {
            errorMsg.textContent = 'Upload failed. Please try again.';
        } finally {
            saveBtn.disabled = false;
            saveBtn.textContent = 'Save';
        }
    });

    // Save profile name, nickname, bio, and personal details
    bioForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const formData = new FormData(bioForm);

        const response = await fetch(BIO_UPDATE_URL, {
            method: 'POST',
            body: formData,
        });
        const data = await response.json();

        if (response.ok && data.status === 'success') {
            document.querySelectorAll('.js-fullname-sync').forEach(el => {
                el.textContent = data.full_name;
            });
            document.title = `${data.full_name} | Facebook`;

            const nicknameEl = document.getElementById('displayNickname');
            if (nicknameEl) {
                nicknameEl.textContent = data.nickname ? `(${data.nickname})` : '';
            }

            const bubbleEl = document.getElementById('displayThoughtBubble');
            if (bubbleEl) {
                bubbleEl.textContent = data.thought_bubble;
            }

            document.getElementById('displayTagline').textContent = data.tagline;
            document.getElementById('displayBio').textContent = data.bio;
            document.getElementById('displayLocation').textContent = data.location;
            document.getElementById('displayEducation').textContent = data.education;

            const handleEl = document.getElementById('displayHandle');
            if (handleEl) {
                handleEl.innerHTML = `<i class="fa-brands fa-instagram"></i> ${data.social_handle}`;
            }

            document.getElementById('displayLivesIn').textContent = data.lives_in;
            document.getElementById('displayHometown').textContent = data.hometown;
            document.getElementById('displayBirthday').textContent = data.birthday;

            bioModal.classList.remove('show');
            showToast('Profile details updated!');
        }
    });

    // Like toggle
    document.querySelectorAll('.js-like-btn').forEach(btn => {
        btn.addEventListener('click', async () => {
            const postId = btn.dataset.postId;
            const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

            const response = await fetch(`/api/like/${postId}/`, {
                method: 'POST',
                headers: { 'X-CSRFToken': csrfToken }
            });
            const data = await response.json();

            if (data.status === 'success') {
                document.getElementById(`like-count-${postId}`).textContent = data.total_likes;
                btn.classList.toggle('liked', data.liked);
            }
        });
    });

    function showToast(message) {
        const toast = document.getElementById('toast');
        toast.textContent = message;
        toast.classList.add('show');
        setTimeout(() => toast.classList.remove('show'), 3000);
    }
});