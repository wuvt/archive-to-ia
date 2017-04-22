# archive-to-ia

A simple Flask application that uses the S3 API to stream uploads from a file
server to the Internet Archive.

## Configuration
You'll want something like this:
```json
{
    "BUCKET_FORMAT": "WUVT{studio_upper}_{barename}",
    "SOURCE_URL_FORMAT": "http://alexandria.wuvt.vt.edu/archive/pgmcheck/{studio}/{year:02d}/{month:02d}/{day:02d}/{filename}",
    "ACCOUNTS": {
        "pgmcheck": "hunter2"
    }
}
```
