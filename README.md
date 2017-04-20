# archive-to-ia

A simple Flask application that uses the S3 API to stream uploads from a file
server to the Internet Archive.

## Configuration
You'll want something like this:
```json
{
    "BUCKET_FORMAT": "WUVTFM_{0}",
    "SOURCE_URL_FORMAT": "http://alexandria.wuvt.vt.edu/archive/pgmcheck/{studio}/{year}/{month}/{day}/{filename}",
    "ACCOUNTS": {
        "pgmcheck": "hunter2"
    }
}
```
