import matplotlib.pyplot as plt

from collections import Counter
from os          import listdir

for path in listdir('input'):
  with open('input/' + path) as f:
    next(f)
    counts = Counter(len(line.split()) - 2 for line in f)
  keys, values = zip(*counts.items())

  plt.bar(keys, values)
  plt.xlabel('Number of tags')
  plt.ylabel('Photos')

  plt.show()
