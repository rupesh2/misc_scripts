#!/usr/bin/env python3

import argparse
import sys
import datetime as dt
import netCDF4 as nc
import numpy as np
from glob import glob
from os import path


def parse_args(args):
    """Parses command line agruments."""

    parser = argparse.ArgumentParser(
        description="Get min max from daymet",
        usage="daymet_minmax.py --year <year>\n"
    )
    
    parser.add_argument(
        "--year",
        required=True, 
        type=check_yrfmt,
        help="year in YYYY format"
    )

    return parser.parse_args(args)

def check_yrfmt(d: str):
    """Checks if year are in correct format.
    """
    try:
        return dt.datetime.strptime(d, "%Y").year
    except ValueError:
        msg = "not a valid year in YYYY format"
        raise argparse.ArgumentTypeError(msg)
    
def get_minmax(y: str, v: str):
    """Returns min max value for Jan 1"""
    DAYMET_DIR = "/data/daymet/Daymet_Daily_V4R1/data/"
    min_arr=[]
    max_arr=[]
    
    for g in glob(path.join(DAYMET_DIR, f"*{v}_{y}*")):
        with nc.Dataset(g, 'r') as ds:
            ds_v = ds.variables[v][0, :, :] # Jan 1 values
            min_arr.append(np.nanmin(ds_v))
            max_arr.append(np.nanmax(ds_v))
    
    return np.nanmin(min_arr), np.nanmax(max_arr)

def main():
    parser = parse_args(sys.argv[1:])
    daymet_yr = parser.year
    DAYMET_VARS = ['tmax', 'tmin', 'prcp', 'dayl', 'srad', 'swe', 'vp']
    tstamp = int(dt.datetime.utcnow().timestamp())
    outf = f"daymet_minmax_jan01_{daymet_yr}_{tstamp}.txt"
    with open(outf, "w") as f:
        for daymet_v in DAYMET_VARS:
            f.write(f"{daymet_v}, {get_minmax(daymet_yr, daymet_v)}\n")

if __name__ == "__main__":
    main()