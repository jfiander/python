#!/usr/bin/python
from collections import OrderedDict
import sys

mandatory_data_lengths = OrderedDict(
  [
    ("Format code", 1),
    ("Number of legs", 1),
    ("Passenger name", 20),
    ("Electronic ticket indicator", 1),
    ("Operating carrier PNR code", 7),
    ("Departure airport (IATA)", 3),
    ("Arrival airport (IATA)", 3),
    ("Operating carrier designator", 3),
    ("Flight number", 5),
    ("Date of flight (Julian)", 3),
    ("Cabin / fare class code", 1),
    ("Seat number", 4),
    ("Check-in sequence number", 5),
    ("Passenger status", 1),
    ("Section length (hexadecimal)", 2)
  ]
)

max_label_length = len(max(mandatory_data_lengths.keys(), key=len))

def chunk_bp(bp, length, label=""):
  global chunk
  chunk = bp[:length]
  bp    = bp[length:]
  if label != "":
    label = label.ljust(max_label_length, ".")
    label += " : "
  print(label + "\033[32m" + chunk + "\033[0m")
  return bp

def security_data(data, offset=1, marker="^"):
  print("\n\033[1m*** Security information:\033[0m")
  print("Beginning of security data".ljust(max_label_length, ".") + " : \033[32m" + marker + "\033[0m")
  print("Type of security data".ljust(max_label_length, ".") + " : \033[32m" + data[offset] + "\033[0m")
  print("Length of security data".ljust(max_label_length, ".") + " : \033[32m" + data[(offset+1):][:2] + "\033[0m")
  print("Security data (encrypted)".ljust(max_label_length, ".") + " : \033[36m" + data[(offset+3):] + "\033[0m")

bp = raw_input().replace(" ", "_")

print("\n\033[1m*** Mandatory information:\033[0m")
for label, length in mandatory_data_lengths.iteritems():
  bp = chunk_bp(bp, length, label)

# Variable-length information
size_label = "Section length (hexadecimal)"
max_label_length = len(size_label)
bp_at_variable = bp
print("\n\033[1m*** Additional per-segment information:\033[0m")
while len(bp) > 0:
  try:
    if bp[0] == ">":
      print("Version number marker".ljust(max_label_length, ".") + " : \033[32m>\033[0m")
      print("Version number".ljust(max_label_length, ".") + " : \033[32m" + bp[1] + "\033[0m")
      bp = bp[2:]
    if bp[0] == "^":
      security_data(bp)
      break
    else:
      bp = chunk_bp(bp, 2, size_label)
      variable_length = int(chunk, 16)
      bp = chunk_bp(bp, variable_length, "Contents")
  except:
    if "^" in bp:
      end_of_bp = bp.split("^")
      print("\033[33m" + "Remaining data (unparsed)".ljust(max_label_length, ".") + "\033[0m" + " : \033[35m" + end_of_bp[0] + "\033[0m")
      print("\033[33m" + "All variable data (unparsed)".ljust(max_label_length, ".") + "\033[0m" + " : \033[31m" + bp_at_variable.split("^")[0] + "\033[0m")
      security_data(end_of_bp[1], offset=0)
    elif ">" in bp:
      bp_sections = bp.split(">")
      i = 1
      for section in bp_sections:
        last_section = section
        if i < len(bp_sections):
          print("\033[33m" + "Unparsed section".ljust(max_label_length, ".") + "\033[0m" + " : \033[35m" + section + "\033[0m")
          i += 1
        else:
          security_data(last_section, offset=0, marker=">")
    else:
      print("\033[33m" + "Remaining data (unparsed)".ljust(max_label_length, ".") + "\033[0m" + " : \033[35m" + bp + "\033[0m")
      print(bp_at_variable)
    break
