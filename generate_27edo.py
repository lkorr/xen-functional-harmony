# Generate 27-EDO data for edo_data.md
from functional_harmony import generate_interval_quality_list

# Generate interval quality list
qualities = generate_interval_quality_list(27)

# Manually specify all triads from 27edo triads.txt
# Ordered by fifth (12, 13, 14, 15, 16, 17, 18, 19, 20) to group chords with the same fifth
triads = [
    (0, 6, 12),   # ss - subminor + subminor
    (0, 6, 13),   # sm - subminor + minor
    (0, 7, 13),   # ms - minor + subminor
    (0, 6, 14),   # sn - subminor + neutral
    (0, 7, 14),   # mm - minor + minor
    (0, 8, 14),   # ns - neutral + subminor
    (0, 6, 15),   # sM - subminor + major
    (0, 7, 15),   # mn - minor + neutral
    (0, 8, 15),   # nm - neutral + minor
    (0, 9, 15),   # Ms - major + subminor
    (0, 6, 16),   # sS - subminor + supermajor
    (0, 7, 16),   # mM - minor + major
    (0, 8, 16),   # nn - neutral + neutral
    (0, 9, 16),   # Mm - major + minor
    (0, 10, 16),  # Ss - supermajor + subminor
    (0, 7, 17),   # mS - minor + supermajor
    (0, 8, 17),   # nM - neutral + major
    (0, 9, 17),   # Mn - major + neutral
    (0, 10, 17),  # Sm - supermajor + minor
    (0, 8, 18),   # nS - neutral + supermajor
    (0, 9, 18),   # MM - major + major
    (0, 10, 18),  # Sn - supermajor + neutral
    (0, 9, 19),   # MS - major + supermajor
    (0, 10, 19),  # SM - supermajor + major
    (0, 10, 20),  # SS - supermajor + supermajor
]

cent_per_step = 1200.0 / 27

# Categorize thirds and fifths based on 27edo triads.txt
third_names = {
    6: 'subminor',     # 266.67c
    7: 'minor',        # 311.11c
    8: 'neutral',      # 355.56c
    9: 'major',        # 400c
    10: 'supermajor'   # 444.44c
}

# Fifth names and their descriptions based on 27edo triads.txt
fifth_info = {
    12: ('sb5', 'subdiminished'),           # 533.33c
    13: ('s^b5', 'subminor up-flat-5'),     # 577.78c
    14: ('d5', 'neutral-diminished'),        # 622.22c
    15: ('v5', 'down-5'),                    # 666.67c
    16: ('', 'perfect'),                     # 711.11c
    17: ('^5', 'up-5'),                      # 755.56c
    18: ('t5', 'neutral-augmented'),         # 800c
    19: ('v#5', 'down-sharp-5'),             # 844.44c
    20: ('#5', 'sharp-5')                    # 888.89c
}

# Chord names from 27edo triads.txt
# Based on /temp/ column (temperament notation)
# Ordered by fifth to match the triads array
temperament_names = [
    'dim=',   # ss: 0, 6, 12
    'dim-',   # sm: 0, 6, 13
    'dim+',   # ms: 0, 7, 13
    'o-',     # sn: 0, 6, 14
    'dim',    # mm: 0, 7, 14
    'o+',     # ns: 0, 8, 14
    'l-',     # sM: 0, 6, 15
    'r-',     # mn: 0, 7, 15
    'r+',     # nm: 0, 8, 15
    'l+',     # Ms: 0, 9, 15
    's',      # sS: 0, 6, 16
    'm',      # mM: 0, 7, 16
    'n',      # nn: 0, 8, 16
    'M',      # Mm: 0, 9, 16
    'S',      # Ss: 0, 10, 16
    'i-',     # mS: 0, 7, 17
    'k-',     # nM: 0, 8, 17
    'h+',     # Mn: 0, 9, 17
    'i+',     # Sm: 0, 10, 17
    'h-',     # nS: 0, 8, 18
    'aug',    # MM: 0, 9, 18
    'k',      # Sn: 0, 10, 18
    'k+',     # MS: 0, 9, 19
    'h',      # SM: 0, 10, 19
    'i'       # SS: 0, 10, 20
]

