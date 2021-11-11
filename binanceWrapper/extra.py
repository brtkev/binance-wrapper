import binanceWrapper


def symbolHistorialKlines(symbol : str, interval : str, startTime : int , endTime : int ):
    """fetch klines from startTime to endTime\n"""
    def filterDups(history : list[list]):
        filter = set()
        for bar in history:
            if bar[0] not in filter:
                filter.add(bar[0])
                yield bar 

    startTime *= 1000
    endTime *= 1000
    klines = []
    while startTime < endTime:
        klines.extend(binanceWrapper.symbolKlines(symbol, interval, 1000, startTime))
        startTime = klines[-1][0]
    return list(filterDups(klines))


