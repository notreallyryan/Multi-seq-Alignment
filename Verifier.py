import re
"""
Object that makes sure the provided inputs are valid. 
"""

class Verifier:
    """
    Constructor: Creates the object. return False if information provided is invalid and True otherwise
    Inputs:
        sequences - a list of all seqeunces added during creation of object
        scorings - a 4x4 pandas matrix giving alignment scores of ACGT pairings
        penalties - an 2 integer list where the first digit is the base gap penalty, and the second digit is the additonal gap penalty
    """

    def __init__(self) -> None:
        pass
        

    def verify(self, sequences, scorings, penalties):
        for seq in sequences:
            if not self.seq_validator(seq): return False
        if not self.scorings_validator(scorings) or not self.penalties_validator(penalties):
            return False
        return True



    """
    Validators: Ensures that the input provided is valid
    Note: the sequence validator is the only one that does it one at a time
    """
    def seq_validator(self, seq):
        if re.search("[^ACGT]", seq): return False #if includes non ACGT chars
        return True;

    def scorings_validator(self, scorings):
        if scorings.shape != (4,4): return False
        for x in ('A', 'C', 'G', 'T'):
            for y in ('A', 'C', 'G', 'T'):
                if x == y and int(scorings.at[x,y]) < 1: return False #scoring for direct match cannot be lower than 1.
                if x != y and int(scorings.at[x,y]) >= 0: return False #scoring for a mismatch must be a negative number
        return True
    
    def penalties_validator(self, penalties):
        if penalties[0]< 0 or penalties[1] < 0: return False
        if penalties[0] < penalties[1]: return False #Initial gap peanlty must be more than continued gap penalty
        return True

