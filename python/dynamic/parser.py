from typing import List, Iterable
from dynamic.model import CompartimentsSimulator

EOF = 'EOF'
QUOTE = '"'
SPACE = 'SPACE'
COMMENT = '#'
DOT = '.'
NL = 'NL'
DIGIT = 'DIGIT'
ALPHA = 'ALPHA'
OTHER = 'OTHER'

SYMBOLS_TR = {
    ' ': SPACE,
    '"': QUOTE,
    '\n': NL,
    '#': COMMENT,
    '.': DOT
}

SPACERS = [SPACE, NL]


class Token:
    def __init__(self, t, v, p=-1):
        self.type = t
        self.value = v
        self.position = p
     
    def __repr__(self) -> str:
        return 'Token({}, {}{})'.format(
            self.type, repr(self.value), ', {}'.format(self.position) if self.position > -1 else '')


class Lexer:
    """Lexer. Tokenize authorized characters. Skip comments.
    """

    def __init__(self, input_):
        self.input = input_
        self.pos = 0
        self.current_char = None
        if len(self.input) > 0:
            self.current_char = self.input[self.pos]

    def next(self) -> None:
        """Go to the next character
        """
        self.pos += 1
        self.current_char = None if self.pos >= len(self.input) else self.input[self.pos]

    def tokenize(self) -> Iterable[Token]:
        """Tokenize the input
        """

        while self.current_char is not None:
            pos = self.pos
            if self.current_char == COMMENT:  # skip comments until newline
                while self.current_char not in [None, '\n', '\0']:
                    self.next()
                continue
            elif self.current_char in SYMBOLS_TR:
                yield Token(SYMBOLS_TR[self.current_char], self.current_char, pos)
            elif self.current_char.isdigit():
                yield Token(DIGIT, int(self.current_char), pos)
            elif self.current_char.isalpha():
                yield Token(ALPHA, self.current_char, pos)
            else:
                yield Token(OTHER, self.current_char, pos)
            
            self.next()

        yield Token(EOF, None, self.pos)


