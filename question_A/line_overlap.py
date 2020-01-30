x1 = float(input('X1: '))
x2 = float(input('X2: '))
x3 = float(input('X3: '))
x4 = float(input('X4: '))
max1 = max(x1,x2)
min2 = min(x3,x4)
if max1 >= min2:
	print('They overlap')
else:
	print('They dont overlap')