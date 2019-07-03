"""
Entrypoint module, in case you use `python -mumq`.
Why does this file exist, and why __main__? For more info, read:
- https://www.python.org/dev/peps/pep-0338/
- https://docs.python.org/2/using/cmdline.html#cmdoption-m
- https://docs.python.org/3/using/cmdline.html#cmdoption-m
"""
from umq.app import create_app

app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=8080)
