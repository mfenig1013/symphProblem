# -*- coding: utf-8 -*-
"""
Created on Sat Mar 28 15:05:48 2020
Example porridge mix optimization problem
@author: Max Fenig
"""
import pandas as pd
import symphProblem

# data on various ingredients that can be used in making a porridge
def genData():
    ingredients = []
    # protein, calories, and price are in units of grams, kcal, and $ respectively
    # note wildRice and wildRice2 are different ingredients but have substring/naming overlap
    ingredients.append({'ingredient': 'wildRice' , 'protein': 4., 'calories': 101., 'price': 5})
    ingredients.append({'ingredient': 'wildRice2' , 'protein': 3., 'calories': 150., 'price': 4})
    ingredients.append({'ingredient': 'buckwheatGroats', 'protein': 19, 'calories': 568, 'price': 10})
    ingredients.append({'ingredient': 'amaranth', 'protein': 9.3, 'calories': 251, 'price': 3})
    ingredients.append({'ingredient': 'millet', 'protein': 22, 'calories': 286, 'price': 5})
    ingredients.append({'ingredient': 'oats', 'protein': 5, 'calories': 140, 'price': 2})
    ingredients.append({'ingredient': 'buckwheatGroats2', 'protein': 5.4, 'calories': 177, 'price': 1.5})
    idf = pd.DataFrame(ingredients)
    return idf

# example problem of making porridge from purchasing various ingredients
class porridge(symphProblem.problem):
    
    def __init__(self, problemName, data):
        super(porridge, self).__init__(problemName)
        self.data = data.copy()

    # create a porridge optimization problem
    def create(self, costConstraint=20):        
        # this is the amount of each ingredient
        amounts = self.data['ingredient'].tolist()
        
        # totals across different metrics
        protein = []
        cost = []
        calories = []
        for ix in range(len(self.data)):
            idict = self.data.iloc[ix].to_dict()
            protein.append(str(idict['protein']) + ' ' + idict['ingredient'])
            cost.append(str(idict['price']) + ' ' + idict['ingredient'])
            calories.append(str(idict['calories']) + ' ' + idict['ingredient'])

        # constraints
        constraints = []
        # create some indicator variables
        indicators = []
        totalProtein = ' + '.join(protein) + ' + -totalProtein = 0'
        totalCalories = ' + '.join(calories) + ' + -totalCalories = 0'
        totalCost = ' + '.join(cost) + ' + -totalCost = 0'
        
        constraints.extend([totalProtein, totalCalories, totalCost])
        indicators.extend(['totalProtein', 'totalCalories', 'totalCost'])
        
        # set objective
        objective = 'totalProtein'
        # constrained by having at least 2000 calories
        calorieConstraint = 'totalCalories >= 2000'
        # constrained by only have costConstraint to spend
        costConstraint = 'totalCost <= ' + str(costConstraint)
        constraints.extend([calorieConstraint, costConstraint])
        
        # construct problem in cplex model file format
        self.problem = 'Maximize\n'
        self.problem += objective + '\n'
        self.problem += 'Subject To\n'
        self.problem += '\n'.join(constraints) + '\n'
        self.problem += 'End'

        # update variable map        
        self.updateVM(amounts)
        self.updateVM(indicators)


def main():
    data = genData()
    budget = 20
    print('Making high-protein porridge with potential ingredients on budget of ' + str(budget))
    print(data)
    o = porridge('porridgeMaker', data)
    o.create(costConstraint=budget)
    o.solve('', 'symphony.exe')
    print('Porridge made! Solution details:')
    print(pd.DataFrame([o.solution]))
    
if __name__ == '__main__':
    main()