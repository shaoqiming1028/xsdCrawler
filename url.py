import os

sum=0;
with open((os.path.join('url.txt')), 'r') as f1:
	data = f1.read()
strlist = data.split('"productId":"')


with open('1.txt', 'w') as f2:
    for item in strlist[1:]:
        try:
            list_link = item.split('"')[0]
            f2.write(list_link + '\n')
            sum+=1
            print(sum)
        except:
            pass