result = '52232480\n52233119\n52233721'


answer = all(value.isdigit() for value in result.split())   # checking for a number
print(answer)