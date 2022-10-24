import pymysql
import time

# # 连接数据库，此前在数据库中创建数据库yuketang
# db = pymysql.connect(host="localhost", user="root", password="123456", db="manage")
# # 使用cursor()方法获取操作游标
# cursor = db.cursor()

# # 连接数据库，此前在数据库中创建数据库manage
db = pymysql.connect(host="localhost", user="root", password="123456", db="manage")
# # 使用cursor()方法获取操作游标
cursor = db.cursor()
# cursor = db.cursor(pymysql.cursors.DictCursor)
# ping()使用该方法 ping(reconnect=True) ，那么可以在每次连接之前，会检查当前连接是否已关闭，如果连接关闭则会重新进行连接。
localtime = time.strftime('%Y-%m-%d %H:%M:%S')

# 以微秒生成随机数
def random_num():
    return int(round(time.time() * 1000 * 1000))

class Dbsql:
    def __init__(self,sql):
        self.sql = sql

    # def content_db(self):
    #     db = pymysql.connect(host="localhost", user="root", password="123456", db="manage")
    #     db.ping(reconnect=True)
    #     return db

    # def close_db(self):
    #     self.content_db().close()

    def select_sql(self):
        db.ping(reconnect=True)
        # cursor = db.cursor(pymysql.cursors.DictCursor)
        cursor.execute(self.sql)
        return cursor.fetchall()

    def exp_sql(self):
        db.ping(reconnect=True)
        cursor.execute(self.sql)
        db.commit()


    def del_sql(self):
        pass

# 医生类
class Doctor:
    def __init__(self,dnum,name,sex,age,phone,page):
        self.dnum = dnum
        self.name = name
        self.sex = sex
        self.age = age
        self.phone = phone
        self.page = page

    # 查询医生信息汇总
    def select_doctors(self):
        sql = f"""
            select * from doctors limit {self.page},20;
        """
        result = Dbsql(sql).select_sql()
        db.close()
        return result


    # 查询单个医生信息
    def select_doctor(self):
        sql = f"""
            select * from doctors where dname = '{self.name}';
        """
        result = Dbsql(sql).select_sql()
        db.close()
        return result

    # 查询修改前医生信息
    def select_doctor_b(self):
        sql = f"""
            select * from doctors where dnum = '{self.dnum}';
        """
        result = Dbsql(sql).select_sql()
        db.close()
        return result

    # 查询医生信息总数
    def select_doctor_allnum(self):
        sql = f"""
            select count(*)  from doctors;
        """
        result = Dbsql(sql).select_sql()
        db.close()
        return result

    # 修改医生信息
    def update_doctor(self):
        sql = f"""
            update doctors set dname = '{self.name}',dsex = '{self.sex}',dage = {self.age} ,phone='{self.phone}' where dnum = {self.dnum};
        """
        Dbsql(sql).exp_sql()
        db.close()

    # 添加医生信息
    def add_doctor(self):
        sql1 = "insert into doctors(dnum, dname, dsex, dage, phone) values(%s,%s,%s,%s,%s)"
        sql = sql1 % (repr(self.dnum),repr(self.name),repr(self.sex),repr(self.age),repr(self.phone))
        Dbsql(sql).exp_sql()
        db.close()


# 药品类
class Drug:
    def __init__(self,ser_num,name,method,money,free,page):
        self.ser_num = ser_num
        self.name = name
        self.method = method
        self.money = money
        self.free = free
        self.page = page

    # 查询药品总览
    def select_drugs(self):
        sql = f"""
            select * from drug;
        """
        result = Dbsql(sql).select_sql()
        db.close()
        return result

    # 查询单个药品
    def select_drug(self):
        sql = f"""
            select * from drug where name = '{self.name}';
        """
        result = Dbsql(sql).select_sql()
        db.close()
        return result

    # 查询药品总数
    def select_drugs_num(self):
        sql = f"""
            select count(*) from drug;
        """
        result = Dbsql(sql).select_sql()
        db.close()
        return result

    # 分页查询
    def select_drugs_page(self):
        sql = f"""
            select * from drug limit {self.page},20;
        """
        result = Dbsql(sql).select_sql()
        db.close()
        return result

    # 查询药品修改前
    def select_drugs_before(self):
        sql = f"""
            select * from drug where ser_num = {self.ser_num};
        """
        result = Dbsql(sql).select_sql()
        db.close()
        return result

    # 修改药品信息
    def update_drug(self):
        sql = f"""
            update drug  set name = '{self.name}',method = '{self.method}',money = '{self.money}',pfree='{self.free}' where ser_num = {self.ser_num};
        """
        Dbsql(sql).exp_sql()
        db.close()


    # 添加药品信息
    def add_drug(self):
        sql1 = "insert into drug(name, method, money, pfree) values(%s,%s,%s,%s)"
        sql = sql1 % (repr(self.name),repr(self.method),repr(self.money),repr(self.free))
        Dbsql(sql).exp_sql()
        db.close()

    # 删除药品信息
    def delete_drug(self):
        sql_all = """ select count(*)+1 from drug;"""
        sql = f"""
            delete from drug where ser_num = '{self.ser_num}';
        """
        Dbsql(sql).exp_sql()
        db.close()

    # 查询药品名称列表
    def select_drugname(self):
        sql = f"""
            select name from drug;
        """
        result = Dbsql(sql).select_sql()
        db.close()
        return result

    # 查询药品价格（通过名字查找）
    def select_drugmoney(self):
        sql = f"""
            select money from drug where name = '{self.name}';
        """
        result = Dbsql(sql).select_sql()
        db.close()
        return result

    # 查询药品用法（通过名字查找）
    def select_drugdec(self):
        sql = f"""
            select method from drug where name = '{self.name}';
        """
        result = Dbsql(sql).select_sql()
        db.close()
        return result

