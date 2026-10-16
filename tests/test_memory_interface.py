"""OpenSpike-compatible external weight memory (docs/openspike-memory-interface.md).

Golden-model side: the fabric holds no weight memory. Weights live in an
external SRAM array addressed by source word; the TB models that SRAM with
weight_words(). Address = source index s, word[s] = concat(w_int[i][s] at
bits [i*WW +: WW]), zero words for pad sources (they never fire).
"""

import numpy as np

from targets.digital.model import sample_weight_ints, weight_words


def _bits(word: int, lo: int, width: int) -> int:
    return (word >> lo) & ((2**width) - 1)


def test_weight_words_shape_and_colmajor():
    cfg = {"neurons": 7, "fanout": 3, "weight_width": 4, "seed": 5}
    w_int = sample_weight_ints(cfg)
    words = weight_words(cfg)

    pad = 8  # next pow2 >= 7
    assert len(words) == pad
    assert all(0 <= w < 2 ** (pad * 4) for w in words)
    for s in range(pad):
        for i in range(7):
            got = _bits(words[s], i * 4, 4)
            signed = got if got < 8 else got - 16
            expect = int(w_int[i, s]) if s < 7 else 0
            assert signed == expect, (i, s)


def test_weight_words_signed_encoding_matches_rtl_slice():
    """Word bit slice decodes back to the signed ints the LIF consumes."""
    cfg = {"neurons": 3, "fanout": 3, "weight_width": 2, "seed": 9,
           "weights": [[1, -2, 0], [0, 1, 2], [-1, 0, 2]]}
    words = weight_words(cfg)
    # row 0 gets its first weight from source 0: word[0] bits [0+:2] == +1
    assert _bits(words[0], 0 * 2, 2) == 1
    # -2 in 2-bit two's complement is 2
    assert _bits(words[1], 0 * 2, 2) == 2
    # source 2 word: row0 weight 0, row1 weight 2, row2 weight 2
    assert _bits(words[2], 1 * 2, 2) == 2
    assert _bits(words[2], 2 * 2, 2) == 2


def test_weight_words_pad_sources_are_zero():
    cfg = {"neurons": 4, "fanout": 2, "weight_width": 4, "seed": 3}
    words = weight_words(cfg)
    pad = 4  # pow2 == n here, extend with a manual wider check instead
    assert len(words) == pad
    cfg2 = {"neurons": 5, "fanout": 2, "weight_width": 4, "seed": 3}
    words2 = weight_words(cfg2)
    assert len(words2) == 8
    assert words2[5] == words2[6] == words2[7] == 0