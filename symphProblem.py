# -*- coding: utf-8 -*-
"""
Created on Sat Mar 28 14:25:05 2020
A class for defining human-readable MILP model formulations
in the CPLEX file format to be used with the symphony open-source solver
File formatting guidelines are described
http://lpsolve.sourceforge.net/5.1/CPLEX-format.htm
@author: Max Fenig
"""
import os
import warnings
from abc import ABC, abstractmethod

# a general problem
class problem(ABC):
    
    def __init__(self, problemName):
        self.problemName = problemName
        self.problem = None
        self.solution = None
    
        # state of object
        self.solved = False
        
        # list of all variables used in the problem
        self.var = set([])
        
        # human-readable variable lengths
        self.varl = []
                
        # variable count
        self.numVar = 0
        
        # map to convert from human-readable to solver readable
        # this is needed to avoid truncation effects on variable names in symphony
        self.variableMap = {'h2c': {}, 'c2h': {}}
        
        super().__init__()
    
    # children must create the problem
    @abstractmethod
    def create(self):
        pass

    # converting text2Convert using self.variableMap
    def convertH2C(self):
        if self.problem is not None:
            self.converted = self.problem
            mapper = self.variableMap['h2c']
            
            # sort varl based on the length of the human-readable variables
            # start with longest-length variable names first to eliminate substring
            # issues with variable naming conventions
            self.varl.sort(key = lambda x: -x[1])
            for tpl in self.varl:
                humanVar = tpl[0]
                replacement = mapper[humanVar]
                self.converted = self.converted.replace(humanVar, replacement)
        else:
            raise Exception('problem is empty!')
    
    # update variable map with new variables from problem
    def updateVM(self, variables):
        for v in variables:
            if v in self.var:
                warnings.warn(v + ' is already in problem variable set, ignoring')
            else:
                # as we input variable names keep track of length of each variable
                self.var.add(v)
                self.numVar += 1
                # this is the converted variable name assigned using self.numVar
                cvar = 'x' + str(self.numVar)
                self.variableMap['h2c'][v] = cvar
                self.variableMap['c2h'][cvar] = v
                
                # the length of the variable matters in determinig the order
                # of which we perform conversions from h2c
                vlen = len(v)
                self.varl.append((v, vlen))
                
    # solve the problem
    def solve(self, outputDirectory, pathToSymphony, pathToParametersFile=None):
        nullProblem = self.problem is None
        missingVariables = len(self.variableMap['h2c'].keys()) == 0
        if nullProblem:
            raise Exception('problem is empty!')
        elif missingVariables:
            raise Exception('variableMap is empty!')
        else: # if both are verified, then attempt to run solver
            hfile = outputDirectory + 'human_' + self.problemName + '.lp'
            cfile = outputDirectory + 'converted_' + self.problemName + '.lp'
            sfile = outputDirectory + 'solution_' + self.problemName + '.txt'
            
            # write the human readable file
            with open(hfile, 'w') as fwrite:
                fwrite.write(self.problem)
            
            # write the converted file for solving
            self.convertH2C()
            with open(cfile, 'w') as cwrite:
                cwrite.write(self.converted)

            # call symphony binary here.  this can be modified 
            # to e.g., include parameter files as inputs etc
            if pathToParametersFile is None:
                os.system(pathToSymphony + ' -L ' + cfile + ' > ' + sfile)
            else:
                os.system(pathToSymphony + ' -f ' + pathToParametersFile + ' -L ' + cfile + ' > ' + sfile)
            
            # read sfile, parse inputs, and map back into human-readable
            # variables into solution dictionary
            with open(sfile, 'r') as fread:
                self.stxt = fread.read().split('\n')
                
            # parse through solution file
            solFoundTxt = 'Column names and values of nonzeros in the solution'
            if solFoundTxt in self.stxt:
                self.solution = {}
                istart = self.stxt.index(solFoundTxt)
                for iparse in range(istart+2, len(self.stxt)):
                    line = self.stxt[iparse]
                    if len(line) > 1:
                        try:
                            ltmp = line.split(' ')
                            varname = ltmp[0]
                            value = float(ltmp[-1])
                            self.solution[self.variableMap['c2h'][varname]] = value
                        except:
                            warnings.warn('skipping line ' + line + ' in solution block')
                self.solved = True
            else:
                warnings.warn('No solution found for problem.  See details in ' + sfile) 