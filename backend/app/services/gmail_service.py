"""
Gmail Integration Service

Handles Gmail API integration for fetching and parsing email data.

Classes:
- GmailService: Provides methods to connect to Gmail and extract email content.

Methods:
- connect_to_gmail: Establishes a connection with Gmail.
- fetch_emails: Retrieves emails matching specific criteria.
"""

from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from fastapi import HTTPException
import os
from app.db.database import database
from app.db.models.gmail_credentials import GmailCredentials
import base64
from datetime import datetime, timedelta
from app.core.config import settings
import re
from app.api.dependencies import get_current_user
import asyncio


class GmailService:
<<<<<<< HEAD
    SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]

=======
    SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
    
>>>>>>> main
    def __init__(self):
        self.creds = None
        self.service = None

<<<<<<< HEAD
=======
    
>>>>>>> main
    async def initialize_service(self, user_id: str):
        """Initialize Gmail API service"""
        try:
            # 1. Fetch stored credentials from database
            stored_creds = await database.db.gmail_credentials.find_one(
                {"user_id": user_id}
            )

            # 2. Convert stored credentials to Google Credentials object
            if stored_creds:
                self.creds = Credentials(
<<<<<<< HEAD
                    token=stored_creds["token"],
                    refresh_token=stored_creds["refresh_token"],
                    token_uri=stored_creds.get(
                        "token_uri", "https://oauth2.googleapis.com/token"
                    ),  # Add default
                    client_id=stored_creds.get(
                        "client_id", settings.gmail_client_id
                    ),  # Add this
                    client_secret=stored_creds.get(
                        "client_secret", settings.gmail_client_secret
                    ),  # Add this
                    scopes=self.SCOPES,
                )
                if stored_creds.get("expiry"):
                    self.creds.expiry = stored_creds["expiry"]
=======
                    token=stored_creds['token'],
                    refresh_token=stored_creds['refresh_token'],
                    token_uri=stored_creds.get('token_uri', "https://oauth2.googleapis.com/token"),  # Add default
                    client_id=stored_creds.get('client_id', settings.gmail_client_id),  # Add this
                    client_secret=stored_creds.get('client_secret', settings.gmail_client_secret),  # Add this
                    scopes=self.SCOPES
                )
                if stored_creds.get('expiry'):
                    self.creds.expiry = stored_creds['expiry']
>>>>>>> main

            # 3. Handle credential refresh or new credential generation
            if not self.creds or not self.creds.valid:
                if self.creds and self.creds.expired and self.creds.refresh_token:
                    print("Refreshing expired credentials")
                    self.creds.refresh(Request())
                    await database.db.gmail_credentials.update_one(
                        {"user_id": user_id},
<<<<<<< HEAD
                        {
                            "$set": {
                                "token": self.creds.token,
                                "refresh_token": self.creds.refresh_token,
                                "token_uri": self.creds.token_uri,
                                "client_id": settings.gmail_client_id,  # Add this
                                "client_secret": settings.gmail_client_secret,  # Add this
                                "scopes": self.SCOPES,
                                "expiry": datetime.now() + timedelta(days=36500),
                                "created_at": datetime.utcnow(),
                                "updated_at": datetime.utcnow(),
                            }
                        },
                        upsert=True,
                    )

=======
                        {"$set": {
                            "token": self.creds.token,
                            "refresh_token": self.creds.refresh_token,
                            "token_uri": self.creds.token_uri,
                            "client_id": settings.gmail_client_id,  # Add this
                            "client_secret": settings.gmail_client_secret,  # Add this
                            "scopes": self.SCOPES,
                            "expiry": datetime.now() + timedelta(days=36500),
                            "created_at": datetime.utcnow(),
                            "updated_at": datetime.utcnow()
                        }},
                        upsert=True
                    )
                
>>>>>>> main
                else:
                    print("Generating new credentials")
                    import socket
                    import asyncio
<<<<<<< HEAD

=======
                    
>>>>>>> main
                    def find_free_port():
                        """Find a free port between 8003-8010"""
                        for port in range(8003, 8011):
                            try:
                                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                                sock.settimeout(1)
<<<<<<< HEAD
                                result = sock.connect_ex(("localhost", port))
=======
                                result = sock.connect_ex(('localhost', port))
