#####################################################################
# Author    	: Rahul Singh
# URL       	: https://github.com/codecliff/NoCommentsPython
# License   	: CC 
# email     	: codecliff@users.noreply.github.com
# Disclaimer	: No warranties, stated or implied.   
# Description 	: A tool to remove comments and docstrings from python scripts 
# 		  Functional part is borrowed from code by dan-mcdougall on stackoverflow
#         Directory recursion, param handling and minor formatting features are added by this project
#####################################################################

import os, sys, io, tokenize, re
import argparse
from subprocess import call

def remove_comments_and_docstrings(source):
    
    """
    Returns 'source' minus comments and docstrings.
    source : #dan-mcdougall  https://stackoverflow.com/a/62074206/5132823    
    """
    io_obj = io.StringIO(source)
    out = ""
    prev_toktype = tokenize.INDENT
    last_lineno = -1
    last_col = 0
    for tok in tokenize.generate_tokens(io_obj.readline):
        token_type = tok[0]
        token_string = tok[1]
        start_line, start_col = tok[2]
        end_line, end_col = tok[3]
        ltext = tok[4] 
        # The following two conditionals preserve indentation.
        # This is necessary because we're not using tokenize.untokenize()
        # (because it spits out code with copious amounts of oddly-placed
        # whitespace).
        if start_line > last_lineno:
            last_col = 0
        if start_col > last_col:
            out += (" " * (start_col - last_col))
        # Remove comments:
        if token_type == tokenize.COMMENT:
            # RS- if there is an attribution url, retain it 
            mtch= re.findall(pattern=r'(https?://\S+)', string= token_string)
            if mtch:
                print("http found")
                for m in mtch:
                    out += f"# {m} \n"
            else:
                #remove all other comments
                pass
        # This series of conditionals removes docstrings:
        elif token_type == tokenize.STRING:
            if prev_toktype != tokenize.INDENT:
        # This is likely a docstring; double-check we're not inside an operator:
                if prev_toktype != tokenize.NEWLINE:
                    # Note regarding NEWLINE vs NL: The tokenize module
                    # differentiates between newlines that start a new statement
                    # and newlines inside of operators such as parens, brackes,
                    # and curly braces.  Newlines inside of operators are
                    # NEWLINE and newlines that start new code are NL.
                    # Catch whole-module docstrings:
                    if start_col > 0:
                        # Unlabelled indentation means we're inside an operator
                        out += token_string
                    # Note regarding the INDENT token: The tokenize module does
                    # not label indentation inside of an operator (parens,
                    # brackets, and curly braces) as actual indentation.
                    # For example:
                    # def foo():
                    #     "The spaces before this docstring are tokenize.INDENT"
                    #     test = [
                    #         "The spaces before this string do not get a token"
                    #     ]
        else:
            out += token_string
        #always:    
        prev_toktype = token_type
        last_col = end_col
        last_lineno = end_line
    
    #This line by Basj https://stackoverflow.com/a/62074206/5132823	
    out = '\n'.join(l for l in out.splitlines() if l.strip())
    
    #RS- add newlines before function and class definitions 
    out2= re.sub(  pattern=r"^([\s]+)?(def\s|class\s)",repl=r'\n\n\g<1>\g<2> ',    string=out, flags=re.MULTILINE)
    return out2

    
    
def main(): 
    

    print("---")  

    parser = argparse.ArgumentParser(description='A tool to strip all comments and docstrings from python files',
                             epilog="See above for directories and header files")
    parser.add_argument('--infile', '-i', help="File to strip. If a directory, all files in it will be processed", type= str)
    parser.add_argument('--copyrightfile', '-c', help="(optional) A file with header text to insert in the output.\n\
                         If omitted, a file {infile}_header.txt will also be looked up ", 
                        type= str, default= "header.txt")
  
    args = parser.parse_args(  )
    infile= args.infile
    outfile=None    
    headerfile= args.copyrightfile if (os.path.exists(args.copyrightfile))  else None    
    headertext=""

    if not os.path.exists(infile):
        print( f"Error! '{infile}' Does not exist" )
        exit(1)
    else:
        outfile=f"{infile}_sanscomments.py" 

    ############ directory handling ###############
    if os.path.isdir(infile):
        #convert to abs path
        infile_abs= os.path.abspath(infile)        
        pyfiles = [os.path.join(d, x)
            for d, dirs, files in os.walk(infile_abs)
            for x in files if x.endswith(".py")]
        
        for pyf in pyfiles:
            print(f"in directory, processing {pyf} : ")
            call(["python", 'nocommentspython.py', f"-i={pyf}"]) 
        print("Done with all files")    
        exit(0)    
    ################################################     
    
    if headerfile is None and os.path.exists(f"{infile}_header.txt"):
        headerfile= f"{infile}_header.txt"    

    if headerfile is not None:
        with open( headerfile, 'r') as h:
            headertext= h.read()

    with open( infile, 'r') as f,  open(  outfile, 'w') as o :
         
        inputtext = f.read()
        outputText=remove_comments_and_docstrings(inputtext)

        if (headertext is not None):
            outputText= headertext + "\n" + outputText
            
        o.write(outputText)
        print(f"\noutput written to {outfile}\n")    

  
 
# python call  
if __name__=="__main__": 
    main() 
    
    
    
