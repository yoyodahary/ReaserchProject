import useful_functions as uf

my_set = {1,2,3,4,5}

# uf.print_dict(uf.get_a_statistic(uf.get_partitions(my_set),"mah",uf.lb,len(my_set)))
# uf.print_dict(uf.get_a_statistic(uf.get_partitions(my_set),"mah",uf.rs,len(my_set)))
# uf.print_dict(uf.get_a_statistic(uf.get_partitions(my_set),"mah",uf.ls,len(my_set)))
# uf.print_dict(uf.get_a_statistic(uf.get_partitions(my_set),"mah",uf.rb,len(my_set)))
# uf.print_dict(uf.get_a_statistic(uf.get_partitions(my_set),"mah",uf.inv,len(my_set)))
# uf.print_dict(uf.get_a_statistic(uf.get_partitions(my_set),"mah",uf.maj,len(my_set)))
# uf.print_dict(uf.get_a_statistic(uf.get_partitions(my_set),"can",uf.lb,len(my_set)))
# uf.print_dict(uf.get_a_statistic(uf.get_partitions(my_set),"can",uf.rs,len(my_set)))
# uf.print_dict(uf.get_a_statistic(uf.get_partitions(my_set),"can",uf.ls,len(my_set)))
# uf.print_dict(uf.get_a_statistic(uf.get_partitions(my_set),"can",uf.rb,len(my_set)))
uf.print_dict(uf.get_a_statistic(uf.get_partitions(my_set),"can",uf.magic_maj,len(my_set)))
print("")
uf.print_dict(uf.get_a_statistic(uf.get_partitions(my_set),"can",uf.magic_inv,len(my_set)))
# uf.print_dict(uf.get_a_statistic(uf.get_partitions(my_set),"can",uf.inv,len(my_set)))
# uf.print_dict(uf.get_a_statistic(uf.get_partitions(my_set),"can",uf.canonical_maj,len(my_set)))

