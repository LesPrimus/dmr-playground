import base64
import datetime as dt
import json
import secrets
import uuid

from django.conf import settings
from django.http import JsonResponse
from django.urls import reverse
from django.views import View

from authlib.integrations.django_client import OAuthError

from account.models import User
from account.oauth import oauth
from dmr.security.jwt.token import JWToken

"""
Before testing, you need a Google OAuth app. Go to https://console.cloud.google.com/ → APIs & Services → Credentials → Create OAuth 2.0 Client ID:                                                                          
  - Application type: Web application                                                                                                                                                                                           
  - Authorized redirect URI: http://localhost:8000/account/auth/google/callback/
                                                                                                                                                                                                                                
  Then export the credentials:                                                                                                                                                                                                
  export GOOGLE_CLIENT_ID=your-client-id                                                                                                                                                                                        
  export GOOGLE_CLIENT_SECRET=your-client-secret                                                                                                                                                                              
                                                                                                                                                                                                                                
  One note: Authlib uses the Django session to store the state nonce between the two requests. The session middleware is already in your stack, so it works out of the box — but if you're testing with a plain HTTP client (not
   a browser), you'll need to persist the session cookie across the two requests.                                                                                                                                               
   
"""


def _make_jwt(user: User, token_type: str, expiration: dt.timedelta) -> str:
    now = dt.datetime.now(dt.UTC)
    return JWToken(
        sub=str(user.pk),
        exp=now + expiration,
        jti=uuid.uuid4().hex,
        extras={"type": token_type},
    ).encode(secret=settings.SECRET_KEY, algorithm="HS256")


def _encode_state(data: dict) -> str:
    payload = {**data, "nonce": secrets.token_urlsafe(16)}
    return base64.urlsafe_b64encode(json.dumps(payload).encode()).decode()


def _decode_state(raw: str) -> dict:
    return json.loads(base64.urlsafe_b64decode(raw))


class GoogleLoginView(View):
    def get(self, request):
        redirect_uri = request.build_absolute_uri(reverse("account:google_callback"))
        state = _encode_state({"next": request.GET.get("next", "/")})
        return oauth.google.authorize_redirect(request, redirect_uri, state=state)


class GoogleCallbackView(View):
    def get(self, request):
        raw_state = request.GET.get("state", "")
        try:
            state_data = _decode_state(raw_state)
        except Exception:
            return JsonResponse({"error": "Invalid state"}, status=400)

        try:
            token = oauth.google.authorize_access_token(request)
        except OAuthError as exc:
            return JsonResponse({"error": str(exc)}, status=400)

        userinfo = token.get("userinfo")
        if not userinfo or not userinfo.get("email"):
            return JsonResponse({"error": "No email returned by provider"}, status=400)

        email = userinfo["email"]
        user, _ = User.objects.get_or_create(
            email=email,
            defaults={"username": email},
        )

        return JsonResponse(
            {
                "access_token": _make_jwt(user, "access", dt.timedelta(days=1)),
                "refresh_token": _make_jwt(user, "refresh", dt.timedelta(days=10)),
                "next": state_data.get("next", "/"),
            }
        )
