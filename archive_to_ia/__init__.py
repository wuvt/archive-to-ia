import datetime
import os.path
import requests
import internetarchive
from flask import abort, Flask, request, Response
from functools import wraps

app = Flask(__name__)
app.config.setdefault('ITEM_METADATA', {})

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


def process_upload(identifier, filename, fileobj, metadata):
    yield "Start upload to {0}...\n".format(identifier)
    internetarchive.upload(
        identifier,
        files={filename: fileobj},
        metadata=metadata,
        checksum=False,
        verify=False,
        access_key=app.config['IA_ACCESS_KEY'],
        secret_key=app.config['IA_SECRET_KEY'])
    yield "Done."


@app.route('/upload/<string:studio>/<int:year>/<int:month>/<int:day>/<int:hour>', methods=['POST'])
@requires_auth
def upload(studio, year, month, day, hour):
    studio = os.path.basename(studio)
    dt = datetime.datetime(year, month, day, hour)
    format_data = dict(studio=studio, studio_upper=studio.upper(), dt=dt)

    filename = app.config['DEST_FILENAME'].format(**format_data)
    identifier = app.config['ITEM_ID'].format(**format_data)

    metadata = {}
    for k in app.config['ITEM_METADATA'].keys():
        metadata[k] = app.config['ITEM_METADATA'][k].format(**format_data)

    r = requests.get(app.config['SOURCE_URL'].format(**format_data),
                     stream=True)
    if r.status_code != 200:
        abort(404)

    return Response(process_upload(identifier, filename, r.raw, metadata))
