#!/usr/bin/env python3
"""
Functional Harmony Chord Classifier

This script assigns harmonic function (tonic, predominant, dominant, mediant)
to chords based on the intervals they contain and their qualities.
"""

from typing import Set, Dict, List, Tuple
from dataclasses import dataclass
from enum import Enum
import json

class Quality(Enum):
    STABLE = 's'      # Points of resolution (root, P5)
    MODAL = 'm'       # Defines tonality (thirds)
    HOLLOW = 'h'      # Color tones, don't affect function much (M6, m7)
    UNSTABLE = 'u'    # Creates tension, moves away from tonic (M2, P4)
    LEADING = 'l'     # Half-step from stable tone, creates direction
    ODD = 'o'         # Dissonant, enhances existing function (m2, tritone)

class Function(Enum):
    TONIC = "tonic"
    PREDOMINANT = "predominant"
    DOMINANT = "dominant"
    MEDIANT = "mediant"

@dataclass
class EDOSystem:
    """Defines an equal temperament system with interval qualities."""
    edo: int
    interval_quality_list: List[str]
    leading_targets: Dict[int, int]
    dominant_leading_intervals: Set[int]
    chord_intervals: List[Tuple[int, ...]]
    chord_notation_systems: Dict[str, List[str]]
    note_name_systems: Dict[str, List[str]]
    current_notation: str = 'full'
    current_note_names: str = 'default'

    def __post_init__(self):
        """Convert quality list to dictionary."""
        if len(self.interval_quality_list) != self.edo:
            raise ValueError(f"Expected {self.edo} qualities, got {len(self.interval_quality_list)}")

        quality_map = {'s': Quality.STABLE, 'm': Quality.MODAL, 'h': Quality.HOLLOW,
                      'u': Quality.UNSTABLE, 'l': Quality.LEADING, 'o': Quality.ODD}
        self.interval_qualities = {i: quality_map[q] for i, q in enumerate(self.interval_quality_list)}

        # Find the perfect fifth (interval closest to 702 cents)
        cent_per_step = 1200.0 / self.edo
        self.perfect_fifth = min(range(self.edo), key=lambda i: abs(i * cent_per_step - 702))

        # Validate notation systems match chord intervals
        for system_name, notations in self.chord_notation_systems.items():
            if len(notations) != len(self.chord_intervals):
                raise ValueError(f"Notation system '{system_name}' has {len(notations)} names but {len(self.chord_intervals)} chord intervals")

        # Validate note name systems match edo
        for system_name, names in self.note_name_systems.items():
            if len(names) != self.edo:
                raise ValueError(f"Note name system '{system_name}' has {len(names)} names but edo is {self.edo}")

    @property
    def chord_types(self) -> Dict[str, Tuple[int, ...]]:
        """Get chord types dict for current notation system (for backward compatibility)."""
        names = self.chord_notation_systems[self.current_notation]
        return {name: intervals for name, intervals in zip(names, self.chord_intervals)}

    def get_note_names(self) -> List[str]:
        """Get note names for current system."""
        return self.note_name_systems[self.current_note_names]

    def get_quality(self, interval: int) -> Quality:
        """Get the quality of an interval (mod edo)."""
        return self.interval_qualities[interval % self.edo]

    def get_qualities(self, intervals: Set[int]) -> Set[Quality]:
        """Get all qualities present in a set of intervals."""
        return {self.get_quality(i) for i in intervals}

    def has_quality(self, intervals: Set[int], quality: Quality) -> bool:
        """Check if any interval has the given quality."""
        return quality in self.get_qualities(intervals)

    def has_active_leading(self, intervals: Set[int]) -> bool:
        """Check if chord has any ACTIVE leading intervals (resolution target not in chord)."""
        intervals_mod = {i % self.edo for i in intervals}
        for interval in intervals:
            if self.get_quality(interval) == Quality.LEADING:
                target = self.leading_targets.get(interval % self.edo)
                if target is not None and (target % self.edo) not in intervals_mod:
                    return True
        return False

    def has_dominant_leading(self, intervals: Set[int]) -> bool:
        """Check if chord has an ACTIVE dominant leading interval (leads to root, root not in chord)."""
        intervals_mod = {i % self.edo for i in intervals}
        for interval in intervals:
            if (interval % self.edo) in self.dominant_leading_intervals:
                target = self.leading_targets.get(interval % self.edo)
                if target is not None and (target % self.edo) not in intervals_mod:
                    return True
        return False


def parse_edo_data_file(filepath: str) -> Dict[int, EDOSystem]:
    """
    Parse the EDO data markdown file and return a dictionary of EDO systems.

    Args:
        filepath: Path to the edo_data.md file

    Returns:
        Dictionary mapping EDO numbers to EDOSystem instances
    """
    import re
    import os

    # If filepath is relative, make it relative to this script's directory
    if not os.path.isabs(filepath):
        script_dir = os.path.dirname(os.path.abspath(__file__))
        filepath = os.path.join(script_dir, filepath)

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    edo_systems = {}

    # Split by EDO sections
    edo_sections = re.split(r'\n---\n', content)

    for section in edo_sections:
        if not section.strip() or '## EDO' not in section:
            continue

        # Extract EDO number
        edo_match = re.search(r'## EDO (\d+)', section)
        if not edo_match:
            continue
        edo_num = int(edo_match.group(1))

        # Extract current note names
        current_note_names_match = re.search(r'\*\*Current Note Names\*\*:\s*(\w+)', section)
        current_note_names = current_note_names_match.group(1) if current_note_names_match else 'default'

        # Extract interval quality list
        quality_match = re.search(r'### Interval Quality List\n```\n(.*?)\n```', section, re.DOTALL)
        if not quality_match:
            continue
        quality_str = quality_match.group(1).strip()
        interval_quality_list = [q.strip() for q in quality_str.split(',')]

        # Extract leading targets
        leading_targets = {}
        leading_match = re.search(r'### Leading Targets\n```\n(.*?)\n```', section, re.DOTALL)
        if leading_match:
            for line in leading_match.group(1).strip().split('\n'):
                if ':' in line:
                    parts = line.split('#')[0].strip()  # Remove comment
                    if ':' in parts:
                        key, val = parts.split(':')
                        leading_targets[int(key.strip())] = int(val.strip())

        # Extract dominant leading intervals
        dominant_leading_intervals = set()
        dom_match = re.search(r'### Dominant Leading Intervals\n```\n(.*?)\n```', section, re.DOTALL)
        if dom_match:
            for line in dom_match.group(1).strip().split('\n'):
                if line.strip() and not line.strip().startswith('#'):
                    num_match = re.match(r'(\d+)', line.strip())
                    if num_match:
                        dominant_leading_intervals.add(int(num_match.group(1)))

        # Extract chord intervals
        chord_intervals = []
        chord_match = re.search(r'### Chord Intervals\n```\n(.*?)\n```', section, re.DOTALL)
        if chord_match:
            for line in chord_match.group(1).strip().split('\n'):
                if line.strip():
                    # Extract numbers before the # comment
                    parts = line.split('#')[0].strip()
                    if parts:
                        intervals = tuple(int(x.strip()) for x in parts.split(','))
                        chord_intervals.append(intervals)

        # Extract chord notation systems
        chord_notation_systems = {}
        notation_matches = re.finditer(r'### Chord Notation: (\w+)\n```\n(.*?)\n```', section, re.DOTALL)
        for match in notation_matches:
            system_name = match.group(1)
            notations = [n.strip() for n in match.group(2).strip().split('\n')]
            chord_notation_systems[system_name] = notations

        # Extract note name systems
        note_name_systems = {}
        note_matches = re.finditer(r'### Note Names: (\w+)\n```\n(.*?)\n```', section, re.DOTALL)
        for match in note_matches:
            system_name = match.group(1)
            notes_str = match.group(2).strip()
            notes = [n.strip() for n in notes_str.split(',')]
            note_name_systems[system_name] = notes

        # Handle special case for 'numbers' system if not present
        if 'numbers' not in note_name_systems:
            note_name_systems['numbers'] = [str(i) for i in range(edo_num)]

        # Create EDO system
        edo_system = EDOSystem(
            edo=edo_num,
            interval_quality_list=interval_quality_list,
            leading_targets=leading_targets,
            dominant_leading_intervals=dominant_leading_intervals,
            chord_intervals=chord_intervals,
            chord_notation_systems=chord_notation_systems,
            note_name_systems=note_name_systems,
            current_notation='full',
            current_note_names=current_note_names
        )

        edo_systems[edo_num] = edo_system

    return edo_systems


# Load EDO systems from data file
_EDO_SYSTEMS = parse_edo_data_file('edo_data.md')
EDO_12 = _EDO_SYSTEMS[12]
EDO_15 = _EDO_SYSTEMS[15]
EDO_17 = _EDO_SYSTEMS[17]
EDO_19 = _EDO_SYSTEMS[19]
EDO_20 = _EDO_SYSTEMS[20]
EDO_22 = _EDO_SYSTEMS[22]
EDO_23 = _EDO_SYSTEMS[23]
EDO_26 = _EDO_SYSTEMS[26]
EDO_31 = _EDO_SYSTEMS[31]
EDO_53 = _EDO_SYSTEMS[53]


