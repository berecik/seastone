

'''First unique element:
Given an array A of N elements, find and print out the first unique element. Sor simplicity, assume that the list is not empty and contains at least one unique element. '''


def first_unique(arr):

    unique = {}

    for x in arr:
        if x in unique:
            unique[x] = False
        else:
            unique[x] = True

    for x, v in unique.items():
        if v:
            return x

    return None

arr = [3,1,1,1,2,3,3,4,4,5,5,6,7,7,2]

# print(first_unique(arr))

'''Numbers :
Write a program which will find all such numbers which are divisible by 7 but are not a multiple of 5, between 2000 and 3200 (both included). The numbers obtained should be printed in a slash-separated sequence on a single line.'''

def numbers(start, end):
    return '/'.join(map(lambda x: str(x), [x for x in range(start - start % 7, end+1, 7) if x % 5 != 0]))

res = numbers(2000, 3200)
print(res)

res = numbers(0, 35)
print(res)