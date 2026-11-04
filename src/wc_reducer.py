#!/usr/bin/env python3
"""Word count - reduce step (Hadoop Streaming).

Hadoop guarantees that the lines arriving on stdin are SORTED by key, so all occurrences
of one word come next to each other: we keep only the current word and its sum,
not a dictionary of all words. The last group is printed after the loop.
"""
import sys

current_word = None
current_count = 0

for line in sys.stdin:
    word, count = line.strip().split("\t")
    count = int(count)

    if word == current_word:
        current_count += count
    else:
        if current_word is not None:
            print(f"{current_word}\t{current_count}")

        current_word = word
        current_count = count

if current_word is not None:
    print(f"{current_word}\t{current_count}")
