import pytest
import redis
from services import queue as q
import tests.mocked_variables as mv
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

    assert queue_size == 3


def test_delete_with_fakeredis():
    r.lpush(mv.key, mv.value1)
    r.lpush(mv.key, mv.value2)

    queue_size = r.llen(mv.key)
    msg = r.lindex(mv.key, queue_size - 1)

    r.lpop(mv.key)
    queue_size_after_delete_one = r.llen(mv.key)

    assert msg == b'The message test'
    assert queue_size_after_delete_one == 4


def test_delete_with_fakeredis_():
    delete = r.lpop(mv.key)
    print(delete)
    queue_size_after_delete_one = r.llen(mv.key)

    assert queue_size_after_delete_one == 3

if __name__ == "__main__":
    pytest.main()