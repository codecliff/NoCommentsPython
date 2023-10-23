# NoCommentsPython
A python script to remove comments from python scripts, with directory recursion 

## Features
  1. Removes comments and docstrings
  2. Removes blank lines
  3. Can handle all files in a given directory
  4. Can attach a predefined header text to each output   
  5. Non destructive - writes output to a separate file

## How to use : 

1. **See help :**
    
    `python nocommentspython.py -h`
      
    
 
2. **Specify an input file to strip** 
   
    `python nocommentspython.py -i /path/to/inputfile.py`       
    
    This will create an output file `inputfile.py_sanscomments.py` in the same directory as input file
   

3. **(Optional) Specify a header file to insert at the top of output file**
      (Say, for copyright and licenses)
     
     `python nocommentspython.py -i /path/to/inputfile.py -c /path/to/headerfile.txt`
            

4. **Strip all files in a directory :**
   
    `python nocommentspython.py -i /path/to/directory`  
    
    This will process each .py file in that directory  and save its respective output file.
    If any input file has an associated header file, it will be duly inserted in its output file (see below).

   
> [!NOTE]
> **Header/Copyright Files: (Automatic headers for output)***
> If an input file is named `abcinput.py`, you can store its header text in a file 
> named `abcinput.py_header.txt` in the same directory.  This text will automatically be inserted in the output. 
> This is specially helpful for processing directories (see above).



     
 
