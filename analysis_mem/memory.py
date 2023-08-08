#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: leeyoshinari
import gc
import tracemalloc
import linecache
logger.info("-" * 99)
gc.collect()
snapshot = tracemalloc.take_snapshot()
snapshot = snapshot.filter_traces((
    tracemalloc.Filter(False, "<frozen importlib._bootstrap>"),
    tracemalloc.Filter(False, "<unknown>"),
))
top_stats = snapshot.statistics('lineno')

for index, stat in enumerate(top_stats[:10], 1):
    frame = stat.traceback[0]
    filename = os.sep.join(frame.filename.split(os.sep)[-2:])
    logger.info("#%s: %s:%s: %.1f KiB"
                % (index, filename, frame.lineno, stat.size / 1024))
    line = linecache.getline(frame.filename, frame.lineno).strip()
    if line:
        logger.info('    %s' % line)

other = top_stats[10:]
if other:
    size = sum(stat.size for stat in other)
    logger.info("%s other: %.1f KiB" % (len(other), size / 1024))
total = sum(stat.size for stat in top_stats)
logger.info("Total allocated size: %.1f KiB" % (total / 1024))
logger.info("-" * 99)
