# codeit_suisse
## Assumptions
- (Given) `timestamp` is in the format hh:mm
- (Given) `price` is a *positive* decimal > 0.0 (float rounded to 1 decimal place in Part 2)
- (Given) each tick arrives in *exactly* the format `timestamp, ticker, quantity, price`
- Solutions are given sufficient time to run (O(n log n))
- Part 2: If a single ticker's quantity increases by multiple times of `quantity_block` within a single `timestamp`, only the last block of `quantity_block` will be reported
    - e.g. for `quantity_block = 5`, if `c_qty` (cumulative quantity) of ticker `A` increases from 3 to 11 within timestamp `00:03`, the program will only report the cumulative quantity and corresponding notional for `c_qty = 10`, skipping over `c_qty = 5`
    - This behaviour can be easily changed to have it report each individual block (`00:03,A,5,5,A,10,10`), but this seemed to be counterproductive to the original aim of Part 1, to *aggregate* the stream by time and ticker