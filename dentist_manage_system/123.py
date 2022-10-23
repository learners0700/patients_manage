import  pandas as pd
import connect_db as db

ll = ((1, '阿莫西林', '28', '消炎', 1.0, 28.0), (1, '铁头功', '28', '铁头', 1.0, 28.0), (2, '阿莫西林', '28', '消炎', 3.0, 84.0), (2, '如来神掌', '23', '如来', 1.0, 23.0), (2, '掏你鸡鸡', '24', '鸡鸡', 1.0, 24.0), (2, '铁头功', '28', '铁头', 1.0, 28.0), (2, '蛤蟆功', '21', '蛤蟆', 3.0, 63.0), (3, '阿莫西林', '28', '消炎', 1.0, 28.0))
s = set()
for i in ll:
    s.add(i[0])

list_all = []
for num in s:
    list_1 = []
    for i in ll:
        if i[0] == num:
            list_1.append(i)
    list_all.append(list_1)
# print(list_all)

for i in list_all:
    print(i)
