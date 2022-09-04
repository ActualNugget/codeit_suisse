from collections import defaultdict

def to_cumulative_delayed(stream: list, quantity_block: int):

    # create 2d list for stream
    df = []
    for row in stream:
        row = row.split(',')
        df.append(row)

    # sort df by timestamp
    df = sorted(df, key = lambda x: (x[0], x[1]))

    # list stores the aggregated stream
    new_df = []

    # dicts keep track of cumulative quantity and notional for each ticker
    c_qty = defaultdict(lambda: 0)
    c_not = defaultdict(lambda: 0)

    # dict keeps track of at what quantity each ticker next fills a block
    c_qty_pop = defaultdict(lambda: quantity_block)

    # bool to create the first row wherever the first block is filled
    first_pop = True

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
            # evaluate and exclude any overflow notional
            overflow = c_qty[ticker] - c_qty_pop[ticker]
            buffer_not = overflow * price
            block_not = c_not[ticker] - buffer_not # this is valid because all overflow tickers should be the price given in current tick
            # append new row to new_df
            if first_pop:
                new_df.append([timestamp, ticker, c_qty_pop[ticker], round(block_not,1)])
                first_pop = False
            elif timestamp == new_df[-1][0]:
                if ticker == new_df[-1][-3]:
                    new_df[-1][-2] = c_qty_pop[ticker]
                    new_df[-1][-1] = round(block_not,1)
                else:
                    new_df[-1].extend([ticker, c_qty_pop[ticker], round(block_not,1)])
            else:
                new_df.append([timestamp, ticker, c_qty_pop[ticker], round(block_not,1)])
            # increment c_qty_pop
            c_qty_pop[ticker] += quantity_block

    # flatten new_df using list comprehension magic
    output = []
    for row in new_df:
        output.append(",".join([str(i) for i in row]))

    return output


print(to_cumulative_delayed([
    '00:03,C,6,5',
    '00:05,C,5,4',
    '00:05,A,1,1',
    '00:00,A,1,2',
    '00:02,A,1,3',
    '00:03,A,1,4',
    '00:04,A,1,5',
    '00:06,A,7,5.6',
    '00:05,B,25,5.6',
    '00:06,A,7,5.6',
    '00:06,A,7,5.6'
], 5))