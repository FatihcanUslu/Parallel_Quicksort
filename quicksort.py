import random, time
from multiprocessing import Process, Pipe

def isSorted(arr):
    for i in range(1, len(arr)):
        if arr[i] < arr[i-1]:
            return False
    return True

# consecutive running quicksort
def quicksort_ardisik(arr):
    if len(arr) <= 1:
        return arr
    else:
        pivot = arr[0]
        less_than_pivot = [x for x in arr[1:] if x <= pivot]
        greater_than_pivot = [x for x in arr[1:] if x > pivot]
        return quicksort_ardisik(less_than_pivot) + [pivot] + quicksort_ardisik(greater_than_pivot)

# Paralel working quicksort
def quicksort_paralel(arr, conn, procNum):
    if procNum <= 0 or len(arr) <= 1:
        conn.send(quicksort_ardisik(arr))
        conn.close()
        return 
    pivot = arr[0]
    less_than_pivot = [x for x in arr[1:] if x <= pivot]
    greater_than_pivot = [x for x in arr[1:] if x > pivot]
    pconnLeft, cconnLeft = Pipe()
    leftProc = Process(target=quicksort_paralel, args=(less_than_pivot, cconnLeft, procNum - 1))
    
    pconnRight, cconnRight = Pipe()
    rightProc = Process(target=quicksort_paralel, args=(greater_than_pivot, cconnRight, procNum - 1))

    #Start subprocesses.
    leftProc.start()
    rightProc.start()
 
    conn.send(pconnLeft.recv() + [pivot] + pconnRight.recv())
    conn.close()

    #Join subprocesses.
    leftProc.join()
    rightProc.join()

def main():
    # Test elements
    arr_short = [3, 6, 8, 10, 1, 2, 1]
    number_of_elements_in_array = 1000000
    arr_long = [random.randint(-10000, 10000) for _ in range(number_of_elements_in_array)]

    # Normal sort
    start_time = time.time()
    sorted_arr = quicksort_ardisik(arr_long)
    end_time = time.time()
    # print("Success for consecutive:", isSorted(sorted_arr))
    print('CPU Execution time for consecutive: {:.2f} seconds'.format(end_time - start_time))
    
    # Parallel sort
    start_time = time.time()
    procNum = 3 #2**(n+1) - 1 is the number of processes created
    pconn, cconn = Pipe()
    p = Process(target=quicksort_paralel, args=(arr_long, cconn, procNum))
    p.start()
    sorted_arr = pconn.recv()
    p.join()
    end_time = time.time()
    # print("Success for parallel:", isSorted(sorted_arr))
    print('CPU Execution time for parallel: {:.2f} seconds'.format(end_time - start_time))


    #Python built-in sort
    start_time = time.time()
    sorted_arr = sorted(arr_long)
    end_time = time.time()
    # print("Success for built-in:", isSorted(sorted_arr))
    print('CPU Execution time for built-in: {:.2f} seconds'.format(end_time - start_time))


#Call the main method if run from the command line.
if __name__ == '__main__':
    main()
