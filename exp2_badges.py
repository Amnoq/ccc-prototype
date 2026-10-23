"""exp2_badges.py -- badge-weighted retrieval prototype for Experiment 2.

Hypothesis (from the cups session): paraphrase-invariant tokens
("badges") -- arXiv IDs, formula fragments, distinctive numbers,
author citations, structured identifiers like D_log -- are reliable
cross-chunk identity signals that TF-IDF destroys (its tokenizer splits
D_log into 'd' [stopword] + 'log').

Method (locked folds, no truth-set changes):
- Same 12 v1 fold registries + concepts as exp2_folds.py (verbatim
  TF-IDF reimplementation as baseline).
- Badge channel: badges extracted by fixed patterns (defined from the
  data's character, not tuned to answers), badge-idf cosine.
- Combined score = tfidf_cosine + badge_cosine (both in [0,1]; no
  tuned weight).
- Ground truth: 144 SAME pairs from fold_*_truth_labels.json
  (pre-correction set; both methods measured identically, so the
  DELTA is the finding).
- Metrics: recall@1, recall@5, MRR over full-registry rankings.
"""
import json, math, re, glob
from collections import Counter, defaultdict

# --- verbatim TF-IDF baseline (from exp2_folds.py) ---
STOP = set("""a an the and or of to in on for with as at by is are was were be been
being it its this that these those from into over after such than then so no not
only own same which who whom whose what when where why how all any both each few
more most other some there their they them he she we you your his her our us vs via
per within without between through during under above below s t d ll m re ve don
does did doing can could shall should will would may might must""".split())
def toks(s):
    return [t for t in re.findall(r'[a-z0-9]+', s.lower()) if t not in STOP and len(t) > 1]

# --- badge extraction: paraphrase-invariant tokens ---
MATH_CHARS = 'ζ∑∏→≤≥Δδλνπσψ·×⟨⟩₀₁₂₃₄₅₆₇₈₉⁵⁶⁻⁺≈∞−–…'
def badges(text):
    """Fixed patterns, defined from the corpus's character. No tuning."""
    t = text.replace(',', '')  # 65,401 -> 65401
    out = []
    # arXiv IDs: 2405.09608
    out += ['arxiv:' + m for m in re.findall(r'\d{4}\.\d{4,5}', t)]
    # structured identifiers: D_log, F_z, E_z (tokenizer destroys these)
    out += ['ident:' + m.lower() for m in re.findall(r'[A-Za-z]+_[A-Za-z0-9]+', t)]
    # author citations: Berry–Keating, Fejér–Riesz ; Name (YYYY)
    out += ['cite:' + m.lower() for m in re.findall(r'[A-Z][A-Za-z]*–[A-Z][A-Za-z]*', t)]
    out += ['cite:' + m.lower().replace(' ', '') for m in
            re.findall(r'[A-Z][a-z]+ \((?:1[0-9]{3}|20[0-9]{2})\)', t)]
    # formula fragments: whitespace-delimited tokens containing math
    for w in re.findall(r'\S+', t):
        wl = w.lower().strip('.,;:()[]{}"\'')
        if not wl:
            continue
        if ('=' in wl or '^' in wl or '_' in wl
                or any(c in MATH_CHARS for c in wl)
                or re.search(r'\d[a-zA-Z]', wl)):
            out.append('formula:' + wl)
    # distinctive numbers: 5+ digits, 3+ decimals, sci notation
    out += ['num:' + m for m in re.findall(r'\d{5,}', t)]
    out += ['num:' + m for m in re.findall(r'\d+\.\d{3,}', t)]
    out += ['num:' + m.lower() for m in re.findall(r'\d+[eE][+-]?\d+', t)]
    # dedupe, drop empties
    seen = []
    for b in out:
        if b and b not in seen:
            seen.append(b)
    return seen

# --- corpus ---
concepts = []
for i in range(1, 13):
    ch = f'c{i:02d}'
    d = json.load(open(f'corpus_runs/r3/{ch}/extraction.json'))
    notes = {a['concept_id']: (a.get('note') or '') for a in d['anchors']}
    for c in d['concepts']:
        concepts.append({'chunk': ch, 'cid': c['id'], 'label': c['label'],
                         'note': notes.get(c['id'], '')})

