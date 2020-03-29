symphony problem class

symphProblem.py contains a 'problem' class meant to be used with the COIN-OR/Symphony Mixed-Integer Linear Program solver [1,2] binaries [3]. It is used to write a text-based MILP model in the CPLEX LP format [4].  The class manages human-readable variable names that may be long and/or have substring issues automatically and also manages calling the Symphony binaries to obtain problem solutions.

symphProblem_example.py - An example pattern for creating a simple mixture problem and reporting on the solution
symphProblem_tests.py - Tests

[1] https://projects.coin-or.org/SYMPHONY

[2] https://prod-ng.sandia.gov/techlib-noauth/access-control.cgi/2013/138847.pdf

[3] https://dl.bintray.com/coin-or/download/

[4] http://lpsolve.sourceforge.net/5.0/CPLEX-format.htm
