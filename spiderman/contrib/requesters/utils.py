from scrapy.http import Request
from scrapy.utils.python import to_unicode, to_native_str
from scrapy.utils.misc import load_object

def request_to_dict(request):
    d = {
        'url': to_unicode(request.url),  # urls should be safe (safe_string_url)
        'callback': request.callback,
        'errback': request.errback,
        'method': request.method,
        'headers': dict(request.headers),
        'body': request.body,
        'cookies': request.cookies,
        'meta': request.meta,
        '_encoding': request._encoding,
        'priority': request.priority,
        'dont_filter': request.dont_filter,
        'flags': request.flags
    }
    if type(request) is not Request:
        d['_class'] = request.__module__ + '.' + request.__class__.__name__
    return d


def request_from_dict(d):
    request_cls = load_object(d['_class']) if '_class' in d else Request
    return request_cls(
        url=to_native_str(d['url']),
        callback=d.callback,
        errback=d.errback,
        method=d['method'],
        headers=d['headers'],
        body=d['body'],
        cookies=d['cookies'],
        meta=d['meta'],
        encoding=d['_encoding'],
        priority=d['priority'],
        dont_filter=d['dont_filter'],
        flags=d.get('flags'))
