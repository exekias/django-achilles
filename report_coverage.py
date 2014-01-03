#!/usr/bin/env python
# coding: utf-8
import json
import os
import sys

from coveralls import Coveralls, cli


# Patch coveralls to get javascript coverage from mocha
orig_get_coverage = Coveralls.get_coverage


def get_coverage_with_js(self):
    report = orig_get_coverage(self)

    js_files = json.load(open('.coverage-js'))['files']
    js_report = []

    for f in js_files:
        source = '\n'.join(open(f['filename']).readlines())
        name = os.path.relpath(f['filename'])
        coverage = [v['coverage'] for v in f['source'].values()]
        coverage = map(lambda x: x if x != '' else None, coverage)

        js_report.append({
            'source': source,
            'name': name,
            'coverage': coverage}
        )

    report += js_report
    return report

Coveralls.get_coverage = get_coverage_with_js

cli.main(sys.argv[1:])
