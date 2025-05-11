class User(object):
    def __init__(self, user_id, email, name):
        self.user_id = user_id
        self.email = email
        self.name = name

def make_user(user_id, email, name):
    user = User(user_id, email, name)
    return user