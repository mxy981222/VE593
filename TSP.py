import sys
from ortools.sat.python import cp_model


def str2pos(s):
    p=[0,0]
    for i in range(len(s)):
        if(s[i]==","):
            p[0]=int(s[0:i])
            if(s[len(s)-1]=="\n"):
                p[1]=int(s[i+1:len(s)-1])
            else:
                p[1]=int(s[i+1:len(s)])
    return p


def distance(p1,p2):
    x=pow(p1[0]-p2[0],2)
    y=pow(p1[1]-p2[1],2)
    dis=pow(x+y,0.5)
    return round(dis*1000)


def main():
    filename=sys.argv[1]
    with open(filename, "r") as f:
        data = f.readline()
    CityCount = int(data)
    pos_str = []
    with open(filename, "r") as f:
        for line in f.readlines():
            pos_str.append(line)
    pos = []
    for i in pos_str[1:]:
        pos.append(str2pos(i))
    dis_mat = []
    for i in pos:
        for j in pos:
            dis_mat.append(int(distance(i, j)))
    #define model
    model = cp_model.CpModel()
    M = [model.NewIntVar(0, 1, '%i to %i' % (i, j)) for i in range(CityCount) for j in range(CityCount)]
    arc = []
    for i in range(CityCount):
        for j in range(CityCount):
            if (j == i): continue
            arc.append([i, j, M[i * CityCount + j]])

    #add constrains
    for i in range(CityCount):
        model.Add(cp_model.LinearExpr.Sum(
            [M[i * CityCount + j] for j in range(CityCount)]) == 1)  # each time only one city can be visited
    for j in range(CityCount):
        model.Add(cp_model.LinearExpr.Sum(
            [M[i * CityCount + j] for i in range(CityCount)]) == 1)  # each city can only be visit once
    model.AddCircuit(arc)
    model.Minimize(cp_model.LinearExpr.ScalProd(M, dis_mat))
    # Create solver
    solver = cp_model.CpSolver()

    # Solve model
    status = solver.Solve(model)
    print(solver.ObjectiveValue())
    print("1, ",end="")
    seq=1
    j=0
    while(seq!=CityCount):
        for i in range(CityCount):
            if (solver.Value(M[j * CityCount + i])==1):
                print(i+1,end="")
                seq += 1
                if(seq!=CityCount):print(", ",end="")
                j=i


if __name__=='__main__':
    main()
