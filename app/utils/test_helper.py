from rest_framework_simplejwt.tokens import RefreshToken


def get_tokens(user):
    refresh = RefreshToken.for_user(user)
    return str(refresh.access_token)


def mock_validate_email(email):
    return "DELIVERABLE" if email == "elfateh91@gmail.com" else "UNDELIVERABLE"
