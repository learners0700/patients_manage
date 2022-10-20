import  pandas as pd
import connect_db as db

# sql = "select dname,ddec,money,count,money*count as all_money from report where pnum = '1';"
# df = pd.read_sql(sql,db.db)
# print(df)
# df = df.groupby(["dname","money","ddec"],as_index=False).sum()
# print(df)
pnum = '1665736808094113'
result = db.Report(pnum,'','','','','','','').select_prescription_one()
for items in result:
    for item in items:
        print(item)
print(result)
