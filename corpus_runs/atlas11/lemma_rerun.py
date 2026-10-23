#!/usr/bin/env python3
"""Atlas-11 lemma rerun (2026-10-08): discriminating test of the mapping hypothesis.

Re-runs the EXACT mechanical candidate generation from merge_atlas11.py
(same IDF-weighted token+bigram scoring, same thresholds: 8.0 direct,
10.0 control arms), with one change: node label+note text is lemmatized
via lemma-db/form2lemma.json before tokenization.

New candidates = pairs not in the original candidates.json. Only those go
to reviewed adjudication. Original 381 verdicts stand untouched.
"""
import json, math, os, sys
from collections import defaultdict

BASE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE)
from merge_atlas11 import (normalize, wtokens, wgrams, constants, node_texts,
                           STOP, META, PREFIX)

GRAPHD = os.path.join(BASE, 'graphs')
F2L = json.load(open(os.path.expanduser('~/workspace/lemma-db/form2lemma.json'),
                     encoding='utf-8'))

def lemmatize(text):
    return ' '.join(F2L.get(w, w) for w in text.split())

def main():
    sky_graphs = {}
    for sky in ['analytics', 'geometry', 'bridge']:
        with open(os.path.join(GRAPHD, f'{sky}_graph.json')) as f:
            sky_graphs[sky] = json.load(f)

    # node_texts but lemmatized: (lemmatized_text, label, status, note0)
    texts = {}
    for sky, g in sky_graphs.items():
        tmap = {}
        for sid, (t, la, sta, na0) in node_texts(g).items():
            tmap[sid] = (lemmatize(t), la, sta, na0)
        texts[sky] = tmap

    n_nodes = sum(len(t) for t in texts.values())
    toksets, gramsets, constsets = {}, {}, {}
    df_tok, df_gram = defaultdict(int), defaultdict(int)
    for sky, tmap in texts.items():
        for sid, (t, _l, _s, _n) in tmap.items():
            ts, gs = set(wtokens(t)), set(wgrams(t, 2))
            toksets[(sky, sid)] = ts
            gramsets[(sky, sid)] = gs
            constsets[(sky, sid)] = constants(t)
            for x in ts:
                df_tok[x] += 1
            for x in gs:
                df_gram[x] += 1
    idf_tok = {x: math.log((n_nodes + 1) / (d + 1)) + 1.0
               for x, d in df_tok.items()}
    idf_gram = {x: math.log((n_nodes + 1) / (d + 1)) + 1.0
                for x, d in df_gram.items()}

    pairs = [('analytics', 'geometry', 8.0),
             ('bridge', 'analytics', 10.0),
             ('bridge', 'geometry', 10.0)]
    candidates = []
    for sa, sb, tau in pairs:
        for sida, (ta, la, sta, na0) in texts[sa].items():
            tsa, gsa, csa = (toksets[(sa, sida)], gramsets[(sa, sida)],
                             constsets[(sa, sida)])
            for sidb, (tb, lb, stb, nb0) in texts[sb].items():
                tsb, gsb, csb = (toksets[(sb, sidb)], gramsets[(sb, sidb)],
                                 constsets[(sb, sidb)])
                shared_t = tsa & tsb
                shared_g = gsa & gsb
                shared_c = csa & csb
                score = (sum(idf_tok[x] for x in shared_t)
                         + 2.5 * sum(idf_gram[x] for x in shared_g)
                         + (8.0 if shared_c else 0.0))
                if score >= tau or shared_c:
                    top_t = sorted(shared_t, key=lambda x: -idf_tok[x])[:12]
                    top_g = sorted(shared_g, key=lambda x: -idf_gram[x])[:8]
                    candidates.append({
                        'pair': f'{sa}<->{sb}',
                        'threshold': tau,
                        'a_sky': sa, 'a': f'{PREFIX[sa]}:{sida}',
                        'a_label': la[:200], 'a_status': sta,
                        'a_note': na0[:300],
                        'b_sky': sb, 'b': f'{PREFIX[sb]}:{sidb}',
                        'b_label': lb[:200], 'b_status': stb,
                        'b_note': nb0[:300],
                        'shared_constants': sorted(shared_c),
                        'shared_tokens': top_t,
                        'shared_bigrams': top_g,
                        'score': round(score, 2)})
    candidates.sort(key=lambda c: (c['pair'], -c['score']))

    old = json.load(open(os.path.join(BASE, 'candidates.json')))
    old_recs = old['candidates'] if isinstance(old, dict) else old
    old_pairs = {(c['a'], c['b']) for c in old_recs}
    new = [c for c in candidates if (c['a'], c['b']) not in old_pairs]

    out = {
        'method': ('Identical to candidates.json generation (IDF-weighted '
                   'token+bigram overlap, same thresholds), except node '
                   'label+note text lemmatized via lemma-db/form2lemma.json '
                   '(182,903 forms) before tokenization. New = pairs absent '
                   'from the original 381; original verdicts untouched.'),
        'rerun_total': len(candidates),
        'original_total': len(old_recs),
        'new_candidates': len(new),
        'candidates': new,
    }
    with open(os.path.join(BASE, 'candidates_lemma_rerun.json'), 'w') as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    from collections import Counter
    print('rerun total:', len(candidates), '| new:', len(new))
    print(Counter(c['pair'] for c in new))

if __name__ == '__main__':
    main()
