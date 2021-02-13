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
