def create_scale(root_note: str, scale_type: str = "major") -> list[str]:
    # Map out pitch semitones from C (C=0, C#/Db=1, D=2 ... B=11)
    pitch_map = {
        'C': 0, 'B#': 0, 'C#': 1, 'Db': 1, 'D': 2, 'D#': 3, 'Eb': 3, 
        'E': 4, 'Fb': 4, 'F': 5, 'E#': 5, 'F#': 6, 'Gb': 6, 'G': 7, 
        'G#': 8, 'Ab': 8, 'A': 9, 'A#': 10, 'Bb': 10, 'B': 11, 'Cb': 11
    }
    
    # 7 core musical letter names in standard sequential order
    letters = ['C', 'D', 'E', 'F', 'G', 'A', 'B']
    
    # Diatonic interval steps (2 = whole step, 1 = half step)
    patterns = {
        "major": [2, 2, 1, 2, 2, 2, 1],
        "minor": [2, 1, 2, 2, 1, 2, 2]
    }
    
    # Normalize text inputs (e.g., 'fb' -> 'Fb', 'major' -> 'major')
    root = root_note.strip().capitalize()
    scale_type = scale_type.strip().lower()
    
    if root not in pitch_map:
        raise ValueError(f"Unsupported root note: {root_note}")
    if scale_type not in patterns:
        raise ValueError(f"Unsupported scale type: {scale_type}")
        
    # 1. Determine target pitch values for the scale degrees
    current_pitch = pitch_map[root]
    target_pitches = [current_pitch]
    for step in patterns[scale_type]:
        current_pitch = (current_pitch + step) % 12
        target_pitches.append(current_pitch)
        
    # 2. Get the correct 8-letter sequence starting on the root letter
    root_letter = root[0]
    start_letter_idx = letters.index(root_letter)
    scale_letters = [letters[(start_letter_idx + i) % 7] for i in range(8)]
    
    # 3. Spell the notes by modifying the base letters with sharps/flats
    scale = []
    for letter, target in zip(scale_letters, target_pitches):
        base_pitch = pitch_map[letter]
        
        # Calculate semitone distance from the raw base letter to the target pitch
        diff = (target - base_pitch) % 12
        if diff > 5:  # If difference is too large forward, look backward (flats)
            diff -= 12
            
        if diff == 0:
            accidental = ""
        elif diff > 0:
            accidental = "#" * diff
        else:
            accidental = "b" * abs(diff)
            
        scale.append(f"{letter}{accidental}")
        
    return scale

# --- Example Usage ---
print("C Major:", create_scale("C", "major"))
# Outputs: ['C', 'D', 'E', 'F', 'G', 'A', 'B', 'C']

print("A Minor:", create_scale("A", "minor"))
# Outputs: ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'A']

print("D Major:", create_scale("D", "major"))
# Outputs ['D', 'E', 'F#', 'G', 'A', 'B', 'C#', 'D']

print("Fb Minor:", create_scale("Fb", "minor"))
# Outputs ['Fb', 'Gb', 'Abb', 'Bbb', 'Cb', 'Dbb', 'Ebb', 'Fb']
