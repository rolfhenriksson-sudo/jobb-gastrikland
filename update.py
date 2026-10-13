#!/usr/bin/env python3
"""Slå ihop nya annonser i jobs.json, rensa utgångna, committa och pusha.
Användning: python3 update.py nya.json [--no-push]
nya.json = lista med objekt: id, rubrik, arbetsgivare, ort, kategori, beskrivning, krav, sista_dag (YYYY-MM-DD), lank (valfri)."""
import json, sys, subprocess, datetime, os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
today = datetime.date.today().isoformat()
data = json.load(open('jobs.json'))
new = json.load(open(sys.argv[1])) if len(sys.argv) > 1 and not sys.argv[1].startswith('--') else []
known = {j['id']: j for j in data['jobb']}
added = 0
for a in new:
    a['id'] = str(a['id'])
    a.setdefault('lank', 'https://arbetsformedlingen.se/platsbanken/annonser/' + a['id'])
    a['sista_dag'] = a['sista_dag'][:10]
    if a['id'] in known:
        known[a['id']].update({k: v for k, v in a.items() if k != 'first_seen'})
    else:
        a['first_seen'] = today; data['jobb'].append(a); added += 1
before = len(data['jobb'])
data['jobb'] = [j for j in data['jobb'] if j['sista_dag'] >= today]
data['jobb'].sort(key=lambda j: (j['first_seen'], j['id']), reverse=True)
data['senast_uppdaterad'] = today
json.dump(data, open('jobs.json', 'w'), ensure_ascii=False, indent=1)
print(f"Nya: {added}, borttagna utgångna: {before-len(data['jobb'])}, totalt: {len(data['jobb'])}")
if '--no-push' not in sys.argv:
    subprocess.run(['git', 'add', 'jobs.json'], check=True)
    if subprocess.run(['git', 'diff', '--cached', '--quiet']).returncode:
        subprocess.run(['git', 'commit', '-m', f'Uppdatera jobb {today} (+{added})'], check=True)
        subprocess.run(['git', 'push'], check=True)
