keyNumDict = {"C": 4, "D": 6, "E": 8, "F": 9, "G": 11, "A": 13, "B": 15}
reverseKeyNumDict = {4: "C", 6: "D", 8: "E", 9: "F", 11: "G", 13: "A", 15: "B"}

class Note:
    def __init__(self, note: str):
        self.note = note

    def __str__(self) -> str:
        return str(self.note)

    def __add__(self, other):
        newNum = self.get_key_number() + other
        newNote = Note("A4")
        newNote.set_key_number(newNum)
        return newNote
    
    def set_key_number(self, new_key_number):
        global reverseKeyNumDict
        octave = (new_key_number + 8) // 12
        noteRelative = (new_key_number - 4) % 12
        noteRelative += 4
        note = reverseKeyNumDict.get(noteRelative)
        if note is None:
            note = reverseKeyNumDict.get(noteRelative - 1) + "#"
        self.note = note + str(octave)

    def get_key_number(self):
        global keyNumDict
        octave = int(self.note[-1]) - 1
        noteNum = keyNumDict[self.note[0]]
        if self.note[1] == "#":
            noteNum += 1
        elif self.note[1] == "b":
            noteNum -= 1
        return noteNum + (octave * 12)

    def get_frequency(self):
        n = self.get_key_number()
        return 2**((n-49)/12) * 440
