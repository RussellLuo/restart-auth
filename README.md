# RESTArt-CrossDomain

A RESTArt extension for cross-domain access.


## Installation

Install `RESTArt-CrossDomain` with `pip`:

    $ pip install RESTArt-CrossDomain

Install development version from `GitHub`:

    $ pip install -e git+https://github.com/RussellLuo/restart-crossdomain.git#egg=restart-crossdomain


## Quickstart

### 1. Create the middleware class

Use the `CORSMiddleware` class:

```python
    from restart.ext.crossdomain.cors import CORSMiddleware
```

which has the default configurations as follows:

```python
    # The configuration that determines the `Access-Control-Allow-Origin` header
    cors_allow_origin = '*'  # any domain

    # The configuration that determines the `Access-Control-Allow-Credentials` header
    cors_allow_credentials = False

    # The configuration that determines the `Access-Control-Allow-Methods` header
    cors_allow_methods = ('GET', 'POST', 'PUT', 'PATCH', 'DELETE')

    # The configuration that determines the `Access-Control-Allow-Headers` header
    cors_allow_headers = ()  # any headers

    # The configuration that determines the `Access-Control-Max-Age` header
    cors_max_age = 864000  # 10 days
```

Or create a new subclass with some customized configurations:

```python
    # my_middlewares.py

    from restart.ext.crossdomain.cors import CORSMiddleware

    class CustomizedCORSMiddleware(CORSMiddleware):
        cors_allow_origin = 'http://example.com'
        cors_allow_credentials = True
```

### 2. Use the middleware class

Set the above middleware class as a [global middleware][1]:

```python
    MIDDLEWARE_CLASSES = (
        'restart.ext.crossdomain.cors.CORSMiddleware',
        # Or
        # 'my_middlewares.CustomizedCORSMiddleware',
    )
```

Or set it as a [resource-level middleware][2]:

```python
    from restart.api import RESTArt
    from restart.resource import Resource
    from restart.ext.crossdomain.cors import CORSMiddleware
    # Or
    # from my_middlewares import CustomizedCORSMiddleware as CORSMiddleware

    api = RESTArt()

    @api.route(methods=['GET'])
    class Demo(Resource):
        name = 'demo'

        middleware_classes = (CORSMiddleware,)

        def read(self, request):
            return 'this is a demo'
```


[1]: http://restart.readthedocs.org/en/latest/middleware.html#global-middlewares
[2]: http://restart.readthedocs.org/en/latest/middleware.html#resource-level-middlewares
