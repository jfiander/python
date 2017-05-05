#!/usr/bin/python
# bp = "M1GRUDE/AMY LYNN      EGG3JLU DTWSFODL 0545 257F001B0001 155>318        DL              2900623680638273    DL 2673181224          DL00187JJU001B>14cMDUCGQDi+hg3tbInPSugRlEH1iHSMZuk67xvRTgCGDk8pcCeJ+hZNcOmmkPvlEUulYArLdAuNQ=="
bp = raw_input()

print("")

mandatory_data_lengths = [1, 1, 20, 1, 7, 3, 3, 3, 5, 3, 1, 4, 5, 1, 2]
optional_data_lengths  = [1, 1, 2]

get_length = 0

def chunk_bp(bp, length):
  global chunk
  chunk = bp[:length]
  bp    = bp[length:]
  print(chunk.replace(" ", "_"))
  return bp

print("\n*** Mandatory information:")
for length in mandatory_data_lengths:
  bp = chunk_bp(bp, length)

print("\n*** Additional per-segment and security information:")
# Initial version and length finding information
for length in optional_data_lengths:
  bp = chunk_bp(bp, length)

# Length-specifying information
while len(bp) > 0:
  try:
    next_length = int(chunk, 16)
    bp = chunk_bp(bp, next_length)
    bp = chunk_bp(bp, 2)
  except:
    print(bp.replace(" ", "_"))
    break
