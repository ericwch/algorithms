from collections import defaultdict
from math import floor

def graph_gernerator(file):
    #input: file --- a txt file with the first line indicates the number of nodes and edges respectively.
    #                the rest of the line indicates an edge (in the form: tail head length)
    #output: a dictionary of edges of the graph in the form: head:(tail,length) and the number of nodes
    #        a dummy node '0' with all other nodes having a 0 weight edge pointing to it is added
    
    graph=defaultdict(list)
    
    with open(file) as content:
        node_num=next(content).split()[0]
        for n in content:
            n=n.split()

            graph[int(n[1])].append((int(n[0]),int(n[2])))
    
    #add dummy node with 0 length edge to other nodes
    for n in list(graph.keys()):
        graph[n].append((0,0))
    
    
    return graph,int(node_num)




def bellman_ford_j(graph,node_num,source):
    # input: graph --- a dictionary of edges of a directed graph in the form: head:(tail,length)
    #                  a dummy node '0' with all other nodes having a 0 weight edge pointing to it is added
    #        node_sum --- a int represents the number of nodes
    #        source --- a int represents the source node
    #
    # output: either 1) an array of the values of the shortest paths from source to other nodes 
    #                2) None if negative cycles exist in the graph
    
    
    
    # A --- a 2d array with first index represent number of nodes on the path and second index represent the target node
    # improvement: could have used a 1d array instead.
    A = [[float('Inf') for n in range(node_num+1)] for n in range(node_num+2)]
    
    # set the base case distance from source node to source node == 0.
    A[0][source]=0
    
    # check --- a flag that indicates if array A remain unchanged in further iterations 
    check=False
    
    # iterate the number of nodes (nodes in graph + a dummy node)-1 times (the number of nodes on a path)
    for n in range(1,node_num+1):
        
        # if array A is unchanged in previous iterations, stop early (shortest paths found) 
        if check:
            return A[n-1]
        
        check=True
        
        # iterate through the nodes (a dummy node '0' + nodes in the graph)
        for m in range(0,node_num+1):
                
                min_node=float('Inf')
                
                # iterate through the nodes p that point at node m
                for p in graph[m]:
                    
                    # find the min source to p + m path 
                    if A[n-1][p[0]]+p[1]<min_node:
                        min_node=A[n-1][p[0]]+p[1]
                        
                # update the value of the source to m path if source to p + m path is the min path so far
                A[n][m]=min(min_node,A[n-1][m])
                
                # set 'check' False to indicate there are changes to array A in this iteration, allowing further iteration
                if A[n][m]!=A[n-1][m]:
                    check=False
    
    # extra iteration to detect negative loop
    # explaination: the above code has iterated the maximum number of nodes that can be on a shorest path. 
    #               Therefore if we do one extra iteration, the value in array A should remain the same. If 
    #               the value decreases, it means there are negative cycles exit in the graph.      
    for m in range(1,node_num+1):
        min_node=float('Inf')
        
        for p in graph[m]:
            if A[node_num][p[0]]+p[1]<min_node:
                    min_node=A[node_num][p[0]]+p[1]
            
            A[node_num+1][m] = min(min_node,A[node_num][m])
        # if the value is changed, negative cycles exit in the graph, return None
        if A[node_num+1][m]!=A[node_num][m]:
            return None
    # return the final value of the shorest paths
    return  A[-1]
    


def unweight_graph_gernerator(file,A):
    #input: file --- a txt file with the first line indicates the number of nodes and edges respectively.
    #                the rest of the line indicates an edge (in the form: tail head length)
    #       A --- a array of the values of the shorest paths from a dummy node to other nodes
    #output: a dictionary of edges of the unwighted graph in the form: head:(tail,length)
    graph=defaultdict(list)
        
    with open(file) as content:
        node_num=next(content).split()[0]
        for n in content:
            n=n.split()

            graph[int(n[0])].append((int(n[1]),A[int(n[0])]-A[int(n[1])]+int(n[2])))
    return graph    


