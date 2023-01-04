
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
  return sorted_lists

def sort_lists_by_smallest_element(lists):
  # Sort the lists in ascending order by their largest element
  sorted_lists = sorted(lists, key=lambda x: min(x))
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

def ls(rep):
  sum = 0
  for i in range(len(rep)):
    instances = []
    for j in range(i):
      if rep[j] < rep[i]:
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

def rb(rep):
  sum = 0
  for i in range(len(rep)):
    instances = []
    for j in range(i+1,len(rep)):
      if rep[j] > rep[i]:
        if rep[j] not in instances:
          sum += 1
          instances.append(rep[j])
  return sum

def inv(rep):
    inversion = 0
    for i in range(len(rep)):
        for j in range(i + 1, len(rep)):
            if rep[i] > rep[j]:
                inversion += 1
    return inversion

def maj(permutation):
    major_index = 0
    for i in range(len(permutation) - 1):
        if permutation[i] > permutation[i + 1]:
            major_index += i + 1
    return major_index


def canonical_inv(rep):
    inversion = 0
    for i in range(len(rep)):
        for j in range(i + 1, len(rep)):
            if rep[i] < rep[j]:
                inversion += 1
    return inversion

def canonical_maj(permutation):
    major_index = 0
    for i in range(len(permutation) - 1):
        if permutation[i] < permutation[i + 1]:
            major_index += len(permutation)-(i+1)
    return major_index

rep_dict = {"mah":sort_lists_by_largest_element,"can":sort_lists_by_smallest_element}

def get_a_statistic(partitions,rep_type:str,statistic,length:int):
  partitions_statistic_dict={}
  for partition in partitions:
    partition = rep_dict[rep_type](partition)
    partition_rep = get_representation(partition,length)

    rep_statistic = statistic(partition_rep)

    if rep_statistic not in partitions_statistic_dict:
      partitions_statistic_dict[rep_statistic] = 1
    else:
      partitions_statistic_dict[rep_statistic] += 1

  return partitions_statistic_dict

def print_dict(dictionary:dict):
  print([dictionary[x] for x in sorted(dictionary.keys())])
