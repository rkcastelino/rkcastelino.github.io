l1 = [["eat","sleep","repeat"],["eat","sleep","repeat"],["eat","sleep","repeat"],["eat","sleep","repeat"]]

# creating enumerate objects
obj1 = enumerate(l1[1:])

for i, c in obj1:
    print(i)

print( list(enumerate(l1)))
