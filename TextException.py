# -*- coding: utf-8 -*-
"""
Created on Mon Mar 13 15:44:31 2017

@author: rain
"""

def main():
    try:
        num1,num2=eval(
            input("Enter two numbers, separated by a comma: "))
        result=num1/num2
        print("result is",result)
    except ZeroDivisionError:
        print("Division by zero!")
    except SyntaxError:
        print("A comma may be missing in the input")
    except:
        print("something wrong in the input")
    else:
        print("No exception")
    finally:
        print("The finally clause is executed")
        
main()