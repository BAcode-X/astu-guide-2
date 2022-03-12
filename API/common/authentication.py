import jwt, datetime
from django.conf import settings
from rest_framework import exceptions
from rest_framework.authentication import BaseAuthentication
from core.models import User

# custom authentication methods
class JWTAuthentication(BaseAuthentication):
    def authenticate(self, request):
        is_admin = "api/admin" in request.path
        token = request.COOKIES.get("jwt")
        
        if not token:
            return None
        
        # decode the token
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            raise exceptions.AuthenticationFailed("unauthenticated")

        # check for the correct scope
        if (is_admin and payload["scope"] == "user") or (
            (not is_admin) and payload["scope"] == "admin"):
            raise exceptions.AuthenticationFailed("Invalid Scope!")

        user = User.objects.get(pk=payload["user_id"])

        if user is None:
            raise exceptions.AuthenticationFailed("User not Found!")

        return (user, None)

    @staticmethod
    def generate_jwt(id, scope):
        payload = {
            "user_id": id,
            "scope": scope,
            "exp": int(
                (datetime.datetime.utcnow() + datetime.timedelta(days=1)).timestamp()  # one day before expire
            ),
            "int": str(datetime.datetime.utcnow()),
        }
        # encode the payload and return it
        return jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")