def classify_chord(intervals: Set[int], system: EDOSystem) -> Function:
    """
    Classify a chord's harmonic function based on its intervals.

    Rules (applied in order):
    1. DOMINANT: Has ACTIVE dominant leading AND (has unstable OR dominant shell)
    2. PREDOMINANT: Has unstable interval AND no active dominant leading
    3. MEDIANT: No unstable AND (has ACTIVE leading OR has hollow OR has odd)
    4. TONIC: No unstable AND no active leading AND no hollow AND no odd AND contains root (0) AND perfect fifth
    5. PREDOMINANT (fallback): Otherwise
    """
    has_u = system.has_quality(intervals, Quality.UNSTABLE)
    has_h = system.has_quality(intervals, Quality.HOLLOW)
    has_o = system.has_quality(intervals, Quality.ODD)
    has_active_l = system.has_active_leading(intervals)
    has_dom_lead = system.has_dominant_leading(intervals)

    # Check for dominant shell: stable fifth present, no root, no internal stable intervals
    stable_intervals = {i for i in intervals if system.get_quality(i) == Quality.STABLE}
    has_fifth_no_root = len(stable_intervals) > 0 and 0 not in intervals

    # Check for internal stable intervals (stable interval between any two chord tones)
    interval_list = sorted(intervals)
    stable_interval_values = {i for i, q in system.interval_qualities.items()
                              if q == Quality.STABLE and i != 0}

    has_internal_stable = any(
        (interval_list[j] - interval_list[i]) % system.edo in stable_interval_values
        for i in range(len(interval_list))
        for j in range(i + 1, len(interval_list))
    )

    is_dominant_shell = has_fifth_no_root and not has_internal_stable

    # Apply rules
    if has_dom_lead and (has_u or is_dominant_shell):
        return Function.DOMINANT
    if has_u and not has_dom_lead:
        return Function.PREDOMINANT
    if not has_u and (has_active_l or has_h or has_o):
        return Function.MEDIANT
    # Rule 4: TONIC requires the chord to contain root (0) AND perfect fifth (closest to 702c)
    # Normalize intervals to check for perfect fifth
    intervals_mod = {i % system.edo for i in intervals}
    if 0 in intervals and system.perfect_fifth in intervals_mod:
        return Function.TONIC
    # Rule 5: Fallback to PREDOMINANT for chords without root or without perfect fifth
    return Function.PREDOMINANT


def analyze_chord(intervals: Set[int], system: EDOSystem, name: str = "") -> Dict:
    """Analyze a chord and return detailed information."""
    qualities = {i: system.get_quality(i) for i in sorted(intervals)}
    quality_set = set(qualities.values())

    return {
        'name': name,
        'intervals': sorted(intervals),
        'qualities': qualities,
        'has_unstable': Quality.UNSTABLE in quality_set,
        'has_active_leading': system.has_active_leading(intervals),
        'has_hollow': Quality.HOLLOW in quality_set,
        'has_odd': Quality.ODD in quality_set,
        'has_dominant_leading': system.has_dominant_leading(intervals),
        'function': classify_chord(intervals, system)
    }


def print_analysis(analysis: Dict):
    """Pretty print chord analysis."""
    q_str = ', '.join(f"{i}:{q.value}" for i, q in analysis['qualities'].items())
    print(f"{analysis['name']:15} | intervals: {str(analysis['intervals']):15} | "
          f"qualities: {q_str:30} | "
          f"u:{int(analysis['has_unstable'])} l:{int(analysis['has_active_leading'])} "
          f"h:{int(analysis['has_hollow'])} o:{int(analysis['has_odd'])} dom_l:{int(analysis['has_dominant_leading'])} | "
          f"-> {analysis['function'].value}")


def run_test_suite(tests: List[Tuple], system: EDOSystem):
    """Run a suite of tests and report results.

    Tests can be specified as (name, intervals, expected) or just (intervals, expected).
    If intervals are provided, the name will be auto-generated from the interval list.
    """
    passed = failed = 0

    for test in tests:
        # Handle both (name, intervals, expected) and (intervals, expected) formats
        if len(test) == 3:
            name, intervals, expected = test
        else:
            intervals, expected = test
            # Auto-generate name from intervals
            interval_str = '-'.join(str(i) for i in sorted(intervals))
            name = f"({interval_str})"

        analysis = analyze_chord(intervals, system, name)
        print_analysis(analysis)

        if expected is not None:
            if analysis['function'] == expected:
                passed += 1
            else:
                failed += 1
                print(f"  ^^^ FAILED: expected {expected.value}, got {analysis['function'].value}")

    if any(test[-1] is not None for test in tests):
        print(f"\nResults: {passed} passed, {failed} failed")


def run_tests():
    """Run test cases for 12-EDO major scale and chromatic chords."""
    print("=" * 110)
    print("FUNCTIONAL HARMONY CLASSIFIER - 12-EDO TEST SUITE")
    print("=" * 110)

    print("\n--- DIATONIC MAJOR SCALE TRIADS ---")
    run_test_suite([
        ("I (C-E-G)",     {0, 4, 7},   Function.TONIC),
        ("ii (D-F-A)",    {2, 5, 9},   Function.PREDOMINANT),
        ("iii (E-G-B)",   {4, 7, 11},  Function.MEDIANT),
        ("IV (F-A-C)",    {5, 9, 0},   Function.PREDOMINANT),
        ("V (G-B-D)",     {7, 11, 2},  Function.DOMINANT),
        ("vi (A-C-E)",    {9, 0, 4},   Function.MEDIANT),
        ("vii° (B-D-F)",  {11, 2, 5},  Function.DOMINANT),
    ], EDO_12)

    print("\n--- DIATONIC SEVENTH CHORDS ---")
    run_test_suite([
        ("Imaj7",         {0, 4, 7, 11}, Function.TONIC),
        ("ii7",           {2, 5, 9, 0},  Function.PREDOMINANT),
        ("iii7",          {4, 7, 11, 2}, Function.DOMINANT),
        ("IVmaj7",        {5, 9, 0, 4},  Function.PREDOMINANT),
        ("V7",            {7, 11, 2, 5}, Function.DOMINANT),
        ("vi7",           {9, 0, 4, 7},  Function.MEDIANT),
        ("viiø7",         {11, 2, 5, 9}, Function.DOMINANT),
    ], EDO_12)

    print("\n--- CHROMATIC / BORROWED CHORDS ---")
    run_test_suite([
        ("bII (Neapol.)", {1, 5, 8},   Function.PREDOMINANT),
        ("bIII",          {3, 7, 10},  Function.MEDIANT),
        ("iv",            {5, 8, 0},   Function.PREDOMINANT),
        ("#iv°",          {6, 9, 0},   Function.MEDIANT),
        ("bVI",           {8, 0, 3},   Function.MEDIANT),
        ("bVII",          {10, 2, 5},  Function.PREDOMINANT),
        ("viio7/V",       {6, 9, 0, 3}, Function.MEDIANT),
    ], EDO_12)

    print("\n--- AUGMENTED SIXTH CHORDS ---")
    run_test_suite([
        ("It+6 (Ab-C-F#)",    {8, 0, 6},    None),
        ("Fr+6 (Ab-C-D-F#)",  {8, 0, 2, 6}, None),
        ("Ger+6 (Ab-C-Eb-F#)",{8, 0, 3, 6}, None),
    ], EDO_12)

    print("\n--- SECONDARY DOMINANTS ---")
    run_test_suite([
        ("V/V (D-F#-A)",      {2, 6, 9},    None),
        ("V7/V",              {2, 6, 9, 0}, None),
        ("V/ii (A-C#-E)",     {9, 1, 4},    None),
        ("V/vi (E-G#-B)",     {4, 8, 11},   None),
        ("V7/vi",             {4, 8, 11, 2},None),
    ], EDO_12)

    print("\n--- HALF-DIMINISHED CHORDS (various positions) ---")
    run_test_suite([
        ("viiø7 (B-D-F-A)",   {11, 2, 5, 9}, Function.DOMINANT),
        ("iiø7 (D-F-Ab-C)",   {2, 5, 8, 0},  Function.PREDOMINANT),
        ("viø7 (A-C-Eb-G)",   {9, 0, 3, 7},  Function.MEDIANT),
    ], EDO_12)

    print("\n--- Sus CHORDS ---")
    run_test_suite([
        ("Isus4 (C-F-G)",     {0, 5, 7},    None),
        ("Isus2 (C-D-G)",     {0, 2, 7},    None),
        ("Vsus4 (G-C-D)",     {7, 0, 2},    None),
    ], EDO_12)


def get_root_names(edo: int, system: EDOSystem = None) -> List[Tuple[int, str]]:
    """Generate root names for a given EDO with cent values."""
    step_size = 1200.0 / edo

    if edo == 12:
        # For 12-EDO, use Roman numerals with cent values
        names = ['I', 'bII', 'II', 'bIII', 'III', 'IV', '#IV', 'V', 'bVI', 'VI', 'bVII', 'VII']
        return [(i, f"{names[i]} ({i * step_size:.0f}¢)") for i in range(edo)]
    elif system is not None:
        # Use note names from the system with cent values
        note_names = system.get_note_names()
        return [(i, f"{note_names[i]} ({i * step_size:.0f}¢)") for i in range(edo)]
    # For all other EDOs without a system, use step numbers with cent values
    return [(i, f"{i} ({i * step_size:.0f}¢)") for i in range(edo)]


