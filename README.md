# archive-to-ia

A simple Flask application that uploads directly from our storage server to the
Internet Archive using their API.

## Configuration
You'll want something like this:
```json
{
    "ITEM_ID": "WUVT{studio_upper}_{dt.year:04d}{dt.month:02d}{dt.day:02d}{dt.hour:02d}",
    "ITEM_METADATA": {
        "collection": "wuvtfm",
        "creator": "WUVT-FM",
        "date": "{dt.year:04d}-{dt.month:02d}-{dt.day:02d} {dt.hour:02d}:00:00",
        "mediatype": "audio",
        "subject": "wuvt-fm;wuvt;airchecks;virginia tech",
        "title": "WUVT-{studio_upper} {dt.year:04d}-{dt.month:02d}-{dt.day:02d} {dt.hour:02d}:00"
    },
    "SOURCE_URL": "http://alexandria.wuvt.vt.edu/archive/pgmcheck/{studio}/{dt.year:04d}/{dt.month:02d}/{dt.day:02d}/{dt.year:04d}-{dt.month:02d}-{dt.day:02d}-{dt.hour:02d}_00_00+0000.flac",
    "DEST_FILENAME": "WUVT{studio_upper}_{dt.year:04d}-{dt.month:02d}-{dt.day:02d}-{dt.hour:02d}_00_00+0000.flac",
    "ACCOUNTS": {
        "pgmcheck": "hunter2"
    }
}
```
