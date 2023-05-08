import copy
import numpy as np
import useful_functions as uf

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
#------------------#

def permutations(n):
    if n == 1:
        yield [1]
    else:
        for p in permutations(n - 1):
            for i in range(n):
                yield p[:i] + [n] + p[i:]

#------------------#

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

def inverse_foata_correct(rep, first_digit):
   length = len(rep)
   if length == 0:
      return
   i = 1
   if first_digit > rep[0]:
      while i < length:
        if rep[i] > first_digit:
          rep[i-1],rep[i] = rep[i],rep[i-1]
        i = i+1
   if first_digit < rep[0]:
      while i < length:
        if rep[i] < first_digit :
          rep[i-1],rep[i] = rep[i],rep[i-1]
        i = i+1
    

def inverse_foata(rep):
  reverse_foata_rep = []
  while len(rep)>0:
     reverse_foata_rep.insert(0,rep[-1])
     rep = rep[:-1]
     inverse_foata_correct(rep,reverse_foata_rep[0])
  return reverse_foata_rep   
        

  

#------------------#

def completion(rep):
    return [len(rep)+1-rep[i] for i in range(len(rep))]

def inverse(rep):
    inverse_rep = []
    for i in range(len(rep)):
        inverse_rep.append(0)
    for i in range(len(rep)):
      inverse_rep[rep[i]-1] = i+1
    return inverse_rep

#------------------#

def permutation_orbits_distribution(n,my_foata):
  found_rep = []
  counter_dict = {}
  orbit_dict = {}

  for rep in permutations(n):
      arr = []
      arr.append(rep)
      found_rep.append(copy.deepcopy(rep))
      foata_rep = my_foata(rep)
      counter = 1
      while foata_rep != rep:
        found_rep.append(copy.deepcopy(foata_rep))
        arr.append(foata_rep)
        foata_rep = my_foata(foata_rep)
        counter += 1
      if counter in counter_dict:
        counter_dict[counter] += 1
        orbit_dict[counter].append(copy.deepcopy(arr))
      else:
        counter_dict[counter] = 1
        orbit_dict[counter] = [copy.deepcopy(arr)]
  
  return orbit_dict
      
#------------------#

def compare_arrays_of_arrays(arr1,arr2):
  if len(arr1) != len(arr2):
    return False
  for x in arr1:
    if x not in arr2:
      return False
  for x in arr2:
    if x not in arr1:
      return False
  return True

def homomesy(arr,func):
  sum = 0
  for rep in arr:
    sum += func(rep)
  return sum/len(arr)

#------------------#
def matrix_to_permutation(mat):
  rep = []
  for i in range(len(mat)):
    for j in range(len(mat)):
      if mat[j][i] == 1:
        rep.append(len(mat)-j)
  return rep

def rotate_matrix_90_degrees(mat):
  rot_90_mat = np.zeros((len(mat),len(mat)))
  for i in range(len(mat)):
    for j in range(len(mat)):
      rot_90_mat[i][j] = mat[len(mat)-1-j][i]
  return rot_90_mat

def permutation_to_matrix(rep):
  mat = np.zeros((len(rep),len(rep)))
  for i in range(len(rep)):
    mat[len(rep)-rep[i]][i] = 1
  return mat

def rotation_90_degrees(rep):
   mat = permutation_to_matrix(rep)
   mat = rotate_matrix_90_degrees(mat)
   return matrix_to_permutation(mat)



function_arr = [lambda x: x ,
                completion,
                inverse,
                lambda x: completion(inverse(x)),
                lambda x: inverse(completion(x)),
                lambda x: inverse(completion(inverse(x))),
                lambda x: completion(inverse(completion(x))),
                lambda x: inverse(completion(inverse(completion(x))))]  


function_dict = {
   'id': lambda x: x ,
    'c': completion,
    'i': inverse,
    'ci': lambda x: completion(inverse(x)),
    'ic': lambda x: inverse(completion(x)),
    'ici': lambda x: inverse(completion(inverse(x))),
    'cic': lambda x: completion(inverse(completion(x))),
    'icic': lambda x: inverse(completion(inverse(completion(x))))
}

function_name_dict = {0: 'id',
                 1: 'c',
                 2: 'i',
                 3: 'ci',
                 4: 'ic',
                 5: 'ici',
                 6: 'cic',
                 7: 'icic'}

