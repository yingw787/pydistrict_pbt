#!/usr/bin/env python3
#
# This file defines a basic password validator, kind of like what you might see
# in a production codebase.
#
# A password must be:
# - At least 8 characters long
# - Contains one special character (!@#$%^&*)
# - Contains at least one uppercase letter
# - Contains at least one lowercase letter
# - Contains at least one number

import string
import sys


def password_is_valid(password: str) -> bool:
    """
    @param password
    @return: password is valid
    """
    if len(password) < 8:
        return False

    if not any([c in password for c in "!@#$%^&*"]):
        return False

    if not any([c in password for c in string.ascii_lowercase]):
        return False

    if not any([c in password for c in string.ascii_uppercase]):
        return False

    if not any([c in password for c in string.digits]):
        return False

    return True


if __name__=='__main__':
    password = sys.argv[1]
    print(password_is_valid(password))
