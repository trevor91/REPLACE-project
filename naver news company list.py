import re

f = open("./coList.txt", 'r')
data = f.read()
f.close()

temp = re.sub('<label for=\"ca_p','\n[<',data)
temp = re.sub('<ul class',']\n<',temp)
temp = re.sub(r'<.*?>',',',temp)
for i in range(10):
	temp = re.sub(r', ',',',temp)
	temp = re.sub(r',,',',',temp)
print(temp)