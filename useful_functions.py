
''' setup functions '''
import copy
import math


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

''' subtle inversion like statistics from wachs and white '''


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

''' regular inv and maj statistics on the mahonian representation '''

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

def maj_d(permutation,d = 5):
    major_index_d = 0
    for i in range(len(permutation)):
      if(i+d<len(permutation)):
        if permutation[i] > permutation[i + d]:
            major_index_d += i + 1
      for j in range(i + 1, i+d):
        if j<len(permutation):
          if permutation[i] > permutation[j]:
              major_index_d += 1
    # print(str(permutation)+'\t'+str(major_index_d))
    return major_index_d

def div_k(rep,k = 2):
  sum = 0
  for i in range(len(rep)):
    for j in range(i+1,len(rep)):
      if rep[i]/rep[j]>1 and rep[i]/rep[j]<=k:
        sum += 1
  for i in range(len(rep)-1):
    if rep[i]/rep[i+1]>k:
      sum+=i+1
  return sum

def stat_even(rep,k = 2):
  sum = 0
  for i in range(len(rep)):
    for j in range(i+1,len(rep)):
      if rep[i]>rep[j] and rep[j]%2==1:
        sum += 1
  for i in range(len(rep)-1):
    if rep[i]>rep[i+1] and rep[i+1]%2==0:
      sum+=i+1
  return sum

def stat_third(rep,k = 2):
  sum = 0
  for i in range(len(rep)):
    for j in range(i+1,len(rep)):
      if rep[i]>rep[j] and rep[j]%3==1:
        sum += 1
  for i in range(len(rep)-1):
    if rep[i]>rep[i+1] and rep[i+1]%3==0:
      sum+=i+1
  return sum

def k_maj(rep,k = 2):
  sum_k_major = 0
  for i in range(len(rep)):
    for j in range(i+1,len(rep)):
      if rep[i]>rep[j] and rep[i]<rep[j]+k:
        sum_k_major += 1
  for i in range(len(rep)-1):
    if rep[i]>=rep[i+1] +k:
      sum_k_major+=i+1 
  return sum_k_major

''' 
maj and inv statistics that are equidistributed on the canonical representation 
and equal the regular maj and inv on the mahonian representation
'''

def canonical_maj(permutation):
    major_index = 0
    for i in range(len(permutation) - 1):
        if permutation[i] > permutation[i + 1]:
            major_index += len(permutation)-(i+1)
    return major_index

def canonical_stat_even(permutation):
  sum = 0
  for i in range(len(permutation)):
    for j in range(i+1,len(permutation)):
      if permutation[i]>permutation[j] and permutation[i]%2==1:
        sum += 1
  for i in range(len(permutation)-1):
    if permutation[i]>permutation[i+1] and permutation[i]%2==0:
      sum+=len(permutation)-(i+1)
  return sum

rep_dict = {"mah":sort_lists_by_largest_element,"can":sort_lists_by_smallest_element}

''' 
reversed version of maj and inv statistics that are equidistributed on the canonical representation 
'''

def magic_inv(rep):
    inversion = 0
    for i in range(len(rep)):
        for j in range(i + 1, len(rep)):
            if rep[i] < rep[j]:
                inversion += 1

    # print(str(rep)+'\t'+str(inversion))
    return inversion


def magic_maj(permutation):
    major_index = 0
    for i in range(len(permutation) - 1):
        if permutation[i] < permutation[i + 1]:
            major_index += len(permutation)-(i+1)
    # print(str(permutation)+'\t'+str(major_index))
    return major_index

def magic_maj_d(permutation,d = 2):
    major_index_d = 0
    for i in range(len(permutation)):
      if(i+d<=len(permutation)-1):
        if permutation[i] < permutation[i + d]:
            major_index_d += len(permutation)-(i+1)
      for j in range(i + 1, i+d):
        if j<len(permutation):
          if permutation[i] < permutation[j]:
              major_index_d += 1
    #print(str(permutation)+'\t'+str(major_index_d))
    return major_index_d

def magic_stat_even(rep):
  sum = 0
  for i in range(len(rep)):
    for j in range(i+1,len(rep)):
      if rep[i]<rep[j] and rep[i]%2==1:
        sum += 1
  for i in range(len(rep)-1):
    if rep[i]<rep[i+1] and rep[i]%2==0:
      sum+=len(rep)-(i+1)
  return sum

def magic_div_k(rep,k = 2):
  sum = 0
  for i in range(len(rep)):
    for j in range(i+1,len(rep)):
      if rep[i]/rep[j]<1 and rep[i]/rep[j]>=1/k:
        sum += 1
  for i in range(len(rep)-1):
    if rep[i]/rep[i+1]<1/k:
      sum+=len(rep)-(i+1)
  return sum

