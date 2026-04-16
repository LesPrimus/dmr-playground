import datetime as dt

from django.http import JsonResponse
from django.urls import reverse
from django.views import View

from authlib.integrations.django_client import OAuthError
from dependency_injector.wiring import Provide, inject

from account.containers import Services
from account.models import User
from account.oauth import oauth
from account.services import OauthService

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


class GoogleLoginView(View):
    @inject
    def get(self, request, oauth_service: OauthService = Provide[Services.oauth]):
        redirect_uri = request.build_absolute_uri(reverse("account:google_callback"))
        state = oauth_service.encode_state({"next": request.GET.get("next", "/")})
        return oauth.google.authorize_redirect(request, redirect_uri, state=state)


class GoogleCallbackView(View):
    @inject
    def get(self, request, oauth_service: OauthService = Provide[Services.oauth]):
        raw_state = request.GET.get("state", "")
        try:
            state_data = oauth_service.decode_state(raw_state)
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
                "access_token": oauth_service.make_jwt(
                    user, "access", dt.timedelta(days=1)
                ),
                "refresh_token": oauth_service.make_jwt(
                    user, "refresh", dt.timedelta(days=10)
                ),
                "next": state_data.get("next", "/"),
            }
        )
