#!/usr/bin/env python3

from ruamel.yaml import YAML
import re
yaml = YAML(typ='safe')

CONFIGFILES = ("config.txt")

# Parse time configs

class Environment():
    """Hey"""
    def __init__(self, unit_config_files:list, epoch=None):
        self.units = {}
        for unit in unit_config_files:
            self.load(unit)
        self.epoch = epoch
    
    def load(self, fileunit):
        """Load unit config into self.units from YAML config string in format: '<file>:<units>'"""
        file, unit = fileunit.split(":")
        with open(file+".yaml", "r") as f:
            self.units[unit] = yaml.load(f)[unit]

class TimeData():
    def __init__(self, env, unit, value=0):
        self.env = env
        self.unit = unit
        
        vals_len = len(env.units[unit])
        self._reviter = range(vals_len-1, -1, -1)  # Reverse range
        
        self._abrvs = [ i["abrv"] for i in env.units[unit] ]
        self._fulls = [ i["full"] for i in env.units[unit] ]
        self._plurals = [ i["plural"] for i in env.units[unit] ]
        self._conversions = [ i["value"] for i in env.units[unit] ]
        self._basevals = []
        for i in self._reviter:
            out = 1
            for j in self._reviter[i:]:
                out *= self._conversions[j]
            self._basevals.append(out)
        self.value = value
    
    def __eq__(self, other):
        if not (self.env is other.env or self.unit is other.unit): #TEST THIAS
            raise TypeError
        return self.value == other.value
    
    def __gt__(self, other):
        if not (self.env is other.env or self.unit is other.unit): #TEST THIAS
            raise TypeError
        return self.value > other.value
    
    def __lt__(self, other):
        if not (self.env is other.env or self.unit is other.unit): #TEST THIAS
            raise TypeError
        return self.value < other.value
    
    def __ge__(self, other):
        if not (self.env is other.env or self.unit is other.unit): #TEST THIAS
            raise TypeError
        return self.value >= other.value
    
    def __le__(self, other):
        if not (self.env is other.env or self.unit is other.unit): #TEST THIAS
            raise TypeError
        return self.value <= other.value
    
    @property
    def abbrev(self):
        inp = self.value
        ret = ""
        for unitindex in self._reviter:
            basevalue = self._basevals[unitindex]
            ret += str(inp // basevalue) + self._abrvs[unitindex] + " "
            inp %= basevalue
        return ret.strip()
    @abbrev.setter
    def abbrev(self, inp):
        in_list = inp.split()
        print(in_list)
        #self.value = 90
    
    #@property
    #def human(self):
    #    """I'm not doing goddamn human-readable coding again"""
    #    split = [ i for i in re.split( "|".join(self._abrvs), self.abbrev ) if i ]
    #    return split
    #@human.setter
    #def h2a(self):
    #    pass
    
    

if __name__ == "__main__":
    import doctest
    import pprint as p
    
    testenv = Environment(["default:time"])
    #p.pprint(testenv.units)
    
    ttest = TimeData(testenv, "time", 4005006)
    
    p.pprint(ttest._conversions)
    p.pprint(ttest._basevals)
    p.pprint(ttest._abrvs)
    p.pprint(ttest._fulls)
    p.pprint(ttest._plurals)
    print()
    
    ttest2 = TimeData(testenv, "time", 906)
    print(ttest == ttest2)
    print(ttest > ttest2)
    print(ttest < ttest2)
    print(ttest >= ttest2)
    print(ttest <= ttest2)
    print()
    
    print(ttest.abbrev)
    ttest.abbrev = "7w 5d 14m 5s"
    print(ttest.abbrev)
    #print(ttest.human)
    print()
    
    pass