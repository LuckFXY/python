# -*- coding: utf-8 -*-
"""
Created on Sun Mar 12 17:53:09 2017

@author: rain
"""

import os.path
import sys

def main():
    #prompt the user to enter filenames
    #f1=input("Enter a source file: ").strip()

    print("You can read from:")
    print("You wrote file %s")
    #f2=input("Enter a target file: ").strip()
    f1=input("Enter a source file:")
    f2=input("Enter a target file:")
    #Check if target file exists
    if os.path.isfile(f2):
        print(f2+" already exists")
        sys.exit()
        
    #open files for input and output
    infile=open(f1,"r")
    outfile=open(f2,"w")
    
    #copy from input file to output file
    countLines=countChars=0
    for line in infile:
        countLines+=1
        countChars+=len(line)
        outfile.write(line)
    
    print(countLines,"lines and ",countChars,"chars copied")
    infile.close()
    outfile.close()
  
    
main()