# EDO System Definitions

This file contains all the data for different Equal Division of the Octave (EDO) systems used in the functional harmony classifier.

---

## EDO 12
**Current Note Names**: letters

### Interval Quality List
```
s, o, u, m, m, u, o, s, l, h, h, l
```

### Leading Targets
```
8: 7   # m6->P5
11: 0  # M7->root
```

### Dominant Leading Intervals
```
11  # Only M7 creates true dominant function
```

### Chord Intervals
```
0, 4, 7   # Major
0, 3, 7   # Minor
0, 3, 6   # Diminished
0, 4, 8   # Augmented
```

### Chord Notation: full
```
maj
min
dim
aug
```

### Chord Notation: symbols
```
M
m
°
+
```

### Note Names: letters
```
C, C♯/D♭, D, D♯/E♭, E, F, F♯/G♭, G, G♯/A♭, A, A♯/B♭, B
```

### Note Names: sharps
```
C, C♯, D, D♯, E, F, F♯, G, G♯, A, A♯, B
```

### Note Names: flats
```
C, D♭, D, E♭, E, F, G♭, G, A♭, A, B♭, B
```

### Note Names: roman_numerals
```
I, ♭II, II, ♭III, III, IV, ♯IV, V, ♭VI, VI, ♭VII, VII
```

---

## EDO 15
**Current Note Names**: numbers

### Interval Quality List
```
s, o, u, u, m, m, u, o, o, s, l, h, h, l, l
```

### Leading Targets
```
10: 9   # m6->P5
14: 0   # M7->root
```

### Dominant Leading Intervals
```
14  # M7 creates dominant function
```

### Chord Intervals
```
0, 5, 9   # Major: root, Maj3, Maj3
0, 4, 9   # Minor: root, min3, Maj3
0, 4, 8  # Diminished: root, min3, min3
0, 5, 10   # Augmented: root, Maj3, min3
```

### Chord Notation: full
```
maj
min
dim
aug
```

### Chord Notation: symbols
```
M
m
°
+
```

### Note Names: numbers
```
0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14
```

---

## EDO 16
**Current Note Names**: numbers

### Interval Quality List
```
s, o, o, u, m, m, u, u, o, s, l, l, h, h, l, l
```

### Leading Targets
```
11: 9    # M6->P5
12: 9    # m6->P5
14: 0    # m7->root
15: 0    # M7->root
```

### Dominant Leading Intervals
```
14  # m7 creates dominant function
15  # M7 creates dominant function
```

### Chord Intervals
```
0, 4, 8   # minor dim
0, 4, 9   # minor
0, 5, 9   # major
0, 5, 10   # major aug
```

### Chord Notation: full
```
minor dim
minor
major
major aug
```

### Chord Notation: symbols
```
mdim
m
M
Maug
```

### Note Names: numbers
```
0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15
```

---

## EDO 17
**Current Note Names**: numbers

### Interval Quality List
```
s, o, o, u, m, m, m, u, o, o, s, l, l, h, h, l, l
```

### Leading Targets
```
11: 10   # m6->P5
12: 10   # M6->P5
15: 0    # m7->root
16: 0    # M7->root
```

### Dominant Leading Intervals
```
15  # m7 creates dominant function
16  # M7 creates dominant function
```

### Chord Intervals
```
0, 4, 8   # minor dim
0, 4, 9   # minor dim+
0, 5, 9   # neutral dim+
0, 4, 10   # minor
0, 5, 10   # neutral
0, 6, 10   # major
0, 5, 11   # neutral aug
0, 6, 11   # major aug
0, 6, 12   # major aug+
```

### Chord Notation: full
```
minor dim
minor dim+
neutral dim+
minor
neutral
major
neutral aug
major aug
major aug+
```

### Chord Notation: standard
```
min dim
min dim+
neut dim+
min
neut
maj
neut aug
maj aug
maj aug+
```

### Chord Notation: symbols
```
mdim
mdim+
ndim+
m
n
M
naug
Maug
Maug+
```

