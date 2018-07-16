class Base(object):
    field = None
    def __init__(self, server, key):
        self.server = server
        self.key = key

    def __len__(self):
        """Return the length of the queue"""
        raise NotImplementedError

    def push(self, value, filed=None):
        """Push a value"""
        raise NotImplementedError

    def pop(self, timeout=0):
        """Pop a value"""
        raise NotImplementedError

    def clear(self):
        """Clear queue/stack"""
        self.server.delete(self.key)


class FifoQueue(Base):
    """Per-spider FIFO queue"""

    def __len__(self):
        """Return the length of the queue"""
        return self.server.llen(self.key)

    def push(self, value, filed=None):
        """Push a value"""
        return self.server.lpush(self.key, value) == 1

    def pop(self, timeout=0):
        """Pop a value"""
        if timeout > 0:
            data = self.server.brpop(self.key, timeout)
            if isinstance(data, tuple):
                data = data[1]
        else:
            data = self.server.rpop(self.key)
        return data


class PriorityQueue(Base):
    """Per-spider priority queue abstraction using redis' sorted set"""

    def __len__(self):
        """Return the length of the queue"""
        return self.server.zcard(self.key)

    def push(self, value, filed=None):
        score = 0
        return self.server.execute_command('ZADD', self.key, score, value) == 1

    def pop(self, timeout=0):
        """
        Pop a value
        timeout not support in this queue class
        """
        # use atomic range/remove using multi/exec
        pipe = self.server.pipeline()
        pipe.multi()
        pipe.zrange(self.key, 0, 0).zremrangebyrank(self.key, 0, 0)
        results, count = pipe.execute()
        if results:
            return results[0]


class LifoQueue(Base):
    """Per-spider LIFO queue."""

    def __len__(self):
        """Return the length of the stack"""
        return self.server.llen(self.key)

    def push(self, value, filed=None):
        return self.server.lpush(self.key, value) == 1

    def pop(self, timeout=0):
        """Pop a value"""
        if timeout > 0:
            data = self.server.blpop(self.key, timeout)
            if isinstance(data, tuple):
                data = data[1]
        else:
            data = self.server.lpop(self.key)

        return data


class UnsortedSet(Base):
    def __len__(self):
        return self.server.scard(self.key)

    def push(self, value):
        """Push a value"""
        return self.server.sadd(self.key, value) == 1

    def pop(self, timeout=0):
        """Pop a value"""
        data = self.server.spop(self.key)
        return data


class HashTable(Base):
    def __len__(self):
        return self.server.hlen(self.key)

    def push(self, value, filed=None):
        if filed is None:
            return False
        return self.server.hset(self.key, filed, value) == 1

    def pop(self, timeout=0):
        """Pop a value"""
        data = self.server.spop(self.key)
        return data