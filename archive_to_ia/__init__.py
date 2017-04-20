import boto3
import botocore.exceptions
import os.path
import requests
from flask import abort, Flask, request, Response
from functools import wraps

app = Flask(__name__)
app.config.setdefault('S3_ENDPOINT', 'https://s3.us.archive.org')

config_path = os.environ.get('APP_CONFIG_PATH', 'config.json')
app.config.from_json(config_path)


def check_auth(username, password):
    if username in app.config['ACCOUNTS'] and len(password) > 0:
        return app.config['ACCOUNTS'][username] == password
    else:
        return False


def requires_auth(f):
    @wraps(f)
    def requires_auth_decorator(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            abort(401)
        return f(*args, **kwargs)
    return requires_auth_decorator


def process_upload(bucket, filename, fileobj):
    s3 = boto3.resource(
        's3',
        endpoint_url=app.config['S3_ENDPOINT'],
        aws_access_key_id=app.config['AWS_ACCESS_KEY_ID'],
        aws_secret_access_key=app.config['AWS_SECRET_ACCESS_KEY'])

    yield "Create bucket if needed...\n"

    # Check if bucket exists and create it if it doesn't
    try:
        s3.meta.client.head_bucket(Bucket=bucket)
    except botocore.exceptions.ClientError as e:
        error_code = int(e.response['Error']['Code'])
        if error_code == 404:
            s3.create_bucket(Bucket=bucket)
        else:
            raise

    yield "Start upload...\n"
    s3.upload_fileobj(fileobj, bucket, filename)
    yield "Done."


@app.route('/upload/<string:studio>/<string:year>/<string:month>/<string:day>/<string:filename>', methods=['POST'])
@requires_auth
def upload(studio, year, month, day, filename):
    r = requests.get(
        app.config['SOURCE_URL_FORMAT'].format(
            studio=studio,
            year=year,
            month=month,
            day=day,
            filename=filename),
        stream=True)
    if r.status_code != 200:
        abort(404)

    barename = os.path.splitext(filename)[0]
    bucket = app.config['BUCKET_FORMAT'].format(barename)
    return Response(process_upload(bucket, filename, r.raw))
