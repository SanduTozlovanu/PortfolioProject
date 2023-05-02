import jwt
from datetime import datetime, timezone, timedelta


class JWTHandler:
    def __init__(self, secret_key: str):
        self.secret_key = secret_key

    def is_token_valid(self, token: str) -> bool:
        try:
            decoded_token = jwt.decode(token, self.secret_key, algorithms=['HS256'])
        except jwt.exceptions.InvalidTokenError:
            # If the decoding fails, the token is invalid
            return False
        exp_timestamp = decoded_token.get('exp', None)
        if exp_timestamp is None:
            return False  # token has no expiration time
        # convert to UTC datetime object
        exp_datetime = datetime.fromtimestamp(exp_timestamp, tz=timezone.utc)
        if datetime.now(timezone.utc) > exp_datetime:
            raise jwt.ExpiredSignatureError("Expired token")
        return True

    def create_jwt_token(self, email: str) -> str:
        # set expiration time to 1 hour from now
        expiration_time = datetime.utcnow() + timedelta(hours=1)
        payload = {'email': email, 'exp': expiration_time}
        token = jwt.encode(payload, self.secret_key, algorithm='HS256')
        return token

    def get_mail_from_jwt(self, token: str) -> str | None:
        try:
            # Decode the token using the secret key
            decoded_token = jwt.decode(token, self.secret_key, algorithms=['HS256'])
            # Extract the user_id claim from the decoded token
            email = decoded_token.get('email')
            return email
        except jwt.exceptions.InvalidTokenError:
            # If the decoding fails, return None
            return None
