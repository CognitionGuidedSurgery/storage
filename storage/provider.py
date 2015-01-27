import os
import fnmatch
import json
import functools

from flask import Flask, send_file, abort, request, Response
import requests

app = Flask(__name__)
CONFIG_FILE = os.path.abspath(
    os.environ.get('STORAGE_PROVIDER_CONFIG', 'providerconfig.py'))

app.config.from_pyfile(CONFIG_FILE)


def filename_matched_patterns(patterns, filename):
    test = functools.partial(fnmatch.fnmatch, filename)
    return any(map(test, patterns))


def is_allowed_file(filename):
    return filename_matched_patterns(app.config['ALLOWED_FILES'], filename) \
           and not filename_matched_patterns(app.config['FORBIDDEN_FILES'], filename) \
           and ( not os.path.exists(filename) or os.path.isfile(filename) )

class JailBreakError(Exception):
    pass


class NotAllowedFileError(Exception):
    pass


class FileNotFoundError(Exception):
    pass


def get_local_filename(path):
    l = os.path.abspath(os.path.join(app.config['ROOT_PATH'], path))
    if not l.startswith(app.config['ROOT_PATH']):
        raise JailBreakError("jail break!")

    if not is_allowed_file(l):
        raise NotAllowedFileError()
    return l


def isfile(filename):
    return os.path.exists(filename) and os.path.isfile(filename)


@app.route("/info")
def info():
    def collect(arg, dirname, fnames):
        for f in fnames:
            arg.append(os.path.join(dirname, f))

    files = []
    os.path.walk(app.config['ROOT_PATH'], collect, files)

    files = filter(is_allowed_file, files)

    return Response(json.dumps(files, sort_keys=True, indent=4), content_type="application/json")


@app.route('/<path:path>', methods=['GET'])
def get(path):
    try:
        file_path = get_local_filename(path)
    except:
        abort(500)
    return send_file(file_path)


@app.route('/<path:path>', methods=['POST'])
def post(path):
    url = request.values['url']
    local = get_local_filename(path)
    response = requests.get('url', raw=True)

    with open(local, 'wb') as fd:
        for chunk in response.iter_content(8192):
            fd.write(chunk)


@app.route('/<path:path>', methods=['DELETE'])
def delete(path):
    local = get_local_filename()
    os.remove(local)


@app.route('/<path:path>', methods=['PUT'])
def put(path):
    local = get_local_filename(path)
    data = request.data
    with open(local, 'wb') as fd:
        fd.write(data)
    return "ok"


if __name__ == '__main__':
    app.run()