''' Eularian distribution '''

def exc(rep):
  exc = 0
  sorted_rep = sorted(rep)
  for i in range(len(rep)):
    if rep[i]>sorted_rep[i]:
      exc+=1
  return exc

def des(rep):
  des = 0
  for i in range(len(rep) - 1):
    if rep[i] > rep[i + 1]:
        des += 1
  return des

def asc(rep):
  asc = 0
  for i in range(len(rep) - 1):
    if rep[i] < rep[i + 1]:
        asc += 1
  return asc

def exc_rev(rep):
  exc_rev = 0
  sorted_rep = sorted(rep)
  for i in range(len(rep)):
    if rep[i]<sorted_rep[i]:
      exc_rev+=1
  return exc_rev

def exc_des(rep):

  exc_des = 0
  sorted_rep = sorted(rep)
  for i in range(len(rep)):
    if rep[i]+1>sorted_rep[i]:
      exc_des+=1

  for i in range(len(rep) - 1):
    if rep[i]+1 > rep[i + 1]:
        exc_des += 1

  return exc_des

def z(rep,func = maj):
  z_sum = 0
  for i in range(len(rep)):
    for j in range(i+1,len(rep)):
      arr_i_j = [a for a in rep if a == i or a == j]
      z_sum += func(arr_i_j)
  return z_sum

def canonical_z(rep,func = canonical_maj):
  z_sum = 0
  for i in range(len(rep)):
    for j in range(i+1,len(rep)):
      arr_i_j = [a for a in rep if a == i or a == j]
      z_sum += func(arr_i_j)
  return z_sum

''' The foata bijection '''

def foata_correct(rep):
  if len(rep)>=2:
    if rep[-1]>=rep[-2]:
      i = len(rep)-2
      while i >=1:
        if rep[i-1]>rep[-1]:
          rep[i-1],rep[i] = rep[i],rep[i-1]
        i-=1
    elif rep[-1]<rep[-2]:
      i = len(rep)-2
      while i >=1:
        if rep[i-1]<=rep[-1]:
          rep[i-1],rep[i] = rep[i],rep[i-1]
        i-=1


def foata(rep):
  foata_rep = []
  for i in range(len(rep)):
    foata_rep.append(rep[i])
    foata_correct(foata_rep)
  return foata_rep

def foata_distance(rep):
  distance = []
  for i in range(len(rep)-1):
    distance.append(rep[i+1]-rep[i])
  return distance


def permutations(n):
    if n == 1:
        yield [1]
    else:
        for p in permutations(n - 1):
            for i in range(n):
                yield p[:i] + [n] + p[i:]
  

def permutation_orbits_distribution(n):
  found_rep = []
  counter_dict = {}
  orbit_dict = {}

  for rep in permutations(n):
    if rep not in found_rep:
      arr = []
      arr.append([rep,inv(rep),maj(rep),foata_distance(rep)])
      found_rep.append(copy.deepcopy(rep))
      foata_rep = foata(rep)
      counter = 1
      while foata_rep != rep:
        found_rep.append(copy.deepcopy(foata_rep))
        arr.append([foata_rep,inv(foata_rep),maj(foata_rep),foata_distance(foata_rep)])
        foata_rep = foata(foata_rep)
        counter += 1
      if counter in counter_dict:
        counter_dict[counter] += 1
        orbit_dict[counter].append(copy.deepcopy(arr))
      else:
        counter_dict[counter] = 1
        orbit_dict[counter] = [copy.deepcopy(arr)]
  print(counter_dict)
  overall_sum = 0
  keys = [key for key,value in counter_dict.items()]
  values = [value for key,value in counter_dict.items()]

  for i in range(len(counter_dict)):
    overall_sum += keys[i]*values[i]
  return orbit_dict



# orbits = permutation_orbits_distribution(5)

# for value in orbits.values():
#   for orbit in value:
#       print(sum([rep[2]+rep[1] for rep in orbit])/len(orbit))

''' The odd even foata bijection '''

def odd_even_foata(rep):
  foata_rep = []
  for i in range(len(rep)):
    foata_rep.append(rep[i])
    odd_even_foata_correct(foata_rep)
  return foata_rep

def odd_even_foata_correct(rep):
  if len(rep)>=2:
    if rep[-2]>rep[-1] and rep[-1]%2 == 0:
      i = len(rep)-2
      while i >=1:
        if not (rep[i-1] > rep[-1] and rep[-1]%2 == 0):
          rep[i-1],rep[i] = rep[i],rep[i-1]
        i-=1
    else:
      i = len(rep)-2
      while i >=1:
        if rep[i-1]>rep[-1] and rep[-1]%2 == 0:
          rep[i-1],rep[i] = rep[i],rep[i-1]
        i-=1

