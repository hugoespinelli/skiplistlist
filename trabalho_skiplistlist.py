from skiplistlist import SkiplistList
import pprint
import numpy

skipll = SkiplistList([0,1,2,3])

sentinela = skipll.sentinel

print('skiplistlist')
pprint.pprint(vars(skipll))
print('*'*30)
print('sentinela')
pprint.pprint(vars(sentinela))
node = sentinela.next[0]
for i in range(skipll.n):
	print('*'*30)
	print('next')
	pprint.pprint(vars(node))
	node = node.next[0]

new_list = skipll.truncar(1)
node = sentinela.next[0]

print('###'*20)
print('ARRAY TRUNCADO')
pprint.pprint(vars(skipll))
for i in range(skipll.n):
	print('*'*30)
	print('next')
	pprint.pprint(vars(node))
	node = node.next[0]

node = new_list.sentinel
print('###'*20)
print('RETORNO ARRAY TRUNCADO')
pprint.pprint(vars(new_list))
for i in range(new_list.n):
	print('*'*30)
	print('next')
	pprint.pprint(vars(node))
	node = node.next[0]