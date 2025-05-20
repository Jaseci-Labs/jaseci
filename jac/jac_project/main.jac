import from lib { tool_func }
import from lib.sub { help_func }

def main() {

    print('Main Execution:\n') ;    
    print('Calling from tools.py...') ;    
    print('Tool says:', tool_func()) ;    
    print('\nCalling from helper.py...') ;    
    print('Helper says:', help_func()) ;
}

with entry {
    if __name__ == '__main__' {

        main() ;
    }
}