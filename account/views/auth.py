import datetime as dt

from typing import final, override

from dmr.plugins.pydantic import PydanticSerializer
from dmr.security.jwt.views import (
    ObtainTokensSyncController,
    ObtainTokensPayload,
    ObtainTokensResponse,
)


@final
class ObtainAccessAndRefreshJwtController(
    ObtainTokensSyncController[
        PydanticSerializer,
        ObtainTokensPayload,
        ObtainTokensResponse,
    ],
):
    @override
    def convert_auth_payload(self, payload: ObtainTokensPayload) -> ObtainTokensPayload:
        return payload

    @override
    def make_api_response(self) -> ObtainTokensResponse:
        now = dt.datetime.now(dt.UTC)
        return {
            "access_token": self.create_jwt_token(
                expiration=now + self.jwt_expiration,
                token_type="access",
            ),
            "refresh_token": self.create_jwt_token(
                expiration=now + self.jwt_refresh_expiration,
                token_type="refresh",
            ),
        }
