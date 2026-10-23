#!/usr/bin/env python3
"""codon.py -- the CCC origin system: a base-9 codon code.

His spec (2026-10-17/18):
- 9 symbols: 4 directional triangles (apex up/right/down/left) + 4 line
  characters (sideways views: vertical, horizontal, two diagonals) + a
  9th: a color change (not a position -- a state).
- Geometry: stella octangula -- 8 positions as the 8 vertices (4+4 across
  the dual tetrahedra), the 9th at the inversion center (the unmoved point).
- The sideways derivation (triangle -> line) IS the inversion exchanging
  the dual pair.
- Constraint: the labeling must exhibit 2*3=6 geometrically ("two and
  three converge every six").
- Rendering: five colors; the ninth renders shiny/metallic.

Provisional choices (labeled; his verdict to change):
- Digit assignment: color-change = 0 (DERIVED: 0 = the unmoved point,
  fixed by inversion since -0 = 0). Triangles 1-4 clockwise from up;
  lines 5-8. Otherwise conventional.
- Triangle->line pairing is FIXED by the negation structure (below), not
  by visual metaphor: inversion must act as mod-9 negation for the
  labeling to exhibit arithmetic, so invert(triangle d) = line (9-d).
- Colors: up red, right yellow, down blue, left green (provisional);
  lines inherit their source triangle's color; ninth shiny-white.
  (The image's fifth color family, purple, is unassigned -- open.)

Derived (exact): with antipodal vertex pairs summing to 9, central
inversion acts as negation mod 9 on digit labels: invert(d) = (-d) mod 9.
Hence invert maps {1,2,3,4} exactly onto {8,7,6,5} -- triangles to lines,
the sideways derivation, as arithmetic. And 6 is doubly determined:
2*3 = 6 AND -3 = 6 (mod 9). "Two and three converge at six," exhibited.
"""

# ---------------------------------------------------------------- symbols

# digit -> symbol record. vertex = cube corner (stella octangula vertex);
# None for the ninth (it is the center, not a vertex).
SYMBOLS = {
    0: dict(glyph='\u2726', name='ninth',      kind='ninth',    color='shiny-white', vertex=None),
    1: dict(glyph='\u25b3', name='up',         kind='triangle', color='red',         vertex=( 1, 1, 1)),
    2: dict(glyph='\u25b7', name='right',      kind='triangle', color='yellow',      vertex=( 1,-1,-1)),
    3: dict(glyph='\u25bd', name='down',       kind='triangle', color='blue',        vertex=(-1, 1,-1)),
    4: dict(glyph='\u25c1', name='left',       kind='triangle', color='green',       vertex=(-1,-1, 1)),
    5: dict(glyph='\u2502', name='vertical',   kind='line',     color='green',       vertex=( 1, 1,-1)),  # invert(4)
    6: dict(glyph='\u2500', name='horizontal', kind='line',     color='blue',        vertex=( 1,-1, 1)),  # invert(3)
    7: dict(glyph='\u2571', name='diag-up',    kind='line',     color='yellow',      vertex=(-1, 1, 1)),  # invert(2)
    8: dict(glyph='\u2572', name='diag-down',  kind='line',     color='red',         vertex=(-1,-1,-1)),  # invert(1)
}

def glyph(d):
    return SYMBOLS[d]['glyph']

def show(digits):
    """Render a digit sequence as glyphs."""
    return ''.join(glyph(d) for d in digits)

# ---------------------------------------------------------------- operations
# All exact (permutations of the 9 digits).

def invert(d):
    """Sideways derivation = central inversion = negation mod 9. Exact."""
    return (-d) % 9

def rotate(d):
    """90-degree clockwise rotation. Triangles 4-cycle; lines pair up."""
    return {0: 0, 1: 2, 2: 3, 3: 4, 4: 1, 5: 6, 6: 5, 7: 8, 8: 7}[d]

def flip(d):
    """Horizontal mirror. Exact."""
    return {0: 0, 1: 1, 2: 4, 3: 3, 4: 2, 5: 5, 6: 6, 7: 8, 8: 7}[d]

def apply(seq, d):
    for op in seq:
        d = op(d)
    return d

def calibration_loop(d):
    """His 16-step word: (rotate x3, flip) x4. Must return d. Exact."""
    block = [rotate, rotate, rotate, flip]
    return apply(block * 4, d)

