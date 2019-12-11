Map = [
    [1,2,4,5,6,7,10,13,14,15,16,17,18,19,20,21,22,23],
    [1,2,3,4,5,6,7,8,9,11,13,14,15,16,17,18,19,20,21,22,23],
    [2,4,7,8,11,12,13,14,15,17,18,19,21],
    [2,4,7,8,10,11,14,15,17,18,19,21]
]

# Decorations
DOTABOVE = 0
DOTBELOW = 1
TWODOTSABOVE = 2
TWODOTSBELOW = 3
THREEDOTSABOVE = 4
HAMZAABOVE= 5
HAMZABELOW = 6
DASHABOVE = 7

# Positions
ISOLATED = 0
END = 1
MIDDLE = 2
BEGINNING = 3

S = 0
E = 1
M = 2
B = 4

S1 = (0, 0)
S2 = (0, 1)
S3 = (0, 2)
S4 = (0, 3)
S5 = (0, 4)
S6 = (0, 5)
S7 = (0, 6)
S8 = (0, 7)
S9 = (0, 8)
S10 = (0, 9)
S11 = (0, 10)
S12 = (0, 11)
S13 = (0, 12)
S14 = (0, 13)
S15 = (0, 14)
S16 = (0, 15)
S17 = (0, 16)
S18 = (0, 17)
S19 = (0, 18)
S20 = (0, 19)
S21 = (0, 20)
S22 = (0, 21)
S23 = (0, 22)
S24 = (0, 23)
S25 = (0, 24)

E1 = (1, 0)
E2 = (1, 1)
E3 = (1, 2)
E4 = (1, 3)
E5 = (1, 4)
E6 = (1, 5)
E7 = (1, 6)
E8 = (1, 7)
E9 = (1, 8)
E10 = (1, 9)
E11 = (1, 10)
E12 = (1, 11)
E13 = (1, 12)
E14 = (1, 13)
E15 = (1, 14)
E16 = (1, 15)
E17 = (1, 16)
E18 = (1, 17)
E19 = (1, 18)
E20 = (1, 19)
E21 = (1, 20)
E22 = (1, 21)
E23 = (1, 22)
E24 = (1, 23)
E25 = (1, 24)

M1 = (2, 0)
M2 = (2, 1)
M3 = (2, 2)
M4 = (2, 3)
M5 = (2, 4)
M6 = (2, 5)
M7 = (2, 6)
M8 = (2, 7)
M9 = (2, 8)
M10 = (2, 9)
M11 = (2, 10)
M12 = (2, 11)
M13 = (2, 12)
M14 = (2, 13)
M15 = (2, 14)
M16 = (2, 15)
M17 = (2, 16)
M18 = (2, 17)
M19 = (2, 18)
M20 = (2, 19)
M21 = (2, 20)
M22 = (2, 21)
M23 = (2, 22)
M24 = (2, 23)
M25 = (2, 24)

B1 = (3, 0)
B2 = (3, 1)
B3 = (3, 2)
B4 = (3, 3)
B5 = (3, 4)
B6 = (3, 5)
B7 = (3, 6)
B8 = (3, 7)
B9 = (3, 8)
B10 = (3, 9)
B11 = (3, 10)
B12 = (3, 11)
B13 = (3, 12)
B14 = (3, 13)
B15 = (3, 14)
B16 = (3, 15)
B17 = (3, 16)
B18 = (3, 17)
B19 = (3, 18)
B20 = (3, 19)
B21 = (3, 20)
B22 = (3, 21)
B23 = (3, 22)
B24 = (3, 23)
B25 = (3, 24)