def print_triad_table(system: EDOSystem = None):
    """Print a clean table of all chord types across all roots and their functions."""
    if system is None:
        system = EDO_12

    roots = get_root_names(system.edo, system)
    func_abbrev = {Function.TONIC: 'T', Function.PREDOMINANT: 'P',
                   Function.DOMINANT: 'D', Function.MEDIANT: 'M'}

    # Calculate column widths
    col_width = max(max(len(name) for name in system.chord_types.keys()) + 2, 10)
    root_col_width = max(max(len(name) for _, name in roots) + 2, 8)
    total_width = root_col_width + 3 + (col_width + 3) * len(system.chord_types)

    # Print header
    print("\n" + "=" * total_width)
    print(f"{system.edo}-EDO CHORD FUNCTION TABLE")
    print("T=Tonic, P=Predominant, D=Dominant, M=Mediant")
    print("=" * total_width)

    header = f"{'Root':<{root_col_width}} |"
    for chord_name in system.chord_types.keys():
        header += f" {chord_name:<{col_width}} |"
    print(f"\n{header}")
    print("-" * total_width)

    # Print rows
    counts = {f: 0 for f in Function}
    for root, root_name in roots:
        row = f"{root_name:<{root_col_width}} |"
        for chord_intervals in system.chord_types.values():
            intervals = {(root + i) % system.edo for i in chord_intervals}
            func = classify_chord(intervals, system)
            counts[func] += 1
            row += f" {func_abbrev[func]:<{col_width}} |"
        print(row)

    print("-" * total_width)

    # Print counts and chord types
    print("\nCOUNTS:")
    for func, count in counts.items():
        print(f"  {func.value}: {count}")

    print("\nCHORD TYPES:")
    for chord_name, chord_intervals in system.chord_types.items():
        print(f"  {chord_name}: {chord_intervals}")


def run_comprehensive_chromatic_tests(system: EDOSystem = None):
    """Test ALL chord types systematically across all roots."""
    if system is None:
        system = EDO_12

    print("=" * 120)
    print(f"COMPREHENSIVE CHORD TEST - {system.edo}-EDO - ALL ROOTS × ALL CHORD TYPES")
    print("=" * 120)

    roots = get_root_names(system.edo, system)
    results = []

    for root, root_name in roots:
        for chord_name, chord_intervals in system.chord_types.items():
            intervals = {(root + i) % system.edo for i in chord_intervals}
            analysis = analyze_chord(intervals, system, f"{root_name}{chord_name}")
            results.append({
                'name': analysis['name'],
                'root': root,
                'root_name': root_name,
                'quality': chord_name,
                'intervals': intervals,
                'function': analysis['function']
            })

    # Print detailed results
    for root, root_name in roots:
        print(f"\n--- Root: {root_name} (interval {root}) ---")
        for r in [r for r in results if r['root'] == root]:
            print_analysis(analyze_chord(r['intervals'], system, r['name']))

    # Summary
    print("\n" + "=" * 120)
    print("SUMMARY BY FUNCTION")
    print("=" * 120)

    for func in Function:
        chords_with_func = [r['name'] for r in results if r['function'] == func]
        print(f"\n{func.value.upper()} ({len(chords_with_func)} chords):")
        print(f"  {', '.join(chords_with_func)}")

    return results


def interactive_mode(system: EDOSystem):
    """Interactive mode to test custom chords."""
    print(f"\n{'='*60}")
    print(f"INTERACTIVE MODE - {system.edo}-EDO")
    print(f"{'='*60}")
    print("Enter chord intervals separated by spaces (e.g., '0 4 7' for major triad)")
    print("Type 'quit' to exit\n")

    while True:
        user_input = input("Intervals: ").strip()
        if user_input.lower() == 'quit':
            break

        try:
            intervals = {int(x) for x in user_input.split()}
            print_analysis(analyze_chord(intervals, system, "Custom"))
            print()
        except ValueError:
            print("Invalid input. Enter integers separated by spaces.\n")


