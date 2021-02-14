from rest_framework.reverse import reverse

from GinderApp.models import MatchChat, Message


# Subscription swipes limits
def get_user_daily_limit(user):
    subscription = user.profile.subscription
    if subscription == 'default':
        return 20
    if subscription == 'silver':
        return 100
    if subscription == 'gold':
        return 99999
    else:
        return False


# is match ckecker
def is_match(user, post_author):
    user.profile.likes.add(post_author.pk)
    # if match:
    if user in post_author.likes.all():
        return True
    # else
    else:
        return False


# Creating match if is_match
def create_match(profile1, profile2, request):
    match = MatchChat.objects.create(user_profile1=profile1, user_profile2=profile2)
    Message.objects.create(chat=match, user=profile1, text="We've got match!")
    Message.objects.create(chat=match, user=profile2, text="We've got match!")
    return reverse('GinderApp:chat', args=[match.pk], request=request)
