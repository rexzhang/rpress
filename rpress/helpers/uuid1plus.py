#!/usr/bin/env python
#coding=utf-8


from __future__ import print_function, unicode_literals, absolute_import

import time
from datetime import datetime
from uuid import UUID, getnode


#----------------------------------------------------------------------
def uuid1plus(datetime, node=None, clock_seq=None):
    """Generate a UUID from a host ID, sequence number, and the current time.
    If 'node' is not given, getnode() is used to obtain the hardware
    address.  If 'clock_seq' is given, it is used as the sequence number;
    otherwise a random 14-bit sequence number is chosen."""

    #nanoseconds = int(time.time() * 1e9)
    # 0x01b21dd213814000 is the number of 100-ns intervals between the
    # UUID epoch 1582-10-15 00:00:00 and the Unix epoch 1970-01-01 00:00:00.
    #timestamp = int(nanoseconds//100) + 0x01b21dd213814000L
    timestamp = int(time.mktime(datetime.timetuple()))

    if clock_seq is None:
        import random
        clock_seq = random.randrange(1<<14L) # instead of stable storage
    time_low = timestamp & 0xffffffffL
    time_mid = (timestamp >> 32L) & 0xffffL
    time_hi_version = (timestamp >> 48L) & 0x0fffL
    clock_seq_low = clock_seq & 0xffL
    clock_seq_hi_variant = (clock_seq >> 8L) & 0x3fL
    if node is None:
        node = getnode()
    return UUID(fields=(time_low, time_mid, time_hi_version,
                        clock_seq_hi_variant, clock_seq_low, node), version=1)


#----------------------------------------------------------------------
def uuid1plus2datetime(uuid):
    """convert uuid object to datetime object"""
    return datetime.fromtimestamp(uuid.get_time())


if __name__ == "__main__":
    d = datetime.now()
    print(d)
    print(int(time.mktime(d.timetuple())))

    u = uuid1plus(datetime=d)
    print(u)
    print(u.get_time())

    print(uuid1plus2datetime(u))
