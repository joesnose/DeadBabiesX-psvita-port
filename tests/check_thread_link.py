#!/usr/bin/env python3
"""Reject Vita ELFs whose static pthread linkage disables C++ threading."""
import subprocess
import sys

if len(sys.argv) != 3:
    raise SystemExit('usage: check_thread_link.py /path/to/arm-vita-eabi-nm /path/to/DeadBabiesXVita')
symbols = subprocess.check_output([sys.argv[1], sys.argv[2]], text=True)
matches = [line.split() for line in symbols.splitlines() if line.split()[-1:] == ['pthread_cancel']]
if len(matches) != 1 or len(matches[0]) != 3 or matches[0][1] != 'T' or int(matches[0][0], 16) == 0:
    raise SystemExit('FAIL: pthread_cancel must be defined; a missing weak symbol disables libstdc++ threading')
missing = [line for line in symbols.splitlines() if len(line.split()) == 2 and line.split()[0] in ('w', 'U') and line.split()[1].startswith(('pthread_', 'sched_'))]
if missing:
    raise SystemExit('FAIL: unresolved threading functions: ' + ', '.join(missing))
print('PASS: pthread_cancel is linked as a defined function; C++ thread availability probe is nonzero')
