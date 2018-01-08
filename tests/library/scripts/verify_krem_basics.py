#!/bin/env python

import subprocess

if __name__ == '__main__':
    out = subprocess.call(["krem", "run", "-j", "simple_job"])

    if out:
        print("ERROR: KREM basics verification failed")
        print("Skipping remaining tests")
    else:
        print("INFO: KREM basics successfully verified")
    exit(out)
