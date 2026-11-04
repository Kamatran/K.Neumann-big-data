#!/usr/bin/env python3
"""Word count - map step (Hadoop Streaming).

Hadoop Streaming starts this program as a separate process, feeds the lines of one input
split to stdin and captures every line printed to stdout as one key<TAB>value pair.
print() hands a pair over to Hadoop; diagnostics would go to stderr, never to stdout.
"""
import sys

for line in sys.stdin:
    words = line.strip().split()

    for word in words:
        print(f"{word}\t1")
