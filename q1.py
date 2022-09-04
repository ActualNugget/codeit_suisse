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
    new_df = [[df[0][0]]]

    # dicts keep track of cumulative quantity and notional for each ticker
    c_qty = defaultdict(lambda: 0)
    c_not = defaultdict(lambda: 0)
    
    # set keeps track of tickers that appear at current timestamp
    tickers_here = set()

    for row in df:
        timestamp = row[0]
        ticker = row[1]
        qty = int(row[2])
        price = float(row[3])
        
        # if timestamp is different from previous timestamp
        # then append [ticker, c_qty, c_not] for each element in tickers_here
        # then clear tickers_here
        # then add a new row
        if timestamp != new_df[-1][0]:
            for tickers in sorted(tickers_here):
                new_df[-1].extend([tickers, c_qty[tickers], round(c_not[tickers],1)])
            tickers_here.clear()
            new_df.append([timestamp])
        
        # update cumulatives
        c_qty[ticker] += qty
        c_not[ticker] += qty * price

        # remember ticker at this timestamp
        tickers_here.add(ticker)

    # add last row
    for tickers in sorted(tickers_here):
        new_df[-1].extend([tickers, c_qty[tickers], round(c_not[tickers],1)])

    # flatten new_df using list comprehension magic
    output = []
    for row in new_df:
        output.append(",".join([str(i) for i in row]))

    return output