# ---------------------------------------------------------------- base-9 codec

def encode(n):
    """Non-negative int -> list of digits, most significant first."""
    if n == 0:
        return [0]
    ds = []
    while n:
        ds.append(n % 9)
        n //= 9
    return ds[::-1]

def decode(digits):
    v = 0
    for d in digits:
        v = v * 9 + d
    return v

# ---------------------------------------------------------------- walks (the 2/3/6 exhibition)

def walk(step, n_steps=9, start=0):
    """Step-k walk on Z/9 from start. Exhibits 'two and three converge
    every six': the step-2 and step-3 walks both pass through 6."""
    ds, d = [], start
    for _ in range(n_steps):
        ds.append(d)
        d = (d + step) % 9
    return ds

# ---------------------------------------------------------------- arithmetic
# Base-9 arithmetic directly on codon digit sequences (MSD first).
# A numeral system that computes, not just notates.

def _pad(a, b):
    n = max(len(a), len(b))
    return [0] * (n - len(a)) + list(a), [0] * (n - len(b)) + list(b)

def add(a, b):
    """Base-9 addition. Exact."""
    a, b = _pad(a, b)
    out, carry = [], 0
    for x, y in zip(reversed(a), reversed(b)):
        s = x + y + carry
        out.append(s % 9)
        carry = s // 9
    if carry:
        out.append(carry)
    return out[::-1]

def sub(a, b):
    """Base-9 subtraction; requires decode(a) >= decode(b). Exact."""
    assert decode(a) >= decode(b), 'negative result'
    a, b = _pad(a, b)
    out, borrow = [], 0
    for x, y in zip(reversed(a), reversed(b)):
        s = x - borrow - y
        if s < 0:
            s += 9
            borrow = 1
        else:
            borrow = 0
        out.append(s)
    return out[::-1]

def mul(a, b):
    """Base-9 multiplication. Exact."""
    if decode(a) == 0 or decode(b) == 0:
        return [0]
    out = [0]
    for i, y in enumerate(reversed(b)):
        row, carry = [], 0
        for x in reversed(a):
            p = x * y + carry
            row.append(p % 9)
            carry = p // 9
        if carry:
            row.append(carry)
        row = row[::-1] + [0] * i
        out = add(out, row)
    return out

def neg_word(ds):
    """Negation mod 9^w for a w-digit word (9's complement + 1). For w=1
    this coincides with invert(); for w>1 it needs the carry. Exact."""
    w = len(ds)
    comp = [(8 - d) for d in ds]
    return add(comp, [1])[-w:]

# ---------------------------------------------------------------- byte codec
# The origin system carrying content: each byte -> 3 codon glyphs.
# 9^2 = 81 < 256 <= 729 = 9^3, so 3 glyphs per byte is forced.
# ("Codon" here in the codec frame's triplet sense: 3 of his codon-symbols.
# 729 possible triplets, 256 used -- the 473 invalid ones are a built-in
# error detector: 473/729 = 64.9% of random triplet corruptions fail.)
# This is the bridge the CCC was built for: origin content -> machine wire.

