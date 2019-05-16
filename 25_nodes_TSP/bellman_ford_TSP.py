def graph_gernerator(file):
    # a function put a txt file of xy coordinates into a list
    #
    # input: a txt file with the first line indicates the number of nodes
    #                        the subsequent line indicates x,y coordinates of the node
    # output: x,y --- the number of the x,y coordiantes respectively
    #         graph --- list of tuples of the nodes' (x,y) coordinates
    #         node_num --- number of nodes
    x=[]
    y=[]
    graph=[]
    m=1
    with open(file) as content:
        node_num=int(next(content))
        acontent=content.readlines() 
        for n in acontent:
            n=n.split()
            x.append(float(n[0]))
            y.append(float(n[1]))
            
            graph.append((float(n[1]),float(n[0])))
    graph=sorted(graph)
    
    return x,y,graph,node_num

def ecli_dist(p1,p2):
    # a function calculates the euclidien distance between the two points
    
    # input: p1 ,p2 --- an list or tuple in the format (x coordinate, y coordinate)
    # output: the euclidien distance between the two points
    return ((p1[0]-p2[0])**2+(p1[1]-p2[1])**2)**0.5

def combination(alist,first=True):
    # a function to calculate the nodes combinations on a path from node '1' to a target node

    # modification for TSP problem: only combinations with the successive elements not have gap greater than 3 are calculated
    #                              example: [1,3] is calcualted, [1,5] is skipped
    
    # input: alist --- a list of numbers (from 1 to n)
    # output: a list of the combinations of the elements containing '1'
    
    # explanation: a backtracking algorithm. See below visualisation of the output of each recursion (start from the most inner recursion call): 
    #              combination([1,2,3,4]): [[4]]-->[[3],[4,3]]-->[[4],[3],[4,3],[2],[4,2],[3,2],[4,3,2]]-->...
    
    # small modification of the code can make the function a more gerneral combination function
    
    if alist==[]:
        return alist
    biglist=[]
    
    biglist.append([alist[0]])
    previous_comb = combination(alist[1:],False)
    for m in previous_comb:
                    
        # skip elements with gap greater than 3 (see modification)
        if alist[0]+3<m[0]:            
            pass
        else:
            biglist.append([alist[0]]+m)
            
    # in the last return we want only the combination with '1' added to it
    return biglist if first else biglist+previous_comb




        



from collections import defaultdict
def bellman_ford_TSP(graph,node_num):
    # a function solves the TSP problems of the graph 'tsp.txt'
    #
    # input:  graph --- list of tuples of the nodes' (x,y) coordinates
    #         node_num --- number of nodes
    # 
    # output: the length of the shorest TSP path
    #
    # brief explanation: the optimal solution of a path with m nodes can be obtain by 
    #                    min(combination of m-1 nodes + node m)
    # comment:
    #         by very sloppy observation from the plot, the dots are spreaded from left to right
    #         and the most possible candidates to travel next are all within 3 nodes away. Traveling to
    #         nodes that are more than 3 nodes away would often skip some nodes in between. Extra travel has to 
    #         be made to go back to these skipped nodes. And it'd result in longer travel length.
    #       
    #         Therefore when calculating the combinations, the elements in the combinations are limited to 
    #         not have a gap greater than 3. Example: [1,3] is calculated but [1,6] is not.
    #
    #         which greatly reduced the time needed to calculate the combinations
    
    # B --- an array of dictionaries of dictionaries, 
    #                               first index: number of nodes n used in the path 
    #                               second index: a set of combinations of the nodes (with node '1' in it) with size n
    #                               third index: the target nodes 
    B=[defaultdict(dict) for n in range(node_num+1)]
    for m in combination([n for n in range(1,node_num+1)]):
        for n in m:
            B[len(m)][frozenset(m)][n]=float('Inf') 
    
    # set base case ==0 : the length from node 1 to node 1 is 0
    B[1][frozenset({1})][1]=0
    
    
    #range(2,node_num) because at most n-1 edges path
    for n in range(2,node_num+1):
        
        # iterate through the the possible paths with length n nodes
        for path in B[n].keys():
                min_path_length=float('Inf')
                
                # iterate through the nodes on the path
                for target in path:
                    if target!=1:
                        
                        # score_list --- a list contains all lengths of
                        #       (the n-1 length paths with end point'to_node'+ length of "to_node" to target)
                        #score_list=[score+ecli_dist(graph[to_node-1],graph[target-1] ) for to_node,score in B[n-1]\
                                    #[path.difference(frozenset([target]))].items() if target!=to_node]
                            
                        # iterate through the n-1 length paths without the node 'target' in it
                        length_list=[]
                        
                        for to_node,length in B[n-1][path.difference(frozenset([target]))].items():
                            
                            # if the endpoint of the path 'to_node' is not the target
                            if target!=to_node:
                                
                                # append (the length of the n-1 path + the length from the 'to_node' to 'target')
                                length_list.append(length + ecli_dist(graph[to_node-1],graph[target-1]))
                            
                                    
                                    
                        # if the length_list is not empty ( there's n-1 length paths that can reach target with 1 hop)
                        if length_list!=[]:
                            
                            # record the min path score
                            B[n][path][target]=min(length_list)
                        
                        # this only has meaning in the last iteration
                        # record the min(n-1 nodes length path with target j + the length of j to origin)
                        min_path_length=min(min_path_length,B[n][path][target]+ecli_dist(graph[target-1],graph[0]))
                        
    return min_path_length


#test_case
#if __name__ == "__main__":
    #x,y,graph,node_num = graph_gernerator('tsp.txt')
    #bellman_ford_TSP(graph,node_num)                  #26442.730308954757 (takes a while)