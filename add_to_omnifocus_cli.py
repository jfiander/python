#!/usr/bin/python
#coding: utf-8
"""
Taskpaper to Omnifocus pre-processor (command line interface)

This script processes a Taskpaper document to detect and fill in specified placeholders, and evaluate mathematical expressions, prior to generating an Omnifocus URL for project creation.

This script is an expanded version of the one provided by Ken Case from the Omni Group as part of an Editorial workflow.

** This version has been modified to run on the command line.
     usage: ./add_to_omnifocus_cli.py path/to/template.Taskpaper

Placeholders:
  All text contained in «guillemets» or <<double greater-than-less-thans>> will be detected as a placeholder. The script will present a dialog form with all detected placeholders.
  All instances of the same placeholder will be replaced by the provided value.

Mathematical expressions:
  All text contained in [[double square brackets]] will be mathematically evaluated.
"""
import re, ast, sys, urllib
import operator as op
from datetime import datetime

### Helper methods

# Supported operators
operators = {ast.Add: op.add, ast.Sub: op.sub, ast.Mult: op.mul,
             ast.Div: op.truediv, ast.Pow: op.pow, ast.BitXor: op.xor,
             ast.USub: op.neg}

def eval_(node):
    if isinstance(node, ast.Num): # <number>
        return node.n
    elif isinstance(node, ast.BinOp): # <left> <operator> <right>
        return operators[type(node.op)](eval_(node.left), eval_(node.right))
    elif isinstance(node, ast.UnaryOp): # <operator> <operand> e.g., -1
        return operators[type(node.op)](eval_(node.operand))
    else:
        raise TypeError(node)

def eval_expr(expr):
    """
    >>> eval_expr('2^6')
    4
    >>> eval_expr('2**6')
    64
    >>> eval_expr('1 + 2*3**(4^5) / (6 + -7)')
    -5.0
    """
    return eval_(ast.parse(expr, mode='eval').body)

def clean_match_math(match):
  """Removes (all) double square bracket wrappers from a match string"""
  return str(match).replace("[[", "").replace("]]", "")

def clean_match_py(match):
  """Removes (all) double pipe wrappers from a match string"""
  return str(match).replace("||", "")

### Prepare for OmniFocus

def url_escape(text):
  """Escapes document text to URL encoding, using % notation for spaces rather than the query string default (+)."""
  return urllib.quote_plus(text).replace("+", "%20")

def omnifocus_url(escaped_text):
  """Adds the Omnifocus paste URL prefix to escaped document text."""
  return "omnifocus://x-callback-url/paste?target=inbox&content=" + escaped_text


### Template parsing

def parse_template(document):
  """Loads template document, and parses through it for placeholders and mathematical expressions."""
  # Get document text
  document_text = open(document, 'r').read()

  # Replace easy-to-type placeholder wrappers with standard wrappers
  document_text = document_text.replace("<<", "«").replace(">>", "»")

  # Find placeholders
  placeholders = []
  fields = []
  values = {}
  for placeholder_match in re.finditer(u"«(.+?)»", document_text):
    placeholder = placeholder_match.group(1)
    if placeholder not in placeholders:
      placeholders.append(placeholder)

  # Substitute the placeholders
  if len(placeholders) == 0:
    print("If your project text has placeholders (that look like «this»), this script will prompt for values you'd like to substitute for them.")
    try:
      input("Press [Enter] to continue, or [Ctrl-C] to abort... ")
    except KeyboardInterrupt:
      sys.exit()
  else:
    for placeholder in placeholders:
      placeholder = placeholder.replace("\xc2", "")
      value = raw_input(placeholder + ": ")
      values.update({placeholder: value})
    if values:
      for key in values:
        pattern = "«" + key + "»"
        document_text = re.sub(pattern, values[key], document_text)

  # Evaluate raw python expressions
  document_text = re.sub(r"(\|\|.+?\|\|)", lambda m: str(eval(clean_match_py(m.group()))), document_text)

  # Evaluate math expressions
  document_text = re.sub(r"(\[\[.+?\]\])", lambda m: str(eval_expr(clean_match_math(m.group()))), document_text)

  # Return parsed document text
  return document_text

if __name__ == "__main__":
  print(omnifocus_url(url_escape(parse_template(sys.argv[1]))))
