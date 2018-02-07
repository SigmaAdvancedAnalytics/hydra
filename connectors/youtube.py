#!/usr/bin/python

from datetime import datetime, timedelta
import httplib2
import os
import sys

from apiclient.discovery import build
from apiclient.errors import HttpError
from oauth2client.client import flow_from_clientsecrets, Credentials
from oauth2client.file import Storage
from oauth2client.tools import argparser, run_flow

import results_generator as rg
from sqlalchemy import *

from api_extractor_utils import *
from api_extractor_config import *

# For debugging
from pprint import pprint

# Please ensure that YouTube Data and YouTube Analytics are enabled the
# APIs for the project.


#-----------------------------------------------------------------------
# Config
#-----------------------------------------------------------------------
# These OAuth 2.0 access scopes allow for read-only access to the youtube
# account for both YouTube Data API resources and YouTube Analytics Data.
YOUTUBE_SCOPES = ["https://www.googleapis.com/auth/youtube.readonly",
  "https://www.googleapis.com/auth/yt-analytics.readonly"]
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"
YOUTUBE_ANALYTICS_API_SERVICE_NAME = "youtubeAnalytics"
YOUTUBE_ANALYTICS_API_VERSION = "v1"

SCRIPT_RUN_TIME = datetime.now().strftime(DATETIME_FORMAT)

# Exceptions
class UnavailableVideo(Exception):
    '''Raise this when a video is (probably) unavailable. See Issue #5'''

#-----------------------------------------------------------------------
# Helper Functions
#-----------------------------------------------------------------------
def paginate(req, per_page=50, **params):
    """Fetch as much data as possible using the specified request.

    This is useful because some request have a limit on the number of items per
    request. Thus, we'll need to paginate untill we have fetched as much as
    possible.

    This function is specific to Youtube. There is a seperate one for Twitter.
    There are minor but essential differences.
    """

    def listify(page):
        """Some times results are returned as a dict with an 'items' key."""
        if type(page) is dict:
            page = page['items']
        return page

    # When debugging, we fetch 3 items per request to test pagination.
    # We only fetch (about) 10 in total to avoid waiting too much ;)
    if DEBUG:
        per_page = 3

    current_page = req(maxResults=per_page, **params).execute()
    aggregate = listify(current_page)

    while "nextPageToken" in current_page and (not DEBUG or len(aggregate) < 10):
        current_page = req(maxResults=per_page,
            pageToken=current_page["nextPageToken"],
            **params).execute()
        aggregate.extend(listify(current_page))

    return aggregate

def get_authenticated_services():
    json = load_credentials('Youtube_API')
    credentials = Credentials.new_from_json(json)

    http = credentials.authorize(httplib2.Http()) 

    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, http=http)
    youtube_analytics = build(YOUTUBE_ANALYTICS_API_SERVICE_NAME,
        YOUTUBE_ANALYTICS_API_VERSION, http=http)

    return (youtube, youtube_analytics)

def get_channel_stats(youtube_data, youtube_analytics):
    """Fetch the general statistics for the channel.

    The number of new subscribers is fetched from the Youtube Analytics API.
    All the other things are fetched from the Youtube Data API.
    """

    def get_new_subscribers_count(channel_id):
        now = datetime.now()
        today = now.strftime("%Y-%m-%d")
        yesterday = (now - timedelta(days=1)).strftime("%Y-%m-%d")
        two_days_ago = (now - timedelta(days=2)).strftime("%Y-%m-%d")

        response = youtube_analytics.reports().query(
            ids="channel==%s" % channel_id,
            metrics="subscribersGained",
            dimensions="day",
            start_date=two_days_ago,
            end_date=yesterday,
        ).execute()
        
        # TODO(mkeyhani): check if this is th right thing to do
        if not ('rows' in response):
            return 0

        return int(response['rows'][0][1])

    log('Fetching Youtube channel stats...')
    results = youtube_data.channels().list(
        part='snippet,statistics,contentDetails',
        mine=True
    ).execute()

    the_channel = results['items'][0]
    channel_id = the_channel['id']
    stats = the_channel['statistics']

    record = {
        'channel_id': channel_id,
        'channel_name': the_channel['snippet']['title'],

        'subscribers': int(stats['subscriberCount']),
        'total_views': int(stats['viewCount']),
        'total_comments': int(stats['commentCount']),
        'videos': int(stats['videoCount']),

        'Extract_Datetime' : SCRIPT_RUN_TIME,

        'new_subscribers': get_new_subscribers_count(channel_id)
    }

    table = [record]
    return table

