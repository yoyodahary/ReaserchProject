import useful_functions as uf

my_set = {1,2,3,4}
counts_inv = {}
counts_maj = {}

partitions = uf.get_partitions(my_set)
for partition in partitions:
    partition = uf.sort_lists_by_largest_element(partition)
    rep = uf.get_representation(partition,len(my_set))
    inv = uf.inv(rep)
    maj = uf.maj(rep)
    if inv not in counts_inv:
      counts_inv[inv] = 1
    else:
      counts_inv[inv] += 1

    if maj not in counts_maj:
      counts_maj[maj] = 1
    else:
      counts_maj[maj] += 1
    print(str(partition)+'  \t'+str(rep) + '\t' +str(inv) + '\t' + str(maj))
print("")
print([counts_inv[x] for x in sorted(counts_inv.keys())])
print([counts_maj[x] for x in sorted(counts_maj.keys())])