class dijkstra_min_heap:
    
    def __init__(self,graph):
        self.heap=[]                                # a list of the heap structure
        self.size=len(self.heap)                    # size of the heap
        self.shortest_paths=defaultdict(list)       # the shorest paths from source node to the other nodes
        self.greedy_crit=defaultdict(int)           # the greedy criteria of each nodes
        self.graph=graph                            # the graph 
        self.check_list=set()                       # a set of already 'seen' nodes
        self.pos={}                                 # the position of nodes in the heap list
    
    
    def check_adj(self,node):
        # check the reachable adjacent nodes
        for adj_node in self.graph[node]:
            
            # if greedy_crit ==0 and not in check_list, it means this adj_node is first to be seen and therefore update its crit.
            # or the current checking path (source to node to adj_node) has a smaller crit, update adj_node's crit
            
            if (self.greedy_crit[adj_node[0]] == 0 and adj_node[0] not in self.check_list) or \
            (self.greedy_crit[node] + adj_node[1] < self.greedy_crit[adj_node[0]]):
                
                self.greedy_crit[adj_node[0]] = self.greedy_crit[node] + adj_node[1]
                
                #update adj_node's postion in heap
                if adj_node[0] in self.pos:
                    
                    self.delete(self.pos[adj_node[0]])
                    self.insert(adj_node[0])
                else:
                    self.insert(adj_node[0])
            
            
    def smallest_child_index(self,index):
        #return the index and key of the smallest child of a node, if there's none return itself's index and key
            
            # node has 2 children
            if index*2+1 <= self.size-1 and index*2+2 <= self.size-1:
                first_child_index=floor(index*2)+1
                second_child_index=floor(index*2)+2
                
                if self.greedy_crit[self.heap[first_child_index]]<=self.greedy_crit[self.heap[second_child_index]]:
                    return self.heap[first_child_index],first_child_index
                else:
                    return self.heap[second_child_index],second_child_index
            
            # node has 1 child
            elif index*2+1 <=self.size-1:
                return self.heap[floor(index*2)+1],floor(index*2)+1
            
            # node has no children
            else:
                return self.heap[index],index
            
    
    def parent_node(self,index):
        # return the paretn node's key and index of a node, return itself if its the root
        if index%2==0 and index!=0:
            return self.heap[floor(index/2)-1],floor(index/2)-1
        else:
            return self.heap[floor(index/2)],floor(index/2)
    
    
    def sift_down(self,index):
        # recurse till the node(index) is in the right position(both child larger than node)
        
        # get the smallest child's key and index
        child,child_index= self.smallest_child_index(index)
        
        # if the child has smaller crit, sift down
        if self.greedy_crit[child]<self.greedy_crit[self.heap[index]]:
            self.pos[self.heap[index]]=child_index
            self.pos[child]=index
            self.heap[child_index]=self.heap[index]
            self.heap[index]=child
            
            index=child_index
            self.sift_down(index)

            
    def sift_up(self, index):
        # recurse till the node(index) is in the right position(both child larger than node)
        
        # get the parent node's key and index
        parent,parent_index = self.parent_node(index)
        
        # if the parent node has a larger crit, sift up
        if self.greedy_crit[self.heap[index]]<self.greedy_crit[parent]:
            self.pos[self.heap[index]]=parent_index
            self.pos[parent]=index
            self.heap[parent_index]=self.heap[index]
            self.heap[index]=parent
            index=parent_index
            self.sift_up(index)
        
        
    def build_heap(self):
        # build heap from bottom to up. Run time O(logn)
        
        for n in range(self.size):
            self.sift_down(self.size-1-n)
           
                
    def insert(self,node):
        # insert a node at the bottom of the heap and sift up to the right position
        
        self.heap.append(node)
        self.size+=1
        self.pos[node]=self.size-1
        self.sift_up(self.size-1)
    
    
    def check_up_down(self,index):
        # return signal of a node should be sifted up or down
        
        # get the node's smallest child and parent 
        child,child_index= self.smallest_child_index(index)
        parent,parent_index = self.parent_node(index)
        
        # if the child's crit is smaller, return signal of sift down, 
        # or if the parent's crit is larger, return signal of sift up
        if self.greedy_crit[child]<self.greedy_crit[self.heap[index]]:
            return 'down'
        elif  self.greedy_crit[self.heap[index]]<self.greedy_crit[parent]:
            return 'up'
    
    
    def delete(self,index):
        # delete a node from heap
        self.size-=1
        
        # if a node is the last node, delete it
        if self.heap[-1]==self.heap[index]:
            
            del self.pos[self.heap[index]]
            self.heap.pop()
            
            return None
        
        # if a node is not the last node
        # delete the node and replace its position with the last node, delete last node
        # sift the replace node to the right position
        
        del self.pos[self.heap[index]]
        self.pos[self.heap[-1]]=index
        self.heap[index]=self.heap[-1]
        self.heap.pop()
        if self.heap!=[]:
            which_way=self.check_up_down(index)
            if which_way =='up':
                self.sift_up(index)
            elif which_way =='down':
                self.sift_down(index)

                
    def insert_multi(self,node_list):
        #insert a list of nodes
        
        for n in node_list:
            self.insert(n)
            
            
    def extract_min(self):
        # extract the root (min node)
        
        min_node=self.heap[0]
        self.delete(0)
        
        return min_node


def dijkstra(graph,start_node):
    
    # make a heap object called heap_list
    heap_list= dijkstra_min_heap(graph)
    
    # initialization
    heap_list.shortest_paths[start_node].append(start_node)
    heap_list.check_adj(start_node)
    heap_list.check_list.add(start_node)
    
    #iterate through all the edges
    while heap_list.heap != []:
        
        # include the nearest unchecked node to checked
        nearest_unchecked_node = heap_list.extract_min()
        heap_list.check_list.add(nearest_unchecked_node)
        
        # scan the adjacent nodes
        heap_list.check_adj(nearest_unchecked_node)
    
    
        
    return heap_list.greedy_crit

def johnsons_all_pairs(file):
    #generate graph with dummy node from file
    graph,node_num = graph_gernerator(file)
    
    #calculate the unweight value of each node using bellman_ford
    unweight_value = bellman_ford_j(graph,node_num,0)
    
    #if no negative cycles
    if unweight_value:
        
        #gernerate graph with unweighted edge leangth
        unweighted_graph=unweight_graph_gernerator(file, unweight_value)
        
        min_value = float('Inf')
        
        # for each node, use dijkstra to find the shorest paths to other nodes
        for source in range(1,node_num+1):
            
            shorest_paths = dijkstra(unweighted_graph, source)
            
            # recover the original edge length and mark the smallest value
            for node,length in shorest_paths.items():
                if min_value > length + unweight_value[source] - unweight_value[node]:
                    min_value = length + unweight_value[source] - unweight_value[node]
        
        #return smallest value
        return min_value
    else: 
        return 'Negative cycles detected!'

# test case

if __name__ == "__main__":
    #print('test case 1')
    #print(johnsons_all_pairs('g1.txt')) # Negative cycles detected!
    #print('test case 2')
    #print(johnsons_all_pairs('g2.txt')) # Negative cycles detected!
    print('test case 3')
    print(johnsons_all_pairs('g3.txt')) # -19

