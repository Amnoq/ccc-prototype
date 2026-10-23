"""build_r3.py -- deterministic R3 pipeline per chunk (coordinator-run, not blind).

Usage: python3 build_r3.py c04
Reads corpus_runs/r3/cNN/extraction.json, validates, builds registry +
R3 injection, computes costs with the R2-identical conventions, writes
injection.txt and a partial report.json (parity filled in after scoring).
"""
import json, sys
import tiktoken
sys.path.insert(0, '/home/hatch/workspace/ccc-prototype')
import memory_harness as mh
from extractor_rev2 import EXTRACTOR_PROMPT_R3

CHUNK_FILES = {
    'c01': 'corpus/c01_completemap.txt',
    'c02': 'corpus/c02_deriv_d1_d5.txt',
    'c03': 'corpus/c03_deriv_d6_d8.txt',
    'c04': 'corpus/c04_deriv_d9_d10a12.txt',
    'c05': 'corpus/c05_deriv_d10a3_d10c.txt',
    'c06': 'corpus/c06_deriv_d10de_n14.txt',
    'c07': 'corpus/c07_dtree_nodes0_9.txt',
    'c08': 'corpus/c08_dtree_node10.txt',
    'c09': 'corpus/c09_dtree_node11.txt',
    'c10': 'corpus/c10_dtree_nodes12_13.txt',
    'c11': 'corpus/c11_dtree_d6gen_priorart_n14_11f.txt',
    'c12': 'corpus/c12_operator_audit.txt',
}

enc = tiktoken.get_encoding('cl100k_base')
PROMPT_TOKENS = len(enc.encode(EXTRACTOR_PROMPT_R3))  # template only; 1014


def main(ch):
    base = f'/home/hatch/workspace/ccc-prototype/corpus_runs/r3/{ch}'
    doc = json.load(open(f'{base}/extraction.json'))
    failures = mh.validate_extraction(doc)
    if failures:
        print(f'{ch}: VALIDATION FAILURES:')
        for f in failures:
            print('  -', f)
        return False
    reg = mh.build_registry(doc)
    inj = mh.inject_grouped_r3(doc, reg)
    open(f'{base}/injection.txt', 'w').write(inj)
    prose = open('/home/hatch/workspace/ccc-prototype/' + CHUNK_FILES[ch]).read()
    prose_tokens = len(enc.encode(prose))
    output_tokens = len(enc.encode(json.dumps(doc)))
    body = inj.split('INJECTED STRUCTURE (grouped compact):\n\n', 1)[1]
    injected_nolegend = len(enc.encode(body))
    savings = prose_tokens - injected_nolegend
    be_lab = (PROMPT_TOKENS + prose_tokens + output_tokens) / savings
    be_dep = (prose_tokens + output_tokens) / savings
    partial = {
        'chunk': ch,
        'chunk_file': CHUNK_FILES[ch],
        'verifier_attempts': 1,
        'repairs': 0,
        'extraction_stats': {
            'concepts': len(doc['concepts']),
            'edges': len(doc['edges']),
            'strands': len(doc['strands']),
            'anchors': len(doc['anchors']),
        },
        'costs': {
            'prose_tokens': prose_tokens,
            'prompt_tokens': PROMPT_TOKENS,
            'output_tokens': output_tokens,
            'injected_tokens': injected_nolegend,
            'injected_tokens_with_legend': len(enc.encode(inj)),
            'savings_per_session': savings,
            'break_even_lab': round(be_lab, 2),
            'break_even_deployment': round(be_dep, 2),
        },
    }
    json.dump(partial, open(f'{base}/report_partial.json', 'w'), indent=1)
    print(f'{ch}: valid | concepts={len(doc["concepts"])} edges={len(doc["edges"])} '
          f'anchors={len(doc["anchors"])} | inj_nolegend={injected_nolegend} '
          f'BE_lab={be_lab:.2f} BE_dep={be_dep:.2f}')
    return True


if __name__ == '__main__':
    ok = main(sys.argv[1])
    sys.exit(0 if ok else 1)
