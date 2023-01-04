import useful_functions as uf

my_set = {1,2,3,4,5}

uf.print_dict(uf.get_a_statistic(uf.get_partitions(my_set),"mah",uf.lb,len(my_set)))
uf.print_dict(uf.get_a_statistic(uf.get_partitions(my_set),"mah",uf.rs,len(my_set)))
uf.print_dict(uf.get_a_statistic(uf.get_partitions(my_set),"can",uf.lb,len(my_set)))
uf.print_dict(uf.get_a_statistic(uf.get_partitions(my_set),"can",uf.rs,len(my_set)))


