#!/usr/bin/python
import time
import re
import subprocess
from optparse import OptionParser

SLEEP_INTERVAL = 1.0

def readlines_then_tail(fin):
    "Iterate through lines and then tail for further lines."
    while True:
        line = fin.readline()
        if line:
            continue
        else:
            break

def tail(fin, exp):
    "Listen for new lines added to file."
    while True:
        where = fin.tell()
        line = fin.readline()
        if not line:
            time.sleep(SLEEP_INTERVAL)
            fin.seek(where)
        else:
            if re.search(exp, line):
                print line.strip()
                # cmd_str needs to be cleaned up to use variables assigned from config file or predefined variables.  Also avoid escaping quotes so use single quotes
                # Also this str can be created using string concatenation
                cmd_str = "./send_email.py -emailServer \"emailServerName\" -subject \"subjectOfEmail\" -from \"fromEmailAddress\" -to \"toEmailAddress01\" \"toEmailAddress02\" \"toEmailAddress03\" -body \"" + line + "\""
                proc = subprocess.Popen([cmd_str], shell=True, stdin=None, stdout=None, stderr=None, close_fds=True)
            yield line
            
def main():
    p = OptionParser("usage: tailmail.py file regex")
    (options, args) = p.parse_args()
    if len(args) < 2:
        p.error("must specify a file to watch with regex after")
    with open(args[0], 'r') as fin:
        readlines_then_tail(fin)
        for line in tail(fin, args[1]):
            continue

if __name__ == '__main__':
    main()
