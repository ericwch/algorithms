from collections import defaultdict
def file_processor(file):
    # this function put the data of a txt file that decirbes a knapsack problem into a list 
    
    # Input: file --- a text file descirbes a knapsack problem. 
    # Output: a list of of (value,weight)
    #        The first line has the format:[knapsack_size][number_of_items]
    #        The subsequent line has the format: [value_1] [weight_1]
    
    with open(file) as content:
            item_list=[]
            capacity,item_num=next(content).split()

            for items in content:
                value1,weight1=items.split()
                item_list.append((int(value1),int(weight1)))
    return item_list, capacity, item_num


def merge_sort(unsorted_list):
    # merge sort from small to large
    # modified for the knapsack problem data
    
    if len((unsorted_list))==1:
        return unsorted_list
    half_index=int(len(unsorted_list)/2)
    
    sorted_list1=merge_sort(unsorted_list[:half_index])
    sorted_list2=merge_sort(unsorted_list[half_index:])
    sorted_list_whole=[]
    
    i=j=0
    while len(sorted_list_whole)<len(sorted_list1)+len(sorted_list2):
        
        if sorted_list1[i][1]<sorted_list2[j][1]:
            sorted_list_whole.append(sorted_list1[i])
            i+=1
            
        else:
            sorted_list_whole.append(sorted_list2[j])
            
            j+=1
        if len(sorted_list1)==i or len(sorted_list2)==j:
            sorted_list_whole.extend(sorted_list1[i:] or sorted_list2[j:])
          
    
    return sorted_list_whole


def large_knapsack (file):
    # Input: file --- a text file descirbes a knapsack problem. 
    #        The first line has the format:[knapsack_size][number_of_items]
    #        The subsequent line has the format: [value_1] [weight_1]
    # Output: the greast value of the knapsack problem
    
    # Breif Explanation: the optimal solution of taking n items 
    #                                        can be obtain ffrom the optimal solution of taking n-1 items
    
    # Imporvement: instead of calculating each A[i][j] where i = [0:number of items] and j = [0:capacity]
    #              mark the i which A[i,j] != A[i,j-1] (the index when the value of A changes)
    #              this approach eliminates the reductant work done by the straight forward approach
    # Example: 
    #         old approach : A[1]=[0,0,0,4,4,4,5,5,5,5]
    #         new approach : A[1]={3:4, 6:5}
    
    # put the knapsack data into a list. [(value of a item, weight of a item),]
    item_list, capacity, item_num = file_processor(file)
    
    # sort the items from lightest to heavest
    item_list=merge_sort(item_list)
    
    # A --- a list of dictionaries. A[i][j] = value where i is the max number of items allow to carry
    #                                                     j is the index when A[i,j]!=A[i,j-1] (see improvement^)
    #                           value is the greatest value can be obtained with capacity j and <=i number of items
    

    A=[defaultdict(int) for n in range(int(item_num)+1)]
    
    n=0
    
    largest=0
    
    # follow code is just obtaining the optimal solution of taking n items 
    #                                        from optimal solution of taking n-1 items
    
    # iterate through all the items from lightest to heavist 
    for value,weight in item_list:
        
        n+=1
        A[n][weight]=value
        
        # iterate through the combinations of items when we are taking at most n-1 items
        for prev_weight,prev_value in A[n-1].items():
            
            if prev_weight<weight and prev_value>A[n][weight]:
                A[n][weight]=prev_value
            
            elif prev_value>value:
                
                if prev_value>A[n][weight]:
                    A[n][prev_weight]=max(prev_value,A[n][prev_weight])
                    largest=max(largest,A[n][prev_weight])
                if prev_weight+weight<=int(capacity):
                    
                    A[n][prev_weight+weight]=max(prev_value+value,A[n][prev_weight+weight])
                    largest=max(largest,A[n][prev_weight+weight])
            else:
                
                if prev_weight+weight<=int(capacity):
                    
                    A[n][prev_weight+weight]=max(prev_value+value,A[n][prev_weight+weight])
                    largest=max(largest,A[n][prev_weight+weight])
    return largest

#test cases
if __name__ == "__main__":
    print(large_knapsack('knapsack_big.txt'))   #4243395
    print(large_knapsack('knapsack1.txt'))      #2493893