# 患者类
class Patient:
    def __init__(self,id,pnum,pname,psex,age,member,phone,addr,page):
        self.id = id
        self.pnum = pnum
        self.pname = pname
        self.psex = psex
        self.age = age
        self.member = member
        self.phone = phone
        self.addr = addr
        self.page = page

    # 查询所有患者
    def select_patients(self):
        sql = f"""
            select * from patients;
        """
        result = Dbsql(sql).select_sql()
        db.close()
        return result

    # 分页查询
    def select_patient_page(self):
        sql = f"""
            select a.id,a.pnum,a.pname,a.psex,a.page,(case when b.type is null then '非会员' else b.type end) as type,a.phone,a.addr from patients a left outer join member b on a.pnum = b.pnum limit {self.page},20;
        """
        result = Dbsql(sql).select_sql()
        db.close()
        return result

    # 根据患者编号查询
    def select_patient_one(self):
        sql = f"""
            select a.id,a.pnum,a.pname,a.psex,a.page,(case when b.type is null then '非会员' else b.type end) as type,a.phone,a.addr from patients a left outer join member b on a.pnum = b.pnum where a.pnum = '{self.pnum}';
        """
        result = Dbsql(sql).select_sql()
        db.close()
        return result

    # 根据患者名称查询
    def select_patient_name(self):
        sql = f"""
            select * from patients where pname = '{self.pname}';
        """
        result = Dbsql(sql).select_sql()
        db.close()
        return result

    # 根据患者手机号查询
    def select_patient_phone(self):
        sql = f"""
            select * from patients where phone = '{self.phone}';
        """
        result = Dbsql(sql).select_sql()
        db.close()
        return result

    # 查询患者总数
    def select_patients_num(self):
        sql = f"""
            select count(*) from patients;
        """
        result = Dbsql(sql).select_sql()
        db.close()
        return result

    # 根据患者编号修改患者信息
    def update_patient(self):
        sql = f"""
            update patients set pname='{self.pname}',psex='{self.psex}',page='{self.age}',member='{self.member}',phone='{self.phone}',addr='{self.addr}' where pnum='{self.pnum}';
        """
        Dbsql(sql).exp_sql()
        db.close()

    # 根据患者编号删除患者
    def delete_patient(self):
        sql = f"""
            delete from patients where pnum = '{self.pnum}';
        """
        Dbsql(sql).exp_sql()
        db.close()

    # 添加医生信息
    def add_patient(self):
        sql1 = "insert into patients(pnum, pname, psex, page, member, phone, addr) values(%s,%s,%s,%s,%s,%s,%s)"
        sql = sql1 % (repr(self.pnum),repr(self.pname),repr(self.psex),repr(self.age),repr(self.member),repr(self.phone),repr(self.addr))
        Dbsql(sql).exp_sql()
        db.close()



# 操作单
class Report:
    def __init__(self,pnum,pname,phone,dname,money,ddec,count,create_time,page=0,index=0):
        self.pnum = pnum
        self.pname = pname
        self.phone = phone
        self.dname = dname
        self.money = money
        self.ddec = ddec
        self.count = count
        self.create_time = create_time
        self.page = page
        self.index = index

    # 开处方单添加到报表
    def create_prescription(self):
        sql1 = "insert into report(pnum, pname, phone, dname,money,ddec,count,create_time,index_1) values(%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        sql = sql1 % (repr(self.pnum),repr(self.pname),repr(self.phone),repr(self.dname),repr(self.money),repr(self.ddec),repr(self.count),repr(self.create_time),repr(self.index))
        # sql = f" insert into report(pnum,create_time) value (2,'{localtime}'); "
        Dbsql(sql).exp_sql()
        db.close()

    # 删除处方单
    def del_prescription(self):
        sql = f"""
            delete from report where id = '{self.pnum}';
        """
        Dbsql(sql).exp_sql()
        db.close()

    # 查询报表单的index，然后提交处方单后+1,用于后面的患者处方单查询
    def select_report_index(self):
        sql = f"""
            SELECT max(index_1) FROM report where pnum = {self.pnum};
        """
        result = Dbsql(sql).select_sql()
        db.close()
        return result

    # 更新index
    def update_report_index(self):
        sql = f"""
            update report set index_1 = {self.index} where index_1 = '0' and pnum = {self.pnum};
        """
        result = Dbsql(sql).exp_sql()
        db.close()

    # 根据患者id和时间去查询处方
    def select_prescription(self):
        # sql = f"""
        #     select * from report where pnum = '{self.pnum}' and date_format(create_time,'YYYYMMDDHHmmss') >= date_format('{self.create_time}','YYYYMMDDHHmmss');
        # """
        sql = f"""
            select id,pnum,pname,phone,dname,money,ddec,count,create_time from report where pnum = '{self.pnum}' and create_time >= '{self.create_time}';
        """
        result = Dbsql(sql).select_sql()
        db.close()
        return result

    # 根据时间和id去差账单总金额
    def select_allmoney(self):
        sql = f"""
            select sum(money * count) from report where pnum = '{self.pnum}' and create_time >= '{self.create_time}';
        """
        result = Dbsql(sql).select_sql()
        db.close()
        return result

    # 患者页面查看单个患者的处方单
    def select_prescription_one(self):
        sql = f"""
            select index_1,dname,money,ddec,create_time,sum(count) as count,sum(all_money) as all_money from 
                (select index_1,dname,money,ddec,DATE_FORMAT(create_time, '%Y-%m-%d') as create_time,count,money*count as all_money from report where pnum = '{self.pnum}') a 
                group by dname,money,ddec,index_1,create_time;
        """
        result = Dbsql(sql).select_sql()
        db.close()
        return result

    # 患者页面查看单个患者的处方单总金额
    def select_prescription_one_money(self):
        sql = f"""
            select sum(money*count) as all_money from report where pnum = '{self.pnum}' and index_1 = '{self.index}'
        """
        result = Dbsql(sql).select_sql()
        db.close()
        return result




