import random
import string
import logging

import netnode



def get_random_data(N):
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(N))


def main():
    logging.basicConfig(level=logging.DEBUG)

    #
    # here are some test cases for the netnode API
    #
    
    n = netnode.Netnode("$ some.namespace")
    n.kill()

    assert(False == (1 in n))

    n[1] = "hello"
    assert(True == (1 in n))

    assert(n[1] == "hello")

    assert(False == ("2" in n))

    n["2"] = "world"
    assert(True == ("2" in n))

    assert(len(n.keys()) == 2)
    assert(n.keys()[0] == 1)
    assert(n.keys()[1] == "2")

    assert(len(n.values()) == 2)
    assert(n.values()[0] == "hello")
    assert(n.values()[1] == "world")

    assert(len(n.items()) == 2)

    del n[1]
    assert(False == (1 in n))

    del n["2"]

    random_data = get_random_data(4096)
    n[3] = random_data
    n[3] = random_data
    assert(n[3] == random_data)

    logging.info("all tests completed successfully")
    n.kill()

    #
    # the following demonstrates that "hashes" are iterated alphabetically
    #

    n = netnode.Netnode("$ some.namespace")
    m = n._n
    fset = m.hashset
    fget = m.hashval
    flast = m.hashlast
    def hashiter():
        i = m.hash1st()
        while i != idaapi.BADNODE and i is not None:
            yield i
            i = m.hashnxt(i)

    def hashdump():
        logging.debug("hash dump:")
        for k in hashiter():
            logging.debug("  key: %s", k)

        logging.debug("  last: %s", flast())

    logging.debug("setting a -> a")
    fset("a", "a")
    hashdump()

    logging.debug("setting c -> c")
    fset("c", "c")
    hashdump()

    logging.debug("setting b -> b")
    fset("b", "b")
    hashdump()

    # note, the output is: a, b, c

    n.kill()




if __name__ == "__main__":
    main()
