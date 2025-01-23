import random as rand
import numpy as np

tracks = [
    [1, 0, 2, 0, 1, 0, 2, 0, 1, 0, 2, 0, 1, 0, 2, 0, 1, 0, 2, 2, 0, 0, 2, 0],
    [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
]

def hihat(length):
    track = []
    for j in range(8):
        if j % 2 == 0:
            probHit = 0.90
        else:
            probHit = 0.85

        if rand.random() < probHit:
            track.append(3)
        else:
            track.append(0)
    return track * (length // len(track))

def snare(length):
    track = []
    for j in range(8):
        if (j-2) % 4 == 0:
            probHit = 0.90
        else:
            probHit = 0.10
        
        if len(track) > 1:
            probDouble = 0.2
            if track[-1] == 2 and track[-2] != 2 and rand.random() < probDouble:
                track.append(2)
                continue
        if rand.random() < probHit:
            track.append(2)
            continue
        
        track.append(0)
    return track * (length // len(track))

def kick(length):
    track = []
    for j in range(8):
        if j % 4 == 0:
            probHit = 0.90
        else:
            probHit = 0.10
        
        if len(track) > 1:
            probDouble = 0.2
            if track[-1] == 1 and track[-2] != 1 and rand.random() < probDouble:
                track.append(1)
                continue
        if rand.random() < probHit:
            track.append(1)
            continue
        
        track.append(0)
    return track * (length // len(track))

def createTrack(length):
    allTracks = []
    allTracks.append(hihat(length))
    allTracks.append(snare(length))
    allTracks.append(kick(length))
    return allTracks