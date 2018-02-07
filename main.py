# Twitter
def update_twitter_metrics(mssql_engine):
    global api, acc_info

    log('Authentication and fetching twitter account stats...')
    api = Api(tweet_mode='extended', **load_credentials('Twitter_API')) # load our API credentials
    acc_info = api.VerifyCredentials().AsDict() # authenticate and get account information

    account_stats = get_account_stats(acc_info)
    tweet_metrics = get_tweet_metrics()

    rg.update_db(account_stats,
        'twitter_account_stats',
        mssql_engine,
        schema=twitter_account_schema())
    rg.update_db(tweet_metrics,
        'twitter_statuses',
        mssql_engine,
        drop=(not DEBUG), # drop the table, but not while debugging
        schema=twitter_status_schema())


if __name__ == "__main__":
    mssql_engine = rg.connect_to_db()
    update_twitter_metrics(mssql_engine)

    #Youtube


def update_youtube_metrics(mssql_engine):
    (youtube_data, youtube_analytics) = get_authenticated_services()

    youtube_channel_stats = get_channel_stats(youtube_data, youtube_analytics)
    youtube_videos_stats = get_videos_stats(youtube_data, youtube_analytics)

    rg.update_db(youtube_channel_stats,
        'youtube_channel_stats',
        mssql_engine,
        schema=channel_table_schema())
    rg.update_db(youtube_videos_stats,
        'youtube_videos_stats',
        mssql_engine,
        drop=(not DEBUG), # drop the table, but not while debugging
        schema=videos_table_schema())


if __name__ == "__main__":
    mssql_engine = rg.connect_to_db()
    update_youtube_metrics(mssql_engine)

#google analytics

def update_ga_metrics(mssql_engine):
    ga_api = get_authenticated_service()

    ga_stats = get_ga_stats(ga_api)

    rg.update_db(ga_stats,
        'google_analytics_stats',
        mssql_engine,
        drop=(not DEBUG) # drop the table, but not while debugging
    )
        # We may not need a schema since we are dropping a table evert time
        #schema=ga_table_schema)


if __name__ == "__main__":
    mssql_engine = rg.connect_to_db()
    update_ga_metrics(mssql_engine)