# Based on /alt/ column (descriptive names)
# Ordered by fifth to match the triads array
descriptive_names = [
    'dim=',    # ss: 0, 6, 12
    'dim-',    # sm: 0, 6, 13
    'dim+',    # ms: 0, 7, 13
    'msh-',    # sn: 0, 6, 14 - mosh minor
    'dim',     # mm: 0, 7, 14
    'msh+',    # ns: 0, 8, 14 - mosh major
    'mav-',    # sM: 0, 6, 15 - mavila minor
    'arc-',    # mn: 0, 7, 15 - archaeminor
    'arc+',    # nm: 0, 8, 15 - archaemajor
    'mav+',    # Ms: 0, 9, 15 - mavila major
    'sub',     # sS: 0, 6, 16 - subminor
    'min',     # mM: 0, 7, 16
    'neu',     # nn: 0, 8, 16 - neutral
    'maj',     # Mm: 0, 9, 16
    'sup',     # Ss: 0, 10, 16 - supermajor
    'mac-',    # mS: 0, 7, 17 - machminor
    'dic-',    # nM: 0, 8, 17 - dicoid minor
    'hyr+',    # Mn: 0, 9, 17 - hyrulic major
    'mac+',    # Sm: 0, 10, 17 - machmajor
    'hyr-',    # nS: 0, 8, 18 - hyrulic minor
    'aug',     # MM: 0, 9, 18
    'dic',     # Sn: 0, 10, 18 - dicoid
    'dic+',    # MS: 0, 9, 19 - superdicoid
    'hyr',     # SM: 0, 10, 19 - hyrulic
    'mac'      # SS: 0, 10, 20 - machinoid
]

print('## EDO 27')
print('**Current Note Names**: numbers')
print()
print('### Interval Quality List')
print('```')
print(', '.join(qualities))
print('```')
print()

print('### Leading Targets')
print('```')
print('19: 18  # M6->P5')
print('25: 0   # m7->root')
print('26: 0   # M7->root')
print('```')
print()

print('### Dominant Leading Intervals')
print('```')
print('25  # m7 creates dominant function')
print('26  # M7 creates dominant function')
print('```')
print()

print('### Chord Intervals')
print('```')
for root, third, fifth in triads:
    third_name = third_names[third]
    fifth_suffix, fifth_desc = fifth_info[fifth]
    print(f'{root}, {third}, {fifth}   # {third_name} {fifth_desc}')
print('```')
print()

# Create standard names (descriptive with temperament in parentheses)
full_names = []
for desc, temp in zip(descriptive_names, temperament_names):
    full_names.append(f"{desc} ({temp})")

print('### Chord Notation: full')
print('```')
for name in full_names:
    print(name)
print('```')
print()

print('### Chord Notation: standard')
print('```')
for name in descriptive_names:
    print(name)
print('```')
print()

print('### Chord Notation: temperament')
print('```')
for name in temperament_names:
    print(name)
print('```')
print()

print('### Note Names: numbers')
print('```')
print(', '.join(str(i) for i in range(27)))
print('```')
print()

print('### Note Names: letters')
print('```')
# 27-EDO letter names with microtonal accidentals
# Using the pattern from the triads.txt file
note_letters = [
    'C',      # 0
    'D♭',     # 1
    '^D♭',    # 2
    'vD',     # 3
    'D',      # 4
    'E♭',     # 5
    '^E♭',    # 6
    'vE',     # 7
    'E',      # 8
    'F',      # 9
    '^F',     # 10
    'vF♯',    # 11
    'F♯',     # 12
    'vG',     # 13
    'G',      # 14
    '^G',     # 15
    'vG♯',    # 16
    'G♯',     # 17
    'vA',     # 18
    'A',      # 19
    'B♭',     # 20
    '^B♭',    # 21
    'vB',     # 22
    'B',      # 23
    'vC',     # 24
    'C',      # 25 (enharmonic)
    '^C'      # 26
]
# Actually, let me use a simpler approach for now - just use the step values from the triads file
# Based on the notes in triads.txt: C, Db, ^Db, vD, D, Eb, ^Eb, Ed (neutral), vE, E, F, ^F/Gb, etc.
print(', '.join(str(i) for i in range(27)))
print('```')
print()

print('---')
print()
