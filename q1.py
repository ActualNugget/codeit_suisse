from collections import defaultdict

def to_cumulative(stream: list):

    # create 2d list for stream
    df = []
    for row in stream:
        row = row.split(',')
        df.append(row)

    # sort df by timestamp
    df.sort(key= lambda i: i[0])

    # list stores the aggregated stream
    newdf = [[df[0][0]]]

    # set keeps track of tickers that appear at current timestamp
    tickers_here = set()

    # dicts keep track of cumulative quantity and notional for each ticker
    c_qty = defaultdict(lambda: 0)
    c_not = defaultdict(lambda: 0)

    for row in df:
        timestamp = row[0]
        ticker = row[1]
        qty = int(row[2])
        price = float(row[3])
        
        # if timestamp is different from previous timestamp
        # then append [ticker, c_qty, c_not] for each element in tickers_here
        # then clear tickers_here
        # then add a new row
        if timestamp != newdf[-1][0]:
            for tickers in sorted(tickers_here):
                newdf[-1].extend([tickers, c_qty[tickers], c_not[tickers]])
            tickers_here.clear()
            newdf.append([timestamp])
        
        # update cumulatives and remember ticker
        c_qty[ticker] += qty
        c_not[ticker] += qty * price
        tickers_here.add(ticker)

    # add last row
    for tickers in sorted(tickers_here):
        newdf[-1].extend([tickers, c_qty[tickers], c_not[tickers]])

    # flatten newdf using list comprehension magic
    output = []
    for row in newdf:
        output.append(",".join([str(i) for i in row]))

    return output