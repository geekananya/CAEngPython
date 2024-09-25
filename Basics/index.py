from operations import calc, sequence_ops

print("product:", calc.prd_a_b(63,21))
print("mod:", calc.mod_a_b(673,21))

my_t = (1,23,45,6,1)
print("max in tuple:", sequence_ops.max_list(my_t))

x = {"apple", "banana", "cherry"}
y = {"google", "microsoft", "apple"}
a = {"google", "ibm"}

print("Set Union:", sequence_ops.set_union(x,y,a))