
def validateList(list, recipeBook):
	if(isInRecipeBook(list, recipeBook)):
		print('List contains valid recipes')
		print(list)
		print()
	else:
		print('List contains invalid recipes')
		print(list)
		print()
def boundryList(list):
	length = len(list)
	if length > 0 and length <= 255:
		print('List has a valid length')
		print(list)
		print()
	elif length == 0:
		print('List cannot have zero length')
		print(list)
		print()
	elif length > 255:
		print('list cannot be longer than 255')
		print(list)
		print()
		
def isInRecipeBook(list, recipeBook):
	for i in list:
		found = False
		for j in recipeBook:
			if i == j:
				found = True
		if found == False:
			return False
	return True

if __name__ == '__main__':
	validList = ['Chicken', 'Steak']
	invalidList = ['Lego', 'Byte']
	noList = []
	longList = []
	for i in range(256):
		longList.append(i)
	recipeBook = ['Chicken', 'Eggs', 'Steak']
	validateList(validList, recipeBook)
	validateList(invalidList, recipeBook)
	boundryList(validList)
	boundryList(noList)
	boundryList(longList)
