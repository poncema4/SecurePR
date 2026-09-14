from werkzeug.security import generate_password_hash

PASSWORD_HASH = generate_password_hash("example-not-a-secret")
