import json
from http import HTTPStatus
from wsgiref.simple_server import make_server

db = [
    {'id': 1, 'name': 'Voolfy', 'type': 'dog'},
    {'id': 2, 'name': 'Snow', 'type': 'cat'},
]


def max_idx() -> int:
    idxs: list[int] = []
    for i in db:
        idxs.append(i['id'])
    return max(idxs)


def get_list(tp: str | None = None) -> list[dict]:
    if tp is None:
        return db
    return list(filter(lambda x: x['type'] == tp, db))


def get_item(idx: int) -> dict | None:
    result = list(filter(lambda x: x.get('id') == idx, db))
    return result[0] if len(result) else None


def add_item(item: dict) -> int | None:
    if item['type'] != 'dog' and item['type'] != 'cat':
        return None
    idx: int = max_idx() + 1
    db.append(dict(id=idx, name=item['name'], type=item['type']))
    return idx


def delete_item(idx: int) -> dict | None:
    global db
    candidate = get_item(idx)

    if candidate is None:
        return None

    db.remove(candidate)
    return candidate


def update_item(item: dict) -> dict | None:
    global db

    idx: int | None = item.get('id')
    if idx is None or (item['type'] != 'dog' and item['type'] != 'cat'):
        return None

    candidate = get_item(idx)
    if candidate is None:
        return None

    candidate['type'] = item['type']
    candidate['name'] = item['name']
    return candidate


# ------- helpers ------
def response(start, data, status: HTTPStatus = HTTPStatus.OK):
    body = json.dumps(data, ensure_ascii=False).encode('utf-8')
    start(f'{status.value} {status.phrase}', [('Content-Type', 'application/json'), ('Content-Length', str(len(body)))])
    return [body]


def read_json(env: dict) -> dict:
    length = int(env.get('CONTENT_LENGTH') or 0)
    if length > 1_000_000:
        raise ValueError('Content length is too large')
    if length == 0:
        raise ValueError('Content length is 0')
    raw = env['wsgi.input'].read(length)
    data = json.loads(raw)
    if isinstance(data, dict):
        raise ValueError('Content type is dict')
    return data


# ---- app
def app(env: dict, start):
    method = env['REQUEST_METHOD']
    path = env['PATH_INFO'].rstrip('/') or '/'

    if method == 'GET' and path == '/animals':
        return response(start, get_list())

    if method == 'POST' and path == '/animals':
        try:
            item = read_json(env)
        except ValueError as e:
            return response(start, {'error': str(e)}, HTTPStatus.BAD_REQUEST)

        idx = add_item(item)
        if idx is None:
            return response(start, {'error': 'Item is not created'}, HTTPStatus.BAD_REQUEST)

        return response(start, {'id': idx}, HTTPStatus.CREATED)

    if path.startswith('/animals'):
        raw_id = path.removeprefix('/animals/')

        try:
            idx = int(raw_id)
        except ValueError:
            return response(start, {'error': 'Invalid item ID'}, HTTPStatus.BAD_REQUEST)

        if method == 'GET':
            item = get_item(idx)
            if item is None:
                return response(start, {'error': 'Item is not found'}, HTTPStatus.NOT_FOUND)
            return response(start, {'id': idx}, HTTPStatus.OK)

        if method == 'PUT':
            try:
                item = read_json(env)
            except ValueError as e:
                return response(start, {'error': str(e)}, HTTPStatus.BAD_REQUEST)

            item['id'] = idx
            updated = update_item(item)
            if updated is None:
                return response(start, {'error': 'Item is not updated'}, HTTPStatus.NOT_FOUND)
            return response(start, {'id': idx}, HTTPStatus.OK)

        if method == 'DELETE':
            idx = delete_item(idx)
            if idx is None:
                return response(start, {'error': 'Item is not found'}, HTTPStatus.NOT_FOUND)
            return response(start, {'id': idx}, HTTPStatus.OK)

    return response(start, {'error': 'Method not supported'}, HTTPStatus.NOT_IMPLEMENTED)

if __name__ == '__main__':
    host = '127.0.0.1'
    port = 8080

    print(f'Listening on {host}:{port}')

    with make_server(host, port, app) as httpd:
        httpd.serve_forever()
