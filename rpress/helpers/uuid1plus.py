#!/usr/bin/env python
#coding=utf-8


from __future__ import print_function, unicode_literals, absolute_import


__all__ = ['uuid1', 'uuid1fromdatetime']

import time
import ctypes
from datetime import datetime
from uuid import UUID, getnode, _uuid_generate_time, _last_timestamp


########################################################################
class UUID1Plus(UUID):
    """"""
    @property
    #----------------------------------------------------------------------
    def datetime(self):
        """convert uuid object to datetime object"""
        return datetime.fromtimestamp((self.time - 0x01b21dd213814000L) * 100 // 1e9)


#----------------------------------------------------------------------
def _unix_timestamp_to_uuid1(unix_timestamp, node, clock_seq):
    """"""
    global _last_timestamp

    nanoseconds = int(unix_timestamp * 1e9)
    # 0x01b21dd213814000 is the number of 100-ns intervals between the
    # UUID epoch 1582-10-15 00:00:00 and the Unix epoch 1970-01-01 00:00:00.
    timestamp = int(nanoseconds//100) + 0x01b21dd213814000L
    if _last_timestamp is not None and timestamp <= _last_timestamp:
        timestamp = _last_timestamp + 1
    _last_timestamp = timestamp
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
    return UUID1Plus(fields=(time_low, time_mid, time_hi_version,
                        clock_seq_hi_variant, clock_seq_low, node), version=1)


#----------------------------------------------------------------------
def uuid1(node=None, clock_seq=None):
    """Generate a UUID from a host ID, sequence number, and the current time.
    If 'node' is not given, getnode() is used to obtain the hardware
    address.  If 'clock_seq' is given, it is used as the sequence number;
    otherwise a random 14-bit sequence number is chosen."""

    # When the system provides a version-1 UUID generator, use it (but don't
    # use UuidCreate here because its UUIDs don't conform to RFC 4122).
    if _uuid_generate_time and node is clock_seq is None:
        _buffer = ctypes.create_string_buffer(16)
        _uuid_generate_time(_buffer)
        return UUID(bytes=_buffer.raw)

    unix_timestamp = time.time()
    return _unix_timestamp_to_uuid1(unix_timestamp, node, clock_seq)


#----------------------------------------------------------------------
def uuid1fromdatetime(datetime_obj, node=None, clock_seq=None):
    """Generate a UUID from a host ID, sequence number, and the current time.
    If 'node' is not given, getnode() is used to obtain the hardware
    address.  If 'clock_seq' is given, it is used as the sequence number;
    otherwise a random 14-bit sequence number is chosen."""

    unix_timestamp = time.mktime(datetime_obj.timetuple())
    return _unix_timestamp_to_uuid1(unix_timestamp, node, clock_seq)


if __name__ == "__main__":
    import uuid

    print(time.time())
    print(time.mktime(datetime.now().timetuple()))

    uuid_list = []
    uuid_list.append(uuid.uuid1())
    uuid_list.append(uuid1())
    uuid_list.append(uuid1fromdatetime(datetime.now()))

    print('-----------')
    for u in uuid_list:
        print(u)
        if hasattr(u, 'datetime'):
            print(u.datetime)
        else:
            print('classics uuid1')

