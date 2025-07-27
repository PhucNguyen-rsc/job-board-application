import re

#validating emails - check if email has valid format
EMAIL_REGEX = r"^(?!.*\.\.)[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z]{2,}$" # nosec B105

def validate_email(email: str = None) -> bool:
    if email:
        return re.match(EMAIL_REGEX, email) is not None
    return False

#Ensure the password is at least 8 characters long and contains at least one uppercase, lowercase, and number
def is_valid_password(password: str) -> bool:
    password_regex = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[A-Za-z\d]{8,}$" # nosec B105
    return bool(re.match(password_regex, password))