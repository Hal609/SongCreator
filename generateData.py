import src

choice = input("What type of data do you want to create ?\n    1. NMultiInstSpectrograms\n    2. SplitTrackSpectrograms\n")
if choice == "1":
   src.createNMultiInstSpectrograms(5000, keepWAVs=False)
elif choice == "2":
   src.createSplitTrackSpectrograms(5000, keepWAVs=False)
else:
   print("Selection not recognised.")