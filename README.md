# symphProblem

symphProblem.py contains a 'problem' class meant to be used with the COIN-OR/Symphony Mixed-Integer Linear Program solver [1,2] binaries [3]. The class is inherited to create a user-defined text-based MILP model in the CPLEX LP format [4].  The class manages human-readable variable names that may be long and/or have substring issues.  It also manages calling of the Symphony binaries to obtain problem solutions and store them within the class for user by other objects/processes.

symphProblem_example.py - An example pattern for creating a simple mixture problem and reporting on the solution.  Running this will create human_porridgeMaker.lp and converted_porridgeMaker.lp corresponding to human-readable and converted model files, respectively.

symphProblem_tests.py - Tests

[1] https://projects.coin-or.org/SYMPHONY

[2] https://prod-ng.sandia.gov/techlib-noauth/access-control.cgi/2013/138847.pdf

[3] https://dl.bintray.com/coin-or/download/

[4] http://lpsolve.sourceforge.net/5.0/CPLEX-format.htm


# problem class functions

### problem.__init__(self, problemName, defaultChar='x')
problemName: a string describing the model name; this will be used in output file naming conventions
defaultChar: default single-character to be used for converted file names

### problem.create(self) 
Model creation function to be overwritten in child classes by the user.  This function should always call problem.updateVM within it to update the internal variable count and mapper.

### problem.convertH2C(self)
Creates a converted string of the problem by mapping all user-defined variables to "x*" where '*' is a natural number.  This should (in general) not be called by the user.

### problem.updateVM(self, variables)
variables is a list of strings corresponding to model variables. This function maps each variable to an internal representation 'x*', where '*' is a number to be used by the symphony solver to eliminate issues arising from user-defined variables.

### problem.solve(self, outputDirectory, pathToSymphony, pathToParametersFile=None)
Runs the symphony binary on the model.  outputDirectory: the directory where model files will be generated and stored.  
pathToSymphony: path to the symphony binary
pathToParametersFile: optional input parameter file location (see [1] for details on valid parameters for the solver)

### useful problem class fields

self.problem: string corresponding to the entire human-readable model specified by the user
self.solution: dictionary of user-defined variables and their values in the solution (if a solution exists)
self.solved: if True means a valid problem has been created and has been solved; False otherwise
self.var: set of human-defined variables
self.numVar: number of variables in the model
self.variableMap = a mapping of user-defined variables and their converted names and vice versa.  'h2c' means user-defined to converted; 'c2h' means converted back to user-defined
