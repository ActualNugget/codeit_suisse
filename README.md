# codeit_suisse
## Assumptions
- (Given) `timestamp` is in the format hh:mm
- (Given) `price` is a *positive* decimal > 0.0 (float rounded to 1 decimal place in Part 2)
- (Given) each tick arrives in *exactly* the format `timestamp, ticker, quantity, price`
- Solutions are given sufficient time to run (O(n log n))
- Part 2: If a single ticker's quantity increases by multiple times of `quantity_block` within a single `timestamp`, only the laargest multiple of `quantity_block` will be reported
    - e.g. for `quantity_block = 5`, if `c_qty` (cumulative quantity) of ticker `A` increases from 3 to 11 timestamp `00:03`, the program will only report the cumulative quantity and corresponding notional for `c_qty = 10`, skipping over `c_qty = 5`