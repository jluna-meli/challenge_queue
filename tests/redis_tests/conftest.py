import pytest
import redis
from redis.connection import parse_url
from __init import create_app


# @pytest.fixture()
# def client(app_main):
#     return app_main.test_client()


REDIS_INFO = {}

@pytest.fixture
def login_env(monkeypatch):
    monkeypatch.setenv('USERNAME', 'Admin')
    monkeypatch.setenv('PASSWORD', '1234')
    monkeypatch.setenv('SECRET', 'ThisIsTheKey')


@pytest.fixture
def app(monkeypatch):
    monkeypatch.setenv('USERNAME', 'Admin')
    monkeypatch.setenv('PASSWORD', '1234')
    monkeypatch.setenv('SECRET', 'ThisIsTheKey')
    flask_app = create_app()
    return flask_app

#
# @pytest.fixture()
# def r(request):
#     with _get_client(redis.Redis, request) as client:
#         yield client
#
#
# def _get_client(
#     cls, request, single_connection_client=True, flushdb=True, from_url=None, **kwargs
# ):
#     """
#     Helper for fixtures or tests that need a Redis client
#     Uses the "--redis-url" command line argument for connection info. Unlike
#     ConnectionPool.from_url, keyword arguments to this function override
#     values specified in the URL.
#     """
#     if from_url is None:
#         redis_url = request.config.getoption("--redis-url")
#     else:
#         redis_url = from_url
#     cluster_mode = REDIS_INFO["cluster_enabled"]
#     if not cluster_mode:
#         url_options = parse_url(redis_url)
#         url_options.update(kwargs)
#         pool = redis.ConnectionPool(**url_options)
#         client = cls(connection_pool=pool)
#     else:
#         client = redis.RedisCluster.from_url(redis_url, **kwargs)
#         single_connection_client = False
#     if single_connection_client:
#         client = client.client()
#     if request:
#
#         def teardown():
#             if not cluster_mode:
#                 if flushdb:
#                     try:
#                         client.flushdb()
#                     except redis.ConnectionError:
#                         # handle cases where a test disconnected a client
#                         # just manually retry the flushdb
#                         client.flushdb()
#                 client.close()
#                 client.connection_pool.disconnect()
#             else:
#                 cluster_teardown(client, flushdb)
#
#         request.addfinalizer(teardown)
#     return client
#
#
# def cluster_teardown(client, flushdb):
#     if flushdb:
#         try:
#             client.flushdb(target_nodes="primaries")
#         except redis.ConnectionError:
#             # handle cases where a test disconnected a client
#             # just manually retry the flushdb
#             client.flushdb(target_nodes="primaries")
#     client.close()
#     client.disconnect_connection_pools()