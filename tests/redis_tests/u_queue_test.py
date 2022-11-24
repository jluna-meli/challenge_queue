import redis
from services import queue as q
import tests.redis_tests.mocked_variables as mv
import fakeredis

r = fakeredis.FakeStrictRedis(version=6)


def test_push_verify_by_msg():
    r.lpush(mv.key, mv.value)

    queue_size = r.llen(mv.key)
    msg = r.lindex(mv.key, queue_size - 1)

    assert msg == b'The message test'


def test_count_verify_by_size():
    r.lpush(mv.key, mv.value)
    r.lpush(mv.key, mv.value)

    queue_size = r.llen(mv.key)

    assert queue_size == 2


def test_delete_with_fakeredis():
    r.lpush(mv.key, mv.value1)
    r.lpush(mv.key, mv.value2)

    queue_size = r.llen(mv.key)
    msg = r.lindex(mv.key, queue_size - 1)

    r.lpop(mv.key)
    queue_size_after_delete_one = r.llen(mv.key)

    assert msg == b'The message test 1'
    assert queue_size_after_delete_one == 1


def test_delete_with_fakeredis():
    delete = r.lpop(mv.key)
    print(delete)
    queue_size_after_delete_one = r.llen(mv.key)

    assert queue_size_after_delete_one == 0
