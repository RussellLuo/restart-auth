from __future__ import absolute_import

from restart.config import config
from restart.resource import Resource
from restart.response import Response
from restart.testing import RequestFactory
from restart.ext.crossdomain.cors import CORSMiddleware


factory = RequestFactory()


class Echo(Resource):
    name = 'echo'

    middleware_classes = (CORSMiddleware,)

    def read(self, request):
        return request.data


class CustomizedCORSMiddleware(CORSMiddleware):
    cors_allow_origin = 'http://localhost'
    cors_allow_credentials = True


class AnotherEcho(Echo):
    middleware_classes = (CustomizedCORSMiddleware,)


class TestCORSMiddleware(object):

    def make_resource(self, resource_class=Echo, action_map=config.ACTION_MAP):
        return resource_class(action_map)

    def test_preflight_request_without_request_headers(self):
        request = factory.options(
            '/',
            headers=[('Origin', 'http://localhost'),
                     ('Access-Control-Request-Method', 'GET')]
        )
        resource = self.make_resource()
        response = resource.dispatch_request(request)

        assert isinstance(response, Response)
        assert response.data == '""'
        assert response.status_code == 200
        assert response.headers['Access-Control-Allow-Origin'] == '*'
        assert (response.headers['Access-Control-Allow-Methods'] ==
                'GET, POST, PUT, PATCH, DELETE')
        assert response.headers['Access-Control-Max-Age'] == '864000'
        assert 'Access-Control-Allow-Headers' not in response.headers
        assert 'Access-Control-Allow-Credentials' not in response.headers
        assert 'Vary' not in response.headers

    def test_preflight_request_with_request_headers(self):
        request = factory.options(
            '/',
            headers=[('Origin', 'http://localhost'),
                     ('Access-Control-Request-Method', 'GET'),
                     ('Access-Control-Request-Headers', 'X-CORS')]
        )
        resource = self.make_resource()
        response = resource.dispatch_request(request)

        assert isinstance(response, Response)
        assert response.data == '""'
        assert response.status_code == 200
        assert response.headers['Access-Control-Allow-Origin'] == '*'
        assert (response.headers['Access-Control-Allow-Methods'] ==
                'GET, POST, PUT, PATCH, DELETE')
        assert response.headers['Access-Control-Max-Age'] == '864000'
        assert response.headers['Access-Control-Allow-Headers'] == 'X-CORS'
        assert 'Access-Control-Allow-Credentials' not in response.headers
        assert 'Vary' not in response.headers

    def test_preflight_request_when_allow_credentials(self):
        request = factory.options(
            '/',
            headers=[('Origin', 'http://localhost'),
                     ('Access-Control-Request-Method', 'GET')]
        )
        resource = self.make_resource(resource_class=AnotherEcho)
        response = resource.dispatch_request(request)

        assert isinstance(response, Response)
        assert response.data == '""'
        assert response.status_code == 200
        assert (response.headers['Access-Control-Allow-Origin'] ==
                'http://localhost')
        assert (response.headers['Access-Control-Allow-Methods'] ==
                'GET, POST, PUT, PATCH, DELETE')
        assert response.headers['Access-Control-Max-Age'] == '864000'
        assert response.headers['Access-Control-Allow-Credentials'] == 'true'
        assert response.headers['Vary'] == 'Origin'

    def test_actual_request(self):
        data = {'hello': 'world'}
        request = factory.get('/', data=data)
        resource = self.make_resource()
        response = resource.dispatch_request(request)

        assert isinstance(response, Response)
        assert response.data == '{"hello": "world"}'
        assert response.status_code == 200
        assert response.headers['Access-Control-Allow-Origin'] == '*'
        assert 'Access-Control-Allow-Credentials' not in response.headers
        assert 'Vary' not in response.headers

    def test_actual_request_when_allow_credentials(self):
        data = {'hello': 'world'}
        request = factory.get('/', data=data)
        resource = self.make_resource(resource_class=AnotherEcho)
        response = resource.dispatch_request(request)

        assert isinstance(response, Response)
        assert response.data == '{"hello": "world"}'
        assert response.status_code == 200
        assert (response.headers['Access-Control-Allow-Origin'] ==
                'http://localhost')
        assert response.headers['Access-Control-Allow-Credentials'] == 'true'
        assert response.headers['Vary'] == 'Origin'
