from skiplistlist import SkiplistList
from skiplistsset import SkiplistSSet
import pprint

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

new_list = skipll.truncar2(2)
print(new_list)
# print(new_list)
# print(new_list.next[0])
node = sentinela.next[0]

print('###'*20)
print('ARRAY TRUNCADO')
pprint.pprint(vars(skipll))
for i in range(skipll.n):
	print('*'*30)
	print('next')
	pprint.pprint(vars(node))
	node = node.next[0]

# print('altura do sentinela:', skipll.h)
# print('n de elementos:', skipll.n)
# print('sentinela:', skipll.stack)