### Note Names: numbers
```
0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16
```

---

## EDO 19
**Current Note Names**: numbers

### Interval Quality List
```
s, o, o, u, m, m, m, m, u, o, o, s, l, l, h, h, h, l, l
```

### Leading Targets
```
12: 11   # m6->P5
13: 11   # M6->P5
17: 0    # m7->root
18: 0    # M7->root
```

### Dominant Leading Intervals
```
17  # m7 creates dominant function
18  # M7 creates dominant function
```

### Chord Intervals
```
0, 4, 8   # subminor dim-
0, 4, 9   # subminor dim
0, 5, 9   # minor dim
0, 4, 10   # subminor dim+
0, 5, 10   # minor dim+
0, 6, 10   # major dim+
0, 4, 11   # subminor
0, 5, 11   # minor
0, 6, 11   # major
0, 7, 11   # supermajor
0, 5, 12   # minor aug
0, 6, 12   # major aug
0, 7, 12   # supermajor aug
0, 6, 13   # major aug+
0, 7, 13   # supermajor aug+
0, 7, 14   # supermajor aug#
```

### Chord Notation: full
```
subminor dim-
subminor dim
minor dim
subminor dim+
minor dim+
major dim+
subminor
minor
major
supermajor
minor aug
major aug
supermajor aug
major aug+
supermajor aug+
supermajor aug#
```

### Chord Notation: standard
```
submin dim-
submin dim
min dim
submin dim+
min dim+
maj dim+
submin
min
maj
supermaj
min aug
maj aug
supermaj aug
maj aug+
supermaj aug+
supermaj aug#
```

### Chord Notation: symbols
```
smdim-
smdim
mdim
smdim+
mdim+
Mdim+
sm
m
M
sM
maug
Maug
sMaug
Maug+
sMaug+
sMaug#
```

### Note Names: numbers
```
0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18
```

---

## EDO 20
**Current Note Names**: numbers

### Interval Quality List
```
s, o, o, u, u, m, m, m, u, u, o, o, s, l, l, h, h, h, l, l
```

### Leading Targets
```
13: 12   # m6->P5
14: 12   # M6->P5
18: 0    # m7->root
19: 0    # M7->root
```

### Dominant Leading Intervals
```
18  # m7 creates dominant function
19  # M7 creates dominant function
```

### Chord Intervals
```
0, 5, 10   # minor dim
0, 5, 11   # minor dim+
0, 6, 11   # neutral dim+
0, 5, 12   # minor
0, 6, 12   # neutral
0, 7, 12   # major
0, 6, 13   # neutral aug
0, 7, 13   # major aug
0, 7, 14   # major aug+
```

### Chord Notation: full
```
minor dim
minor dim+
neutral dim+
minor
neutral
major
neutral aug
major aug
major aug+
```

### Chord Notation: standard
```
min dim
min dim+
neut dim+
min
neut
maj
neut aug
maj aug
maj aug+
```

### Chord Notation: symbols
```
mdim
mdim+
ndim+
m
n
M
naug
Maug
Maug+
```

### Note Names: numbers
```
0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19
```

---

## EDO 22
**Current Note Names**: letters

### Interval Quality List
```
s, o, u, u, u, m, m, m, m, u, u, o, o, s, h, l, h, h, h, h, l, l
```

### Leading Targets
```
15: 13  # m6->P5
20: 0   # M7->root
21: 0   # sM7->root
```

### Dominant Leading Intervals
```
20  # M7 creates dominant function
21  # sM7 creates dominant function
```

