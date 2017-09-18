#!/usr/bin/python
from collections import OrderedDict
import sys

class ReadBP():
  def __color(self, color):
    if 'bp' not in sys.modules:
      if color == "bold":
        output = "\033[1m"
      elif color == "green":
        output = "\033[32m"
      elif color == "cyan":
        output = "\033[36m"
      elif color == "yellow":
        output = "\033[33m"
      elif color == "magenta":
        output = "\033[35m"
      elif color == "reset":
        output = "\033[0m"
      else:
        output = ""
    else:
      output = ""

    return output

  def __chunk_bp(self, bp, length, label=""):
    global chunk
    global master_output
    global max_label_length
    chunk = bp[:length]
    bp    = bp[length:]
    if label != "":
      master_output = master_output + [(label, chunk)]
      label = label.ljust(max_label_length, ".")
      label += " : "
    print(label + self.__color("green") + chunk + self.__color("reset"))
    return bp

  def __security_data(self, data, offset=1, marker="^"):
    global master_output
    global max_label_length
    print("\n" + self.__color("bold") + "*** Security information:" + self.__color("reset"))
    print("Beginning of security data".ljust(max_label_length, ".") + " : " + self.__color("green") + marker + self.__color("reset"))
    master_output = master_output + [("Beginning of security data", marker)]
    print("Type of security data".ljust(max_label_length, ".") + " : " + self.__color("green") + data[offset] + self.__color("reset"))
    master_output = master_output + [("Type of security data", data[offset])]
    print("Length of security data".ljust(max_label_length, ".") + " : " + self.__color("green") + data[(offset+1):][:2] + self.__color("reset"))
    master_output = master_output + [("Length of security data", data[(offset+1):][:2])]
    print("Security data (encrypted)".ljust(max_label_length, ".") + " : " + self.__color("cyan") + data[(offset+3):] + self.__color("reset"))
    master_output = master_output + [("Security data (encrypted)", data[(offset+3):])]

  def run(self, bp=None):
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

    global max_label_length
    max_label_length = len(max(mandatory_data_lengths.keys(), key=len))

    global master_output
    master_output = []

    if bp:
      bp = bp.replace(" ", "_")
    else:
      bp = raw_input().replace(" ", "_")

    print("\n" + self.__color("bold") + "*** Mandatory information:" + self.__color("reset"))
    for label, length in mandatory_data_lengths.iteritems():
      bp = self.__chunk_bp(bp, length, label)

    # Variable-length information
    size_label = "Section length (hexadecimal)"
    max_label_length = len(size_label)
    bp_at_variable = bp
    print("\n" + self.__color("bold") + "*** Additional per-segment information:" + self.__color("reset"))
    # delta = (sys.argv[1].lower() in ["delta", "dl", "dal"])
    while len(bp) > 0:
      try:
        if bp[0] == ">":
          print("Version number marker".ljust(max_label_length, ".") + " : " + self.__color("green") + ">" + self.__color("reset"))
          master_output = master_output + [("Version number marker", ">")]
          print("Version number".ljust(max_label_length, ".") + " : " + self.__color("green") + bp[1] + self.__color("reset"))
          master_output = master_output + [("Version number", bp[1])]
          bp = bp[2:]
        if bp[0] == "^":
          self.__security_data(bp)
          break
        else:
          bp = self.__chunk_bp(bp, 2, size_label)
          variable_length = int(chunk, 16)
          bp = self.__chunk_bp(bp, variable_length, "Contents")
      except:
        if "^" in bp:
          end_of_bp = bp.split("^")
          print(self.__color("yellow") + "Remaining data (unparsed)".ljust(max_label_length, ".") + " : " + self.__color("magenta") + end_of_bp[0] + self.__color("reset"))
          master_output = master_output + [("Remaining data (unparsed)", end_of_bp[0])]
          print(self.__color("yellow") + "All variable data (unparsed)".ljust(max_label_length, ".") + " : " + self.__color("magenta") + bp_at_variable.split("^")[0] + self.__color("reset"))
          master_output = master_output + [("All variable data (unparsed)", bp_at_variable.split("^")[0])]
          self.__security_data(end_of_bp[1], offset=0)
        elif ">" in bp:
          bp_sections = bp.split(">")
          i = 1
          for section in bp_sections:
            last_section = section
            if i < len(bp_sections):
              print(self.__color("yellow") + "Unparsed section".ljust(max_label_length, ".") + " : " + self.__color("magenta") + section + self.__color("reset"))
              master_output = master_output + [("Unparsed section", section)]
              i += 1
            else:
              self.__security_data(last_section, offset=0, marker=">")
        else:
          print(self.__color("yellow") + "Remaining data (unparsed)".ljust(max_label_length, ".") + " : " + self.__color("magenta") + bp + self.__color("reset"))
          master_output = master_output + [("Remaining data (unparsed)", bp)]
          print(self.__color("yellow") + "All variable data (unparsed)".ljust(max_label_length, ".") + " : " + self.__color("magenta") + bp_at_variable + self.__color("reset"))
          master_output = master_output + [("All variable data (unparsed)", bp_at_variable)]
        break

    return master_output

if __name__ == "__main__":
  ReadBP().run()
