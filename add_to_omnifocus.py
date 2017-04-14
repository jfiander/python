#coding: utf-8
"""
Taskpaper to Omnifocus pre-processor

This script processes a Taskpaper document to detect and fill in specified placeholders, and evaluate mathematical expressions, prior to URL escaping and submitting to Omnifocus for project creation.

This script is an expanded version of the one provided by Ken Case from the Omni Group as part of an Editorial workflow.

Placeholders:
  All text contained in «guillemets» or <<double greater-than-less-thans>> will be detected as a placeholder. The script will present a dialog form with all detected placeholders.
  All instances of the same placeholder will be replaced by the provided value.

Mathematical expressions:
  All text contained in [[double square brackets]] will be mathematically evaluated.
"""
import workflow, dialogs, re, ast
import operator as op

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

def clean_match(match):
  """Removes (all) double square bracket wrappers from a match string"""
  return str(match).replace("[[", "").replace("]]", "")


### Template parsing

# Get document text
document_text = workflow.get_input()

# Replace easy-to-type placeholder wrappers with standard wrappers
document_text = document_text.replace("<<", "«").replace(">>", "»")

# Find placeholders
known_placeholders = set()
placeholders = []
fields = []
for placeholder_match in re.finditer(u"«(.+?)»", document_text):
  placeholder = placeholder_match.group(1)
  if placeholder not in known_placeholders:
    known_placeholders.add(placeholder)
    placeholders.append(placeholder)
    fields.append({'type': 'text', 'title': placeholder, 'key': placeholder})

# Substitute the placeholders
if len(placeholders) == 0:
  if dialogs.alert(u"No template placeholders were found.", u"""
If your project text has placeholders (that look like «this»), this script will prompt for values you'd like to substitute for them.
""", u"Continue") != 1:
    workflow.stop()
else:
  values = dialogs.form_dialog(title='', fields=fields, sections=None)
  if values:
    for key in values:
      document_text = re.sub(u"«" + key + "»", values[key], document_text)

# Evaluate math expressions
document_text = re.sub(r"(\[\[.+?\]\])", lambda m: str(eval_expr(clean_match(m.group()))), document_text)

# Return parsed document text
workflow.set_output(document_text)
