#This tests whether the given list contains valid recipes saved into the recipe book. 
#It calls isInRecipeBook to check entry by entry if each recipe in the list is in the recipe book.
def validateList(list, recipeBook):
	if(isInRecipeBook(list, recipeBook)):
		print('List contains valid recipes')
		print(list)
		print()
	else:
		print('List contains invalid recipes')
		print(list)
		print()
		
#This test checks whether the list has a valid length. Length can range from 1 to 255.
#Lists of zero recipes are invalid and 256 or greater are invalid.
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

#Checks entry by entry for whether a recipe is in the recipe book.		
def isInRecipeBook(list, recipeBook):
	for i in list:
		found = False
		for j in recipeBook:
			if i == j:
				found = True
		if found == False:
			return False
	return True

#Example test values to show functionality.
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