class Redis:
    def __init__(self,pnum,times,dname,dfree=0):
        self.pnum = pnum
        self.times = times
        self.dname = dname
        self.dfree = dfree

    # redis表中存储此次开处方的时间，以这个时间为基准来查这次的处方单
    def save_time_redis(self):
        sql1 = "insert into redis(pnum, times, dname,dfree) value (%s,%s,%s,%s)"
        sql = sql1 % (repr(self.pnum), repr(self.times), repr(self.dname),repr(self.dfree))
        Dbsql(sql).exp_sql()
        db.close()

    # 获取此次订单的首次点击时间
    def select_createtime(self):
        sql = f"""
            select times from redis where pnum = '{self.pnum}' limit 1;
        """
        result = Dbsql(sql).select_sql()
        db.close()
        return result

    # 清空缓存
    def del_redis(self):
        sql = f"""
            delete from redis where pnum = '{self.pnum}';
        """
        Dbsql(sql).exp_sql()
        db.close()

    # 更新药品库存
    def update_drugcount(self):
        sql = f"""
            update drug set pfree = pfree - {self.dfree} where name = '{self.dname}';
        """
        Dbsql(sql).exp_sql()
        db.close()
        result = 1
        return result

    # 查询需要更新库存的药品名称和数量
    def select_drugcount(self):
        sql = f"""
            select dname,dfree from redis where pnum = '{self.pnum}' ;
        """
        result = Dbsql(sql).select_sql()
        db.close()
        return result

    # 删除处方单
    def del_prescription(self):
        sql = f"""
            delete from redis where id = '{self.pnum}';
        """
        Dbsql(sql).exp_sql()
        db.close()




# 查询会员信息
class Member:
    def __init__(self,pnum,type,free_money,update_time,care_number,page):
        self.pnum = pnum
        self.type = type
        self.free_money = free_money
        self.update_time = update_time
        self.care_number = care_number
        self.page = page
    def create_member(self):
        sql1 = "insert into member(pnum, type, free_money,update_time,care_number) value (%s,%s,%s,%s,%s)"
        sql = sql1 % (repr(self.pnum), repr(self.type), repr(self.free_money),repr(self.update_time),repr(self.care_number))
        Dbsql(sql).exp_sql()
        db.close()

    def delete_member(self):
        sql = f"""
            delete from member where pnum = '{self.pnum}';
        """
        Dbsql(sql).exp_sql()
        db.close()

    # 查询余额
    def select_free_money(self):
        sql = f"""
            select free_money from member where pnum = '{self.pnum}';
        """
        result = Dbsql(sql).select_sql()
        db.close()
        return result

    # 会员充值
    def member_charge(self):
        sql = f"""
            update member set free_money = free_money + {self.free_money} where pnum = '{self.pnum}';
        """
        Dbsql(sql).exp_sql()
        db.close()

    # 患者界面查询某个会员信息
    def select_member_one(self):
        sql = f"""
            select a.care_number, b.pname, a.type, a.free_money from member a , patients b
             where a.pnum = b.pnum
             and a.pnum = '{self.pnum}';
        """
        result = Dbsql(sql).select_sql()
        db.close()
        return result


    # # ping()使用该方法 ping(reconnect=True) ，那么可以在每次连接之前，会检查当前连接是否已关闭，如果连接关闭则会重新进行连接。
    # db.ping(reconnect=True)
    # # 查询sql语句
    # # cursor对象，pymysql.cursors.DictCursor 返回字典格式
    # cursor = db.cursor(pymysql.cursors.DictCursor)
    # cursor.execute(sql)
    # return cursor.fetchall()


