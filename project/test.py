
def normalize(x,d):
  return ((d - min(x)) / (max(x) - min(x)))


print(normalize([1,2,3,4,5],3))
print(normalize([10, 20, 30, 40, 50],30))