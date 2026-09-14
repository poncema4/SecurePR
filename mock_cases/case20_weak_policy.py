MIN_PASSWORD_LENGTH = 4


def password_is_valid(password):
    return len(password) >= MIN_PASSWORD_LENGTH
