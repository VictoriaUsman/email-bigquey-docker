import os
import base64
import io
import pandas as pd
from datetime import datetime
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from pandas_gbq import read_gbq, to_gbq

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def get_gmail_service():
    """Handles OAuth2 authentication and returns the Gmail API service object."""
    creds = None
    # The file token.json stores the user's access and refresh tokens
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            # Ensure client_secrets.json is in your directory!
            flow = InstalledAppFlow.from_client_secrets_file('client_secrets.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
            
    return build('gmail', 'v1', credentials=creds)

def run_gmail_to_bigquery_pipeline():
    # --- 1. INITIAL SETUP ---
    service = get_gmail_service()
    print("Successfully connected to Gmail Service")
    
    PROJECT_ID = "conductive-bot-480110-g0"
    DATASET_ID = "IanTristanTESTDATA" 
    TABLE_ID = "testTABLE"
    UNIQUE_COL = "timestamp" # Your unique identifier
    
    # Search for emails from today
    today_str = datetime.now().strftime('%Y/%m/%d')
    query = f"has:attachment filename:csv after:{today_str}"
    
    print(f"Searching Gmail for: {query}...")
    results = service.users().messages().list(userId='me', q=query).execute()
    messages = results.get('messages', [])

    if not messages:
        print("No emails found for today matching the query.")
        return

    # --- 2. EXTRACTION ---
    all_dfs = []
    for msg in messages:
        message = service.users().messages().get(userId='me', id=msg['id']).execute()
        
        # Walk through email parts to find CSVs (handles nested/forwarded emails)
        parts = [message['payload']]
        while parts:
            part = parts.pop()
            if 'parts' in part:
                parts.extend(part['parts'])
            
            if part.get('filename') and part['filename'].lower().endswith('.csv'):
                print(f"Extracting attachment: {part['filename']}")
                att_id = part['body']['attachmentId']
                att = service.users().messages().attachments().get(
                    userId='me', messageId=msg['id'], id=att_id).execute()
                
                # Decode and load to Dataframe
                data = base64.urlsafe_b64decode(att['data'].encode('UTF-8'))
                df = pd.read_csv(io.BytesIO(data))
                all_dfs.append(df)

    if not all_dfs:
        print("Emails found, but no CSV attachments inside them.")
        return

    # Combine all found CSVs into one DataFrame
    raw_df = pd.concat(all_dfs).drop_duplicates()
    print(f"Total rows extracted from Gmail: {len(raw_df)}")

    # --- 3. DEDUPLICATION ---
    try:
        # Fetch existing unique keys from BigQuery
        sql = f"SELECT DISTINCT CAST({UNIQUE_COL} AS STRING) as {UNIQUE_COL} FROM `{PROJECT_ID}.{DATASET_ID}.{TABLE_ID}`"
        existing_ids_df = read_gbq(sql, project_id=PROJECT_ID)
        
        # Clean both sides for a perfect match (Stringify + Strip whitespace)
        existing_ids = set(existing_ids_df[UNIQUE_COL].str.strip().tolist())
        raw_df[UNIQUE_COL] = raw_df[UNIQUE_COL].astype(str).str.strip()

        # Filter: Keep only the rows that DO NOT exist in BigQuery
        final_df = raw_df[~raw_df[UNIQUE_COL].isin(existing_ids)]
        
        print(f"Deduplication: {len(existing_ids)} IDs in BQ. {len(final_df)} new rows to add.")

    except Exception as e:
        # This handles the case where the table doesn't exist yet
        print(f"Starting fresh (Table not found or empty).")
        final_df = raw_df

    # --- 4. LOAD ---
    if not final_df.empty:
        print(f"Uploading {len(final_df)} new unique rows to BigQuery...")
        to_gbq(
            final_df, 
            f"{DATASET_ID}.{TABLE_ID}", 
            project_id=PROJECT_ID, 
            if_exists="append"
        )
        print("Upload successful!")
    else:
        print("No new data to add. BigQuery is already up to date.")

if __name__ == "__main__":
    run_gmail_to_bigquery_pipeline()