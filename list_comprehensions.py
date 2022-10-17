myList = [1,2,3,4,5]
myList2 = [2*item for item in myList]
print(myList2)

myList3 = list(range(100))
filteredList = [item for item in myList3 if item % 10 == 0]
print(filteredList)

myList4 = list(range(100))
filteredList2 = [item for item in myList3 if item % 10 < 3]
print(filteredList2)

myString = 'My name is Mitesh Patel. I live in Cleveland'
print(myString.split())

def cleanWord(word):
    return word.replace('.', '').lower()

print([cleanWord(word) for word in myString.split()])