def encode_bytes(data):
    """bytes -> list of digits, 3 per byte. Exact."""
    out = []
    for b in data:
        out.append(b // 81)
        out.append((b // 9) % 9)
        out.append(b % 9)
    return out

def decode_bytes(digits):
    """3-digit groups -> bytes. Raises ValueError on invalid triplet
    (value >= 256) or ragged tail. Exact."""
    if len(digits) % 3:
        raise ValueError('ragged codon tail: length not a multiple of 3')
    out = bytearray()
    for i in range(0, len(digits), 3):
        v = digits[i] * 81 + digits[i + 1] * 9 + digits[i + 2]
        if v >= 256:
            raise ValueError('invalid codon triplet at position %d' % i)
        out.append(v)
    return bytes(out)

def encode_text(s):
    return encode_bytes(s.encode('utf-8'))

def decode_text(digits):
    return decode_bytes(digits).decode('utf-8')

# ---------------------------------------------------------------- self-test

if __name__ == '__main__':
    # 1. inversion is negation mod 9 and an involution; 0 fixed
    assert all(invert(invert(d)) == d for d in range(9))
    assert all(invert(d) == (-d) % 9 for d in range(9))
    assert invert(0) == 0
    # 2. antipodal vertex pairs sum to 9 (negation = central inversion)
    verts = {d: s['vertex'] for d, s in SYMBOLS.items() if s['vertex']}
    for d, v in verts.items():
        w = verts[invert(d)]
        assert tuple(-x for x in v) == w and d + invert(d) == 9, d
    # 3. triangles map exactly onto lines under inversion (sideways derivation)
    assert {invert(d) for d in (1, 2, 3, 4)} == {5, 6, 7, 8}
    # 4. calibration loop closes on every triangle orientation (his hunch)
    assert all(calibration_loop(d) == d for d in (1, 2, 3, 4))
    # 5. base-9 codec round-trips, incl. boundary values
    assert all(decode(encode(n)) == n for n in [0, 1, 8, 9, 80, 81, 1000, 10**9])
    assert encode(6) == [6] and encode(11) == [1, 2]  # 11 = 12_9
    # 6. step-2 and step-3 walks both pass through 6 ("converge every six")
    assert 6 in walk(2) and 6 in walk(3)
    # 7. 6 doubly determined: 2*3 = 6 and -3 = 6 (mod 9)
    assert (2 * 3) % 9 == 6 and invert(3) == 6
    # 8. glyph arithmetic: add/sub/mul agree with integer arithmetic
    import random
    random.seed(9)
    for _ in range(300):
        x, y = random.randrange(0, 9**4), random.randrange(0, 9**4)
        assert decode(add(encode(x), encode(y))) == x + y
        assert decode(mul(encode(x), encode(y))) == x * y
        if x >= y:
            assert decode(sub(encode(x), encode(y))) == x - y
    # 9. word negation: w=1 coincides with invert; involution; a + (-a) = 0
    assert neg_word([3]) == [invert(3)] == [6]
    for _ in range(100):
        w = random.randrange(1, 5)
        ds = encode(random.randrange(0, 9**w))
        ds = [0] * (w - len(ds)) + ds
        assert neg_word(neg_word(ds)) == ds
        assert decode(add(ds, neg_word(ds))) % (9**w) == 0
    # 10. the exhibitions, in glyphs
    assert show(add([2], [3])) == show([5])          # triangle+triangle=line
    assert show(mul([2], [3])) == show([6])          # 2*3 = 6
    assert show(add([8], [1])) == show([1, 0])       # carry into the ninth

    print('codon self-test: all exact.')
    print('alphabet :', show(range(9)), ' (0..8)')
    print('invert   :', show(invert(d) for d in range(9)), ' (negation mod 9)')
    print('11 decimal =', show(encode(11)), '= 12_9')
    print('step-2 walk:', show(walk(2)))
    print('step-3 walk:', show(walk(3)))
    print('glyph arithmetic:')
    print(' ', show([2]), '+', show([3]), '=', show(add([2], [3])))
    print(' ', show([2]), 'x', show([3]), '=', show(mul([2], [3])))
    print(' ', show([8]), '+', show([1]), '=', show(add([8], [1])), '(carry into the ninth)')
    # 11. byte codec: round-trips, text round-trip, invalid-triplet rejection
    import random
    random.seed(99)
    for _ in range(200):
        n = random.randrange(0, 64)
        data = bytes(random.randrange(256) for _ in range(n))
        assert decode_bytes(encode_bytes(data)) == data
    assert decode_text(encode_text('prime 2, 3, 5: never put the answer in by hand')) == \
        'prime 2, 3, 5: never put the answer in by hand'
    assert decode_text(encode_text('')) == ''
    try:
        decode_bytes([8, 8, 8])   # 8*81+8*9+8 = 728 >= 256
        raise SystemExit('invalid triplet not rejected')
    except ValueError:
        pass
    try:
        decode_bytes([1, 2])      # ragged tail
        raise SystemExit('ragged tail not rejected')
    except ValueError:
        pass
    # 12. exact corruption-detection rate of the triplet space
    invalid = sum(1 for a in range(9) for b in range(9) for c in range(9)
                  if a * 81 + b * 9 + c >= 256)
    assert invalid == 473  # 473/729 = 64.9% of random triplet corruptions fail

    print('byte codec: 3 glyphs/byte,', invalid, '/ 729 triplets invalid (corruption-detecting)')
    print(' ', repr('Hi'), '->', show(encode_text('Hi')))
