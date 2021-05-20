from .scheduler import Scheduler


def query(resolvable):
    scheduler = Scheduler(resolvable)
    scheduler.schedule()
    result = []
    for promises in scheduler.buckets.values():
        for item in promises:
            #TODO CHECK THIS
            if item['status'] == 'fulfilled':
                result.append(item['value'])
            else:
                pass
    return result
