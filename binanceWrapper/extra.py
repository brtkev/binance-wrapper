import binanceWrapper, time


def symbolHistorialKlines(symbol : str, interval : str, startTime : str , endTime : str ):
    """fetch klines from startTime to endTime\n"""
    def filterDups(history : list[list]):
        filter = set()
        for bar in history:
            if bar[0] not in filter:
                filter.add(bar[0])
                yield bar 

    startTime =  int(time.mktime(time.strptime(startTime, "%d %b %Y"))) * 1000
    endTime = int(time.mktime(time.strptime( endTime, "%d %b %Y"))) * 1000
    klines = []
    while startTime < endTime:
        klines.extend(binanceWrapper.symbolKlines(symbol, interval, 1000, startTime))
        startTime = klines[-1][0]
    return list(filterDups(klines))