function_arr_90 = [lambda x: x ,
                    rotation_90_degrees,
                    lambda x:rotation_90_degrees(rotation_90_degrees(x)),
                    lambda x: rotation_90_degrees(rotation_90_degrees(rotation_90_degrees(x))),
                    inverse,
                    completion,
                    lambda x: rotation_90_degrees(rotation_90_degrees(inverse(x))),
                    lambda x: inverse(rotation_90_degrees(x))] 

function_dict_90 = {
    'id': lambda x: x ,
    'q': rotation_90_degrees,
    'q^2': lambda x:rotation_90_degrees(rotation_90_degrees(x)),
    'q^3': lambda x: rotation_90_degrees(rotation_90_degrees(rotation_90_degrees(x))),
    'i': inverse,
    'c': completion,
    'd': lambda x: rotation_90_degrees(rotation_90_degrees(inverse(x))),
    'r': lambda x: inverse(rotation_90_degrees(x))
} 

function_name_dict_90 = {0: 'id',
                 1: 'q',
                 2: 'q^2',
                 3: 'q^3',
                 4: 'i',
                 5: 'c',
                 6: 'd',
                 7: 'r'}    


def permutation_orbits_distribution(n,func):
  found_rep = []
  counter_dict = {}
  orbit_dict = {}

  for rep in permutations(n):
    if rep not in found_rep:
      arr = []
      arr.append(rep)
      found_rep.append(copy.deepcopy(rep))
      func_rep = func(rep)
      counter = 1
      while func_rep != rep:
        found_rep.append(copy.deepcopy(func_rep))
        arr.append(func_rep)
        func_rep = func(func_rep)
        counter += 1
      if counter in counter_dict:
        counter_dict[counter] += 1
        orbit_dict[counter].append(copy.deepcopy(arr))
      else:
        counter_dict[counter] = 1
        orbit_dict[counter] = [copy.deepcopy(arr)]
  return orbit_dict

def is_homomesic(n,func):
  orbit_dict = permutation_orbits_distribution(n,func)
  arr = []
  for key in orbit_dict:
    for orbit in orbit_dict[key]:
      arr.append(homomesy(orbit,uf.des))
      # print(orbit,'\n',len(orbit))
      # print('------------------')
  if not is_identical(arr):
    return "not homomesic"
  return arr

def my_debug(orbit):
    if(len(orbit) == 2):
      for rep in orbit:
        print(rep,uf.des_tuple(rep))
      print('------------------')

def is_identical(arr):
   for x in arr:
     if x != arr[0]:
       return False
   return True

def test(n):
  for func1 in function_arr:
    for func2 in function_arr:
      if func1!=func2:
          arr = is_homomesic(n,lambda x: func1(inverse_foata(func2(foata(x)))))
          if is_identical(arr):
            print(arr[0],len(arr),'homomesic',
                   function_name_dict[function_arr.index(func1)],
                     function_name_dict[function_arr.index(func2)])

def test_90(n):
  for func1 in function_arr_90:
    for func2 in function_arr_90:
      if func1!=func2:
          arr = is_homomesic(n,lambda x: func1(inverse_foata(func2(foata(x)))))
          if is_identical(arr):
            print(arr[0],len(arr),'homomesic',
                   function_name_dict_90[function_arr_90.index(func1)],
                     function_name_dict_90[function_arr_90.index(func2)])


# arr = is_homomesic(3,lambda x: function_dict['ici'](inverse_foata(function_dict['i'](foata(x)))))
# arr = is_homomesic(4,lambda x: function_dict['ici'](inverse_foata(function_dict['i'](foata(x)))))
# print(arr)



test(4)

# arr = []
# n = 6
# func = lambda x: inverse_foata(inverse(foata(x)))
# for rep in permutations(n):
#   orbit_dict = permutation_orbits_distribution(n,func)
#   arr = []
#   for key in orbit_dict:
#     for orbit in orbit_dict[key]:
#       arr.append(homomesy(orbit,uf.des))

# print(len(arr))


# x = [1,2,3,4,5]
# def something(func1,func2,perm):
#   perm = foata(perm)
#   print(perm)
#   perm = func1(perm)
#   print(perm)
#   perm = inverse_foata(perm)
#   print(perm)
#   perm = func2(perm)
#   print(perm)
#   return perm


# rep  = something(function_dict['i'],function_dict['ici'],x)
# print(uf.des(rep))
# print('-------------------')
# while rep != x:
#   rep = something(function_dict['i'],function_dict['ici'],rep)
#   print(uf.des(rep))
#   print('-------------------')
   
  
   
  

   
