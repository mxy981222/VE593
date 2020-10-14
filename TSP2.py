from ortools.constraint_solver import pywrapcp
from ortools.constraint_solver import routing_enums_pb2

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

def print_solution(manager, routing, solution):#print the solution
    print(solution.ObjectiveValue()/1000)#the optimal distance needed
    #start from city0
    print("1, ",end="")
    print("%i, " %(solution.Value(routing.NextVar(0))+1),end="")
    city=solution.Value(routing.NextVar(0))
    num=2
    while (num!=CityCount):
        print(solution.Value(routing.NextVar(city))+1,end="")
        if (num!=CityCount-1):print(", ",end="")
        else:
            print()
        city=solution.Value(routing.NextVar(city))
        num+=1

def main():
    filename=sys.argv[1]
    with open(filename, "r") as f:
        data = f.read；line()
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
        dis_v = [];
        for j in pos:
            dis_v.append(int(distance(i, j)))
        dis_mat.append(dis_v)
    #define the model
    num_routes = 1
    depot = 0  # since the final route is a circle, we can start at any point
    manager = pywrapcp.RoutingIndexManager(CityCount, 1, depot)
    routing = pywrapcp.RoutingModel(manager)
    
    def distance_callback(from_index, to_index):#define the callback function
        from_node=manager.IndexToNode(from_index)
        to_node=manager.IndexToNode(to_index)
        return dis_mat[from_node][to_node]
    
    tran_callback = routing.RegisterTransitCallback(distance_callback)
    routing.SetArcCostEvaluatorOfAllVehicles(tran_callback)
    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    search_parameters.first_solution_strategy = (routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC)
    solution = routing.SolveWithParameters(search_parameters)
    print_solution(manager, routing, solution)


if __name__=='__main__':
    main()
