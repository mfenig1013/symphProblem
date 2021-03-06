# -*- coding: utf-8 -*-
"""
Created on Sat Mar 28 14:27:55 2020
Tests for symphProblem class
@author: Max Fenig
"""
import unittest
import symphProblem_example as spe

# Tests for daUtils
class symphProblemTests(unittest.TestCase):
    
    # test missing value statistics
    def testExample(self):
        data = spe.genData()
        
        # test for feasible solution
        highProtein = spe.porridge('highProtein', data)
        highProtein.create(costConstraint=20)
        highProtein.solve('', 'symphony.exe', 'symphonyParameters.txt')
        self.assertTrue(highProtein.solution['buckwheatGroats2'] >= 9.38)
        self.assertTrue(highProtein.solution['millet'] >= 1.18)
        
        # test for infeasible
        noFunds = spe.porridge('noFunds', data)
        noFunds.create(costConstraint=1)
        noFunds.solve('', 'symphony.exe', 'symphonyParameters.txt')
        self.assertTrue(noFunds.solved == False)
        
if __name__ == '__main__':
    unittest.main()