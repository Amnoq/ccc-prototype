#!/usr/bin/env python3
"""Router prototype v0.1 — the programmable routing layer.

Reads the machine's real state (prediction ledger, atlas run charters /
reports / grading packets) and proposes next actions under the router's
standing rules. It PROPOSES; the router (human) approves. It never launches.

Standing rules encoded:
  R1  Anything awaiting the router's word (grading verdicts, p_router,
      narrow/wide calls) is surfaced, never auto-decided.
  R2  Both splits: at a fork, cover all branches — never ask which.
  R3  Blind discipline preserved: proposals never pre-state outcomes.
  R4  The map, not the proof: proposals are mapping runs; proof walks
      belong to the research program (his).
  R5  Wall thesis: prefer unmapped sky pairs (the crossings not yet run).
"""
import csv, json, os, re, glob

BASE = os.path.dirname(os.path.abspath(__file__))
RUNS = os.path.join(BASE, 'corpus_runs')

def ledger_state():
    items = []
    with open(os.path.join(BASE, 'prediction_ledger', 'ledger.csv')) as f:
        for row in csv.DictReader(f):
            items.append(row)
    return items

def run_state(name):
    d = os.path.join(RUNS, name)
    st = {'name': name, 'chartered': False, 'complete': False,
          'verdict': None, 'grading_packet': False}
    if not os.path.isdir(d):
        return st
    st['chartered'] = any('CHARTER' in b for b in os.listdir(d))
    rep = glob.glob(os.path.join(d, '*REPORT.md'))
    if rep:
        st['complete'] = True
        txt = open(rep[0]).read()
        m = re.search(r'## Verdict\n\n(.+?)(?:\n\n## |\Z)', txt, re.S)
        if m:
            st['verdict'] = ' '.join(m.group(1).split())[:280]
    st['grading_packet'] = bool(
        glob.glob(os.path.join(d, '*rading*acket*')) +
        glob.glob(os.path.join(d, '*RADING*ACKET*')))
    return st

def main():
    ledger = ledger_state()
    runs = [run_state('atlas%d' % i) for i in range(2, 10)]
    pilot = run_state('atlas')

    needs_router = []
    for i, row in enumerate(ledger, start=1):
        if not row['p_router'].strip():
            needs_router.append(
                'Ledger item %d (%s): p_router still pending — his blind '
                'number, whenever ready.' % (i, row['artifact'][:60]))
        if not row['result'].strip() and row['outcome_class'] in ('pass',):
            pass  # outcome pending by design (dated horizon)
    # grading verdicts known pending from the program record
    needs_router.append(
        'Atlas-3 / Atlas-4: his narrow/wide verdicts still pending '
        '(resolve ledger items 3 and 4).')
    needs_router.append(
        'Atlas-2 / Atlas-5 / Atlas-6 / Atlas-7 / Atlas-8: grading packets '
        'delivered; his grades are the final leg of each verdict.')

    proposals = []
    # R5: unmapped pairs among mapped skies
    mapped = ['pilot/relational', 'analytic-NT (Atlas-2)', 'algebra',
              'geometry(diff)', 'AI-symbolic', 'AI-connectionist',
              'AI-statistical', 'AI-neuro', 'RH-computation', 'RH-proportion',
              'RH-density', 'BSD-analytic', 'BSD-algebraic', 'BSD-computational',
              'prime-literature', 'circle-sieve', 'market-tape*', 'market-fundamentals*',
              'market-narrative*']
    proposals.append({
        'title': 'Analytics↔geometry (the queued follow-up)',
        'why': 'His original intent for ledger item 3 (dictation-corrected); '
               'Atlas-3 tested algebra by mistake. Unmapped pair.',
        'rule': 'R5',
    })
    proposals.append({
        'title': 'Work the Atlas-8 crack shortlist',
        'why': '4 verified cracks (PNT weight-1, admissibility emergent, '
               'twin constant, independent sieve) are program nodes now; '
               'the ND-1 upgrade path (proof of admissible⟺survivors) is '
               'the sharpest. This is program work (R4), not a mapping run '
               '— surfaced, not chartered.',
        'rule': 'R4',
    })
    proposals.append({
        'title': 'Chess atlas (theory vs annotations vs engine)',
        'why': 'His 2026-10-07 musing; the engine is executable ground '
               'truth — the Atlas-8 move in a new domain. Unmapped skies.',
        'rule': 'R5',
    })
    proposals.append({
        'title': 'News-narrative atlas (standalone)',
        'why': 'His 2026-10-07 note: "news is such a great program." '
               'Atlas-9 covers narrative↔tape, but a dedicated narrative-sky '
               'deep map (outlets, wires, analysts as sub-skies) is unmapped.',
        'rule': 'R5',
    })

    # R2: forks currently open get all branches covered
    forks = [
        'Atlas-9 quantitative-sky adaptation: grade runs both ways — '
        'tape-sky succeeds AND tape-sky fails are both findings (R2).',
    ]

    out = ['# Router proposal — %s' % 'generated from live state',
           '',
           '## NEEDS THE ROUTER (his word; never auto-decided)',
           '']
    out += ['- ' + n for n in needs_router]
    out += ['', '## PROPOSED NEXT (rationale each; approval gates each)',
            '']
    for p in proposals:
        out.append('- **%s** [%s]\n  %s' % (p['title'], p['rule'], p['why']))
    out += ['', '## OPEN FORKS (both branches covered)', '']
    out += ['- ' + f for f in forks]
    out += ['', '## RUN LEDGER (as read)', '']
    for r in [pilot] + runs:
        flag = 'COMPLETE' if r['complete'] else ('CHARTED' if r['chartered'] else '—')
        gp = ' + grading packet' if r['grading_packet'] else ''
        out.append('- %s: %s%s' % (r['name'], flag, gp))
    out += ['', '## LEDGER ITEMS (as read)', '']
    for i, row in enumerate(ledger, start=1):
        out.append('- item %d: %s | p_router=%s | result=%s'
                   % (i, row['artifact'][:55], row['p_router'] or '—',
                      row['result'] or 'pending'))
    text = '\n'.join(out)
    path = os.path.join(BASE, 'ROUTING_PROPOSAL.md')
    open(path, 'w').write(text)
    print(text)
    print('\nwrote', path)

if __name__ == '__main__':
    main()
