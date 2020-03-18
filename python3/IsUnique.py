def IsUnique(string):
  #Considering the string in ASCII chars
  max_ascii_unique_char = 128

  if len(string) > 128:
    return False
  
  ascii_bool = [True for i in range(128)] 

  for i in range(len(string)):
    ascii_idx = ord(string[i])
    if ascii_bool[ascii_idx] == False:
      return False
    else:
      ascii_bool[ascii_idx] = False
  
  return True

s = ""
print("String is {}".format(s),IsUnique(s))

s = "123abc"
print("String is {}".format(s),IsUnique(s))

s = "123abc12"
print("String is {}".format(s),IsUnique(s))