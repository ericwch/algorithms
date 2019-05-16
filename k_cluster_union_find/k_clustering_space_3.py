from collections import defaultdict
def big_graph_gernerator(file):
    
    # input: file --- a text file with the format: first line: [# of nodes] [# of bits for each node's label]
    #                                      rest of the lines: 24 bits accociate with the distance of a node
    #        the distance between each pair of nodes is given by the Hamming distance between their bit string label
    
    # output: graph --- a dictionary of a graph in the form: bit string label: list of nodes associated with that bit string
    #         node_num --- number of nodes
    graph=defaultdict(list)
    node=1
    with open(file) as content:
        node_num=next(content).split()[0]
        for n in content:
            
            n=n.replace(' ','')
        
            graph[int(n,2)].append(node)
            node+=1
            
    return graph,int(node_num)


class union_find:
    def __init__(self,node_num):
        
        # self.node_list --- list of nodes. Each node is a dictionary with format:
        # node:['leader' of the node, rank(# of nodes has it as leader)]
        self.node_list={n:[n,0] for n in range(1,node_num+1)}     
        self.cluster_num=node_num                                 # number of nodes
        
        
    def find(self,x):
        # return the 'leader' of the cluster
        # recurse until the top 'leader' is found
        if self.node_list[x][0]==x:
            return x
        else:
            self.node_list[x][0]=self.find(self.node_list[x][0])
            return self.node_list[x][0]
        
        
    def union(self,x,y):
        #merge two clusters
        
        #get the leaders of the two cluster
        leader1=self.node_list[x][0]
        leader2=self.node_list[y][0]
        
        #get the rank(size) of the two leader(cluster)
        leader1_rank=self.node_list[leader1][1]
        leader2_rank=self.node_list[leader2][1]
        
        #merge the smaller one into the larger one (so that the maximum rank doesnt change)
        if leader1_rank==leader2_rank:
            self.node_list[leader1][1]+=1
            self.node_list[leader2][0]=leader1
        elif leader1_rank>leader2_rank:
            self.node_list[leader2][0]=leader1
        else:
            self.node_list[leader1][0]=leader2
            
    def in_same_cluster(self,x,y):
        # check if x,y are in the same cluster by checking if they have the same leader
        if self.find(x)==self.find(y):
            return True
        else:
            return False


def set_bit(num,index):
    #return binary(num) with ith number negated
    mask=1<<index
    return num^mask


def k_clustering_space_3(graph,node_num):
    
    # input: graph --- a dictionary of a graph in the form: bit string label: list of nodes associated with that bit string
    #        the distance between each pair of nodes is given by the Hamming distance between their bit string label
    #        node_num --- number of nodes
    
    # output: number of clusters that makes sure no nodes with distance smaller than 2 split into different cluster
    
    # method: group nodes by their implicit distance bit string, 
    #         then for each bit string iterate through all possible bit string with 0,1,2 bit difference.
    #         merge these nodes
    
    # some reductant work need to be fixed
    
    
    # create union_find object called cluster
    # cluster.cluster_num == number of nodes
    cluster=union_find(node_num)
    
    # iterate through all bit string groups in 'graph'
    for leader_bit,nodes in graph.items():
        
        # set nodes[0] as the 'leader' of the cluster
        leader = nodes[0]
        #this block merges nodes with the same bit string as the 'leader'(distance == 0 bit)
        for node in nodes:
            if not cluster.in_same_cluster(node,leader):
                cluster.union(node,leader)
                cluster.cluster_num-=1
        
        #this block merges nodes with distance 1 bit different from 'leader' 
        #iterate through all possible bit string that's 1 bit different from 'leader''s
        for i in range(24):
            
            # 'one_off_bit' == 'leader_bit' with ith number negated
            one_off_bit = set_bit(leader_bit,i)
            # if 'one_off_bit' is in graph, merge the nodes that has 'one_off_bit' label with 'leader'
            if one_off_bit in graph:
                
                #if the node is not in the same cluster as the 'leader', merge them
                if not cluster.in_same_cluster(leader,graph[one_off_bit][0]):
                    cluster.union(leader,graph[one_off_bit][0])
                    
                    # one less cluster since two cluster are merge into one
                    cluster.cluster_num-=1
                    
                    
            #this block merge nodes with distance 2 bits different from 'leader'
            for j in range(i+1,24):
                
                #'two_off_bit' == 'leader_bit' with ith, jth number negated
                two_off_bit=set_bit(one_off_bit,j)
                
                # if 'two_off_bit' is in graph, merge the nodes that has 'two_off_bit' label with 'leader'
                if two_off_bit in graph:
                    
                    #if the node is not in the same cluster as the 'leader', merge them
                    if not cluster.in_same_cluster(leader,graph[two_off_bit][0]):
                        cluster.union(leader,graph[two_off_bit][0])
                        
                        # one less cluster since two cluster are merge into one
                        cluster.cluster_num-=1
            
    # return the number of remaining cluster
    return cluster.cluster_num
                        
           
 #test case:
#if __name__ == "__main__":
     #graph,node_num=big_graph_gernerator('clustering_big.txt')   #6118
     #print(k_clustering_space_3(graph,node_num))