import os
import random
import string
import logging
import contextlib

import idaapi
import pytest

import netnode


TEST_NAMESPACE = '$ some.namespace'


def get_random_data(N):
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(N))


@contextlib.contextmanager
def killing_netnode(namespace):
    '''
    wraps a netnode in a contextmanager that will
     eventually destroy its contents.
    probably only useful for testing when a clean state is req'd.
    '''
    n = netnode.Netnode(namespace)
    try:
        yield n
    finally:
        n.kill()


def test_basic_features():
    '''
    demonstrate the basic netnode API (like a dict)
    '''
    with killing_netnode(TEST_NAMESPACE) as n:
        # there is nothing in the netnode to begin with
        assert(False == (1 in n))

        # when we add one key, there is one thing in it
        n[1] = 'hello'
        assert(True == (1 in n))
        assert(n[1] == 'hello')
        # but nothing else
        assert(False == ('2' in n))

        # then when we add a second thing, its also there
        n['2'] = 'world'
        assert(True == ('2' in n))
        assert(len(n.keys()) == 2)
        assert(n.keys()[0] == 1)
        assert(n.keys()[1] == '2')
        assert(len(n.values()) == 2)
        assert(n.values()[0] == 'hello')
        assert(n.values()[1] == 'world')
        assert(len(n.items()) == 2)

        # and when we delete the first item, only it is deleted
        del n[1]
        assert(False == (1 in n))

        # and finally everything is gone
        del n['2']


def test_large_data():
    '''
    demonstrate that netnodes support large data values.
    '''
    with killing_netnode(TEST_NAMESPACE) as n:
        random_data = get_random_data(1024 * 8)
        n[3] = random_data
        assert(n[3] == random_data)


def test_hash_ordering():
    ''' 
    the following demonstrates that 'hashes' are iterated alphabetically.
    this is an IDAPython implementation feature.
    '''

    with killing_netnode(TEST_NAMESPACE) as n:
        m = n._n

        def hashiter(m):
            i = m.hash1st()
            while i != idaapi.BADNODE and i is not None:
                yield i
                i = m.hashnxt(i)

        def get_hash_order(hiter):
            return [k for k in hiter]

        m.hashset('a', 'a')
        assert get_hash_order(hashiter(m)) == ['a']

        m.hashset('c', 'c')
        assert get_hash_order(hashiter(m)) == ['a', 'c']

        m.hashset('b', 'b')
        assert get_hash_order(hashiter(m)) == ['a', 'b', 'c']


def test_iterkeys():
    LARGE_VALUE = get_random_data(16 * 1024)
    LARGE_VALUE2 = get_random_data(16 * 1024)
    import zlib
    assert(zlib.compress(LARGE_VALUE) > 1024)
    assert(zlib.compress(LARGE_VALUE2) > 1024)

    assert LARGE_VALUE != LARGE_VALUE2

    with killing_netnode(TEST_NAMESPACE) as n:
        n[1] = LARGE_VALUE
        assert set(n.keys()) == set([1])

        n[2] = LARGE_VALUE2
        assert set(n.keys()) == set([1, 2])

        assert n[1] != n[2]

    with killing_netnode(TEST_NAMESPACE) as n:
        n['one'] = LARGE_VALUE
        assert set(n.keys()) == set(['one'])

        n['two'] = LARGE_VALUE2
        assert set(n.keys()) == set(['one', 'two'])

        assert n['one'] != n['two']
        
    with killing_netnode(TEST_NAMESPACE) as n:
        n[1] = LARGE_VALUE
        assert set(n.keys()) == set([1])

        n[2] = LARGE_VALUE
        assert set(n.keys()) == set([1, 2])

        n['one'] = LARGE_VALUE
        assert set(n.keys()) == set([1, 2, 'one'])

        n['two'] = LARGE_VALUE
        assert set(n.keys()) == set([1, 2, 'one', 'two'])

        n[3] = "A"
        assert set(n.keys()) == set([1, 2, 'one', 'two', 3])
 
        n['three'] = "A"
        assert set(n.keys()) == set([1, 2, 'one', 'two', 3, 'three'])
 

def main():
    logging.basicConfig(level=logging.DEBUG)

    # cleanup any existing data
    netnode.Netnode(TEST_NAMESPACE).kill()

    pytest.main(['--capture=sys', os.path.dirname(__file__)])


if __name__ == '__main__':
    main()
