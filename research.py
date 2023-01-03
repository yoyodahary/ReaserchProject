import copy

def get_partitions(set_):
  if not set_:
    yield []
    return
  for i in range(2**len(set_)//2):
    parts = [set(), set()]
    for item in set_:
      parts[i&1].add(item)
      i >>= 1
    for b in get_partitions(parts[1]):
      yield  [sorted(parts[0], key=lambda x: x)] + [sorted(part, key=lambda x: x) for part in b]

def sort_lists_by_largest_element(lists):
  # Sort the lists in ascending order by their largest element
  sorted_lists = sorted(lists, key=lambda x: max(x))
  global flag
  flag = "mh"
  # Return the sorted list of lists
  return sorted_lists

def sort_lists_by_smallest_element(lists):
  # Sort the lists in ascending order by their largest element
  sorted_lists = sorted(lists, key=lambda x: min(x))
  global flag
  flag = "rg"
  # Return the sorted list of lists
  return sorted_lists

def get_representation(partition, n):
  string_rep = []
  for i in range (1,n+1):
    for part in partition:
      if i in part:
        string_rep.append(partition.index(part)+1)

  return string_rep

def lb(rep):
  sum = 0
  for i in range(len(rep)):
    instances = []
    for j in range(i):
      if rep[j] > rep[i]:
        if rep[j] not in instances:
          sum += 1
          instances.append(rep[j])
  return sum

def rs(rep):
  sum = 0
  for i in range(len(rep)):
    instances = []
    for j in range(i+1,len(rep)):
      if rep[j] < rep[i]:
        if rep[j] not in instances:
          sum += 1
          instances.append(rep[j])
  return sum



my_set = {1,2,3,4,5,6}

left_big_arr = []
right_small_arr = []
counts_lb = {}
counts_rs = {}
equal_counter = [0,0]
second_equal_counter = [0]
for partition in get_partitions(my_set):
  compare = []
  temp_array = []
  for i in range(2):

    if i == 0:
      partition = sort_lists_by_largest_element(partition)
      compare.append(copy.deepcopy(partition))
    else:
      partition = sort_lists_by_smallest_element(partition)
      compare.append(copy.deepcopy(partition))

    rep_string = get_representation(partition,len(my_set))
    

    current_lb, current_rs = lb(rep_string), rs(rep_string)
    temp_array.append(current_lb)
    temp_array.append(current_rs)

    if len(temp_array) == 4:
      if temp_array[0] == temp_array[2]:
        equal_counter[0]+=1
      if temp_array[1] == temp_array[3]:
        equal_counter[1]+=1
    if len(temp_array) == 4:
      if temp_array[0] == temp_array[2] == temp_array[1] == temp_array[3]:
        second_equal_counter[0]+=1



    if current_lb not in counts_lb:
      counts_lb[current_lb] = 1
    else:
      counts_lb[current_lb] += 1

    if current_rs not in counts_rs:
      counts_rs[current_rs] = 1
    else:
      counts_rs[current_rs] += 1

    left_big_arr.append(current_lb)
    right_small_arr.append(current_rs)
    #print(str(partition).replace('[','{').replace(']','}') + "   \t"  + str(rep_string)+  '\t' + str(current_lb) + '\t' + str(current_rs) + '\n')

print([counts_lb[x] for x in sorted(counts_lb.keys())])
print([counts_rs[x] for x in sorted(counts_rs.keys())])
print(sum(left_big_arr))
print(sum(right_small_arr))
print(equal_counter)
print(second_equal_counter)