### Chord Intervals
```
0, 5, 10   # Subdiminished: root, sub3, sub3 - orwell
0, 5, 11   # Subminor up-flat five: root, sub3, min3 - utonal diminished
0, 6, 11   # Diminished: root, min3, sub3 - otonal diminished
0, 5, 12   # Subminor down five: root, sub3, Maj3 - orwell minor
0, 6, 12   # Minor down five: root, min3, min3 - keemic
0, 7, 12   # Down-five: root, Maj3, sub3 - orwell major
0, 5, 13   # Subminor: root, sub3, Sup3
0, 6, 13   # Minor: root, min3, Maj3
0, 7, 13   # Major: root, Maj3, min3
0, 8, 13   # Supermajor: root, Sup3, sub3
0, 6, 14   # Minor up five: root, min3, Sup3 - sensaminor
0, 7, 14   # Augmented: root, Maj3, Maj3 - magic
0, 8, 14   # Supermajor up five: root, Sup3, min3 - sensamajor
0, 7, 15   # Down-sharp five: root, Maj3, Sup3 - magic minor
0, 8, 15   # Supermajor down-sharp five: root, Sup3, Maj3 - magic major
0, 8, 16   # Supermajor sharp five: root, Sup3, Sup3 - sensamagic
```

### Chord Notation: full
```
sb5 (w)
s^b5 (d−)
dim (d+)
sv5 (w−)
mv5 (k)
v5 (w+)
submin (s)
min (m)
maj
supermaj (S)
m^5 (Z−)
aug (J)
S^5 (Z+)
v#5 (J−)
Sv#5 (J+)
S#5 (Z)
```

### Chord Notation: standard
```
sb5
s^b5
dim
sv5
mv5
v5
submin
min
maj
supermaj
m^5
aug
S^5
v#5
Sv#5
S#5
```

### Chord Notation: temperament
```
w
d−
d+
w−
k
w+
s
m
M
S
Z−
J
Z+
J−
J+
Z
```

### Chord Notation: descriptive
```
subdiminished
subminor up-flat-5
diminished
subminor down-5
minor down-5
down-5
subminor
minor
major
supermajor
minor up-5
augmented
supermajor up-5
down-sharp-5
supermajor down-sharp-5
supermajor sharp-5
```

### Note Names: letters
```
C, D♭, ^D♭, vD, D, E♭, ^E♭, vE, E, F, ^F/G♭, vF♯/^G♭, F♯/vG, G, A♭, ^A♭, vA, A, B♭, ^B♭, vB, B
```

---

## EDO 23
**Current Note Names**: numbers

### Interval Quality List
```
s, o, u, u, u, m, m, m, m, u, u, o, o, s, s, l, l, h, h, h, h, l, l
```

### Leading Targets
```
15: 13  # m6->P5
16: 14  # ^m6->^P5
21: 0   # m7->root
22: 0   # M7->root
```

### Dominant Leading Intervals
```
21  # m7 creates dominant function
22  # M7 creates dominant function
```

### Chord Intervals
```
0, 5, 10   # Subdiminished v5
0, 5, 11   # Subdiminished ^5
0, 6, 11   # Diminished v5
0, 6, 12   # Diminished ^5
0, 5, 13   # Subminor v5
0, 5, 14   # Subminor ^5
0, 6, 13   # Minor v5
0, 6, 14   # Minor ^5
0, 7, 13   # Major v5
0, 7, 14   # Major ^5
0, 8, 13   # Supermajor v5
0, 8, 14   # Supermajor ^5
0, 7, 15   # Augmented v5
0, 7, 16   # Augmented ^5
0, 8, 15   # Supermajor up5 v5
0, 8, 16   # Supermajor up5 ^5
```

### Chord Notation: full
```
subdim v5
subdim ^5
dim v5
dim ^5
subminor v5
subminor ^5
minor v5
minor ^5
major v5
major ^5
supermajor v5
supermajor ^5
aug v5
aug ^5
supermajor #v5
supermajor #^5
```

### Chord Notation: abbreviated
```
sd v5
sd ^5
dim v5
dim ^5
s v5
s ^5
m v5
m ^5
M v5
M ^5
S v5
S ^5
aug v5
aug ^5
S #v5
S #^5
```

### Chord Notation: symbols
```
sd↓
sd↑
d↓
d↑
s↓
s↑
m↓
m↑
M↓
M↑
S↓
S↑
+↓
+↑
S+↓
S+↑
```

