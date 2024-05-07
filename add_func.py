import base64
from datetime import datetime, timedelta
import secrets
import string
import hashlib


def generate_random_string(length):
    possible_chars = string.ascii_letters + string.digits
    random_string = ''.join(secrets.choice(possible_chars) for _ in range(length))
    return random_string


def sha256(plain):
    data = plain.encode("utf-8")
    hash_object = hashlib.sha256()
    hash_object.update(data)
    return hash_object.digest()


def base64encode(input_data):
    encoded_data = base64.b64encode(input_data)
    encoded_string = encoded_data.decode('utf-8').replace('+', '-').replace('/', '_').rstrip('=')
    return encoded_string


def validate_date(date):
    min_date_possible = datetime(1958, 8, 4).date()
    max_date_possible = datetime.now().date() - timedelta(days=1)
    try:
        entered_date = datetime.strptime(date, "%Y-%m-%d").date()
    except ValueError:
        return False

    if min_date_possible <= entered_date <= max_date_possible:
        return True
    else:
        return False
