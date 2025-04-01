from .noteClass import Note
import random

def createBass(progression):
    bassNotes = []
    for note in progression:
        for i in range(8):
            if random.random() < 0.7:
                bassNotes.append(Note(note) - 12)
            else:
                bassNotes.append(Note(note) - 12 + 5)
    
    return bassNotes