### Note Names: letters
```
C, C♯, ^C♯, vD, D, D♯, ^D♯, vE♭, E♭, ^E♭, E, E♯, F, F♯, ^F♯, vG♭, G♭, ^G♭, vG, G, A♭, ^A♭, vA
```

---

## EDO 26
**Current Note Names**: numbers

### Interval Quality List
```
s, o, o, o, u, u, m, m, m, m, u, u, u, o, o, s, l, l, l, h, h, h, h, l, l, l
```

### Leading Targets
```
16: 15   # m6->P5
17: 15   # M6->P5
18: 15   # aug6->P5
23: 0    # m7->root
24: 0    # M7->root
25: 0    # aug7->root
```

### Dominant Leading Intervals
```
23  # m7 creates dominant function
24  # M7 creates dominant function
25  # aug7 creates dominant function
```

### Chord Intervals
```
0, 6, 12   # subminor dim-
0, 6, 13   # subminor dim
0, 7, 13   # minor dim
0, 6, 14   # subminor dim+
0, 7, 14   # minor dim+
0, 8, 14   # major dim+
0, 6, 15   # subminor
0, 7, 15   # minor
0, 8, 15   # major
0, 9, 15   # supermajor
0, 7, 16   # minor aug
0, 8, 16   # major aug
0, 9, 16   # supermajor aug
0, 8, 17   # major aug+
0, 9, 17   # supermajor aug+
0, 9, 18   # supermajor aug#
```

### Chord Notation: full
```
subminor dim-
subminor dim
minor dim
subminor dim+
minor dim+
major dim+
subminor
minor
major
supermajor
minor aug
major aug
supermajor aug
major aug+
supermajor aug+
supermajor aug#
```

### Chord Notation: standard
```
submin dim-
submin dim
min dim
submin dim+
min dim+
maj dim+
submin
min
maj
supermaj
min aug
maj aug
supermaj aug
maj aug+
supermaj aug+
supermaj aug#
```

### Chord Notation: symbols
```
smdim-
smdim
mdim
smdim+
mdim+
Mdim+
sm
m
M
sM
maug
Maug
sMaug
Maug+
sMaug+
sMaug#
```

### Note Names: numbers
```
0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25
```

---

## EDO 31
**Current Note Names**: letters

### Interval Quality List
```
s, o, o, o, o, u, u, m, m, m, m, m, u, u, u, o, o, o, s, l, l, l, h, h, h, h, h, l, l, l, l
```

### Leading Targets
```
20: 18  # m6->P5
21: 18  # m6->P5
27: 0   # M7->root
28: 0   # M7->root
29: 0   # M7->root
30: 0   # M7->root
```

### Dominant Leading Intervals
```
27  # M7 variant creates dominant function
28  # M7 variant creates dominant function
29  # M7 variant creates dominant function
30  # M7 variant creates dominant function
```

### Chord Intervals
```
0, 7, 14   # Subminor triad
0, 7, 15   # Subminor third + minor third
0, 8, 15   # Minor third + subminor third
0, 7, 16   # Subminor third + neutral third
0, 8, 16   # Minor triad
0, 9, 16   # Neutral third + subminor third
0, 7, 17   # Subminor third + major third
0, 8, 17   # Minor third + neutral third
0, 9, 17   # Neutral third + minor third
0, 10, 17   # Major third + subminor third
0, 7, 18   # Subminor third + supermajor third
0, 8, 18   # Minor third + major third
0, 9, 18   # Neutral triad
0, 10, 18   # Major third + minor third
0, 11, 18   # Supermajor third + subminor third
0, 8, 19   # Minor third + supermajor third
0, 9, 19   # Neutral third + major third
0, 10, 19   # Major third + neutral third
0, 11, 19   # Supermajor third + minor third
0, 9, 20   # Neutral third + supermajor third
0, 10, 20   # Major triad
0, 11, 20   # Supermajor third + neutral third
0, 10, 21   # Major third + supermajor third
0, 11, 21   # Supermajor third + major third
0, 11, 22   # Supermajor triad
```

