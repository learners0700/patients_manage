from flask import Flask,render_template,request,redirect,url_for
from datetime import datetime
import connect_db as db
import functions as func
import math
import time



app = Flask(__name__)
app.secret_key = 'abcd1234bnmv'

# 设置默认界面
@app.route('/')
def root_dir():
    return redirect('/login')

@app.route('/login', methods = ['POST','GET'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    if request.method == 'POST':
        result = func.login()
        if result == 1:
            return redirect('/index')

@app.route('/index')
def main_index():
    return render_template('index_1.html')

@app.route('/logout', methods = ['POST','GET'])
def logout():
    result = func.logout()
    if result == 1:
        return redirect('/login')

# 查询医生信息
@app.route('/select_doctors', methods=['POST','GET'])
def select_doctors():
    all_num = db.Doctor('','','','','','').select_doctor_allnum()
    total_num = math.ceil(list(all_num[0])[0]/20)
    num_list = [i for i in range(1,total_num+1)]
    if request.method == 'GET':
        page = request.args.get('page')
        if page == None:
            page2 = 1
            next_page = 2
            last_page = 1
            db1 = db.Doctor('', '', '', '', '', 0)
            doc_res = db1.select_doctors()
            return render_template('select_doctors_1.html', doc_res=doc_res,num_list=num_list,total_num=total_num
                                   ,page1=page2,next_page=next_page,last_page=last_page)
        elif page == 1:
            next_page = int(page) + 1
            last_page = 1
            db1 = db.Doctor('', '', '', '', '', 0)
            doc_res = db1.select_doctors()
            return render_template('select_doctors_1.html', doc_res=doc_res,num_list=num_list,total_num=total_num
                                   ,page1=page,next_page=next_page,last_page=last_page)

        elif int(page) >= 1:
            next_page = int(page) + 1
            last_page = int(page) - 1
            page_20 = (int(page)-1) * 20
            db1 = db.Doctor('', '', '', '', '', page_20)
            doc_res = db1.select_doctors()
            return render_template('select_doctors_1.html', doc_res=doc_res,num_list=num_list,total_num=total_num
                                   ,page1=page,next_page=next_page,last_page=last_page)

        else:
            page2 = 1
            next_page = 1
            last_page = 1
            db1 = db.Doctor('', '', '', '', '', 0)
            doc_res = db1.select_doctors()
            return render_template('select_doctors_1.html', doc_res=doc_res,num_list=num_list,total_num=total_num
                                   ,page1=page2,next_page=next_page,last_page=last_page)

    if request.method == 'POST':
        doc_name = request.form.get('dname')
        one_doc_result = db.Doctor('',doc_name,'','','','').select_doctor()
        return render_template('select_doctors_1.html', doc_res=one_doc_result)

# 修改医生信息
@app.route('/update_doctor/<items>', methods=['POST','GET'])
def update_doctor(items):
    # print(items)
    items = items.replace('(','').replace("'","").replace(')','').replace(' ','').replace('[','').replace(']','').split(',')
    # print(items)
    dnum = items[1]
    doc_name = items[2]
    doc_sex = items[3]
    doc_age = items[4]
    doc_phone = items[5]
    # print(doc_phone)
    #print(dnum,doc_name,doc_sex,doc_age,doc_phone)
    db1 = db.Doctor(dnum,'','','','','')
    doc_list_new = db1.select_doctor_b()
    # print(doc_list_new)
    if request.method == 'GET':
        return render_template('update_doctor_1.html',doc_list_new=doc_list_new,dnum = dnum,
                               doc_name2=doc_name,doc_sex2=doc_sex,doc_age2=doc_age,doc_phone2=doc_phone)
    if request.method == 'POST':
        doc_name1 = request.form.get('doc_name')
        doc_sex1 = request.form.get('doc_sex')
        doc_age1 = request.form.get('doc_age')
        doc_phone1 = request.form.get('doc_phone')
        # print(doc_name1, doc_sex1, doc_age1, doc_phone1)
        db2 = db.Doctor(dnum,doc_name1,doc_sex1,doc_age1,doc_phone1,'')
        db2.update_doctor()
        #return redirect('/select_doctors')
        return redirect(f'/update_doctor/{items}')

# 添加医生
@app.route('/add_doctor', methods=['POST','GET'])
def add_doctor():
    dnum = db.random_num()
    if request.method == 'GET':
        return render_template('add_doctor_1.html',dnum=dnum)
    if request.method == 'POST':
        doc_name = request.form.get('doc_name')
        doc_sex = request.form.get('doc_sex')
        doc_age = request.form.get('doc_age')
        doc_phone = request.form.get('doc_phone')
        db.Doctor(dnum, doc_name, doc_sex, doc_age, doc_phone,'').add_doctor()
        return redirect('/select_doctors')



# 查询药品信息
@app.route('/select_drug', methods=['POST','GET'])
def select_drug():
    if request.method == 'GET':
        page = request.args.get('page')
        total_num = db.Drug('', '', '', '','','').select_drugs_num()
        total_num = math.ceil(list(total_num[0])[0] / 20)
        num_list = [i for i in range(1,total_num + 1)]
        if page == None:
            page = 1
            last_page = 1
            next_page = 2
            drug_list = db.Drug('','','','','','0').select_drugs_page()
            return render_template('select_drug_1.html',drug_list=drug_list,total_num=total_num,page=page
                                   ,last_page=last_page,next_page=next_page,num_list=num_list)
        elif page == 1:
            page = 1
            last_page = 1
            next_page = 2
            drug_list = db.Drug('','','','','','0').select_drugs_page()
            return render_template('select_drug_1.html',drug_list=drug_list,total_num=total_num,page=page
                                   ,last_page=last_page,next_page=next_page,num_list=num_list)

        elif int(page) >= 1:
            page_20 = (int(page) - 1) * 20
            last_page = int(page) -1
            next_page = int(page) +1
            drug_list = db.Drug('','','','','',page_20).select_drugs_page()
            return render_template('select_drug_1.html',drug_list=drug_list,total_num=total_num,page=page
                                   ,last_page=last_page,next_page=next_page,num_list=num_list)

        else:
            page = 1
            last_page = 1
            next_page = 2
            drug_list = db.Drug('','','','','','0').select_drugs_page()
            return render_template('select_drug_1.html',drug_list=drug_list,total_num=total_num,page=page
                                   ,last_page=last_page,next_page=next_page,num_list=num_list)

    if request.method == 'POST':
        pname = request.form.get('pname')
        drug_list = db.Drug('',pname,'','','','').select_drug()
        return render_template('select_drug_1.html',drug_list=drug_list)

# 修改药品
@app.route('/update_drug/<items>', methods=['POST','GET'])
def update_drug(items):
    items = items.replace('(','').replace("'","").replace(')','').replace(' ','').replace('[','').replace(']','').split(',')
    pnum = items[0]
    pname = items[1]
    pdec = items[2]
    pmoney = items[3]
    pfree = items[4]
    if request.method == 'GET':
        db1 = db.Drug(pnum,'','','','','')
        drug_list_new = db1.select_drugs_before()
        return render_template('update_drug_1.html',pnum=pnum,pname=pname,pdec=pdec,pmoney=pmoney,pfree=pfree,drug_list_new=drug_list_new)

    if request.method == 'POST':
        pser_num = pnum
        pname = request.form.get('pname')
        pdec = request.form.get('pdec')
        pmoney = request.form.get('pmoney')
        pfree = request.form.get('pfree')
        db1 = db.Drug(pser_num,pname,pdec,pmoney,pfree,'')
        db1.update_drug()
        return redirect(f'/update_drug/{items}')


# 增加药品
@app.route('/add_drug', methods=['POST','GET'])
def add_drug():
    if request.method == 'GET':
        return render_template('add_drug_1.html')
    if request.method == 'POST':
        pname = request.form.get('pname')
        pdec = request.form.get('pdec')
        pmoney = request.form.get('pmoney')
        pfree = request.form.get('pfree')
        db.Drug('',pname,pdec,pmoney,pfree,'').add_drug()
        return redirect('/select_drug')

# 删除药品
@app.route('/delete_drug/<items>',methods=['post','get'])
def delete_drug(items):
    items = items.replace('(', '').replace("'", "").replace(')', '').replace(' ', '').replace('[', '').replace(']',
                                                                                                                   '').split(
            ',')
    pnum = items[0]
    if request.method == 'GET':
        db1 = db.Drug(pnum, '', '', '', '', '')
        drug_list_new = db1.select_drugs_before()
        return render_template('delete_drug_1.html',pnum=pnum,drug_list_new=drug_list_new)
    if request.method == 'POST':
        pnum = items[0]
        yes = request.form.get('yes')
        no = request.form.get('no')
        if yes == '确认删除':
            db.Drug(pnum, '', '', '', '', '').delete_drug()
            return redirect('/select_drug')
        if no == '取消删除':
            return redirect('/select_drug')

# 查询药品名称列表list测试
@app.route('/select_drugname',methods=['post','get'])
def select_drugname():
    if request.method =='GET':
        drug_list = db.Drug('','','','','','').select_drugname()
        return render_template('create_prescription.html',drug_list=drug_list)

# 查询所有患者列表
@app.route('/select_patients',methods=['POST','GET'])
def select_patients():
    if request.method == 'GET':
        total_num = db.Patient('', '', '', '', '', '', '', '', '').select_patients_num()
        total_num = math.ceil(list(total_num[0])[0] / 20)
        num_list = [i for i in range(1,total_num + 1)]
        page = request.args.get('page')
        if page == None:
            page2 = 1
            next_page = 2
            last_page = 1
            patient_list = db.Patient('', '', '', '', '', '', '', '', 0).select_patient_page()
            return render_template('select_patients_1.html', patient_list=patient_list, num_list=num_list, total_num=total_num
                                   , page=page2, next_page=next_page, last_page=last_page)
        elif page == 1:
            next_page = int(page) + 1
            last_page = 1
            patient_list = db.Patient('', '', '', '', '', '', '', '', 0).select_patient_page()
            return render_template('select_patients_1.html', patient_list=patient_list, num_list=num_list, total_num=total_num
                                   , page=page, next_page=next_page, last_page=last_page)

        elif int(page) >= 1:
            next_page = int(page) + 1
            last_page = int(page) - 1
            page_20 = (int(page) - 1) * 20
            patient_list = db.Patient('', '', '', '', '', '', '', '', page_20).select_patient_page()
            return render_template('select_patients_1.html', patient_list=patient_list, num_list=num_list, total_num=total_num
                                   , page=page, next_page=next_page, last_page=last_page)

        else:
            page2 = 1
            next_page = 1
            last_page = 1
            patient_list = db.Patient('', '', '', '', '', '', '', '', 0).select_patient_page()
            return render_template('select_patients_1.html', patient_list=patient_list, num_list=num_list, total_num=total_num
                                   , page=page2, next_page=next_page, last_page=last_page)
    if request.method == 'POST':
        input_type = request.form.get('input_type')
        print(input_type)
        if input_type == 'phone':
            phone_number = request.form.get('pname_phone')
            select_patients_phone = db.Patient('', '', '', '', '', '', phone_number, '', '').select_patient_phone()
            print(select_patients_phone)
            return render_template('select_patients_1.html', patient_list=select_patients_phone)
        if input_type == 'drugname':
            drugname = request.form.get('pname_phone')
            select_patients_name = db.Patient('', '', drugname, '', '', '', '', '', '').select_patient_name()
            print(select_patients_name)
            return render_template('select_patients_1.html', patient_list=select_patients_name)

# 修改患者信息
@app.route('/update_patient/<items>',methods=['POST','GET'])
def update_patient(items):
    items = items.replace('(','').replace("'","").replace(')','').replace(' ','').replace('[','').replace(']','').split(',')
    print(items)
    p_num = items[1]
    p_name = items[2]
    p_sex = items[3]
    p_age = items[4]
    memtype = items[5]
    p_phone = items[6]
    p_adr = items[7]
    if request.method == 'GET':
        p_list_new = db.Patient('', p_num, '', '', '', '', '', '', '').select_patient_one()
        return render_template('update_patient.html',p_num=p_num,p_name=p_name,p_sex=p_sex,p_age=p_age,p_phone=p_phone,memtype=memtype,p_adr=p_adr
                               ,p_list_new=p_list_new)
    if request.method == 'POST':
        p_name = request.form.get('p_name')
        p_sex = request.form.get('p_sex')
        p_age = request.form.get('p_age')
        memtype = request.form.get('memtype')
        p_phone = request.form.get('p_phone')
        p_adr = request.form.get('p_adr')
        db.Patient('', p_num, p_name, p_sex, p_age, memtype, p_phone, p_adr, '').update_patient()
        return redirect(url_for('update_patient',items=items))


# 添加患者
@app.route('/add_patient',methods=['POST','GET'])
def add_patient():
    p_num = db.random_num()
    if request.method == 'GET':
        return render_template('add_patient.html',p_num=p_num)
    if request.method == 'POST':
        pname = request.form.get('pname')
        psex = request.form.get('psex')
        page = request.form.get('page')
        member_type = request.form.get('member_type')
        phone = request.form.get('phone')
        paddr = request.form.get('paddr')
        db.Patient('',p_num,pname,psex,page,member_type,phone,paddr,'').add_patient()
        return redirect('/select_patients')

# 开处方
@app.route('/create_prescription/<items>',methods=['POST','GET'])
def create_prescription(items):
    items = items.replace('(', '').replace("'", "").replace(')', '').replace(' ', '').replace('[', '').replace(']',
                                                                                                               '').split(
        ',')
    pnum = items[1]
    name = items[2]
    phone = items[-2]
    localtime = time.strftime('%Y-%m-%d %H:%M:%S')
    if request.method =='GET':
        create_time = db.Redis(pnum, '', '', '').select_createtime()
        if create_time: # 判断create_time这个tuple是否为空，为空的走else
            create_time = list(create_time[0])[0]
            drug_list = db.Drug('', '', '', '', '', '').select_drugname()
            all_money = db.Report(pnum, '', '', '', '', '', '', create_time).select_allmoney()
            prescription_list = db.Report(pnum, '', '', '', '', '', '', create_time).select_prescription()
            if all_money:
                all_money = all_money[0][0]
                return render_template('create_prescription.html', drug_list=drug_list, name=name, pnumber=pnum,
                                   phone=phone, localtime=localtime, prescription_list=prescription_list
                                   ,all_money=all_money)
            else:
                all_money = 0
                return render_template('create_prescription.html', drug_list=drug_list, name=name, pnumber=pnum,
                                       phone=phone, localtime=localtime, prescription_list=prescription_list
                                       , all_money=all_money)
        else:
            drug_list = db.Drug('', '', '', '', '', '').select_drugname()
            all_money = 0
            prescription_list = db.Report(pnum, '', '', '', '', '', '', localtime).select_prescription()
            return render_template('create_prescription.html',drug_list=drug_list,name=name,pnumber=pnum,
                                   phone=phone,localtime=localtime,prescription_list=prescription_list
                                   ,all_money=all_money)
    if request.method == 'POST':
        drugname = request.form.get('drugname')
        number = request.form.get('durgnumber')
        money = db.Drug('',drugname,'','','','').select_drugmoney()
        money = list(money[0])[0]
        dec = request.form.get('dec')
        if dec == '':
            dec = db.Drug('', drugname, '', '', '', '').select_drugdec()
            dec = list(dec[0])[0]
            db.Report(pnum, name, phone, drugname, money, dec, number, localtime).create_prescription()
            # db.Report(pnum, '', '', drugname, '', '', '', localtime).save_time_redis()
            db.Redis(pnum,localtime,drugname,number).save_time_redis()
            return redirect(f'/create_prescription/{items}')
        else:
            db.Report(pnum, name, phone, drugname, money, dec, number, localtime).create_prescription()
            # db.Report(pnum, '', '', drugname, '', '', '', localtime).save_time_redis()
            db.Redis(pnum, localtime, drugname, number).save_time_redis()
            return redirect(f'/create_prescription/{items}')

# 清空redis并且结算
@app.route('/truncate_redis/<pnumber>',methods=['POST','GET'])
def truncate_redis(pnumber):
    # 库存减去开的处方数量
    result = 0
    pnum = pnumber
    select_drugcount = db.Redis(pnum,'','','').select_drugcount()
    for drugname_count in select_drugcount:
        drugname = drugname_count[0]
        count = drugname_count[1]
        result = db.Redis('', '', drugname, count).update_drugcount()
    if result == 1:
        # 清空指定患者的redis
        db.Redis(pnum,'','','').del_redis()

    return redirect('/select_patients')

# 删除处方单中某一条
@app.route('/del_prescription/<items>',methods=['POST','GET'])
def del_prescription(items):
    items = items.replace('(', '').replace("'", "").replace(')', '').replace(' ', '').replace('[', '').replace(']',
                                                                                                               '').split(
        ',')
    report_number = items[0]
    pnum = items[1]
    db.Redis(report_number,"","","").del_prescription()
    db.Report(report_number,'','','','','','','').del_prescription()
    patient_list = db.Patient('', pnum, '', '', '', '', '', '', '').select_patient_one()
    return redirect(url_for('create_prescription',items=patient_list))


# 删除药品
@app.route('/delete_patient/<items>',methods=['post','get'])
def delete_patient(items):
    items = items.replace('(', '').replace("'", "").replace(')', '').replace(' ', '').replace('[', '').replace(']',
                                                                                                                   '').split(
            ',')
    pnum = items[1]
    if request.method == 'GET':
        patient_list_new = db.Patient('', pnum, '', '', '', '', '', '', '').select_patient_one()
        return render_template('delete_patient.html',pnum=pnum,patient_list_new=patient_list_new)
    if request.method == 'POST':
        pnum = items[1]
        yes = request.form.get('yes')
        no = request.form.get('no')
        if yes == '确认删除':
            db.Patient('', pnum, '', '', '', '', '', '', '').delete_patient()
            return redirect(url_for('select_patients'))
        if no == '取消删除':
            return redirect('/select_patients')



if __name__ == '__main__':
    app.run()
