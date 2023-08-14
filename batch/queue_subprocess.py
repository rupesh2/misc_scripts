#!/usr/bin/env python3

import subprocess

for j in range(1980, 1985):
    output = subprocess.Popen(f"./daymet_minmax.py --year {j} | batch ", shell=True)
