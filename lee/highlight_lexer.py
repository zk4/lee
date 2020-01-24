# a smple lexer just for teminal display
from pygments import highlight
from pygments.lexers import PythonLexer,CppLexer,MarkdownLexer,JavascriptLexer, JavascriptSmartyLexer, JavaLexer
from pygments.formatters import TerminalFormatter  as tf
from termcolor import colored

def lexer(s):
    code = False
    bold = False
    code_block = False
    language = ""
    b=[]
    
    l =len(s)
    i =0
    while i < l:
        c=s[i]
        if c == "`":
            if s[i+1] =="`" and s[i+2]=="`":
                code_block=not code_block
                i+=2
                while s[i] !='\n':
                    language+=s[i]
                    i+=1

                if not code_block:
                    yield "break",""
                    print("...",language.strip())
                    yield language.strip(),"".join(b)
                    language=""
                    b=[]

            else:
                code=not code
                if not code:
                    yield "block","".join(b)
                    b=[]
        elif c=="*":
            if s[i+1] =="*":
                bold=not bold
                i+=1
                if not bold:
                    yield "bold","".join(b)
                    b=[]

        else:
            if code or code_block:
                b.append(c)

            else:
                yield "normal" , c
        i+=1

def terminal_print(ss):
    for t, st in lexer(ss):
        if t == "cpp":
            print(highlight(st, CppLexer(), tf()))
        elif t == "python":
            print(highlight(st, PythonLexer(), tf()))
        elif t == "js":
            print(highlight(st, JavascriptSmartyLexer(), tf()))
        elif t == "java":
            print(highlight(st, JavaLexer(), tf()))
        elif t =="block":
            print(colored(st,'yellow'),end="")
        elif t =="break":
            print("\n")
        else:
            print(st,end="")

if __name__ == "__main__":
    s='''
    this isi goodfosdf
    ``` java 
    System.out.println("helo");

    ```

    '''
    terminal_print(s)