### Chord Notation: full
```
subminor
subminor down-flat-5
minor down-flat-5
subminor down-5
minor
neutral down-5
subminor down-5
minor down-5
neutral down-5
major down-5
subminor
minor
neutral
major
supermajor
minor up-5
neutral up-5
major up-5
supermajor up-5
neutral up-5
major
supermajor up-5
major up-sharp-5
supermajor up-sharp-5
supermajor
```

### Chord Notation: standard
```
subminor
sm vb5
m vb5
sm v5
minor
n v5
sm v5
m v5
n v5
M v5
sm
m
neutral
M
sM
m ^5
n ^5
M ^5
sM ^5
n ^5
major
sM ^5
M ^#5
sM ^#5
supermajor
```

### Chord Notation: abbreviated
```
sm
smvb5
mvb5
smv5
m
nv5
smv5
mv5
nv5
Mv5
sm
m
n
M
sM
m^5
n^5
M^5
sM^5
n^5
M
sM^5
M^#5
sM^#5
sM
```

### Note Names: letters
```
C, C♯, D♭♭, D♭, C♯♯, D, D♯, E♭♭, E♭, D♯♯, E, E♯, F, F♯, G♭♭, G♭, F♯♯, G♭♭♭, G, G♯, A♭♭, A♭, G♯♯, A, A♯, B♭♭, B♭, A♯♯, B, B♯, C♭
```

---

## EDO 53
**Current Note Names**: numbers

### Interval Quality List
```
s, o, o, o, o, o, o, o, u, u, u, u, m, m, m, m, m, m, m, m, u, u, u, u, u, o, o, o, o, o, s, s, s, l, l, l, l, l, h, h, h, h, h, h, h, h, l, l, l, l, l, l, l
```

### Leading Targets
```
33: 31  # Leading to perfect fifth
34: 31  # Leading to perfect fifth
35: 31  # Leading to perfect fifth
46: 0   # Leading to root
47: 0   # Leading to root
48: 0   # Leading to root
49: 0   # Leading to root
50: 0   # Leading to root
51: 0   # Leading to root
52: 0   # Leading to root
```

### Dominant Leading Intervals
```
46  # M7 variant creates dominant function
47  # M7 variant creates dominant function
48  # M7 variant creates dominant function
49  # M7 variant creates dominant function
50  # M7 variant creates dominant function
51  # M7 variant creates dominant function
52  # M7 variant creates dominant function
```

