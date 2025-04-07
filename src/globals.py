numeralDict = {"I": 1, "II": 2, "III": 3, "IV": 4, "V": 5, "VI": 6, "VII": 7,
               "i": 1, "ii": 2, "iii": 3, "iv": 4, "v": 5, "vi": 6, "vii": 7}

majorKeyIntervals = [2, 2, 1, 2, 2, 2, 1]
minorKeyIntervals = [2, 1, 2, 2, 1, 2, 2]
bluesKeyIntervals = [2, 1, 2, 1, 1, 2, 1, 1]

instruments = ["piano", "bass", "drums", "guitar", "synth"]
instrument_dict = {"piano": 0, "bass": 1, "drums": 2, "guitar": 3, "synth": 4}

voices = {
   "piano": [
      "Studio Grand",
      "Silver Age",
      "Steinway",
      "Songwriter",
      "Squeeze Pop"],
   "drums": [
      "Beat Machine",
      "Modern Chiptune",
      "Compact",
      "Grimey Funk",
      "Detroit Garage",
      "SoCal",
      "Dembow",
      "Sunset",
      "Lo-Fi Hype",
      "Heavy",
      "Retro Rock",
      "Brooklyn",
      "808",
      "Modern Disco",
      "Modern TR-707",
      "Manchester",
      "Autumn Leaves",
      "Liverpool",
      "Electronic Pop"],
   "guitar": [
      "British Stack Synth Lead",
      "Classic Clean",
      "Hard Rock",
      "Tweed Picked Synth",
      "Classical Acoustic Guitar",
      "Acoustic Guitar",
      "British Combo Synth Lead",
      "Roots Rock",
      "Steel String Acoustic",
      "Amped Synth Lead"],
   "bass": [
      "Warm & Clear",
      "Fuzzy",
      "Club Ambience Upright",
      "Roots Upright",
      "Crunchy Vintage",
      "Dancefloor"],
   "synth": [
         "Smooth Analog Lead",
         "Soft Square Lead",
         "Searing Lead",
         "Classic Pad"]
}

parts_can_add = {
    "piano": ["chords", "melody", "bass"],
    "guitar": ["chords", "melody"],
    "bass": ["bass"],
    "drums": ["drums"],
    "synth": ["chords", "melody", "bass"]
}