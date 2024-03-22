from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from channels.db import database_sync_to_async
from channels.middleware import BaseMiddleware
from django.conf import settings
from django.db import close_old_connections
import jwt

User = get_user_model()

class JWTAuthMiddleware(BaseMiddleware):
    def __init__(self, inner):
        self.inner = inner

    async def __call__(self, scope, receive, send):
        # Get the token from the query parameters
        token = scope.get("query_string", b"").decode("utf-8").split("=")[1]

        # Attempt to authenticate the user
        user = await self.get_user(token)

        # Add the user to the scope
        scope["user"] = user

        # Continue with the inner middleware/consumer
        return await self.inner(scope, receive, send)

    @database_sync_to_async
    def get_user(self, token):
        if token:
            try:
                # Decode and validate the JWT token
                payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
                user = User.objects.get(pk=payload["user_id"])
                return user
            except (jwt.ExpiredSignatureError, jwt.DecodeError, User.DoesNotExist):
                pass

        # If the token is invalid or the user doesn't exist, return an anonymous user
        return AnonymousUser()