def generate_html_table(system: EDOSystem = None, filename: str = None) -> str:
    """Generate a color-coded HTML table of chord functions."""
    if system is None:
        system = EDO_12

    roots = get_root_names(system.edo, system)
    func_abbrev = {Function.TONIC: 'T', Function.PREDOMINANT: 'P',
                   Function.DOMINANT: 'D', Function.MEDIANT: 'M'}

    # Get note names for the current system
    note_names = system.get_note_names()

    # Build table and count functions
    counts = {f: 0 for f in Function}
    table_rows = []

    # For each root, create a row
    for root, root_name in roots:
        cells = []
        # For each chord type (iterate over chord_intervals and get names from all notation systems)
        for chord_idx, chord_intervals in enumerate(system.chord_intervals):
            intervals = {(root + i) % system.edo for i in chord_intervals}
            func = classify_chord(intervals, system)
            counts[func] += 1
            abbrev = func_abbrev[func]
            # Create data attributes for the chord to be played
            intervals_list = sorted([(root + i) % system.edo for i in chord_intervals])
            intervals_str = ','.join(str(i) for i in intervals_list)

            # Store all notation names as data attributes
            notation_data = ' '.join(f'data-notation-{name}="{system.chord_notation_systems[name][chord_idx]}"'
                                     for name in system.chord_notation_systems.keys())

            cells.append(f'<td data-chord-index="{chord_idx}"><span class="func {abbrev} clickable" data-root="{root}" data-chord-index="{chord_idx}" data-intervals="{intervals_str}" data-edo="{system.edo}" {notation_data}>{abbrev}</span></td>')

        # Store all note name options as data attributes for the root cell
        root_note_data = ' '.join(f'data-notename-{name}="{system.note_name_systems[name][root]}"'
                                   for name in system.note_name_systems.keys())
        table_rows.append(f'<tr><td class="delete-cell" data-row-index="{root}"></td><td class="root-cell" data-root="{root}" {root_note_data}>{root_name}</td>{"".join(cells)}</tr>')

    # Create header cells with data attributes for all notation systems
    header_cells = []
    for chord_idx, chord_intervals in enumerate(system.chord_intervals):
        notation_data = ' '.join(f'data-notation-{name}="{system.chord_notation_systems[name][chord_idx]}"'
                                 for name in system.chord_notation_systems.keys())
        # Use first notation system as default
        default_name = system.chord_notation_systems[system.current_notation][chord_idx]
        header_cells.append(f'<th data-chord-index="{chord_idx}" {notation_data}>{default_name}</th>')
    header_cells_str = ''.join(header_cells)

    chord_defs = '<br>'.join(f'{name}: {intervals}'
                             for name, intervals in zip(system.chord_notation_systems[system.current_notation],
                                                       system.chord_intervals))

    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{system.edo}-EDO Chord Function Table</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;600;700&family=JetBrains+Mono:wght@400;600&display=swap" rel="stylesheet">
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        body {{
            font-family: 'Space Grotesk', -apple-system, BlinkMacSystemFont, sans-serif;
            background: linear-gradient(135deg, #0a0e27 0%, #1a1234 50%, #2a1b3d 100%);
            background-attachment: fixed;
            color: #e8e6f0;
            padding: 40px 20px;
            min-height: 100vh;
        }}
        .container {{
            display: flex;
            gap: 35px;
            justify-content: center;
            align-items: flex-start;
            max-width: none;
            margin: 0 auto;
            width: 100%;
            padding: 0 20px;
        }}
        .main-content {{
            display: flex;
            flex-direction: column;
            align-items: center;
        }}
        h1 {{
            color: #fff;
            margin-bottom: 12px;
            font-size: 42px;
            font-weight: 700;
            letter-spacing: -1px;
            text-transform: uppercase;
            background: linear-gradient(135deg, #a78bfa 0%, #ec4899 50%, #f59e0b 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }}
        .subtitle {{
            color: #9ca3af;
            margin-bottom: 30px;
            font-size: 15px;
            font-family: 'JetBrains Mono', monospace;
            letter-spacing: 0.3px;
        }}
        .legend {{
            display: flex;
            gap: 24px;
            margin-bottom: 28px;
            flex-wrap: wrap;
            justify-content: center;
            padding: 16px;
            background: rgba(139, 92, 246, 0.08);
            border-radius: 16px;
            border: 1px solid rgba(167, 139, 250, 0.2);
        }}
        .legend-item {{
            display: flex;
            align-items: center;
            gap: 10px;
            font-size: 14px;
            font-weight: 500;
            font-family: 'JetBrains Mono', monospace;
        }}
        .legend-box {{
            width: 32px;
            height: 32px;
            border-radius: 8px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: 700;
            font-size: 14px;
            border: 2px solid rgba(255, 255, 255, 0.15);
        }}
        table {{
            border-collapse: separate;
            border-spacing: 0;
            background: rgba(15, 23, 42, 0.7);
            backdrop-filter: blur(10px);
            border-radius: 20px;
            overflow: hidden;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.5), 0 0 0 1px rgba(167, 139, 250, 0.1);
            flex-shrink: 0;
        }}
        th, td {{
            padding: 12px 16px;
            text-align: center;
            border-bottom: 1px solid rgba(139, 92, 246, 0.1);
            border-right: 1px solid rgba(139, 92, 246, 0.1);
        }}
        th {{
            background: linear-gradient(135deg, rgba(88, 28, 135, 0.5), rgba(59, 7, 100, 0.5));
            color: #e0d9f0;
            font-weight: 700;
            font-size: 13px;
            letter-spacing: 0.5px;
            cursor: pointer;
            user-select: none;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            position: relative;
            font-variant: normal;
        }}
        th::after {{
            content: '';
            position: absolute;
            bottom: 0;
            left: 0;
            right: 0;
            height: 2px;
            background: linear-gradient(90deg, #a78bfa, #ec4899);
            transform: scaleX(0);
            transition: transform 0.3s ease;
        }}
        th:hover::after {{
            transform: scaleX(1);
        }}
        th:hover {{
            background: linear-gradient(135deg, rgba(109, 40, 217, 0.6), rgba(88, 28, 135, 0.6));
            color: #fff;
        }}
        th.collapsed {{
            opacity: 0.4;
        }}
        th:nth-child(2) {{
            text-align: left;
            font-family: 'JetBrains Mono', monospace;
        }}
        td:nth-child(2) {{
            background: linear-gradient(135deg, rgba(88, 28, 135, 0.4), rgba(59, 7, 100, 0.4));
            color: #d8b4fe;
            font-weight: 700;
            text-align: left;
            cursor: pointer;
            user-select: none;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            font-family: 'JetBrains Mono', monospace;
            letter-spacing: 0.5px;
        }}
        td:nth-child(2):hover {{
            background: linear-gradient(135deg, rgba(109, 40, 217, 0.5), rgba(88, 28, 135, 0.5));
            color: #fbbf24;
            transform: translateX(4px);
        }}
        tr.highlighted td {{
            background: rgba(251, 191, 36, 0.15) !important;
            border-color: rgba(251, 191, 36, 0.3) !important;
        }}
        tr.highlighted td:nth-child(2) {{
            background: linear-gradient(135deg, rgba(251, 191, 36, 0.3), rgba(245, 158, 11, 0.3)) !important;
            color: #fbbf24 !important;
        }}
        tr.highlighted td.delete-cell {{
            background: rgba(220, 38, 38, 0.2) !important;
        }}
        .hidden {{
            display: none;
        }}
        .delete-cell {{
            width: 36px;
            background: rgba(15, 23, 42, 0.5);
            cursor: pointer;
            text-align: center;
            color: rgba(239, 68, 68, 0.4);
            font-size: 22px;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            user-select: none;
            font-weight: 700;
        }}
        .delete-cell:hover {{
            background: linear-gradient(135deg, rgba(220, 38, 38, 0.5), rgba(185, 28, 28, 0.5));
            color: #fca5a5;
            transform: scale(1.1);
        }}
        .delete-cell::before {{
            content: '×';
        }}
        .table-controls {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 20px;
            gap: 24px;
            padding: 14px 20px;
            background: rgba(139, 92, 246, 0.08);
            border-radius: 12px;
            border: 1px solid rgba(167, 139, 250, 0.15);
        }}
        .control-group {{
            display: flex;
            align-items: center;
            gap: 12px;
        }}
        .control-label {{
            font-size: 13px;
            color: #c4b5fd;
            font-family: 'JetBrains Mono', monospace;
            font-weight: 600;
            letter-spacing: 0.5px;
        }}
        .btn {{
            padding: 10px 20px;
            background: linear-gradient(135deg, rgba(139, 92, 246, 0.3), rgba(109, 40, 217, 0.3));
            color: #e0d9f0;
            border: 1px solid rgba(167, 139, 250, 0.3);
            border-radius: 8px;
            cursor: pointer;
            font-size: 13px;
            font-weight: 600;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            font-family: 'Space Grotesk', sans-serif;
        }}
        .btn:hover {{
            background: linear-gradient(135deg, rgba(167, 139, 250, 0.5), rgba(139, 92, 246, 0.5));
            color: #fff;
            border-color: rgba(167, 139, 250, 0.6);
            transform: translateY(-2px);
            box-shadow: 0 8px 20px rgba(139, 92, 246, 0.3);
        }}
        .btn:active {{
            transform: translateY(0px);
            box-shadow: 0 4px 12px rgba(139, 92, 246, 0.2);
        }}
        select {{
            padding: 10px 16px;
            background: rgba(15, 23, 42, 0.6);
            color: #e0d9f0;
            border: 1px solid rgba(139, 92, 246, 0.3);
            border-radius: 8px;
            font-size: 13px;
            cursor: pointer;
            font-family: 'JetBrains Mono', monospace;
            font-weight: 500;
            transition: all 0.3s ease;
        }}
        select:hover {{
            border-color: rgba(167, 139, 250, 0.5);
            background: rgba(15, 23, 42, 0.8);
        }}
        select:focus {{
            outline: none;
            border-color: #a78bfa;
            box-shadow: 0 0 0 3px rgba(167, 139, 250, 0.1);
        }}
        .func {{
            display: inline-block;
            width: 38px;
            height: 38px;
            border-radius: 10px;
            line-height: 38px;
            font-weight: 800;
            font-size: 16px;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            border: 2px solid transparent;
            position: relative;
            overflow: hidden;
        }}
        .func::before {{
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.3), transparent);
            transition: left 0.5s ease;
        }}
        .func.clickable {{
            cursor: pointer;
        }}
        .func.clickable:hover::before {{
            left: 100%;
        }}
        .func.clickable:hover {{
            transform: scale(1.15) rotate(-3deg);
            border-color: rgba(255, 255, 255, 0.3);
        }}
        .func.clickable:active {{
            transform: scale(0.9) rotate(0deg);
        }}
        .T {{
            background: linear-gradient(135deg, #14b8a6 0%, #06b6d4 100%);
            color: #fff;
            box-shadow: 0 4px 16px rgba(20, 184, 166, 0.5), inset 0 -2px 8px rgba(0, 0, 0, 0.2);
        }}
        .T:hover {{
            box-shadow: 0 8px 24px rgba(20, 184, 166, 0.7), inset 0 -2px 8px rgba(0, 0, 0, 0.2);
        }}
        .P {{
            background: linear-gradient(135deg, #f59e0b 0%, #f97316 100%);
            color: #78350f;
            box-shadow: 0 4px 16px rgba(245, 158, 11, 0.5), inset 0 -2px 8px rgba(0, 0, 0, 0.15);
        }}
        .P:hover {{
            box-shadow: 0 8px 24px rgba(245, 158, 11, 0.7), inset 0 -2px 8px rgba(0, 0, 0, 0.15);
        }}
        .D {{
            background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
            color: #fff;
            box-shadow: 0 4px 16px rgba(239, 68, 68, 0.5), inset 0 -2px 8px rgba(0, 0, 0, 0.2);
        }}
        .D:hover {{
            box-shadow: 0 8px 24px rgba(239, 68, 68, 0.7), inset 0 -2px 8px rgba(0, 0, 0, 0.2);
        }}
        .M {{
            background: linear-gradient(135deg, #a78bfa 0%, #8b5cf6 100%);
            color: #fff;
            box-shadow: 0 4px 16px rgba(139, 92, 246, 0.5), inset 0 -2px 8px rgba(0, 0, 0, 0.2);
        }}
        .M:hover {{
            box-shadow: 0 8px 24px rgba(139, 92, 246, 0.7), inset 0 -2px 8px rgba(0, 0, 0, 0.2);
        }}
        .counts {{
            margin-top: 28px;
            display: flex;
            gap: 20px;
            flex-wrap: wrap;
            justify-content: center;
        }}
        .count-item {{
            padding: 14px 24px;
            border-radius: 12px;
            font-size: 14px;
            font-family: 'JetBrains Mono', monospace;
            font-weight: 600;
            letter-spacing: 0.3px;
            transition: all 0.3s ease;
            border: 2px solid transparent;
        }}
        .count-item:hover {{
            transform: translateY(-3px);
        }}
        .count-item.T {{
            background: rgba(20, 184, 166, 0.15);
            border-color: #14b8a6;
            color: #5eead4;
        }}
        .count-item.T:hover {{
            background: rgba(20, 184, 166, 0.25);
            box-shadow: 0 8px 20px rgba(20, 184, 166, 0.3);
        }}
        .count-item.P {{
            background: rgba(245, 158, 11, 0.15);
            border-color: #f59e0b;
            color: #fbbf24;
        }}
        .count-item.P:hover {{
            background: rgba(245, 158, 11, 0.25);
            box-shadow: 0 8px 20px rgba(245, 158, 11, 0.3);
        }}
        .count-item.D {{
            background: rgba(239, 68, 68, 0.15);
            border-color: #ef4444;
            color: #fca5a5;
        }}
        .count-item.D:hover {{
            background: rgba(239, 68, 68, 0.25);
            box-shadow: 0 8px 20px rgba(239, 68, 68, 0.3);
        }}
        .count-item.M {{
            background: rgba(139, 92, 246, 0.15);
            border-color: #8b5cf6;
            color: #c4b5fd;
        }}
        .count-item.M:hover {{
            background: rgba(139, 92, 246, 0.25);
            box-shadow: 0 8px 20px rgba(139, 92, 246, 0.3);
        }}
        .chord-defs {{
            margin-top: 28px;
            padding: 20px 24px;
            background: rgba(15, 23, 42, 0.6);
            backdrop-filter: blur(10px);
            border-radius: 12px;
            font-family: 'JetBrains Mono', monospace;
            font-size: 12px;
            border: 1px solid rgba(139, 92, 246, 0.2);
            line-height: 1.8;
        }}
        .chord-defs strong {{
            color: #a78bfa;
            font-size: 14px;
            letter-spacing: 0.5px;
        }}
        .chord-history {{
            background: rgba(15, 23, 42, 0.7);
            backdrop-filter: blur(10px);
            border-radius: 20px;
            padding: 20px;
            width: auto;
            min-width: 280px;
            max-width: 600px;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.5), 0 0 0 1px rgba(167, 139, 250, 0.1);
            display: flex;
            flex-direction: column;
            align-self: stretch;
        }}
        .chord-history h3 {{
            margin: 0 0 18px 0;
            font-size: 18px;
            color: #fff;
            text-align: center;
            font-weight: 700;
            letter-spacing: 0.5px;
            text-transform: uppercase;
            background: linear-gradient(135deg, #a78bfa, #ec4899);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            flex-shrink: 0;
        }}
        .chord-history-list {{
            display: flex;
            flex-direction: column;
            gap: 10px;
            flex: 1;
            overflow-y: auto;
            padding-right: 8px;
            min-height: 0;
        }}
        .chord-history-list::-webkit-scrollbar {{
            width: 6px;
        }}
        .chord-history-list::-webkit-scrollbar-track {{
            background: rgba(139, 92, 246, 0.1);
            border-radius: 10px;
        }}
        .chord-history-list::-webkit-scrollbar-thumb {{
            background: rgba(167, 139, 250, 0.4);
            border-radius: 10px;
        }}
        .chord-history-list::-webkit-scrollbar-thumb:hover {{
            background: rgba(167, 139, 250, 0.6);
        }}
        .chord-history-item {{
            background: linear-gradient(135deg, rgba(88, 28, 135, 0.3), rgba(59, 7, 100, 0.3));
            padding: 12px 14px;
            border-radius: 10px;
            font-family: 'JetBrains Mono', monospace;
            font-size: 13px;
            border-left: 3px solid #a78bfa;
            transition: all 0.3s ease;
            white-space: nowrap;
            display: flex;
            justify-content: space-between;
            align-items: center;
            gap: 10px;
            cursor: pointer;
        }}
        .chord-history-item:hover {{
            background: linear-gradient(135deg, rgba(109, 40, 217, 0.4), rgba(88, 28, 135, 0.4));
            transform: translateX(4px);
            border-left-color: #ec4899;
        }}
        .chord-history-item-content {{
            flex: 1;
        }}
        .chord-history-delete {{
            color: rgba(239, 68, 68, 0.5);
            cursor: pointer;
            font-size: 18px;
            font-weight: 700;
            transition: all 0.2s ease;
            padding: 2px 6px;
            border-radius: 4px;
            user-select: none;
        }}
        .chord-history-delete:hover {{
            color: #fca5a5;
            background: rgba(220, 38, 38, 0.3);
            transform: scale(1.2);
        }}
        .chord-history-item .chord-name {{
            font-weight: 700;
            color: #c4b5fd;
            margin-bottom: 6px;
            font-size: 14px;
        }}
        .chord-history-item .chord-intervals {{
            color: #9ca3af;
            font-size: 11px;
            line-height: 1.5;
        }}
        .scale-filter {{
            background: rgba(15, 23, 42, 0.7);
            backdrop-filter: blur(10px);
            border-radius: 20px;
            padding: 20px;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.5), 0 0 0 1px rgba(167, 139, 250, 0.1);
            margin-bottom: 20px;
            max-width: 500px;
        }}
        .scale-filter h3 {{
            margin: 0 0 12px 0;
            font-size: 16px;
            color: #fff;
            font-weight: 700;
            letter-spacing: 0.5px;
            text-transform: uppercase;
        }}
        .scale-filter-input {{
            width: 100%;
            padding: 12px 16px;
            background: rgba(15, 23, 42, 0.6);
            color: #e0d9f0;
            border: 2px solid rgba(139, 92, 246, 0.3);
            border-radius: 10px;
            font-size: 14px;
            font-family: 'JetBrains Mono', monospace;
            transition: all 0.3s ease;
        }}
        .scale-filter-input:focus {{
            outline: none;
            border-color: #a78bfa;
            box-shadow: 0 0 0 3px rgba(167, 139, 250, 0.2);
        }}
        .scale-filter-input::placeholder {{
            color: rgba(156, 163, 175, 0.5);
        }}
        .scale-filter-hint {{
            margin-top: 8px;
            font-size: 12px;
            color: #9ca3af;
            font-family: 'JetBrains Mono', monospace;
        }}
        td.scale-match {{
            background: rgba(34, 197, 94, 0.25) !important;
            border-color: rgba(34, 197, 94, 0.4) !important;
        }}
        td.scale-match .func {{
            border-color: rgba(34, 197, 94, 0.6);
            box-shadow: 0 4px 16px rgba(34, 197, 94, 0.4), inset 0 -2px 8px rgba(0, 0, 0, 0.2);
        }}
        .func.playing {{
            animation: pulseGlow 0.6s ease-in-out 3;
            border-color: rgba(255, 255, 255, 0.8) !important;
        }}
        @keyframes pulseGlow {{
            0%, 100% {{
                transform: scale(1);
                box-shadow: 0 4px 16px rgba(255, 255, 255, 0.3);
            }}
            50% {{
                transform: scale(1.2);
                box-shadow: 0 8px 32px rgba(255, 255, 255, 0.8);
            }}
        }}
    </style>
</head>
<body>
    <div class="main-content">
        <h1>{system.edo}-EDO Chord Function Table</h1>
        <p class="subtitle">Harmonic function classification for all chord types (click any chord to play it)</p>

        <div class="legend">
        <div class="legend-item">
            <div class="legend-box T">T</div>
            <span>Tonic (stable, home)</span>
        </div>
        <div class="legend-item">
            <div class="legend-box P">P</div>
            <span>Predominant (away from tonic)</span>
        </div>
        <div class="legend-item">
            <div class="legend-box D">D</div>
            <span>Dominant (tension -> tonic)</span>
        </div>
        <div class="legend-item">
            <div class="legend-box M">M</div>
            <span>Mediant (color, prolongation)</span>
        </div>
    </div>

    <div class="scale-filter">
        <h3>Scale Filter</h3>
        <input type="text" id="scaleFilterInput" class="scale-filter-input" placeholder="Enter scale intervals (e.g., 0 2 4 5 7 9 11)">
        <div class="scale-filter-hint">Enter space-separated intervals to highlight chords that use only those notes</div>
    </div>

    <div class="table-controls">
        <div class="control-group">
            <span class="control-label">Chord Notation:</span>
            <select id="chordNotationSelect">
                {''.join(f'<option value="{name}"{"selected" if name == system.current_notation else ""}>{name.title()}</option>' for name in system.chord_notation_systems.keys())}
            </select>
        </div>
        <div class="control-group">
            <span class="control-label">Note Names:</span>
            <select id="noteNameSelect">
                {''.join(f'<option value="{name}"{"selected" if name == system.current_note_names else ""}>{name.title()}</option>' for name in system.note_name_systems.keys())}
            </select>
        </div>
        <div class="control-group">
            <span class="control-label">Root/Tonic:</span>
            <select id="rootSelect">
            </select>
        </div>
        <div class="control-group">
            <span class="control-label">Waveform:</span>
            <select id="waveformSelect">
                <option value="sine">Sine</option>
                <option value="triangle">Triangle</option>
                <option value="sawtooth">Sawtooth</option>
                <option value="square">Square</option>
            </select>
        </div>
        <button id="refreshTableBtn" class="btn">Refresh Table</button>
    </div>

    <div class="container">
        <table>
        <thead>
            <tr>
                <th class="delete-cell" style="cursor: default;"></th>
                <th>Root</th>
                {header_cells_str}
            </tr>
        </thead>
        <tbody>
            {''.join(table_rows)}
        </tbody>
    </table>

    <div class="chord-history">
        <button id="downloadMidiBtn" class="btn" style="width: 100%; margin-bottom: 12px;">Download MIDI</button>
        <h3>Chord History</h3>
        <div class="chord-history-list" id="chordHistoryList">
            <div style="color: #666; text-align: center; font-size: 12px; font-style: italic;">Click chords to play</div>
        </div>
    </div>
    </div>

    <div class="counts">
        <div class="count-item T"><strong>Tonic:</strong> {counts[Function.TONIC]} chords</div>
        <div class="count-item P"><strong>Predominant:</strong> {counts[Function.PREDOMINANT]} chords</div>
        <div class="count-item D"><strong>Dominant:</strong> {counts[Function.DOMINANT]} chords</div>
        <div class="count-item M"><strong>Mediant:</strong> {counts[Function.MEDIANT]} chords</div>
    </div>

    <div class="chord-defs">
        <strong>Chord Types:</strong><br>
        {chord_defs}
    </div>
    </div>

    <script>
        // Web Audio API setup
        const audioContext = new (window.AudioContext || window.webkitAudioContext)();

        // Track last played chord for voice leading
        let lastChordPitches = null;

        // Track current waveform
        let currentWaveform = 'sine';

        // Chord history tracking
        const chordHistory = [];
        const MAX_HISTORY = 15;

        // Store all note name systems
        const noteNameSystems = {json.dumps({name: names for name, names in system.note_name_systems.items()})};

        // Current note name system
        let currentNoteNameSystem = '{system.current_note_names}';

        // Current root offset (for rotation)
        let currentRootOffset = 0;

        // Get note names for current system
        function getNoteNames() {{
            return noteNameSystems[currentNoteNameSystem];
        }}

        // Populate root select dropdown
        function populateRootSelect() {{
            const rootSelect = document.getElementById('rootSelect');
            const noteNames = getNoteNames();
            rootSelect.innerHTML = '';

            noteNames.forEach((name, index) => {{
                const option = document.createElement('option');
                option.value = index;
                option.textContent = name;
                if (index === currentRootOffset) {{
                    option.selected = true;
                }}
                rootSelect.appendChild(option);
            }});
        }}

        // Update all root cell labels based on current root offset
        function updateRootLabels() {{
            const noteNames = getNoteNames();
            const edo = noteNames.length;

            document.querySelectorAll('.root-cell').forEach(rootCell => {{
                const originalRoot = parseInt(rootCell.getAttribute('data-root'));
                // Rotate: table position 0 shows noteNames[offset], position 1 shows noteNames[offset+1], etc.
                const rotatedIndex = (originalRoot + currentRootOffset) % edo;
                const displayName = noteNames[rotatedIndex];
                rootCell.textContent = displayName;
            }});
        }}

        // Initialize root select
        populateRootSelect();

        // Chord notation selector
        document.getElementById('chordNotationSelect').addEventListener('change', function(e) {{
            const selectedNotation = e.target.value;
            // Update all column headers
            document.querySelectorAll('th[data-chord-index]').forEach(th => {{
                const chordIndex = th.getAttribute('data-chord-index');
                const newName = th.getAttribute(`data-notation-${{selectedNotation}}`);
                if (newName) {{
                    th.textContent = newName;
                }}
            }});
            // Update chord history to show new notation
            updateHistoryDisplay();
        }});

        // Note name selector
        document.getElementById('noteNameSelect').addEventListener('change', function(e) {{
            currentNoteNameSystem = e.target.value;

            // Reset root offset when changing note name system
            currentRootOffset = 0;

            // Repopulate root select dropdown with new names
            populateRootSelect();

            // Update all root cells in the table
            updateRootLabels();

            // Update chord history to show new note names
            updateHistoryDisplay();
        }});

        // Root/Tonic selector
        document.getElementById('rootSelect').addEventListener('change', function(e) {{
            currentRootOffset = parseInt(e.target.value);

            // Update all root cell labels
            updateRootLabels();

            // Update chord history to show new root names
            updateHistoryDisplay();
        }});

        // Waveform selector
        document.getElementById('waveformSelect').addEventListener('change', function(e) {{
            currentWaveform = e.target.value;
        }});

        // Scale filter functionality
        function updateScaleFilter() {{
            const input = document.getElementById('scaleFilterInput').value.trim();

            // Clear all highlights
            document.querySelectorAll('td.scale-match').forEach(td => {{
                td.classList.remove('scale-match');
            }});

            if (!input) {{
                return; // No filter applied
            }}

            // Parse the scale intervals
            try {{
                const scaleIntervals = new Set(
                    input.split(/\\s+/).map(s => {{
                        const num = parseInt(s);
                        if (isNaN(num)) throw new Error('Invalid number');
                        return num;
                    }})
                );

                if (scaleIntervals.size === 0) return;

                // Get EDO from the first chord button
                const edo = parseInt(document.querySelector('.func.clickable').getAttribute('data-edo'));

                // Normalize scale intervals to be within EDO range
                const normalizedScale = new Set([...scaleIntervals].map(i => ((i % edo) + edo) % edo));

                // Check each chord cell
                document.querySelectorAll('td[data-chord-index]').forEach(td => {{
                    const funcSpan = td.querySelector('.func.clickable');
                    if (!funcSpan) return;

                    const intervalsStr = funcSpan.getAttribute('data-intervals');
                    const chordIntervals = intervalsStr.split(',').map(s => parseInt(s));

                    // Check if all chord intervals are in the scale
                    const allInScale = chordIntervals.every(interval => {{
                        const normalized = ((interval % edo) + edo) % edo;
                        return normalizedScale.has(normalized);
                    }});

                    if (allInScale) {{
                        td.classList.add('scale-match');
                    }}
                }});
            }} catch (e) {{
                console.error('Error parsing scale:', e);
            }}
        }}

        // Add input listener for scale filter
        document.getElementById('scaleFilterInput').addEventListener('input', updateScaleFilter);

        // Refresh table button - restore all hidden columns and rows
        document.getElementById('refreshTableBtn').addEventListener('click', function() {{
            // Restore all collapsed columns
            document.querySelectorAll('th.collapsed').forEach(th => {{
                th.classList.remove('collapsed');
            }});

            // Restore all hidden cells
            document.querySelectorAll('td.hidden, th.hidden').forEach(cell => {{
                cell.classList.remove('hidden');
            }});

            // Restore all hidden rows
            document.querySelectorAll('tbody tr').forEach(row => {{
                row.style.display = '';
            }});

            // Clear undo stack
            undoStack.length = 0;
        }});

        // Function to play a note
        function playNote(frequency, startTime, duration, gain = 0.15) {{
            const oscillator = audioContext.createOscillator();
            const gainNode = audioContext.createGain();

            oscillator.type = currentWaveform;
            oscillator.frequency.setValueAtTime(frequency, startTime);

            gainNode.gain.setValueAtTime(0, startTime);
            gainNode.gain.linearRampToValueAtTime(gain, startTime + 0.01);
            gainNode.gain.exponentialRampToValueAtTime(0.001, startTime + duration);

            oscillator.connect(gainNode);
            gainNode.connect(audioContext.destination);

            oscillator.start(startTime);
            oscillator.stop(startTime + duration);
        }}

        // Convert interval to pitch (in semitones from C4)
        function intervalToPitch(interval, edo) {{
            // Apply root offset to transpose the pitch
            const offsetInSemitones = (currentRootOffset / edo) * 12;
            return ((interval / edo) * 12) + offsetInSemitones;
        }}

        // Find best voicing with minimal movement from last chord
        function findBestVoicing(intervals, edo) {{
            const basePitches = intervals.map(i => intervalToPitch(i, edo));

            // If no previous chord, use root position in comfortable range
            if (!lastChordPitches) {{
                return basePitches.map(p => p + 60); // Start at middle C (MIDI 60)
            }}

            // Generate all possible inversions within a 2-octave range
            const possibleVoicings = [];

            // Try different octaves for the chord
            for (let octaveShift = -1; octaveShift <= 1; octaveShift++) {{
                const baseVoicing = basePitches.map(p => p + 60 + (octaveShift * 12));

                // For each base voicing, try all permutations (inversions)
                const notes = [...baseVoicing];

                // Generate inversions by moving lowest note up an octave
                for (let inv = 0; inv < notes.length; inv++) {{
                    const voicing = [...notes];
                    // Move notes that are too low up by octaves
                    for (let i = 0; i < voicing.length; i++) {{
                        while (voicing[i] < 48) voicing[i] += 12; // Keep above C3
                        while (voicing[i] > 84) voicing[i] -= 12; // Keep below C6
                    }}
                    possibleVoicings.push(voicing.sort((a, b) => a - b));

                    // Rotate for next inversion
                    notes.push(notes.shift() + 12);
                }}
            }}

            // Find voicing with minimal total movement from last chord
            let bestVoicing = possibleVoicings[0];
            let minDistance = Infinity;

            for (const voicing of possibleVoicings) {{
                // Calculate total distance (sum of squared differences)
                let distance = 0;
                const sortedVoicing = [...voicing].sort((a, b) => a - b);
                const sortedLast = [...lastChordPitches].sort((a, b) => a - b);

                // Handle different chord sizes by comparing available voices
                const minLen = Math.min(sortedVoicing.length, sortedLast.length);
                for (let i = 0; i < minLen; i++) {{
                    distance += Math.pow(sortedVoicing[i] - sortedLast[i], 2);
                }}

                // Penalize voicings with very different sizes
                distance += Math.pow(sortedVoicing.length - sortedLast.length, 2) * 100;

                if (distance < minDistance) {{
                    minDistance = distance;
                    bestVoicing = sortedVoicing;
                }}
            }}

            return bestVoicing;
        }}

        // Function to play a chord with voice leading
        function playChord(intervals, edo) {{
            const baseFreq = 261.63; // Middle C (C4)
            const duration = 2.0; // seconds
            const startTime = audioContext.currentTime + 0.05;

            // Find best voicing for smooth voice leading
            const pitches = findBestVoicing(intervals, edo);

            // Remember this chord for next time
            lastChordPitches = pitches;

            // Play each note at its voiced pitch
            pitches.forEach(pitch => {{
                // Convert MIDI pitch to frequency
                const frequency = baseFreq * Math.pow(2, (pitch - 60) / 12);
                playNote(frequency, startTime, duration);
            }});
        }}

        // Function to add chord to history
        function addToHistory(root, chordIndex, intervals) {{
            const chordInfo = {{
                root: root,
                chordIndex: chordIndex,
                intervals: intervals
            }};

            // Add to beginning of array
            chordHistory.unshift(chordInfo);

            // Keep only last 15
            if (chordHistory.length > MAX_HISTORY) {{
                chordHistory.pop();
            }}

            // Update display
            updateHistoryDisplay();
        }}

        // Function to update history display
        function updateHistoryDisplay() {{
            const historyList = document.getElementById('chordHistoryList');
            historyList.innerHTML = '';

            if (chordHistory.length === 0) {{
                historyList.innerHTML = '<div style="color: #666; text-align: center; font-size: 12px; font-style: italic;">Click chords to play</div>';
                return;
            }}

            const edo = parseInt(document.querySelector('.func.clickable').getAttribute('data-edo'));
            const noteNames = getNoteNames();
            const currentNotation = document.getElementById('chordNotationSelect').value;

            chordHistory.forEach((chord, index) => {{
                const item = document.createElement('div');
                item.className = 'chord-history-item';

                // Get root name from current note name system with rotation
                const rotatedIndex = (chord.root + currentRootOffset) % edo;
                const rootName = noteNames[rotatedIndex];

                // Get chord name from the table using chord index and current notation
                const chordCell = document.querySelector(`[data-chord-index="${{chord.chordIndex}}"][data-root="${{chord.root}}"]`);
                const chordName = chordCell ? chordCell.getAttribute(`data-notation-${{currentNotation}}`) : '';

                // Build interval display with rotation
                let intervalDisplay;
                if (currentNoteNameSystem === 'numbers') {{
                    // Just show numbers
                    intervalDisplay = chord.intervals.join(', ');
                }} else if (currentNoteNameSystem === 'letters_and_numbers') {{
                    // Show both: "0 C, 4 E, 7 G"
                    intervalDisplay = chord.intervals.map(i => {{
                        const rotatedNoteIndex = (i + currentRootOffset) % edo;
                        return noteNames[rotatedNoteIndex];
                    }}).join(', ');
                }} else {{
                    // Just show letter names: "C, E, G"
                    intervalDisplay = chord.intervals.map(i => {{
                        const rotatedNoteIndex = (i + currentRootOffset) % edo;
                        return noteNames[rotatedNoteIndex];
                    }}).join(', ');
                }}

                item.innerHTML = `
                    <div class="chord-history-item-content">
                        <div class="chord-name">${{rootName}} ${{chordName}}</div>
                        <div class="chord-intervals">${{intervalDisplay}}</div>
                    </div>
                    <span class="chord-history-delete" data-index="${{index}}">×</span>
                `;
                item.setAttribute('data-intervals', chord.intervals.join(','));
                item.setAttribute('data-root', chord.root);
                item.setAttribute('data-chord-index', chord.chordIndex);
                item.setAttribute('data-edo', edo);
                historyList.appendChild(item);
            }});

            // Add delete handlers
            document.querySelectorAll('.chord-history-delete').forEach(deleteBtn => {{
                deleteBtn.addEventListener('click', function(e) {{
                    e.stopPropagation();
                    const index = parseInt(this.getAttribute('data-index'));
                    chordHistory.splice(index, 1);
                    updateHistoryDisplay();
                }});
            }});

            // Add click handlers to replay chord and highlight on grid
            document.querySelectorAll('.chord-history-item').forEach(item => {{
                item.addEventListener('click', function(e) {{
                    // Don't trigger if clicking the delete button
                    if (e.target.classList.contains('chord-history-delete')) {{
                        return;
                    }}

                    const intervalsStr = this.getAttribute('data-intervals');
                    const edo = parseInt(this.getAttribute('data-edo'));
                    const intervals = intervalsStr.split(',').map(x => parseInt(x));
                    const root = this.getAttribute('data-root');
                    const chordIndex = this.getAttribute('data-chord-index');

                    // Resume audio context if needed
                    if (audioContext.state === 'suspended') {{
                        audioContext.resume();
                    }}

                    // Play the chord
                    playChord(intervals, edo);

                    // Highlight the chord on the grid
                    const gridChord = document.querySelector(`.func.clickable[data-root="${{root}}"][data-chord-index="${{chordIndex}}"]`);
                    if (gridChord) {{
                        // Add playing animation
                        gridChord.classList.add('playing');

                        // Remove after animation completes (0.6s * 3 = 1.8s)
                        setTimeout(() => {{
                            gridChord.classList.remove('playing');
                        }}, 1800);
                    }}
                }});
            }});
        }}

        // Add click handlers to all chord buttons
        document.querySelectorAll('.func.clickable').forEach(element => {{
            element.addEventListener('click', function(e) {{
                e.stopPropagation(); // Prevent row highlight when clicking chord
                const intervalsStr = this.getAttribute('data-intervals');
                const edo = parseInt(this.getAttribute('data-edo'));
                const intervals = intervalsStr.split(',').map(x => parseInt(x));
                const root = this.getAttribute('data-root');
                const chordIndex = this.getAttribute('data-chord-index');

                // Resume audio context if needed (browser security requirement)
                if (audioContext.state === 'suspended') {{
                    audioContext.resume();
                }}

                playChord(intervals, edo);
                addToHistory(root, chordIndex, intervals);
            }});
        }});

        // Undo stack for deleted rows and columns
        const undoStack = [];

        // Column collapse/expand functionality
        const headerCells = document.querySelectorAll('th:not(:first-child):not(:nth-child(2))'); // Skip delete column and root column
        headerCells.forEach((th, index) => {{
            th.addEventListener('click', function() {{
                const columnIndex = index + 2; // +2 because we skip delete column and root column
                const wasCollapsed = this.classList.contains('collapsed');

                // Save state for undo BEFORE making changes
                undoStack.push({{
                    type: 'column',
                    index: columnIndex,
                    isCollapsed: wasCollapsed,
                    header: this
                }});

                const isCollapsed = this.classList.toggle('collapsed');

                // Toggle all cells in this column
                document.querySelectorAll(`tr`).forEach(row => {{
                    const cell = row.cells[columnIndex];
                    if (cell) {{
                        cell.classList.toggle('hidden', isCollapsed);
                    }}
                }});
            }});
        }});

        // Row highlighting functionality (click on root label)
        const rows = document.querySelectorAll('tbody tr');
        rows.forEach(row => {{
            const rootCell = row.cells[1]; // Second cell is the root label
            if (rootCell) {{
                rootCell.addEventListener('click', function(e) {{
                    e.stopPropagation();
                    row.classList.toggle('highlighted');
                }});
            }}
        }});

        // Row deletion functionality (click on delete cell)
        rows.forEach(row => {{
            const deleteCell = row.cells[0]; // First cell is the delete button
            if (deleteCell && deleteCell.classList.contains('delete-cell')) {{
                deleteCell.addEventListener('click', function(e) {{
                    e.stopPropagation();

                    // Save state for undo
                    undoStack.push({{
                        type: 'row',
                        row: row,
                        parent: row.parentNode,
                        nextSibling: row.nextSibling
                    }});

                    // Remove the row
                    row.style.display = 'none';
                }});
            }}
        }});

        // Undo functionality (Ctrl+Z)
        document.addEventListener('keydown', function(e) {{
            if ((e.ctrlKey || e.metaKey) && e.key === 'z') {{
                e.preventDefault();

                if (undoStack.length > 0) {{
                    const action = undoStack.pop();

                    if (action.type === 'row') {{
                        // Restore deleted row
                        action.row.style.display = '';
                    }} else if (action.type === 'column') {{
                        // Restore column to saved state
                        action.header.classList.toggle('collapsed', action.isCollapsed);

                        // Restore all cells in this column to saved state
                        document.querySelectorAll(`tr`).forEach(row => {{
                            const cell = row.cells[action.index];
                            if (cell) {{
                                cell.classList.toggle('hidden', action.isCollapsed);
                            }}
                        }});
                    }}
                }}
            }}
        }});

        // MIDI file generation
        function generateMIDI() {{
            if (chordHistory.length === 0) {{
                alert('No chords in history!');
                return;
            }}

            const edo = parseInt(document.querySelector('.func.clickable').getAttribute('data-edo'));

            // MIDI file structure helpers
            function writeVarLen(value) {{
                let buffer = [];
                buffer.push(value & 0x7F);
                while (value >>= 7) {{
                    buffer.unshift((value & 0x7F) | 0x80);
                }}
                return buffer;
            }}

            function writeString(str) {{
                return Array.from(str).map(c => c.charCodeAt(0));
            }}

            function write32Bit(value) {{
                return [
                    (value >> 24) & 0xFF,
                    (value >> 16) & 0xFF,
                    (value >> 8) & 0xFF,
                    value & 0xFF
                ];
            }}

            function write16Bit(value) {{
                return [(value >> 8) & 0xFF, value & 0xFF];
            }}

            // MIDI parameters
            const ticksPerQuarterNote = 480;
            const wholeNoteTicks = ticksPerQuarterNote * 4; // 4 quarter notes = 1 whole note
            const velocity = 80;

            // Build MIDI events (reverse history to play in order from oldest to newest)
            let midiEvents = [];
            let currentTime = 0;

            [...chordHistory].reverse().forEach((chord, chordIndex) => {{
                // For each note in the chord
                chord.intervals.forEach(interval => {{
                    // Simple conversion: EDO step number = MIDI note number
                    // Start at C3 (MIDI 48) and add the interval directly
                    // Also add the root offset for transposition
                    const midiNote = 48 + interval + currentRootOffset;

                    // Clamp to valid MIDI range (0-127)
                    const clampedNote = Math.max(0, Math.min(127, midiNote));

                    // Note On event
                    midiEvents.push({{
                        time: currentTime,
                        type: 'noteOn',
                        note: clampedNote,
                        velocity: velocity
                    }});

                    // Note Off event (after 1 whole note)
                    midiEvents.push({{
                        time: currentTime + wholeNoteTicks,
                        type: 'noteOff',
                        note: clampedNote,
                        velocity: 0
                    }});
                }});

                // Move to next chord (1 whole note later)
                currentTime += wholeNoteTicks;
            }});

            // Sort events by time
            midiEvents.sort((a, b) => a.time - b.time);

            // Convert to MIDI track format
            let trackData = [];
            let lastTime = 0;

            midiEvents.forEach(event => {{
                // Delta time
                const deltaTime = event.time - lastTime;
                trackData.push(...writeVarLen(deltaTime));

                // Event data
                if (event.type === 'noteOn') {{
                    trackData.push(0x90, event.note, event.velocity); // Note On, channel 0
                }} else if (event.type === 'noteOff') {{
                    trackData.push(0x80, event.note, event.velocity); // Note Off, channel 0
                }}

                lastTime = event.time;
            }});

            // End of track
            trackData.push(0x00, 0xFF, 0x2F, 0x00);

            // Build MIDI file
            let midiFile = [];

            // Header chunk
            midiFile.push(...writeString('MThd'));
            midiFile.push(...write32Bit(6)); // Header length
            midiFile.push(...write16Bit(0)); // Format 0
            midiFile.push(...write16Bit(1)); // 1 track
            midiFile.push(...write16Bit(ticksPerQuarterNote));

            // Track chunk
            midiFile.push(...writeString('MTrk'));
            midiFile.push(...write32Bit(trackData.length));
            midiFile.push(...trackData);

            // Create blob and download
            const blob = new Blob([new Uint8Array(midiFile)], {{ type: 'audio/midi' }});
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = 'chord_history.mid';
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
            URL.revokeObjectURL(url);
        }}

        // Download MIDI button handler
        document.getElementById('downloadMidiBtn').addEventListener('click', generateMIDI);
    </script>
</body>
</html>'''

    if filename:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(html)
        print(f"HTML table saved to {filename}")

    return html


def generate_interval_quality_list(edo: int) -> List[str]:
    """
    Generate an interval quality list for a given EDO based on cent ranges.

    Rules:
    - 0 cents (root): 's' (stable)
    - 0-160c: 'o' (odd/dissonant)
    - 160-255c: 'u' (unstable)
    - 255-445c: 'm' (modal)
    - 445-560c: 'u' (unstable)
    - 560-665c: 'o' (odd/dissonant)
    - 665-735c: 's' (stable)
    - 735-850c: 'l' (leading)
    - 850-1040c: 'h' (hollow)
    - 1040-1200c: 'l' (leading)

    Args:
        edo: The equal division of the octave

    Returns:
        List of quality strings, one for each step of the EDO
    """
    cent_per_step = 1200.0 / edo
    qualities = []

    for step in range(edo):
        cents = step * cent_per_step

        if step == 0:
            quality = 's'
        elif 0 < cents < 160:
            quality = 'o'
        elif 160 <= cents < 255:
            quality = 'u'
        elif 255 <= cents < 445:
            quality = 'm'
        elif 445 <= cents < 560:
            quality = 'u'
        elif 560 <= cents < 665:
            quality = 'o'
        elif 665 <= cents < 735:
            quality = 's'
        elif 735 <= cents < 850:
            quality = 'l'
        elif 850 <= cents < 1040:
            quality = 'h'
        elif 1040 <= cents < 1200:
            quality = 'l'
        else:  # Should not happen for valid EDO
            quality = 's'

        qualities.append(quality)

    return qualities


def print_interval_quality_list(edo: int):
    """
    Generate and print an interval quality list for a given EDO in a format
    that can be added to edo_data.md.

    Args:
        edo: The equal division of the octave
    """
    qualities = generate_interval_quality_list(edo)
    cent_per_step = 1200.0 / edo

    print(f"\n## EDO {edo}")
    print(f"**Current Note Names**: default")
    print(f"\n### Interval Quality List")
    print("```")
    print(", ".join(qualities))
    print("```")

    # Print detailed breakdown showing cents for each interval
    print(f"\n### Interval Quality Breakdown (for reference)")
    print("```")
    for step, quality in enumerate(qualities):
        cents = step * cent_per_step
        quality_name = {
            's': 'stable',
            'o': 'odd',
            'u': 'unstable',
            'm': 'modal',
            'l': 'leading',
            'h': 'hollow'
        }[quality]
        print(f"{step:3d}: {cents:7.2f}¢ -> {quality} ({quality_name})")
    print("```")


def sort_chord_intervals_by_fifth_then_third(chord_lines: List[str]) -> List[str]:
    """
    Sort chord interval lines by fifth (third number) then by third (second number).

    Takes lines in format: "0, 7, 15   # Comment" and sorts them so that:
    1. Chords are grouped by the fifth (third number in the tuple)
    2. Within each fifth group, sorted by the third (second number in the tuple)

    Args:
        chord_lines: List of chord interval lines from edo_data.md

    Returns:
        Sorted list of chord interval lines
    """
    import re

    # Parse each line to extract intervals and comment
    parsed_chords = []
    for line in chord_lines:
        line = line.strip()
        if not line or line.startswith('#'):
            continue

        # Extract the interval numbers and comment
        match = re.match(r'(\d+),\s*(\d+),\s*(\d+)\s*(#.*)?', line)
        if match:
            root = int(match.group(1))
            third = int(match.group(2))
            fifth = int(match.group(3))
            comment = match.group(4) if match.group(4) else ''
            parsed_chords.append((root, third, fifth, comment.strip(), line))

    # Sort by fifth (index 2), then by third (index 1)
    sorted_chords = sorted(parsed_chords, key=lambda x: (x[2], x[1]))

    # Reconstruct the lines
    result = []
    for root, third, fifth, comment, original_line in sorted_chords:
        # Format consistently
        if comment:
            result.append(f"{root}, {third}, {fifth}   {comment}")
        else:
            result.append(f"{root}, {third}, {fifth}")

    return result


def print_sorted_chord_intervals(chord_lines: List[str]):
    """
    Print sorted chord intervals for easy copy-paste into edo_data.md.

    Args:
        chord_lines: List of chord interval lines from edo_data.md
    """
    sorted_lines = sort_chord_intervals_by_fifth_then_third(chord_lines)
    print("### Chord Intervals")
    print("```")
    for line in sorted_lines:
        print(line)
    print("```")


def generate_all_triads(edo: int, qualities: List[str] = None) -> List[Tuple[int, int, int]]:
    """
    Generate all possible triads from available thirds in an EDO.

    A triad consists of: root (0), third (modal interval), fifth (two stacked thirds).
    This function finds all intervals marked as 'm' (modal/thirds) and generates
    all permutations where the fifth is the sum of two thirds (which may be different).

    For example, with thirds [7, 8, 9, 10, 11], it generates:
    - (0, 7, 14)  # third=7, fifth=7+7
    - (0, 7, 15)  # third=7, fifth=7+8
    - (0, 7, 16)  # third=7, fifth=7+9
    - etc.

    Args:
        edo: The equal division of the octave
        qualities: Optional list of interval qualities. If None, generates from edo.

    Returns:
        List of triad tuples (0, third, fifth), sorted by fifth then third
    """
    if qualities is None:
        qualities = generate_interval_quality_list(edo)

    # Find all thirds (modal intervals)
    thirds = [i for i, q in enumerate(qualities) if q == 'm' and i > 0]

    # Generate all triads by stacking two thirds
    triads = []
    for third1 in thirds:
        for third2 in thirds:
            fifth = (third1 + third2) % edo
            # Create triad: root (0), third (third1), fifth (sum of two thirds)
            triads.append((0, third1, fifth))

    # Sort by fifth, then by third
    triads.sort(key=lambda x: (x[2], x[1]))

    return triads


def print_generated_triads(edo: int, qualities: List[str] = None):
    """
    Generate and print all possible triads for an EDO system.

    Args:
        edo: The equal division of the octave
        qualities: Optional list of interval qualities. If None, generates from edo.
    """
    if qualities is None:
        qualities = generate_interval_quality_list(edo)

    triads = generate_all_triads(edo, qualities)
    cent_per_step = 1200.0 / edo

    # Find the thirds used
    thirds = sorted(set(t[1] for t in triads))
    unique_triads = []
    seen = set()
    for triad in triads:
        if triad not in seen:
            unique_triads.append(triad)
            seen.add(triad)

    print(f"\n### Generated Triads for {edo}-EDO")
    print(f"Found {len(unique_triads)} unique triads ({len(thirds)} thirds × {len(thirds)} thirds = {len(thirds)**2} permutations)\n")

    print(f"Thirds (modal 'm' intervals): {thirds}")
    print(f"  Cents: {[f'{t * cent_per_step:.1f}¢' for t in thirds]}")

    print(f"\n### Chord Intervals")
    print("```")
    for root, third1, fifth in unique_triads:
        third1_cents = third1 * cent_per_step
        fifth_cents = fifth * cent_per_step

        # Find which two thirds make up this fifth
        thirds_list = [i for i, q in enumerate(qualities) if q == 'm' and i > 0]
        third2 = None
        for t2 in thirds_list:
            if (third1 + t2) % edo == fifth:
                third2 = t2
                break

        if third2 is not None:
            print(f"{root}, {third1}, {fifth}   # {third1_cents:.1f}¢ + {third2 * cent_per_step:.1f}¢ = {fifth_cents:.1f}¢")
        else:
            print(f"{root}, {third1}, {fifth}   # {third1_cents:.1f}¢ + ? = {fifth_cents:.1f}¢")
    print("```")


def run_22edo_tests():
    """Run test cases for 22-EDO."""
    print("=" * 110)
    print("FUNCTIONAL HARMONY CLASSIFIER - 22-EDO TEST SUITE")
    print("=" * 110)

    print("\n--- ALL TRIADS (all chord types from root 0) ---")
    run_test_suite([
        ("Subdiminished",               {0, 5, 10},  None),
        ("Subminor up-flat five",       {0, 5, 11},  None),
        ("Diminished",                  {0, 6, 11},  None),
        ("Subminor down five",          {0, 5, 12},  None),
        ("Minor down five",             {0, 6, 12},  None),
        ("Down-five",                   {0, 7, 12},  None),
        ("Subminor",                    {0, 5, 13},  None),
        ("Minor",                       {0, 6, 13},  None),
        ("Major",                       {0, 7, 13},  None),
        ("Supermajor",                  {0, 8, 13},  None),
        ("Minor up five",               {0, 6, 14},  None),
        ("Augmented",                   {0, 7, 14},  None),
        ("Supermajor up five",          {0, 8, 14},  None),
        ("Down-sharp five",             {0, 7, 15},  None),
        ("Supermajor down-sharp five",  {0, 8, 15},  None),
        ("Supermajor sharp five",       {0, 8, 16},  None),
    ], EDO_22)


if __name__ == "__main__":
    # Choose which system to test
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == "--generate-html":
        # Generate HTML tables for all EDO systems
        print("Generating HTML tables from edo_data.md...")
        edo_systems = parse_edo_data_file('edo_data.md')
        for edo_num, system in sorted(edo_systems.items()):
            filename = f'{edo_num}edo_table.html'
            generate_html_table(system, filename)
        print("\nAll HTML tables generated successfully!")
    elif len(sys.argv) > 1 and sys.argv[1] == "22":
        # Run 22-EDO tests
        run_22edo_tests()
        print("\n\n")
        print_triad_table(EDO_22)
    elif len(sys.argv) > 1 and sys.argv[1] == "23":
        # Run 23-EDO tests
        print("=" * 110)
        print("FUNCTIONAL HARMONY CLASSIFIER - 23-EDO")
        print("=" * 110)
        print_triad_table(EDO_23)
    else:
        # Run 12-EDO tests (default)
        run_tests()
        print("\n\n")
        print_triad_table()
