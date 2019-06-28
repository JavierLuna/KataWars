from functools import wraps

from flask import jsonify, request, current_app

from .schemas import PaginationSchema


def json(f):
    @wraps(f)
    def wrapped(*args, **kwargs):
        rv = f(*args, **kwargs)
        code = 200
        if isinstance(rv, tuple):
            code = rv[1]
            rv = rv[0]
        return jsonify(rv), code

    return wrapped


def paginate(schema):
    def inception(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            s = schema(many=True)
            page = request.args.get('page', 1, type=int)
            rv = f(*args, **kwargs)
            paginator = rv.paginate(page, per_page=current_app.config['RESULTS_PER_API_CALL'], error_out=False)
            resulting_data = PaginationSchema().dump({'objects': s.dump(paginator.items, many=True),
                                                      'next_page': paginator.next_num if paginator.has_next else None,
                                                      'prev_page': paginator.prev_num if paginator.has_prev else None,
                                                      'pages': paginator.pages,
                                                      'total_objects': paginator.total})
            return jsonify(resulting_data)

        return wrapped

    return inception


def detail(schema):
    def inception(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            s = schema()
            instance = f(*args, **kwargs)
            return jsonify(s.dump(instance))

        return wrapped

    return inception
