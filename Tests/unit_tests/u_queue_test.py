import redis
from services import queue as q
import Tests.unit_tests.mocked_variables as mv
import fakeredis
r = fakeredis.FakeStrictRedis(version=6)

def test_push_with_fakeredis():


    r.lpush(mv.key, mv.value)
    tamanio =r.llen(mv.key)
    msg = r.lindex(mv.key, tamanio-1)
    assert msg == b'The message test'

def test_push_with_():

    q.push_redis(mv.key, mv.value)
    tamanio = q.counter_messages(mv.key)
    msg = q.lindex(mv.key, tamanio-1)
    assert msg == b'The message test'