>>>>>>> main
                                sock.close()
                                if result != 0:  # Port is free
                                    return port
                            except:
                                continue
                        raise Exception("No free ports available")

                    try:
                        port = find_free_port()
                        client_config = {
                            "installed": {
                                "client_id": settings.gmail_client_id,
                                "client_secret": settings.gmail_client_secret,
                                "redirect_uris": [f"http://localhost:{port}/"],
                                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
<<<<<<< HEAD
                                "token_uri": "https://oauth2.googleapis.com/token",
=======
                                "token_uri": "https://oauth2.googleapis.com/token"
>>>>>>> main
                            }
                        }

                        flow = InstalledAppFlow.from_client_config(
                            client_config,
                            self.SCOPES,
<<<<<<< HEAD
                            redirect_uri=f"http://localhost:{port}/",
                        )

                        auth_url, _ = flow.authorization_url(
                            access_type="offline",
                            include_granted_scopes="true",
                            prompt="consent select_account",
=======
                            redirect_uri=f"http://localhost:{port}/"
                        )

                        auth_url, _ = flow.authorization_url(
                            access_type='offline',
                            include_granted_scopes='true',
                            prompt='consent select_account'
>>>>>>> main
                        )

                        self.creds = await asyncio.wait_for(
                            asyncio.to_thread(
                                flow.run_local_server,
<<<<<<< HEAD
                                host="localhost",
                                port=port,
                                open_browser=True,
                                authorization_prompt_message="Please authorize access to Gmail",
                                success_message="Authentication successful! You can close this window.",
                                open_browser_new=2,
                            ),
                            timeout=45,
=======
                                host='localhost',
                                port=port,
                                open_browser=True,
                                authorization_prompt_message='Please authorize access to Gmail',
                                success_message='Authentication successful! You can close this window.',
                                open_browser_new=2
                            ),
                            timeout=45
>>>>>>> main
                        )
                    except Exception as e:
                        print(f"Authentication error: {str(e)}")
                        raise e
<<<<<<< HEAD

                    await database.db.gmail_credentials.update_one(
                        {"user_id": user_id},
                        {
                            "$set": {
                                "token": self.creds.token,
                                "refresh_token": self.creds.refresh_token,
                                "token_uri": self.creds.token_uri,
                                "scopes": self.SCOPES,
                                "expiry": datetime.now() + timedelta(days=36500),
                                "created_at": datetime.utcnow(),
                                "updated_at": datetime.utcnow(),
                            }
                        },
                        upsert=True,
                    )

            # 4. Build the Gmail service
            self.service = build("gmail", "v1", credentials=self.creds)
=======
                    
                    await database.db.gmail_credentials.update_one(
                        {"user_id": user_id},
                        {"$set": {
                            "token": self.creds.token,
                            "refresh_token": self.creds.refresh_token,
                            "token_uri": self.creds.token_uri,
                            "scopes": self.SCOPES,
                            "expiry": datetime.now() + timedelta(days=36500),
                            "created_at": datetime.utcnow(),
                            "updated_at": datetime.utcnow()
                        }},
                        upsert=True
                    )

            # 4. Build the Gmail service
            self.service = build('gmail', 'v1', credentials=self.creds)
>>>>>>> main
            return True

        except Exception as e:
            print(f"Error initializing Gmail service: {str(e)}")
            raise HTTPException(
<<<<<<< HEAD
                status_code=500, detail=f"Failed to initialize Gmail service: {str(e)}"
            )

    async def fetch_emails(
        self, query: str, last_email_date_extracted: datetime = None
    ):
=======
                status_code=500,
                detail=f"Failed to initialize Gmail service: {str(e)}"
            )


    async def fetch_emails(self, query: str, last_email_date_extracted: datetime = None):
>>>>>>> main
        """Fetch emails based on query"""
        try:
            if not self.service:
                await self.initialize_service()

            # Build the query with date range
            if last_email_date_extracted:
<<<<<<< HEAD
                full_query = f"{query} after:{last_email_date_extracted}"
            else:
                # Default to last 7 days if no last email date
                date_from = (datetime.now() - timedelta(days=7)).strftime("%Y/%m/%d")
                full_query = f"{query} after:{date_from}"

            print(full_query)

            results = (
                self.service.users()
                .messages()
                .list(userId="me", q=full_query, maxResults=50)
                .execute()
            )

            messages = results.get("messages", [])
