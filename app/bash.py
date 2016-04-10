'''
Created on 10/04/2016

@author: rlima
'''

import subprocess
import re


class Bash():
    
    
    
    def send(self, comando):
        
        if not comando.strip().lower() == 'exit':
            try:
                cmd = subprocess.Popen(re.split(r'\s+', comando), stdout=subprocess.PIPE)
                cmd_out = cmd.stdout.read()
                
                return cmd_out
            except OSError:
                print "Invalid command"