from users.models import User

def add_user(user_id, user_name):
    """ Adds user"""
    user = User(user_id=user_id, user_name=user_name)
    user.save()

def check_user_status_and_add(user_id, user_name):
    """ Check whether user exists and and active , if not adds and chanegs status"""
    user_details = User.objects.filter(user_id=user_id)
    if user_details:
        is_active = user_details[0].is_active
        if not is_active:
            user_details.update(is_active=True)
    else:
        add_user(user_id, user_name)

def get_user(user_id):
    """ Returns user details from user id"""
    res = User.objects.filter(user_id=user_id).values()
    return res and res[0] or {}

def disable_user(user_id):
    user_details = User.objects.filter(user_id=user_id)
    if user_details:
        user_details.update(is_active=False)
