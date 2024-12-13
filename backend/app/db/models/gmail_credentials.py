from datetime import datetime
from typing import List, Optional

<<<<<<< HEAD

=======
>>>>>>> main
class GmailCredentials:
    """
    Represents Gmail OAuth2 credentials for a user.

    Attributes:
        id (str): Unique identifier for the credentials.
        user_id (str): Identifier for the associated user.
        token (str): Access token for Gmail API.
        refresh_token (Optional[str]): Token to refresh the access token.
        token_uri (str): URI endpoint for token refresh.
        client_id (str): Client ID for the OAuth2 application.
        client_secret (str): Client secret for the OAuth2 application.
        scopes (List[str]): List of Gmail API scopes associated with the token.
        expiry (Optional[datetime]): Expiry date and time of the access token.
        created_at (datetime): Timestamp when the credentials were created.
        updated_at (datetime): Timestamp when the credentials were last updated.
    """
<<<<<<< HEAD

=======
>>>>>>> main
    def __init__(
        self,
        id: str,
        user_id: str,
        token: str,
        refresh_token: Optional[str],
        token_uri: str,
        client_id: str,
        client_secret: str,
        scopes: List[str],
        expiry: Optional[datetime],
        created_at: datetime = datetime.utcnow(),
<<<<<<< HEAD
        updated_at: datetime = datetime.utcnow(),
=======
        updated_at: datetime = datetime.utcnow()
>>>>>>> main
    ):
        self.id = id
        self.user_id = user_id
        self.token = token
        self.refresh_token = refresh_token
        self.token_uri = token_uri
        self.client_id = client_id
        self.client_secret = client_secret
        self.scopes = scopes
        self.expiry = expiry
        self.created_at = created_at
<<<<<<< HEAD
        self.updated_at = updated_at
=======
        self.updated_at = updated_at
>>>>>>> main
