# program to display the functioning of 
# settrace() 
from sys import settrace 
  
  
# local trace function which returns itself 
def my_tracer(frame, event, arg = None): 
    # extracts frame code 
    code = frame.f_code 
  
    # extracts calling function name 
    func_name = code.co_name 
  
    # extracts the line number 
    line_no = frame.f_lineno 
  
    print(f"A {event} encountered in {func_name}() at line number {line_no} ") 
  
    return my_tracer 
  
  
# global trace function is invoked here and 
# local trace function is set for fun() 
def fun(): 
    return "GFG"
  
  
# global trace function is invoked here and 
# local trace function is set for check() 
def check(): 
    return fun() 
  
  
# returns reference to local 
# trace function (my_tracer) 
settrace(my_tracer) 
  
check() 