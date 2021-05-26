from .scheduler import Scheduler


def query(resolvable):
    scheduler = Scheduler(resolvable)
    scheduler.schedule()
    result = []
    for promises in scheduler.buckets.values():
        for item in promises:
            if item:
                result.append(item)
            else:
                pass
    return result