### Chord Intervals
```
0, 12, 24   # Subsubminor triad
0, 12, 25   # Subsubminor third + subminor third
0, 13, 25   # Subminor third + subsubminor third
0, 12, 26   # Subsubminor third + minor third
0, 13, 26   # Subminor triad
0, 14, 26   # Minor third + subsubminor third
0, 12, 27   # Subsubminor third + neutral-minor third
0, 13, 27   # Subminor third + minor third
0, 14, 27   # Minor third + subminor third
0, 15, 27   # Neutral-minor third + subsubminor third
0, 12, 28   # Subsubminor third + neutral-major third
0, 13, 28   # Subminor third + neutral-minor third
0, 14, 28   # Minor triad
0, 15, 28   # Neutral-minor third + subminor third
0, 16, 28   # Neutral-major third + subsubminor third
0, 12, 29   # Subsubminor third + major third
0, 13, 29   # Subminor third + neutral-major third
0, 14, 29   # Minor third + neutral-minor third
0, 15, 29   # Neutral-minor third + minor third
0, 16, 29   # Neutral-major third + subminor third
0, 17, 29   # Major third + subsubminor third
0, 12, 30   # Subsubminor third + supermajor third
0, 13, 30   # Subminor third + major third
0, 14, 30   # Minor third + neutral-major third
0, 15, 30   # Neutral-minor triad
0, 16, 30   # Neutral-major third + minor third
0, 17, 30   # Major third + subminor third
0, 18, 30   # Supermajor third + subsubminor third
0, 12, 31   # Subsubminor third + supersupermajor third
0, 13, 31   # Subminor third + supermajor third
0, 14, 31   # Minor third + major third
0, 15, 31   # Neutral-minor third + neutral-major third
0, 16, 31   # Neutral-major third + neutral-minor third
0, 17, 31   # Major third + minor third
0, 18, 31   # Supermajor third + subminor third
0, 19, 31   # Supersupermajor third + subsubminor third
0, 13, 32   # Subminor third + supersupermajor third
0, 14, 32   # Minor third + supermajor third
0, 15, 32   # Neutral-minor third + major third
0, 16, 32   # Neutral-major triad
0, 17, 32   # Major third + neutral-minor third
0, 18, 32   # Supermajor third + minor third
0, 19, 32   # Supersupermajor third + subminor third
0, 14, 33   # Minor third + supersupermajor third
0, 15, 33   # Neutral-minor third + supermajor third
0, 16, 33   # Neutral-major third + major third
0, 17, 33   # Major third + neutral-major third
0, 18, 33   # Supermajor third + neutral-minor third
0, 19, 33   # Supersupermajor third + minor third
0, 15, 34   # Neutral-minor third + supersupermajor third
0, 16, 34   # Neutral-major third + supermajor third
0, 17, 34   # Major triad
0, 18, 34   # Supermajor third + neutral-major third
0, 19, 34   # Supersupermajor third + neutral-minor third
0, 16, 35   # Neutral-major third + supersupermajor third
0, 17, 35   # Major third + supermajor third
0, 18, 35   # Supermajor third + major third
0, 19, 35   # Supersupermajor third + neutral-major third
0, 17, 36   # Major third + supersupermajor third
0, 18, 36   # Supermajor triad
0, 19, 36   # Supersupermajor third + major third
0, 18, 37   # Supermajor third + supersupermajor third
0, 19, 37   # Supersupermajor third + supermajor third
0, 19, 38   # Supersupermajor triad
```

### Chord Notation: full
```
subsubminor
subsubminor down-double-flat-5
subminor down-double-flat-5
subsubminor down-double-flat-5
subminor
minor down-double-flat-5
subsubminor down-flat-5
subminor down-flat-5
minor down-flat-5
neutral-minor down-flat-5
subsubminor down-flat-5
subminor down-flat-5
minor
neutral-minor down-flat-5
neutral-major down-flat-5
subsubminor down-5
subminor down-5
minor down-5
neutral-minor down-5
neutral-major down-5
major down-5
subsubminor down-5
subminor down-5
minor down-5
neutral-minor
neutral-major down-5
major down-5
supermajor down-5
subsubminor
subminor
minor
neutral-minor
neutral-major
major
supermajor
supersupermajor
subminor up-5
minor up-5
neutral-minor up-5
neutral-major
major up-5
supermajor up-5
supersupermajor up-5
minor up-5
neutral-minor up-5
neutral-major up-5
major up-5
supermajor up-5
supersupermajor up-5
neutral-minor up-sharp-5
neutral-major up-sharp-5
major
supermajor up-sharp-5
supersupermajor up-sharp-5
neutral-major up-sharp-5
major up-sharp-5
supermajor up-sharp-5
supersupermajor up-sharp-5
major up-double-sharp-5
supermajor
supersupermajor up-double-sharp-5
supermajor up-double-sharp-5
supersupermajor up-double-sharp-5
supersupermajor
```

### Chord Notation: standard
```
subsubminor
ssm vbb5
sm vbb5
ssm vbb5
subminor
m vbb5
ssm vb5
sm vb5
m vb5
nm vb5
ssm vb5
sm vb5
minor
nm vb5
nM vb5
ssm v5
sm v5
m v5
nm v5
nM v5
M v5
ssm v5
sm v5
m v5
neutral-minor
nM v5
M v5
sM v5
ssm
sm
m
nm
nM
M
sM
ssM
sm ^5
m ^5
nm ^5
neutral-major
M ^5
sM ^5
ssM ^5
m ^5
nm ^5
nM ^5
M ^5
sM ^5
ssM ^5
nm ^#5
nM ^#5
major
sM ^#5
ssM ^#5
nM ^#5
M ^#5
sM ^#5
ssM ^#5
M ^##5
supermajor
ssM ^##5
sM ^##5
ssM ^##5
supersupermajor
```

