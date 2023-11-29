import itertools

class Sentence():
    def evaluate(self,model):
        """Evaluates the logical sentence."""
        raise Exception("Nothing to Evaluate.")
    def formula(self):
        """Returns string formula representing logical sentence."""
        return ""
    
    def Symbol(self):
        """Returns a set of all symbols in a logical sentence."""
        return set()

    @classmethod
    def validate(cls,other):
        if not isinstance(other,Sentence):
            raise TypeError("Must be of same type.")


    @classmethod
    def parenthesis(cls,s):
        """Parenthesizes an expression if not already parenthesized."""
        def balanced(s):
            """Checks if a string has balanced parentheses."""
            count = 0
            for c in s:
                if c == '(':
                    count +=1
                elif c== ")":
                    if count <=0:
                        return False
                    
                    count -=1
                    
            return count ==0
        
        if not len(s) or s.isalpha() or [s[0] == '(' and s[-1] == ')' and balanced(s[1:-1])]:
            return s
        else:
            return f"({s})"


class Symbol(Sentence):
    def __init__(self,name) -> None:
        self.name = name

    def __eq__(self, other) -> bool:
        return (isinstance(other,Symbol) and self.name == other.name)
    def __hash__(self) -> int:
        return hash(("symbol",self.name))

    def __repr__(self) -> str:
        return self.name
    
    def evaluate(self, model):
        try:
            return bool(model[self.name])
        except KeyError:
            return f"variable {self.name} is not in Model."
    
    def formula(self):
        return self.name
    
    def symbols(self):
        return {self.name}
    
class Not(Sentence):

    def __init__(self,operand) -> None:
        Sentence.validate(operand)
        self.operand = operand

    def __eq__(self, other) -> bool:
        return (isinstance(other,Not) and self.operand == other.operand)
    
    def __hash__(self) -> int:
        return hash("not",self.operand)
    
    def __repr__(self) -> str:
        return self.operand
    
    def formula(self):
        return "¬" + Sentence.parenthesis(self.operand.formula())
    
    def symbols(self):
        return self.operand.symbols()
    
    def evaluate(self, model):
        return not self.operand.evaluate(model)


class And(Sentence):

    def __init__(self,*others) -> None:
        for other in others:
            Sentence.validate(other)
        self.others = list(*others)
    
    def __eq__(self, other: object) -> bool:
        return (isinstance(other,And) and self.others == other.others)
    
    def formula(self):
        return "^" + Sentence.parenthesis(other for other in self.others)
        
    def __hash__(self):
        return hash("and",tuple(hash(conjuct) for conjuct in self.others))
    
    def __repr__(self) -> str:
        conjuction = ",".join(str(other) for other in self.others)
        return f"and({conjuction})"
    
    def add(self, other):
        Sentence.parenthesis(other)
        self.others.append(other)
    
    def evaluate(self, model):
        return all(other.evaluate(other) for other in self.others)