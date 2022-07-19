a=1

def abc():
  global a
  print(a)
  a = [1,2,3]
  
def xyz():
  print(a)

abc()
xyz()  
