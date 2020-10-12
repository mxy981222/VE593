import sys
from ortools.sat.python import cp_model


# define the callback for arranging instructors to courses
class Solution1Register(cp_model.CpSolverSolutionCallback):  # save each feasible solution to Sol1
    def __init__(self, variables, l, instr, cour, Sol1):  # initialization of the object
        cp_model.CpSolverSolutionCallback.__init__(self)
        self.__M = variables
        self.__l = l
        self.__instr = instr
        self.__cour = cour
        self.__Sol1 = Sol1
        """"""
        self.__solution_count = 0

    def on_solution_callback(self):  # function called during each successful search
        if (self.__solution_count >= self.__l):
            self.StopSearch()  # solutions enough
            return
        sol = []
        self.__solution_count += 1
        for c in self.__cour:
            for i in self.__instr:
                if (self.BooleanValue(self.__M[i - 1][c - 1])):  # if instructor i is assigned to course c
                    sol.append((c, i))
        self.__Sol1.append(sol)
        """"""

    def solution_count(self):  # number of solutions
        return self.__solution_count


# define the callback for arranging courses to days
class Solution2Register(cp_model.CpSolverSolutionCallback):  # save each feasible solution to Sol2
    def __init__(self, variables, l, cour, Sol2):  # initialization of the object
        cp_model.CpSolverSolutionCallback.__init__(self)
        self.__M = variables
        self.__l = l
        self.__cour = cour
        self.__Sol2 = Sol2
        """"""
        self.__solution_count = 0

    def on_solution_callback(self):  # function called during each successful search
        if (self.__solution_count >= self.__l):
            self.StopSearch()  # solutions enough
            return
        sol = []
        self.__solution_count += 1
        for _d in range(5):
            for c in self.__cour:
                if (self.BooleanValue(self.__M[_d][c - 1])):  # if course c is arranged on day _d+1
                    sol.append((_d + 1, c))
        self.__Sol2.append(sol)
        """"""

    def solution_count(self):  # number of solutions
        return self.__solution_count


#define the solution printer
def printsol(Sol1,Sol2,l,mL):
    num=min(l,len(Sol1)*len(Sol2))
    n=0;
    for i in range(len(Sol1)):
        for j in range(len(Sol2)):
            if (n==num):break
            print("Solution %i"%n)
            n+=1
            for s in Sol1[i]:
                print("Course %i, Instructor %i,"%s,end=" ")
                d=0
                for t in Sol2[j]:
                    if(t[1]==s[0]):
                        print(t[0],end="")
                        d+=1
                        if (d==mL):
                            print(end="")
                            break
                        print(",",end=" ")
                print()


def main():
    l = int(sys.argv[2])
    nI = 0
    nC = 0
    mL = 0
    mD = 0
    mC = 0
    C = []
    filename=sys.argv[1]
    with open(filename, "r") as f:
        nI, nC, mL, mD, mC = [int(s) for s in f.readline().split(',')]
        for i in range(nI):
            C.append([int(c) for c in str(f.readline()).split(',')])  # instructor i can teach all courses in C[i]
    instr = list(range(1, nI + 1))  # list of instructors
    cour = list(range(1, nC + 1))  # list of courses
    days = [1, 2, 3, 4, 5]  # weekdays
    """define model1"""
    model1 = cp_model.CpModel()
    Sol1 = []
    M1 = []
    for i in instr:
        M_v = []
        for c in cour:
            if (c not in C[i - 1]):  # if instructor i cannot teach course c
                # M_v.append(model1.NewIntVar(0,0,'C%i, In%i'%(c,i)))
                M_v.append(0)
            else:
                M_v.append(model1.NewBoolVar('C%i, In%i' % (c, i)))
        M1.append(M_v)

    """add constrains to model1"""
    # each course can only be taught by one instructor
    for c in cour:
        model1.Add(cp_model.LinearExpr.Sum(M1[i - 1][c - 1] for i in instr) == 1)

    # each instructor can teach at most mC courses
    for i in instr:
        model1.Add(cp_model.LinearExpr.Sum(M1[i - 1]) <= mC)

    """define model2"""
    model2 = cp_model.CpModel()
    Sol2 = []
    M2 = []
    for d in days:
        M_v = []
        for c in cour:
            M_v.append(model2.NewBoolVar('Day%i, C%i' % (d, c)))
        M2.append(M_v)

    """add constrains to model2"""
    # each day can have at most mD lectures
    for _d in range(5):
        model2.Add(cp_model.LinearExpr.Sum(M2[_d]) <= mD)

    # each course has exactly mL lectures
    for c in cour:
        model2.Add(cp_model.LinearExpr.Sum(M2[_d][c - 1] for _d in range(5)) == mL)

    """solve model1"""
    solver1 = cp_model.CpSolver()
    sol_reg1 = Solution1Register(M1, l, instr, cour, Sol1)
    solver1.SearchForAllSolutions(model1, sol_reg1)
    """solve model2"""
    solver2 = cp_model.CpSolver()
    sol_reg2 = Solution2Register(M2, l, cour, Sol2)
    solver2.SearchForAllSolutions(model2, sol_reg2)
    printsol(Sol1, Sol2, l, mL)


if __name__=='__main__':
    main()