def entity_text(e):
    return e['label'] + ' ' + ' '.join(e['notes']) + ' ' + ' '.join(e['aliases'])

def idf_weights(docs):
    df = Counter()
    for doc in docs:
        for t in set(doc):
            df[t] += 1
    N = len(docs)
    return {t: math.log(N / (1 + c)) for t, c in df.items()}

def vec(doc, idf):
    tf = Counter(doc)
    v = {t: (1 + math.log(c)) * idf[t] for t, c in tf.items() if t in idf}
    n = math.sqrt(sum(x * x for x in v.values())) or 1.0
    return {t: x / n for t, x in v.items()}

def cos(a, b):
    if len(a) > len(b):
        a, b = b, a
    return sum(v * b.get(t, 0.0) for t, v in a.items())

# --- ground truth: SAME pairs (held_cid -> entity_id), pre-correction set ---
truth = defaultdict(list)  # (chunk) -> [(held_cid, entity_id)]
pair_rank_in_batch = {}
for f in sorted(glob.glob('corpus_runs/exp2_folds/fold_c*_truth_labels.json')):
    ch = f.split('fold_')[1].split('_')[0]
    batch = {p['pair_id']: p for p in
             json.load(open(f'corpus_runs/exp2_folds/fold_{ch}_truth.json'))}
    for l in json.load(open(f)):
        if l['verdict'] == 'SAME':
            p = batch[l['pair_id']]
            truth[ch].append((p['held_cid'], p['entity_id']))
            pair_rank_in_batch[(ch, p['held_cid'], p['entity_id'])] = int(l['pair_id'].split('_')[1])

results = []
for i in range(1, 13):
    held = f'c{i:02d}'
    registry = json.load(open(f'corpus_runs/exp2_folds/fold_{held}_registry.json'))
    hcon = [c for c in concepts if c['chunk'] == held]
    hidx = {c['cid']: k for k, c in enumerate(hcon)}

    edocs = [toks(entity_text(e)) for e in registry]
    qdocs = [toks(c['label'] + ' ' + c['note']) for c in hcon]
    tidf = idf_weights(edocs + qdocs)
    rvecs = [vec(d, tidf) for d in edocs]

    ebadges = [badges(entity_text(e)) for e in registry]
    qbadges = [badges(c['label'] + ' ' + c['note']) for c in hcon]
    bidf = idf_weights(ebadges + qbadges)
    bvecs = [vec(d, bidf) for d in ebadges]
    # rare badges: df <= 3 (a badge shared by many isn't identifying)
    bdf = Counter()
    for doc in ebadges + qbadges:
        for b in set(doc):
            bdf[b] += 1
    rare = {b for b, c in bdf.items() if c <= 3}
    rvecs_rare = [vec([b for b in d if b in rare], bidf) for d in ebadges]

    for (held_cid, true_eid) in truth[held]:
        qi = hidx[held_cid]
        true_ei = next(k for k, e in enumerate(registry) if e['entity_id'] == true_eid)
        qv, qb = vec(qdocs[qi], tidf), vec(qbadges[qi], bidf)
        qbr = vec([b for b in qbadges[qi] if b in rare], bidf)
        cands = []
        for ei in range(len(registry)):
            s_tfidf = cos(qv, rvecs[ei])
            s_badge = cos(qb, bvecs[ei])
            s_rare = cos(qbr, rvecs_rare[ei])
            cands.append((ei, round(s_tfidf, 6), round(s_badge, 6),
                          round(s_rare, 6)))
        # keep top-40 by tfidf (enough for all variants) + always the truth
        cands.sort(key=lambda x: -x[1])
        keep = {ei for ei, _, _, _ in cands[:40]} | {true_ei}
        results.append({'chunk': held, 'held_cid': held_cid,
                        'true_ei': true_ei,
                        'n_entities': len(registry),
                        'q_has_badge': len(qbadges[qi]) > 0,
                        'q_has_rare_badge': len([b for b in qbadges[qi]
                                                 if b in rare]) > 0,
                        'held_label': hcon[qi]['label'][:70],
                        'cands': [(ei, st, sb, sr) for ei, st, sb, sr in cands]})

json.dump(results, open('corpus_runs/exp2_badge_cands.json', 'w'))
print(f"saved {len(results)} queries with candidates")
