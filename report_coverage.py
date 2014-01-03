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
        source = '\n'.join(l.rstrip() for l in open(f['filename']))
        name = os.path.relpath(f['filename'])
        coverage = []

        # Create sorted coverage array from original dict
        for k, v in sorted(f['source'].items(), key=lambda x:int(x[0])):
            coverage.append(v['coverage'] if v['coverage'] != '' else None)

        js_report.append({
            'source': source,
            'name': name,
            'coverage': coverage}
        )

    report += js_report
    return report

Coveralls.get_coverage = get_coverage_with_js

cli.main(sys.argv[1:])