def get_videos_stats(youtube_data, youtube_analytics):
    """Fetch the stats for every video in the channel.

    Statistics are fetched from the Youtube Data API.
    """

    def get_playlists():
        """This function is not currently used, but may be useful in future"""
        params =  { 'part': 'id', 'mine': True }
        playlists = paginate(youtube_data.playlists().list, **params)

        playlist_ids = [playlist["id"] for playlist in playlists["items"]]
        return playlist_ids

    def list_playlist_videos(playlist_id):
        """Fetch the list of all videos in a playlist.

        This function is also used to fetch the list of all the vidoes in the channel
        by passing the 'Uploads' playlist id to it. Thge API limits the number
        of videos which you can fetch directly from the channel to 200,
        so we need to do this to circumvent the limitation.

        For each vidoe, we also return the video_title and date in additonal to
        video_id. This comes handy when in cases which the Analytics API
        reports do not have the title and date. 

        Returns:
            A list of (video_id, video_title) pairs
        """
        params = { 'part': 'id,snippet', 'playlistId': playlist_id}
        videos = paginate(youtube_data.playlistItems().list, **params)

        videos_cleaned_up = []
        for item in videos:
            snippet = item["snippet"]
            video_id = snippet['resourceId']['videoId']
            video_title = snippet["title"]
            published_at = datetime.strptime(snippet['publishedAt'], '%Y-%m-%dT%H:%M:%S.000Z').strftime(DATETIME_FORMAT)
            videos_cleaned_up.append( (video_id, video_title, published_at) )


        return videos_cleaned_up


    def get_video_stats(video_id):
        now = datetime.now()
        today = now.strftime("%Y-%m-%d")
        long_time_ago = (now - timedelta(days=365*30)).strftime("%Y-%m-%d")

        response = youtube_analytics.reports().query(
            ids="channel==MINE",
            metrics="views,likes,dislikes,comments,shares,averageViewDuration,subscribersGained,subscribersLost",
            dimensions="video",
            filters="video==%s" % video_id,
            start_date=long_time_ago,
            end_date=today
        ).execute()

        if not ('rows' in response):
            raise UnavailableVideo("Video with ID %s is unavailable." % video_id)

        the_row = response['rows'][0]
        headers = [header["name"] for header in response["columnHeaders"]]

        record = {}

        # To determine the ordering of columns, see API Quirks § Order of Columns
        for i, header in enumerate(headers):
            record[header] = the_row[i]

            # Convert the strings to ints if necessary
            should_be_int = ['comments', 'dislikes', 'views', 'likes', 'shares', 'averageViewDuration', 'subscribersGained', 'subscribersLost']
            if header in should_be_int:
                record[header] = int(the_row[i])
            else:
                record[header] = the_row[i]

            record['Extract_Datetime'] = SCRIPT_RUN_TIME

        return record

    log('Fetching Youtube vidoes stats...')

    # The uploads playlist inculdes all of the uploaded videos for a channel.
    # To find the id for a particular channel see:
    # https://stackoverflow.com/questions/18953499/youtube-api-to-fetch-all-videos-on-a-channel
    uploads_playlist = 'UUb9CssYHERvbKNVIZkAna9g'
    channel_videos = list_playlist_videos(uploads_playlist)
    table = []
    for (video_id, video_title, published_at) in channel_videos:
        try:
            record = get_video_stats(video_id)
        except UnavailableVideo as err:
            log(str(err))
            continue

        record["title"] = video_title

        # convert to datetime object
        published_at = datetime.strptime(published_at, DATETIME_FORMAT) 
        # convert to Eastern Time Zone, format properly
        record["publishedAt"] = utc_to_eastern(published_at).strftime(DATETIME_FORMAT)
        
        table.append(record)

    return table
