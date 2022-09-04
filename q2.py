from collections import defaultdict

def to_cumulative_delayed(stream: list, quantity_block: int):

    # create 2d list for stream
    df = []
    for row in stream:
        row = row.split(',')
        df.append(row)

    # sort df by timestamp
    df.sort(key= lambda i: i[0])

    # list stores the aggregated stream
    new_df = []

    # dicts keep track of cumulative quantity and notional for each ticker
    c_qty = defaultdict(lambda: 0)
    c_not = defaultdict(lambda: 0)

    # dict keeps track of at what quantity each ticker next fills a block
    c_qty_pop = defaultdict(lambda: quantity_block)

    for row in df:
        timestamp = row[0]
        ticker = row[1]
        qty = int(row[2])
        price = float(row[3])
        
        # update cumulatives
        c_qty[ticker] += qty
        c_not[ticker] += qty * price

        # while quantity_block is filled
        while c_qty[ticker] >= c_qty_pop[ticker]:
            # evaluate and exclude overflow notional
            overflow = c_qty[ticker] - c_qty_pop[ticker]
            buffer_not = overflow * price
            block_not = c_not[ticker] - buffer_not
            # append new row to new_df
            new_df.append([timestamp, ticker, c_qty_pop[ticker], round(block_not,1)])
            # increment c_qty_pop
            c_qty_pop[ticker] += quantity_block

    # flatten new_df using list comprehension magic
    output = []
    for row in new_df:
        output.append(",".join([str(i) for i in row]))

    return output