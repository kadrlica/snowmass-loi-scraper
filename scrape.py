#!/usr/bin/env python
"""
Scrape LOI information for Snowmass
"""
__author__ = "Alex Drlica-Wagner"
from collections import OrderedDict as odict
import requests
from lxml import html
import numpy as np
import pandas as pd

FRONTIERS = odict([
    ('AF',['AF%d'%i for i in range(0,8)]),
    ('CF',['CF%d'%i for i in range(0,8)]),
    ('CommF',['CommF%d'%i for i in range(0,7)]),
    ('CompF',['CompF%d'%i for i in range(0,8)]),
    ('EF',['EF%d'%i for i in range(0,11)]),
    ('IF',['IF%d'%i for i in range(0,11)]),
    ('NF',['NF%d'%i for i in range(0,11)]),
    ('RF',['RF%d'%i for i in range(0,8)]),
    ('TF',['TF%d'%i for i in range(0,12)]),
    ('UF',['TF%d'%i for i in range(0,7)]),
])
TOPICS = [topic for topics in list(FRONTIERS.values()) for topic in topics]
URL = 'https://www.snowmass21.org/docs/files/?dir=summaries/'

import argparse
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('-f','--frontier',default=None,choices=(FRONTIERS.keys()))
args = parser.parse_args()

if args.frontier: topics = FRONTIER[args.frontier]
else: topics = TOPICS

dtype = [('filename',object),('frontier',object),('number',object),('topics',object)]

results = []
for f in FRONTIERS:
    print("Frontier: %s"%f)
    page = requests.get(URL+'/'+f)
    tree = html.fromstring(page.content)
    files = tree.xpath('//span[@class="file-name col-md-7 col-sm-6 col-xs-9"]/text()')
    files = np.char.strip(np.unique(files))
    files = files[ (files != '') & (files != '..')]
    info = np.char.replace(np.char.partition(files,'-')[:,-1],'.pdf','')
    junk = np.char.rpartition(info,'-')[:,0]
    number = np.char.rpartition(info,'-')[:,-1]

    result = np.recarray(len(files),dtype=dtype)
    result['filename'] = files
    result['frontier'] = f
    result['number'] = number
    result['topics'] = ''

    for t in topics:
        sel = (np.char.count(junk,t) > 0)
        result['topics'] += np.where(sel,t+',','')

    result = result[np.argsort(number)]
    print("  %d"%len(result))
    results.append(result)
results = np.concatenate(results)
results['topics'] = np.char.strip(results['topics'].astype(str),',')

outfile = 'scrape_loi_all.csv'

if args.frontier:
    sel = (results['topics'] != '')
    results = results[sel]
    outfile = 'scrape_loi_%s.csv'%args.frontier

pd.DataFrame(results).to_csv(outfile,index=False,encoding="utf-8")

