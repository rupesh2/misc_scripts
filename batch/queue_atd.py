#!/usr/bin/env python3

from atd import atd
import datetime as dt

# submit jobs
for j in range(1980, 1985):
    atd.at(f"./daymet_minmax.py --year {j}", dt.datetime.now()+ dt.timedelta(seconds=1), queue='b')