import matplotlib.pyplot as plt

from collections import Counter

path = 'e_shiny_selfies.txt'

with open('input/' + path) as f:
  next(f)
  counts = Counter(tag for line in f for tag in line.split()[2:])
keys, values = zip(*counts.items())

plt.bar(keys, values)
plt.xlabel('Number of tags')
plt.ylabel('Photos')

plt.show()

print(values)
