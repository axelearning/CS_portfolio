"""Implement quick sort in Python.
Input a list.
Output a sorted list."""

def quicksort(array):
    if len(array) > 1:
    	p_ind = -1
    	compared_index = 0
        # run one sorting step
        for step in range(len(array)-1):
            if array[p_ind] < array[compared_index]: 
                array[p_ind],array[compared_index], array[p_ind-1] = array[compared_index],array[p_ind-1], array[p_ind]
                p_ind = p_ind - 1
            else:
                compared_index = compared_index + 1
        array[:p_ind] = quicksort(array[:p_ind])
        array[p_ind:] = quicksort(array[p_ind:])
    else:
    	pass
    return array

test = [21, 4, 1, 3, 9, 20, 25, 6, 21, 14]
print(quicksort(test))