### Chord Notation: abbreviated
```
ssm
ssmvbb5
smvbb5
ssmvbb5
sm
mvbb5
ssmvb5
smvb5
mvb5
nmvb5
ssmvb5
smvb5
m
nmvb5
nMvb5
ssmv5
smv5
mv5
nmv5
nMv5
Mv5
ssmv5
smv5
mv5
nm
nMv5
Mv5
sMv5
ssm
sm
m
nm
nM
M
sM
ssM
sm^5
m^5
nm^5
nM
M^5
sM^5
ssM^5
m^5
nm^5
nM^5
M^5
sM^5
ssM^5
nm^#5
nM^#5
M
sM^#5
ssM^#5
nM^#5
M^#5
sM^#5
ssM^#5
M^##5
sM
ssM^##5
sM^##5
ssM^##5
ssM
```

### Note Names: numbers
```
0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52
```

---

## EDO 27
**Current Note Names**: numbers

### Interval Quality List
```
s, o, o, o, u, u, m, m, m, m, u, u, u, o, o, s, s, l, l, l, h, h, h, h, l, l, l
```

### Leading Targets
```
19: 18  # M6->P5
25: 0   # m7->root
26: 0   # M7->root
```

### Dominant Leading Intervals
```
25  # m7 creates dominant function
26  # M7 creates dominant function
```

### Chord Intervals
```
0, 6, 12   # subminor subdiminished
0, 6, 13   # subminor subminor up-flat-5
0, 6, 14   # subminor neutral-diminished
0, 6, 15   # subminor down-5
0, 6, 16   # subminor perfect
0, 7, 13   # minor subminor up-flat-5
0, 7, 14   # minor neutral-diminished
0, 7, 15   # minor down-5
0, 7, 16   # minor perfect
0, 7, 17   # minor up-5
0, 8, 14   # neutral neutral-diminished
0, 8, 15   # neutral down-5
0, 8, 16   # neutral perfect
0, 8, 17   # neutral up-5
0, 8, 18   # neutral neutral-augmented
0, 9, 15   # major down-5
0, 9, 16   # major perfect
0, 9, 17   # major up-5
0, 9, 18   # major neutral-augmented
0, 9, 19   # major down-sharp-5
0, 10, 16   # supermajor perfect
0, 10, 17   # supermajor up-5
0, 10, 18   # supermajor neutral-augmented
0, 10, 19   # supermajor down-sharp-5
0, 10, 20   # supermajor sharp-5
```

### Chord Notation: full
```
dim= (dim=)
dim- (dim-)
msh- (o-)
mav- (l-)
sub (s)
dim+ (dim+)
dim (dim)
arc- (r-)
min (m)
mac- (i-)
msh+ (o+)
arc+ (r+)
neu (n)
dic- (k-)
hyr- (h-)
mav+ (l+)
maj (M)
hyr+ (h+)
aug (aug)
dic+ (k+)
sup (S)
mac+ (i+)
dic (k)
hyr (h)
mac (i)
```

### Chord Notation: standard
```
dim=
dim-
msh-
mav-
sub
dim+
dim
arc-
min
mac-
msh+
arc+
neu
dic-
hyr-
mav+
maj
hyr+
aug
dic+
sup
mac+
dic
hyr
mac
```

### Chord Notation: temperament
```
dim=
dim-
o-
l-
s
dim+
dim
r-
m
i-
o+
r+
n
k-
h-
l+
M
h+
aug
k+
S
i+
k
h
i
```

### Note Names: numbers
```
0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26
```

### Note Names: letters
```
0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26
```

---

