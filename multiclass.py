#!/usr/local/bin/python3
#coding: utf-8
import sys

class Exiter:
  def exit(self, code=0, status=None):
    if type(status) is Status and status.state:
      print('Exiting with status.')
    sys.exit(code)

class Status:
  def __init__(self):
    self.state = False

  def true(self):
    self.state = True

  def false(self):
    self.state = False

class Worker:
  def __init__(self):
    self.status = Status()

  def do(self):
    self.status.true()
    Exiter().exit(status=self.status)