class Parser:
    """Parse a very simple file to describe a compartimental model

    ```
    model := (delim? section)* delim? EOF
    section := vardef | compartiment | transition
    
    vardef := 'V' delim varname delim float
    compartiment := 'C' delim '"' (alphanum | SPACE)* '"' delim (float | varname)
    transition := 'T' delim integer delim integer delim (float | varname) delim 'r' ('s' | 's' 't' | 't')
    
    delim := (SPACE | NL) (SPACE | NL)*
    alphanum := ALPHA | DIGIT
    integer := DIGIT DIGIT*
    float := (number DOT number*) | (DOT number)
    varname := ALPHA alphanum*
    ```
    
    For example, a SIR model would be
    
    ```
    # transition rates
    V b .1  # S → I
    V g .05 # I → R
    # compartiments
    C "S" .99 # susceptible
    C "I" .01 # infected
    C "R" .0  # recovered
    # transitions
    T 0 1 b rst
    T 1 2 g rs
    ```
    
    Note that :
    
    + `rs` is of the form `rate * source.actual`
    + `rt` is of the form `rate * arget.actual`
    + `rst` is of the form `rate * source.actual * target.actual`
    
    """
    
    def __init__(self, source):
        self.source = source
        self.current_tok = None
        self.lexer = Lexer(source)
        self.tokenizer = self.lexer.tokenize()
        
        self.next() # get the first token
        self.cs = None
        self.variables = {}
   
    def next(self):
        try:
            self.current_tok = next(self.tokenizer)
        except StopIteration:
            self.current_tok = Token(EOF, None, self.pos)
     
    def eat(self, t: str):
       if self.current_tok.type != t:
           raise Exception('Expected token type {}, got {}'.format(t, self.current_tok))
        
       self.next()
    
    def delim(self, must_be=True):
        if must_be and self.current_tok.type not in SPACERS:
            raise Exception('expected SPACE, got {}'.format(self.current_tok))
            
        while self.current_tok.type in SPACERS:
            self.next()
     
    def parse(self) -> CompartimentsSimulator:

        self.cs = CompartimentsSimulator()
        self.variables = {}
        
        while True:
            self.delim(must_be=False)
            
            if self.current_tok.value == 'V':
                self.vardef()
            elif self.current_tok.value == 'T':
                self.transition()
            elif self.current_tok.value == 'C':
                self.compartiment()
            elif self.current_tok.type == EOF:
                break
            else:
                raise Exception('expected `C`, `T` or `V` got {}'.format(self.current_tok))
        
        return self.cs
    
    def vardef(self):
        self.eat(ALPHA)
        self.delim()
        name = self.varname()
        self.delim()
        value = self.float()
        
        self.variables[name] = value
    
    def compartiment(self):
        self.eat(ALPHA)
        self.delim()
        
        self.eat(QUOTE)
        name = ''
        while self.current_tok.type in [SPACE, ALPHA, DIGIT, OTHER]:
            name += self.current_tok.value
            self.next()
        
        self.eat(QUOTE)
        self.delim()
        
        if self.current_tok.type in [DOT, DIGIT]:
            initial = self.float()
        elif self.current_tok.type == ALPHA:
            n = self.varname()
            try:
                initial = self.variables[n]
            except KeyError:
                raise Exception('unknown variable {} (in compartiment)'.format(n))
        
        self.cs.add_compartiment(name, initial)
    
    def transition(self):
        self.eat(ALPHA)
        self.delim()
        source = self.number()
        self.delim()
        target = self.number()
        
        self.delim()
        
        if self.current_tok.type in [DOT, DIGIT]:
            rate = self.float()
        elif self.current_tok.type == ALPHA:
            n = self.varname()
            try:
                rate = self.variables[n]
            except KeyError:
                raise Exception('unknown variable {} (in compartiment)'.format(n))
        
        self.delim()
        
        if self.current_tok.value != 'r':
            raise Exception('expected `r` (in transition), got {}'.format(self.current_tok))
        
        self.eat(ALPHA)
        
        callback = None
        if self.current_tok.value == 's':
            self.eat(ALPHA)
            if self.current_tok.value == 't':
                self.eat(ALPHA)
                callback = lambda t, r, sp, tp: r * sp * tp
            else:
                callback = lambda t, r, sp, tp: r * sp
        elif self.current_tok.value == 't':
            self.eat(ALPHA)
            callback = lambda t, r, sp, tp: r * tp
        else:
            raise Exception('expected `s` or `t` (in transition), got {}'.format(self.current_tok))
        
        self.cs.add_transition(source, target, rate, callback)
    
    def number(self) -> int:
        n = 0
        
        if self.current_tok.type != DIGIT:
            raise Exception('expected DIGIT, got {}'.format(self.current_tok))
        
        while self.current_tok.type == DIGIT:
            n = n * 10 + self.current_tok.value
            self.next()
        
        return n
     
    def float(self) -> float:
        int_part = 0
        float_part = 0
        how_many_digits = 0
        
        if self.current_tok.type == DIGIT:
            int_part = self.number()
            self.eat(DOT)
            if self.current_tok_type == DIGIT:
                p = self.lexer.pos
                float_part = self.number()
                how_many_digits = self.lexer.pos - p
        elif self.current_tok.type == DOT:
            self.next()
            p = self.lexer.pos
            float_part = self.number()
            how_many_digits = self.lexer.pos - p
        else:
            raise Exception('expected DIGIT or DOT, got {}'.format(self.current_tok))
        
        return int_part + float_part * 10 ** -how_many_digits
    
    def varname(self):
        n = ''
        if self.current_tok.type != ALPHA:
            raise Exception('expected ALPHA, got {}'.format(self.current_tok))
        
        while self.current_tok.type in [ALPHA, DIGIT]:
            n += str(self.current_tok.value)
            self.next()
        
        return n

