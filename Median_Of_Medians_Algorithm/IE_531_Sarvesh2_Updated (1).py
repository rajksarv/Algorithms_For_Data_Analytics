
# coding: utf-8

# In[18]:


import sys
import argparse
import random
import numpy as np 
import time
import math
sys.setrecursionlimit(3000)
import matplotlib.pyplot as plt


# In[11]:


# first command line argument is the array size
array_size = 10000

# read the value of k (i.e we are looking for the k-th smallest value in the array)
k = 22

# fill the array with random values
my_array = [random.randint(1,100*array_size) for _ in range(array_size)]


# In[12]:


# sort the array and pick the k-th smallest element from the sorted-array
def sort_and_select(current_array, k) :
    # sort the array
    #print(k)
    sorted_current_array = np.sort(current_array)
    return sorted_current_array[k]


# In[13]:


def deterministic_select(current_array, k,m=5) :
    #print(current_array)
    if (len(current_array) <= m) :
        # just use any method to pick the k-th smallest element in the array
        # I am using the sort-and-select method here
        return sort_and_select(current_array, k)
    else : 
        # I need this array to compute the median-of-medians...
        medians_of_smaller_arrays_of_size_five = []
        
        # first, split current_array into smaller arrays with 5 elements each
        # there might be a better way than what I am doing... but this will work... 
        for i in range(0,len(current_array),m):
            #print(i)
            try:
                smaller_array_of_size_five = current_array[i:i+m]
            except IndexError:
                smaller_array_of_size_five = current_array[i:]
    
            #print(smaller_array_of_size_five)
            # we need each of these cases as len(smaller_array_of_size_five) can be anything between 1 and 5
            # based on len(smaller_array_of_size_five) we are computing the median of smaller_array_of_size_five for each case
            length = len(smaller_array_of_size_five)
            #print(length)
            check = length%2==0
            if length==1:
                medians_of_smaller_arrays_of_size_five.extend([smaller_array_of_size_five[0]])
            elif length == 2:
                medians_of_smaller_arrays_of_size_five.extend([np.mean(smaller_array_of_size_five)])
            else:
                if check:
                    first = deterministic_select(smaller_array_of_size_five,int(length/2))
                    second = deterministic_select(smaller_array_of_size_five,int((length/2)+1))
                    medians_of_smaller_arrays_of_size_five.extend([(first+second)/2])
                else:
                    k1 = length//2 + 1
                    #print(length)
                    #print(k1)
                    medians_of_smaller_arrays_of_size_five.extend([deterministic_select(smaller_array_of_size_five,k1)])
            

        # compute the meadian of the medians_of_smaller_arrays_of_size_five array by recursion
        p = deterministic_select(medians_of_smaller_arrays_of_size_five, int(len(medians_of_smaller_arrays_of_size_five)/2))
        # split the current_array into three sub-arrays: Less_than_p, Equal_to_p and Greater_than_p
        Less_than_p = []
        Equal_to_p = []
        Greater_than_p = []
        for x in current_array : 
            if (x < p) : 
                Less_than_p.extend([x])
            if (x == p) : 
                Equal_to_p.extend([x])
            if (x > p) : 
                Greater_than_p.extend([x])
                
        if (k < len(Less_than_p)) :
            return deterministic_select(Less_than_p, k)
        elif (k >= len(Less_than_p) + len(Equal_to_p)) : 
            return deterministic_select(Greater_than_p, k - len(Less_than_p) - len(Equal_to_p))
        else :
            return p


# In[14]:


print("Looking for the ", k, "-th smallest element in a ", len(my_array), "long array")

t0 = time.time()
sorted_my_array = np.sort(my_array)

t1 = time.time()

print ("Sort-and-Pick Method        : ", sort_and_select(my_array, k))
t2 = time.time()
print ("Deterministic-Select Method : ", deterministic_select(my_array, k,9))
t3 = time.time()

print ("It took ", t1-t0, "seconds for the Sort-and-Pick Method")
print ("It took ", t3-t2, "seconds for the Randomized-Select Method")


# In[16]:


number_of_trials = 200


# In[19]:


for n in range(1000,10000,1000):
    plot_mean_time_values = []
    for m in range(5,20,2):
        mean_time = []
        for i in range(200):
            my_array = [random.randint(1,100*n) for _ in range(n)]
            k = math.ceil(n/2)
            t1 = time.time()
            deterministic_select(my_array, k,m)
            t2 = time.time()
            mean_time.append(t2-t1)
        plot_mean_time_values.append(np.mean(mean_time))
    plt.plot([5,7,9,11,13,15,17,19],plot_mean_time_values,lw = 2)
    plt.title('Array Size'+str(n))
    plt.xlabel('m')
    plt.ylabel('Mean Running Time')
    plt.show()

