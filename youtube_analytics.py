


import os
import pandas as pd
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# Specify the scopes required for accessing the YouTube Analytics API
SCOPES = ['https://www.googleapis.com/auth/youtube.readonly']

# Path to the credentials file downloaded in Step 2
CLIENT_SECRETS_FILE = 'path-json-file'

# Path to the token.json file, which will store your access and refresh tokens
TOKEN_FILE = 'token.json'

def get_authenticated_service():
    creds = None
    # Check if token.json file exists, which stores user's access and refresh tokens
    if os.path.exists(TOKEN_FILE):
        creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)
    
    # If no valid credentials are available, request the user to log in
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)
            creds = flow.run_local_server(port=0)
        
        # Save the credentials to token.json for future use
        with open(TOKEN_FILE, 'w') as token:
            token.write(creds.to_json())
    
    # Build the YouTube Analytics and Data API services
    youtube_analytics = build('youtubeAnalytics', 'v2', credentials=creds)
    youtube_data = build('youtube', 'v3', credentials=creds)
    
    return youtube_analytics, youtube_data

def get_all_videos(youtube_data, channel_id):
    videos = []
    request = youtube_data.search().list(
        part="id,snippet",
        channelId=channel_id,
        maxResults=50,
        order="date"
    )
    response = request.execute()

    # Get video IDs and titles
    while response:
        for item in response['items']:
            if item['id']['kind'] == 'youtube#video':
                video_id = item['id']['videoId']
                video_title = item['snippet']['title']
                videos.append({'video_id': video_id, 'video_title': video_title})

        # Check if there is a next page
        if 'nextPageToken' in response:
            request = youtube_data.search().list(
                part="id,snippet",
                channelId=channel_id,
                maxResults=50,
                order="date",
                pageToken=response['nextPageToken']
            )
            response = request.execute()
        else:
            break
    
    return videos

def get_video_statistics(youtube_analytics, channel_id, videos):
    all_video_data = []

    for video in videos:
        video_id = video['video_id']
        video_title = video['video_title']
        
        # Query the YouTube Analytics API for the video statistics
        response = youtube_analytics.reports().query(
            ids='channel=={}'.format(channel_id),
            startDate='2023-01-01',  # Set your desired date range
            endDate='2023-12-31',
            metrics='views,comments,likes,dislikes,estimatedMinutesWatched,subscribersGained,subscribersLost',
            dimensions='video',
            filters='video=={}'.format(video_id)
        ).execute()

        # Extract the rows of data
        data = response.get('rows', [])
        for row in data:
            # Add video title to the row data
            row_with_title = [video_title] + row
            all_video_data.append(row_with_title)

    # Extract column headers and add 'video_title' as the first column
    column_headers = ['video_title'] + [header['name'] for header in response['columnHeaders']]
    
    # Convert to DataFrame
    df = pd.DataFrame(all_video_data, columns=column_headers)
    return df

def main():
    # Authenticate and construct the YouTube Analytics API client
    youtube_analytics, youtube_data = get_authenticated_service()
    
    # Replace with your channel ID
    channel_id = 'youtube_channel_id'

    # Get all video IDs and titles on the channel
    videos = get_all_videos(youtube_data, channel_id)
    
    # Fetch statistics for each video
    df_video_statistics = get_video_statistics(youtube_analytics, channel_id, videos)

    # Save the DataFrame to a CSV file
    df_video_statistics.to_csv('youtube_video_statistics_with_titles.csv', index=False)
    print('Video statistics with titles saved to youtube_video_statistics_with_titles.csv')

# Run the script
if __name__ == '__main__':
    main()
