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
        
        self._abbrevs = [ i["abrv"] for i in env.units[unit] ]
        self._fulls = [ i["full"] for i in env.units[unit] ]
        self._plurals = [ i["plural"] for i in env.units[unit] ]
        self._conversions = [ i["value"] for i in env.units[unit] ]
        self._basevalues = []
        for i in self._reviter:
            out = 1
            for j in self._reviter[i:]:
                out *= self._conversions[j]
            self._basevalues.append(out)
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
            basevalue = self._basevalues[unitindex]
            ret += str(inp // basevalue) + self._abbrevs[unitindex] + " "
            inp %= basevalue
        return ret.strip()
    @abbrev.setter
    def abbrev(self, inp):
        inp_list = inp.split()
        print(inp_list)
        output = 0
        for dataseg in inp_list:
            number_split = 1
            cur_unit_index = None
            for pos_abrv_index in self._reviter:
                cur_abvr = self._abbrevs[pos_abrv_index]
                if dataseg.endswith(cur_abvr):
                    cur_unit_index = pos_abrv_index
                    number_split = dataseg[:-len(cur_abvr)]
                    break
            else: raise Exception #Make a better exception
            print(":::", int(number_split), self._basevalues[cur_unit_index])
            number_to_add = int(number_split) * self._basevalues[cur_unit_index]
            output += number_to_add
        self.value = output
    
    #@property
    #def human(self):
    #    """I'm not doing goddamn human-readable coding again"""
    #    split = [ i for i in re.split( "|".join(self._abbrevs), self.abbrev ) if i ]
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
    p.pprint(ttest._basevalues)
    p.pprint(ttest._abbrevs)
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