
# ~ ==============================================================================================================
# ~ Search Terms
    # debugger, debugging, tracer, set trace, debug profile, custom debugger, context manager, debug context
    # debugging context, with keyword
# ~ ==============================================================================================================

# Postit - Does not trace lines that are in the module, only when it enters functions

# ~ ======================================================================
# ~ Imports
# ~ ======================================================================

import os
import sys
import linecache
from typing import List

# ~ ======================================================================
# ~ Debugger
# ~ ======================================================================

class Debugger:
    """
    ```python

    # Test function

    def multiply(x, y):
        '''Function to multiply two numbers'''
        z = x * y
        return z

    # To debug in context:

    with Debugger(print_return_types = False, show_filenames = False):
        multiply(8, 9)

    '''
    Output:
    -------------------------------------------------------------------------------
    Entering Debug Context
    -------------------------------------------------------------------------------
    [181] [call] function: multiply
        [182] [line] z = x * y
        [183] [line] return z
        [183] [locals] {'x': 8, 'y': 9, 'z': 72}
        [183] [returned] 72
    -------------------------------------------------------------------------------
    Exiting Debug Context
    -------------------------------------------------------------------------------
    [146] [call] method: Debugger.__exit__
        [148] [line] sys.settrace(None)
    [---] [TRACEBACK] None
    [---] [EXC_TYPE] None
    [---] [EXC_VALUE] None
    -------------------------------------------------------------------------------
    '''
    ```
    """
    zfill = 3 # ~ Minimum length for line numbers 6 -> 006 for a zfill of 3
    placeholder = f'[{"-" * zfill}]' # ~ Placeholder to align things without line numbers [---]/[123]
    line_break = f'{"-" * 79}' # ~ Simple hypehnated linebreak for readability

    ANSI_RESET = ANSI_OFF = '\033[0m'
    ANSI_COLOUR_OFF = '\033[39m'
    ANSI_BOLD = '\033[1m'
    ANSI_BOLD_OFF = '\033[22m'
    ANSI_UNDERLINE = '\033[4m'
    ANSI_UNDERLINE_OFF = '\033[24m'
    ANSI_LIGHTMAGENTA = '\033[95m'
    ANSI_LIGHTBLUE = '\033[94m'
    ANSI_LIGHTCYAN = '\033[96m'
    ANSI_LIGHTGREEN = '\033[92m'
    ANSI_YELLOW = '\033[93m'
    ANSI_DARKRED = '\033[91m'
    ANSI_BLACK = '\033[30m'
    ANSI_RED = '\033[31m'
    ANSI_LIMEGREEN = '\033[32m'
    ANSI_LIGHTYELLOW = '\033[33m'
    ANSI_BLUE = '\033[34m'
    ANSI_MAGENTA = '\033[35m'
    ANSI_CYAN = '\033[36m'
    ANSI_WHITE = '\033[37m'
    ANSI_POSTIT = '\033[48;2;255;238;88m\033[38;2;0;0;0m'
    ANSI_POSTIT_OFF = '\033[0m'

    def __init__(self, print_return_types = False, show_filenames = False) -> None:
        self.logbook: List[str] = [] # ~ A list of strings to be printed at the end
        self.print_return_types: bool = print_return_types # ~ Boolean to enable/disable printing the types of any/all returned values
        self.show_filenames: bool = show_filenames # ~ Boolean to enable/disable printing filename of each line/call

    def log(self, page):
        """Add page to logbook to be printed later"""
        self.logbook.append(page) # ~ Add a string to the logbook to be printed later

    def custom_trace(self, frame, event, arg, indent = [0]):
        """Custom trace to print events from sys trace"""

        excluded_classes = ['IncrementalEncoder'] # ~ Classes to avoid when tracing methods
        excluded_functions = ['__repr__', '__instancecheck__', '__subclasscheck__'] # ~ Functions and methods to avoid

        # * IncrementalEncoder is for print() as print is hard to catch as it runs in C

        line_no = frame.f_lineno # ~ Get the current line number
        line_prefix = str(line_no).zfill(self.zfill) # ~ Current line number with a minimum character width

        if self.show_filenames:
            filename = os.path.basename(frame.f_code.co_filename) # ~ Get the filename of the current line/call
            prefix = f"{filename} {(indent[0]) * ('    ' + '  ')}[{line_prefix}]" # ~ Prefix with filename
        else:
            prefix = f"{(indent[0]) * ('    ' + '  ')}[{line_prefix}]" # ~ Prefix with no filename

        indented_prefix = f"      " + prefix # ~ Prefix with an extra level of indentation

        # ~ Handle call event
        if event == "call":

            caller_frame = frame.f_back  # ~ Access the frame where the function was called
            if caller_frame:
                caller_line_no = caller_frame.f_lineno # ~ Get the line where function is called
                caller_line_prefix = str(caller_line_no).zfill(self.zfill) # ~ Get prefix for the caller line number
                if self.show_filenames:
                    filename = os.path.basename(caller_frame.f_code.co_filename)  # ~ Get the filename of the caller
                    prefix = f"{filename} {(indent[0]) * ('    ' + '  ')}[{caller_line_prefix}]" # ~ Update with caller filename
                else:
                    prefix = f"{(indent[0]) * ('    ' + '  ')}[{caller_line_prefix}]" # ~ Update prefix with no filename

            function_name = frame.f_code.co_name # ~ Get the name of the function being called

            # ~ Ignore certain functions
            if function_name in excluded_functions:
                return # ~ Returning self.custom_trace would cause issues

            # ~ Check for self in local variables as an indicator that that the call is from an object method
            if 'self' in frame.f_locals:
                class_name = frame.f_locals['self'].__class__.__name__

                # ~ Ignore certain excluded classes
                if class_name in excluded_classes:
                    return # ~ Returning self.custom_trace would cause issues
                
                # ~ Handle calls from this Debugger manually
                if class_name == 'Debugger':
                    self.log(self.line_break) # ~ Print a hyphenated line break for readability
                    self.log(f'{self.ANSI_LIGHTGREEN}Exiting Debug Context{self.ANSI_OFF}') # ~ Print header with colour
                    self.log(self.line_break) # ~ Print a hyphenated line break for readability

                self.log(f"{self.ANSI_CYAN}{prefix} [call] method: {class_name}.{function_name}{self.ANSI_OFF}") # ~ Log a method call

            else:
                self.log(f"{self.ANSI_CYAN}{prefix} [call] function: {function_name}{self.ANSI_OFF}") # ~ Log a function call

            indent[0] += 1 # ~ Enter a called function and increase indentation

        # ~ Handle line event
        elif event == "line":
            filename = frame.f_code.co_filename # ~ Get the filename of the currently executing line
            line = linecache.getline(filename, line_no).strip() # ~ Get the current line as a string from the linecache
            self.log(f"{prefix} [{event}] {line}") # ~ Log the current line with prefixes

        # ~ Handle return event
        elif event == "return":

            local_vars = frame.f_locals # ~ Get the local variables at the point of returning
            return_value = arg # ~ Alias arg as return_value
            self.log(f"{prefix} [locals] {local_vars}") # ~ Log local variables

            # ~ Check if setting to print return types is enabled
            if not self.print_return_types:
                self.log(f"{self.ANSI_LIGHTMAGENTA}{prefix} [returned] {return_value}{self.ANSI_OFF}") # ~ Log return without types in colour

            else:
                return_type = type(return_value) # ~ Get the type of the return value
                self.log(f"{self.ANSI_LIGHTMAGENTA}{prefix} [returned] {return_value}: {return_type}{self.ANSI_OFF}") # ~ Log return with types in colour

                # ~ Check if the return value is iterable
                if hasattr(return_value, '__iter__'):
                    
                    for item in return_value:
                        item_type = type(item) # ~ Get the type of each item in the returned iterable
                        self.log(f"{indented_prefix} [type] {item}: {item_type}")  # ~ Log the item and item type for each item in returned iterable

            indent[0] -= 1 # ~ Leave the current called function and reduce indentation

        return self.custom_trace # ~ Continue tracing by returning the custom_trace function to be called for the next event
    
    def __enter__(self):
        """Enter debugging context to trace lines"""
        sys.stdout = open(os.devnull, 'w') # ~ Disable stdout printing by writing to null
        self.log(self.line_break) # ~ Print a hyphenated line break for readability
        self.log(f'{self.ANSI_LIMEGREEN}Entering Debug Context: Green = Header, Blue = Function/Method, Magenta = Return{self.ANSI_OFF}') # ~ Print header with colour
        self.log(self.line_break) # ~ Print a hyphenated line break for readability
        sys.settrace(self.custom_trace) # ~ Set cuistom trace function as trace function for sys.settrace

    def __exit__(self, exc_type, exc_value, traceback):
        """Exit debugging context to print debug log to terminal"""

        sys.settrace(None)  # ~ Restore the default trace function of sys.settrace

        sys.stdout = sys.__stdout__ # ~ Enable stdout printing

        for page in self.logbook:
            print(page) # ~ Print all pages in the logbook

        print(f'{self.placeholder} [TRACEBACK] {traceback}') # ~ Print Traceback Information
        print(f'{self.placeholder} [EXC_TYPE] {exc_type}') # ~ Print Exception Type Information
        print(f'{self.placeholder} [EXC_VALUE] {exc_value}') # ~ Print Exception Instance Information

        print(self.line_break) # ~ Print a hyphenated line break for readability

# ~ ======================================================================
# ~ Testing
# ~ ======================================================================

if __name__ == '__main__':

    os.system('cls')

    def test(x, y):
        """Useless test function"""
        print('test printer')
        z = x + y
        return z

    def main(value, x, y):
        """Useless main function"""
        print('main printer')
        value += x
        value = y
        os.system('cls')
        value *= test(x, y)
        return [value, y]

    # ~ Enter the Debugging context using the with keyword
    with Debugger(print_return_types = True, show_filenames = False):

        # ~ Run the main function
        main(8, 2, 9)

        # ~ Test errors for traceback
        5 / 0