def permutation_orbits_distribution_odd_even(n):
  found_rep = []
  counter_dict = {}
  orbit_dict = {}

  for rep in permutations(n):
    if rep not in found_rep:
      arr = []
      arr.append([rep,inv(rep),stat_even(rep)])
      found_rep.append(copy.deepcopy(rep))
      foata_rep = odd_even_foata(rep)
      counter = 1
      while foata_rep != rep:
        found_rep.append(copy.deepcopy(foata_rep))
        arr.append([foata_rep,inv(foata_rep),stat_even(foata_rep)])
        foata_rep = odd_even_foata(foata_rep)
        counter += 1
      if counter in counter_dict:
        counter_dict[counter] += 1
        orbit_dict[counter].append(copy.deepcopy(arr))
      else:
        counter_dict[counter] = 1
        orbit_dict[counter] = [copy.deepcopy(arr)]
  print(counter_dict)
  overall_sum = 0
  keys = [key for key,value in counter_dict.items()]
  values = [value for key,value in counter_dict.items()]

  for i in range(len(counter_dict)):
    overall_sum += keys[i]*values[i]
  return orbit_dict


''' modolu 3 foata bijection'''

def third_foata(rep):
  foata_rep = []
  for i in range(len(rep)):
    foata_rep.append(rep[i])
    third_foata_correct(foata_rep)
  return foata_rep

def third_foata_correct(rep):
  if len(rep)>=2:
    if rep[-2]>rep[-1] and rep[-1]%3 == 0:
      i = len(rep)-2
      while i >=1:
        if not (rep[i-1] > rep[-1] and rep[-1]%3 == 0):
          rep[i-1],rep[i] = rep[i],rep[i-1]
        i-=1
    else:
      i = len(rep)-2
      while i >=1:
        if rep[i-1]>rep[-1] and rep[-1]%3 == 0:
          rep[i-1],rep[i] = rep[i],rep[i-1]
        i-=1

def permutation_orbits_distribution_third(n):
  found_rep = []
  counter_dict = {}
  orbit_dict = {}

  for rep in permutations(n):
    if rep not in found_rep:
      arr = []
      arr.append([rep,inv(rep),stat_third(rep)])
      found_rep.append(copy.deepcopy(rep))
      foata_rep = third_foata(rep)
      counter = 1
      while foata_rep != rep:
        found_rep.append(copy.deepcopy(foata_rep))
        arr.append([foata_rep,inv(foata_rep),stat_third(foata_rep)])
        foata_rep = third_foata(foata_rep)
        counter += 1
      if counter in counter_dict:
        counter_dict[counter] += 1
        orbit_dict[counter].append(copy.deepcopy(arr))
      else:
        counter_dict[counter] = 1
        orbit_dict[counter] = [copy.deepcopy(arr)]
  print(counter_dict)
  overall_sum = 0
  keys = [key for key,value in counter_dict.items()]
  values = [value for key,value in counter_dict.items()]

  for i in range(len(counter_dict)):
    overall_sum += keys[i]*values[i]
  return orbit_dict

for i in range(5,6):
  orbit_dict = permutation_orbits_distribution(i)
  arr1 = []
   # dictionary with the inversion number as key and the number of permutations in an orbit of length k as the value
  for key,value in orbit_dict.items():
    arr1.append(sum([sum([inv(rep[0]) for rep in orbit]) for orbit in value])/(key*len(value)))
    dist_dict = {}
    for orbit in value:
      for rep in orbit:
        if rep[1] in dist_dict:
          dist_dict[rep[1]]+=1
        else:
          dist_dict[rep[1]]=1
    print(dist_dict)
  print('------------>')

  # sorted_keys = [key for key in dist_dict.keys()]
  # print([dist_dict[key] for key in sorted_keys])
  xml = 5

# for i in range(1,11):
#   orbit_dict_odd_even = permutation_orbits_distribution_odd_even(i)
#   arr2 = []
#   for key,value in orbit_dict_odd_even.items():
#     arr2.append(sum([sum([inv(rep[0]) for rep in orbit]) for orbit in value])/(key*len(value)))


# for i in range(1,9):
#   orbit_dict_third = permutation_orbits_distribution_third(i)
#   arr3 = []
#   for key,value in orbit_dict_third.items():
#     arr3.append(sum([sum([inv(rep[0]) for rep in orbit]) for orbit in value])/(key*len(value)))
#   xml = 5
