import pandas as pd
import numpy as np
from pandas.core.algorithms import unique

class Database:
    """A class for the database of skier information"""

    def __init__(self, df):
        self.df = df

    def add2data(self, user_name, user_email, user_phone):
        self.n = user_name
        self.e = user_email
        self.p = user_phone
        data = {'name':self.n, 'email':self.e, 
        'phone':self.p}
        self.df.append(data)

    def __repr__(self):
        return(' '.join(map(str,self.df)))
    
class Ticket:
    """A class to check ticket validity and generate new tickets"""

    def __init__(self, unique):
        self.unique = unique

    def isValid(self):
        if self.unique[7] == 'T':
            self.unique[7] = 'F'
            return True

        elif self.unique[7] == 'F':
            return False

        else:
            print('Ticket does not end in T/F')
            return False

    def createTick(self):
        self.unique = []
        for i in range(7):
            self.unique.append(np.random.randint(0,9))
        self.unique += 'T'

    def __repr__(self): 
        return str(' '.join(map(str,self.unique)))

class Daily_Skiers:
    """A class to keep count of the daily skiers"""

    counter = 0
    def __init__(self):
        Daily_Skiers.counter += 1
        self.count = Daily_Skiers.counter
    
    def canSki(self):
        if self.count <= 200:
            return True
        else:
            return False

    def clearCount(self):
        Daily_Skiers.counter = 0

    def __repr__(self):
        return str(self.count)