Letters = {
    'ا': {
        'decoration': [HAMZAABOVE, HAMZABELOW],
        'seqs': {
            ISOLATED:   [[S1]],
            END:        [[E1]],
            MIDDLE:     [],
            BEGINNING:  []
        }
    },
    'ب': {
        'decoration': [DOTBELOW],
        'seqs': {
            ISOLATED:   [[S2], [B2, E2]],
            END:        [[E3], [M2, E2]],
            MIDDLE:     [[M2]],
            BEGINNING:  [[B2]]
        }
    },
    'ت': {
        'decoration': [TWODOTSABOVE],
        'seqs': {
            ISOLATED:   [[S2], [B2, E2]],
            END:        [[E3], [M2, E2]],
            MIDDLE:     [[M2]],
            BEGINNING:  [[B2]]
        }
    },
    'ث': {
        'decoration': [THREEDOTSABOVE],
        'seqs': {
            ISOLATED:   [[S2], [B2, E2]],
            END:        [[E3], [M2, E2]],
            MIDDLE:     [[M2]],
            BEGINNING:  [[B2]]
        }
    },
    'ج': {
        'decoration': [DOTBELOW],
        'seqs': {
            ISOLATED:   [[S4]],
            END:        [[E4]],
            MIDDLE:     [[M4]],
            BEGINNING:  [[B4]]
        }
    },
    'ح': {
        'decoration': [],
        'seqs': {
            ISOLATED:   [[S4]],
            END:        [[E4]],
            MIDDLE:     [[M4]],
            BEGINNING:  [[B4]]
        }
    },
    'خ': {
        'decoration': [DOTABOVE],
        'seqs': {
            ISOLATED:   [[S4]],
            END:        [[E4]],
            MIDDLE:     [[M4]],
            BEGINNING:  [[B4]]
        }
    },
    'د': {
        'decoration': [],
        'seqs': {
            ISOLATED:   [[S5]],
            END:        [[E5]],
            MIDDLE:     [],
            BEGINNING:  []
        }
    },
    'ذ': {
        'decoration': [DOTABOVE],
        'seqs': {
            ISOLATED:   [[S5]],
            END:        [[E5]],
            MIDDLE:     [],
            BEGINNING:  []
        }
    },
    'ر': {
        'decoration': [],
        'seqs': {
            ISOLATED:   [[S6]],
            END:        [[E6]],
            MIDDLE:     [],
            BEGINNING:  []
        }
    },
    'ز': {
        'decoration': [DOTABOVE],
        'seqs': {
            ISOLATED:   [[S6]],
            END:        [[E6]],
            MIDDLE:     [],
            BEGINNING:  []
        }
    },
    'س': {
        'decoration': [],
        'seqs': {
            ISOLATED:   [[S7], [B2, M2, E7], [B7,E7]],
            END:        [[E8], [M2, E9], [M2, M2, E7], [M7, E7]],
            MIDDLE:     [[M8], [M2, M2, M2], [M7, M2], [M2, M7]],
            BEGINNING:  [[B8], [B2, M2, M2], [B2, M7], [B7, M2]]
        }
    },
    'ش': {
        'decoration': [THREEDOTSABOVE],
        'seqs': {
            ISOLATED:   [[S7], [B2, M2, E7], [B7,E7]],
            END:        [[E8], [M2, E9], [M2, M2, E7], [M7, E7]],
            MIDDLE:     [[M8], [M2, M2, M2], [M7, M2], [M2, M7]],
            BEGINNING:  [[B8], [B2, M2, M2], [B2, M7], [B7, M2]]
        }
    },
    'ص': {
        'decoration': [],
        'seqs': {
            ISOLATED:   [[S10], [B10, E7]],
            END:        [[E11], [M12, E7]],
            MIDDLE:     [[M11], [M12, M2]],
            BEGINNING:  [[B11], [B10, M2]]
        }
    },
    'ض': {
        'decoration': [DOTABOVE],
        'seqs': {
            ISOLATED:   [[S10], [B10, E7]],
            END:        [[E11], [M12, E7]],
            MIDDLE:     [[M11], [M12, M2]],
            BEGINNING:  [[B11], [B10, M2]]
        }
    },
    'ط': {
        'decoration': [],
        'seqs': {
            ISOLATED:   [[S13]],
            END:        [[E13]],
            MIDDLE:     [[M13]],
            BEGINNING:  [[B13]]
        }
    },
    'ظ': {
        'decoration': [DOTABOVE],
        'seqs': {
            ISOLATED:   [[S13]],
            END:        [[E13]],
            MIDDLE:     [[M13]],
            BEGINNING:  [[B13]]
        }
    },
    'ع': {
        'decoration': [],
        'seqs': {
            ISOLATED:   [[S14]],
            END:        [[E14]],
            MIDDLE:     [[M14]],
            BEGINNING:  [[B14]]
        }
    },
    'غ': {
        'decoration': [DOTABOVE],
        'seqs': {
            ISOLATED:   [[S14]],
            END:        [[E14]],
            MIDDLE:     [[M14]],
            BEGINNING:  [[B14]]
        }
    },
    'ف': {
        'decoration': [DOTABOVE],
        'seqs': {
            ISOLATED:   [[S15], [B15, E2]],
            END:        [[E15], [M15, E2]],
            MIDDLE:     [[M15]],
            BEGINNING:  [[B15]]
        }
    },
    'ق': {
        'decoration': [TWODOTSABOVE],
        'seqs': {
            ISOLATED:   [[S16]],
            END:        [[E16]],
            MIDDLE:     [[M15]],
            BEGINNING:  [[B15]]
        }
    },
    'ك': {
        'decoration': [HAMZAABOVE],
        'seqs': {
            ISOLATED:   [[S17], [B18, E2]],
            END:        [[E17], [M18, E2]],
            MIDDLE:     [[M17]],
            BEGINNING:  [[B17]]
        }
    },
    'ل': {
        'decoration': [],
        'seqs': {
            ISOLATED:   [[S18]],
            END:        [[E18]],
            MIDDLE:     [[M18]],
            BEGINNING:  [[B18]]
        }
    },
    'م': {
        'decoration': [],
        'seqs': {
            ISOLATED:   [[S19]],
            END:        [[E19]],
            MIDDLE:     [[M19]],
            BEGINNING:  [[B19]]
        }
    },
    'ن': {
        'decoration': [DOTABOVE],
        'seqs': {
            ISOLATED:   [[S20]],
            END:        [[E7]],
            MIDDLE:     [[M2]],
            BEGINNING:  [[B2]]
        }
    },
    'ه': {
        'decoration': [],
        'seqs': {
            ISOLATED:   [[S21]],
            END:        [[E21]],
            MIDDLE:     [[M21]],
            BEGINNING:  [[B21]]
        }
    },
    'و': {
        'decoration': [],
        'seqs': {
            ISOLATED:   [[S22]],
            END:        [[E22]],
            MIDDLE:     [],
            BEGINNING:  []
        }
    },
    'ي': {
        'decoration': [TWODOTSBELOW],
        'seqs': {
            ISOLATED:   [[S23]],
            END:        [[E23]],
            MIDDLE:     [[M2]],
            BEGINNING:  [[B2]]
        }
    },
    'آ': {
        'decoration': [DASHABOVE],
        'seqs': {
            ISOLATED:   [[S1]],
            END:        [[E1]],
            MIDDLE:     [],
            BEGINNING:  []
        }
    },
    'ه': {
        'decoration': [TWODOTSABOVE],
        'seqs': {
            ISOLATED:   [[S21]],
            END:        [[E21]],
            MIDDLE:     [[M21]],
            BEGINNING:  [[B21]]
        }
    },
    'ى': {
        'decoration': [TWODOTSBELOW],
        'seqs': {
            ISOLATED:   [[S23]],
            END:        [[E23]],
            MIDDLE:     [[M2]],
            BEGINNING:  [[B2]]
        }
    },
    'لا': {
        'decoration': [],
        'seqs': {
            ISOLATED:   [[S24]],
            END:        [[E24]],
            MIDDLE:     [],
            BEGINNING:  []
        }
    },
    'ء': {
        'decoration': [],
        'seqs': {
            ISOLATED:   [[S25]],
            END:        [],
            MIDDLE:     [],
            BEGINNING:  []
        }
    },
}


def getLetters(position, seq, decoration=None):
    ReqLetters = []
    SearchLetters = Letters if decoration == None else [Letter for Letter in Letters \
        if all([decoration[Idx] in Letters[Letter]['decoration'] for Idx in range(len(decoration))])]
    for _, Letter in enumerate(SearchLetters):
        for Seq in Letters[Letter]['seqs'][position]:
            if len(Seq) < len(seq):
                continue
            elif all([Seq[Idx] == seq[Idx] for Idx in range(len(seq))]):
                ReqLetters.append(Letter)
                break
    return ReqLetters