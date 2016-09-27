'''
Created on 10/04/2016

@author: rlima
'''

import subprocess
import re
import os
import pty

def inpty(argv):
  output = []
  def reader(fd):
    c = os.read(fd, 1024)
    while c:
      output.append(c)
      c = os.read(fd, 1024)

  pty.spawn(argv, master_read=reader)
  return ''.join(output)
    

class Bash():

    def send(self, comando):

        if not comando.strip().lower() == 'exit':
            try:
                cmd_out = inpty(comando.split())
#                 cmd = subprocess.Popen(re.split(r'\s+', comando), stdout=subprocess.PIPE)
#                 cmd_out = cmd.stdout.read()

                return cmd_out
            except OSError:
                print "Invalid command"
