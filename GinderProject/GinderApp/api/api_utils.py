from GinderApp.models import MatchChat

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
# def create_match(profile1, profile2)