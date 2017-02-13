from .models import Profile

def save_avatar(backend, user, response, *args, **kwargs):
    try:
        profile = Profile.objects.get(user_id=user.id)
    except Profile.DoesNotExist:
        profile = Profile(user_id=user.id)

    if backend.name == 'facebook':
        profile.avatar = 'http://graph.facebook.com/%s/picture?type=large' % response.get('id')
        if not profile.email:
        	profile.email = response.get('email')
        	# or use => profile.email = response['email']
    profile.save()
