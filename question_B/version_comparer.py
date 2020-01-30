from random import choice
def compare_versions(v1, v2):
	v1_array = v1.split('.')
	v2_array = v2.split('.')
	len_v1 = len(v1_array)
	len_v2 = len(v2_array)
	min_range = min(len_v1, len_v2)
	for x in range(0, min_range):
		if v1_array[x] == v2_array[x]:
			continue
		elif v1_array[x] < v2_array[x]:
			return f'The version {v1} is less than {v2}.'
			
		elif v1_array[x] > v2_array[x]:
			return f'The version {v1} is greater than {v2}.'
	if len_v1 > len_v2:
		return f'The version {v1} is greater than {v2}.'
	elif len_v1 < len_v2:
		return f'The version {v1} is less than {v2}.'
	else:
		return 'The two versions are the same.'

v1 = input("Version: ")
v2 = input("The other version: ")
print(compare_versions(v1, v2))

####  random generated versions ####
#possible_versions = [0,1,2,3,4,5]
# for x in range(20):
# 	version_1 = str(choice(possible_versions))
# 	version_2 = str(choice(possible_versions))
# 	for y in range(choice(possible_versions)): 
# 		version_1 += '.'+ str(choice(possible_versions))
# 	for z in range(choice(possible_versions)): 
# 		version_2 += '.'+ str(choice(possible_versions))
# 	print(compare_versions(version_1, version_2))