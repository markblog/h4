import re
import inspect
from functools import wraps
from ext import mc

__formaters = {}
percent_pattern = re.compile(r'%\w')
brace_pattern = re.compile(r'\{[\w\d\.\[\]_]+\}')

def formater(text):
    percent = percent_pattern.findall(text)
    brace = brace_pattern.search(text)

    if percent and brace:
        raise Exception('mixed format is not allowed')

    if percent:
        n = len(percent)
        return lambda *a, **kw: text % tuple(a[:n])
    elif '%(' in text:
        return lambda *a, **kw: text % kw
    else:
        return text.format

def format(text, *a, **kw):
    f = __formaters.get(text)
    if f is None:
        f = formater(text)
        __formaters[text] = f
    return f(*a, **kw)

def gen_key_factory(key_pattern,arg_names,defaults):
    args = dict(zip(arg_names[-len(defaults):],defaults)) if defaults else {}
    if callable(key_pattern):
        names = inspect.getargspec(key_pattern)[0]

    def gen_key(*a, **kw):
        aa = args.copy()
        aa.update(zip(arg_names,a))
        aa.update(kw)
        if callable(key_pattern):
            key = key_pattern(*[aa[n] for n in names])
        else:
            key = format(key_pattern, *[aa[n] for n in arg_names], **aa)
        return key and key.replace(' ','_'), aa

    return gen_key

def cache(key_pattern,get_from_db):

    def deco(f):
        arg_names, varargs, varkw, defaults = inspect.getargspec(f)
        if varargs or varkw:
            raise Exception('do not support varargs')
        gen_key = gen_key_factory(key_pattern,arg_names,defaults)

        @wraps(f)
        def _(*a, **kw):
            key, args = gen_key(*a, **kw)
            if not key:
                return f(*a, **kw)
            r = mc.get(key)

            if r == None and get_from_db:
                r = f(*a, **kw)
                if r is not None:
                    mc[key] = r
            return r

        _.original_function = f
        return _

    return deco

    
if __name__ == '__main__':
    key = 'web_develop:users:%s'
    id_ = 1
    #print format(key % '{id_}',id_ = id_)