=======
                full_query = f'{query} after:{last_email_date_extracted}'
            else:
                # Default to last 7 days if no last email date
                date_from = (datetime.now() - timedelta(days=7)).strftime('%Y/%m/%d')
                full_query = f'{query} after:{date_from}'

            print(full_query)
            
            results = self.service.users().messages().list(
                userId='me',
                q=full_query,
                maxResults=50
            ).execute()

            messages = results.get('messages', [])
>>>>>>> main
            emails_data = []
            email_dates = []

            for message in messages:
<<<<<<< HEAD
                msg = (
                    self.service.users()
                    .messages()
                    .get(userId="me", id=message["id"], format="full")
                    .execute()
                )

                headers = msg["payload"]["headers"]
                subject = next(
                    (h["value"] for h in headers if h["name"].lower() == "subject"), ""
                )
                date_str = next(
                    (h["value"] for h in headers if h["name"].lower() == "date"), ""
                )
                from_email = next(
                    (h["value"] for h in headers if h["name"].lower() == "from"), ""
                )

                try:
                    email_date = datetime.strptime(date_str, "%a, %d %b %Y %H:%M:%S %z")
=======
                msg = self.service.users().messages().get(
                    userId='me',
                    id=message['id'],
                    format='full'
                ).execute()

                headers = msg['payload']['headers']
                subject = next((h['value'] for h in headers if h['name'].lower() == 'subject'), '')
                date_str = next((h['value'] for h in headers if h['name'].lower() == 'date'), '')
                from_email = next((h['value'] for h in headers if h['name'].lower() == 'from'), '')
                
                try:
                    email_date = datetime.strptime(date_str, '%a, %d %b %Y %H:%M:%S %z')
>>>>>>> main
                    email_dates.append(email_date)
                except ValueError:
                    # Fallback if date format is different
                    email_date = datetime.utcnow()
                    email_dates.append(email_date)

<<<<<<< HEAD
                body = self._get_email_body(msg["payload"])

                emails_data.append(
                    {
                        "id": message["id"],
                        "subject": subject,
                        "date": date_str,
                        "from": from_email,
                        "body": body,
                    }
                )
=======
                body = self._get_email_body(msg['payload'])
                
                emails_data.append({
                    'id': message['id'],
                    'subject': subject,
                    'date': date_str,
                    'from': from_email,
                    'body': body
                })
>>>>>>> main

            # Calculate first and last email dates
            first_email_date = min(email_dates) if email_dates else datetime.utcnow()
            last_email_date = max(email_dates) if email_dates else datetime.utcnow()
<<<<<<< HEAD

=======
        
>>>>>>> main
            return emails_data, first_email_date, last_email_date

        except Exception as e:
            print(f"Error fetching emails: {str(e)}")
            raise HTTPException(
<<<<<<< HEAD
                status_code=500, detail=f"Failed to fetch emails: {str(e)}"
=======
                status_code=500,
                detail=f"Failed to fetch emails: {str(e)}"
>>>>>>> main
            )

    def _get_email_body(self, payload):
        """Extract email body from payload"""
        try:
<<<<<<< HEAD
            if "body" in payload and payload["body"].get("data"):
                return base64.urlsafe_b64decode(
                    payload["body"]["data"].encode("ASCII")
                ).decode("utf-8")

            if "parts" in payload:
                for part in payload["parts"]:
                    if part["mimeType"] == "text/plain":
                        if "data" in part["body"]:
                            return base64.urlsafe_b64decode(
                                part["body"]["data"].encode("ASCII")
                            ).decode("utf-8")
            return ""
        except Exception as e:
            print(f"Error extracting email body: {str(e)}")
            return ""
=======
            if 'body' in payload and payload['body'].get('data'):
                return base64.urlsafe_b64decode(
                    payload['body']['data'].encode('ASCII')
                ).decode('utf-8')
            
            if 'parts' in payload:
                for part in payload['parts']:
                    if part['mimeType'] == 'text/plain':
                        if 'data' in part['body']:
                            return base64.urlsafe_b64decode(
                                part['body']['data'].encode('ASCII')
                            ).decode('utf-8')
            return ""
        except Exception as e:
            print(f"Error extracting email body: {str(e)}")
            return ""
>>>>>>> main
