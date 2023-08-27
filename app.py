from flask import Flask,redirect,url_for,render_template,request,session
from datetime import datetime
import ibm_db

app=Flask("__name__")

conn=ibm_db.connect('DATABASE=bludb; HOSTNAME=b1bc1829-6f45-4cd4-bef4-10cf081900bf.c1ogj3sd0tgtu0lqde00.databases.appdomain.cloud; PORT=32304; UID=xrs30327;PWD=5Fljv8ohuf1m9iMH; SECURITY=SSL;SSLCertificate=DigiCertGlobalRootCA.crt','','')
connState=ibm_db.active(conn)
app.secret_key= b'_5#y2L"F4Q8z\n\xec]/'
@app.route("/")
def home():
    return render_template("login.html")

@app.route("/login",methods=['GET','POST'])
def login():
    global uemail
    if request.method=='POST':
        email=request.form['email'].strip()
        password=request.form['pwd']
        type=request.form['type']
        if type=="patient":
            sql="SELECT * FROM PATIENTS where EMAIL=? and PASSWORD=?"
            stmt=ibm_db.prepare(conn,sql)
            ibm_db.bind_param(stmt,1,email)
            ibm_db.bind_param(stmt,2,password)
            ibm_db.execute(stmt)
            acc=ibm_db.fetch_assoc(stmt)  
            if acc:
                session['email']=email
                uemail=session['email']
                return redirect("/patient_home")
            else:
                msg="invalid credentials"
                return render_template("login.html",msg=msg)
        elif type=="donor":
            sql="SELECT * FROM DONOR where EMAIL=? and PASSWORD=?"
            stmt=ibm_db.prepare(conn,sql)
            ibm_db.bind_param(stmt,1,email)
            ibm_db.bind_param(stmt,2,password)
            ibm_db.execute(stmt)
            acc=ibm_db.fetch_assoc(stmt)  
            if acc:
                session['email']=email
                uemail=session['email']
                return redirect("/donor_home")
            else:
                msg="invalid credentials"
                return render_template("login.html",msg=msg)
        elif type=="doctor":
            sql="SELECT * FROM DOCTORS where EMAIL=? and PASSWORD=?"
            stmt=ibm_db.prepare(conn,sql)
            ibm_db.bind_param(stmt,1,email)
            ibm_db.bind_param(stmt,2,password)
            ibm_db.execute(stmt)
            acc=ibm_db.fetch_assoc(stmt)  
            if acc:
                session['email']=email
                uemail=session['email']
                return redirect("/doctor_home")
            else:
                msg="invalid credentials"
                return render_template("login.html",msg=msg)
        elif type=="receptionist":
            sql="SELECT * FROM RECEPTIONIST where HOSPITAL=? and PASSWORD=?"
            stmt=ibm_db.prepare(conn,sql)
            ibm_db.bind_param(stmt,1,email)
            ibm_db.bind_param(stmt,2,password)
            ibm_db.execute(stmt)
            acc=ibm_db.fetch_assoc(stmt)  
            if acc:
                session['email']=email
                uemail=session['email']
                return redirect("/reception_home")
            else:
                msg="invalid credentials"
                return render_template("login.html",msg=msg)
        elif type=="None":
           msg="please select the type of user"
           return render_template("login.html",msg=msg)
    return render_template("login.html")



#-------------------------register--------------------



@app.route("/patient_register",methods=['GET','POST'])
def patient_register():
    if request.method=="POST":
        name=request.form['name']
        email=request.form['email']
        password=request.form['password']
        phone=request.form['phone']
        gender=request.form['gender']
        address=request.form['address']
        pin=request.form['pin']
        print(name,email,password,phone,gender,address,pin)
        sql="SELECT * FROM PATIENTS where EMAIL=?"
        stmt=ibm_db.prepare(conn,sql)
        ibm_db.bind_param(stmt,1,email)
        ibm_db.execute(stmt)
        acc=ibm_db.fetch_assoc(stmt)    
        if acc:
            msg="you have been already registered, pls login!"
            return render_template("login.html",msg=msg)
        else:
            sql="INSERT INTO PATIENTS VALUES(?,?,?,?,?,?,?)"
            stmt=ibm_db.prepare(conn,sql)
            ibm_db.bind_param(stmt,1,name)
            ibm_db.bind_param(stmt,2,email)
            ibm_db.bind_param(stmt,3,password)
            ibm_db.bind_param(stmt,4,phone)
            ibm_db.bind_param(stmt,5,gender)
            ibm_db.bind_param(stmt,6,address)
            ibm_db.bind_param(stmt,7,pin)
            ibm_db.execute(stmt)  
            msg="you have successsfully registred , pls login!"        
            return render_template("login.html",msg=msg)
        
    return render_template("patient_register.html")



@app.route("/donor_register",methods=['GET','POST'])
def donor_register():
    if request.method=="POST":
        name=request.form['name']
        email=request.form['email']
        password=request.form['password']
        gender=request.form['gender']
        sql="SELECT count(*) FROM DONOR where EMAIL=?"
        stmt=ibm_db.prepare(conn,sql)
        ibm_db.bind_param(stmt,1,email)
        ibm_db.execute(stmt)
        acc=ibm_db.fetch_assoc(stmt)    
        if acc['1']==1:
            msg="you have been already registered, pls login!"
            return render_template("login.html",msg=msg)
        else:
            sql="INSERT INTO DONOR VALUES(?,?,?,?)"
            stmt=ibm_db.prepare(conn,sql)
            ibm_db.bind_param(stmt,1,name)
            ibm_db.bind_param(stmt,2,email)
            ibm_db.bind_param(stmt,3,password)
            ibm_db.bind_param(stmt,4,gender)
            ibm_db.execute(stmt)  
            msg="you have successsfully registred , pls login!"        
            return render_template("login.html",msg=msg)
        
    return render_template("donor_register.html")




#---------------------------------------------patient-------------------




@app.route('/patient_home')
def patient_home():
    if 'email' in session:
        return render_template("patient_home.html")
    msg="you signed out pls! login in"
    return render_template("login.html",msg=msg)

@app.route('/patient_history')
def patient_history():
    if 'email' in session:
        sql="SELECT ID,PATIENT_NAME,DOCTOR_NAME,HOSPITAL,DATE,SLOT,DISEASE from APPOINTMENTS where email=?"
        stmt=ibm_db.prepare(conn,sql)
        ibm_db.bind_param(stmt,1,session['email'])
        ibm_db.execute(stmt)
        data = []
        while True:
            row = ibm_db.fetch_assoc(stmt)
            if not row:
                break
            data.append(row)
        return render_template("patient_history.html",data=data)
    msg="you signed out pls! login in"
    return render_template("login.html",msg=msg)

@app.route('/hospital/<hospital_name>')
def hospital(hospital_name):
    if 'email' in session:
        hospital_name=hospital_name.replace('_',' ')
        session['hospital_name']=hospital_name
        sql="SELECT NAME,SPECIALIZATION,EXPERIENCE,FEE FROM DOCTORS where HOSPITAL=?"
        stmt=ibm_db.prepare(conn,sql)
        ibm_db.bind_param(stmt,1,hospital_name)
        ibm_db.execute(stmt)
        data = []
        while True:
            row = ibm_db.fetch_assoc(stmt)
            if not row:
                break
            data.append(row)
        print(data)
        return render_template('hospital_doctor.html', hospital_name=hospital_name,data=data)
    msg="you signed out pls! login in"
    return render_template("login.html",msg=msg)

@app.route('/hospital/appointment',methods=['POST'])
def appointment():
    if 'email' in session:
        current_date = datetime.now()
        formatted_date = current_date.strftime('%Y-%m-%d')
        date=current_date.date()
        application_id=formatted_date.replace('-','')
        sql="SELECT count(*) FROM APPOINTMENTS where DATE=? and HOSPITAL=?"
        stmt=ibm_db.prepare(conn,sql)
        ibm_db.bind_param(stmt,1,date)
        ibm_db.bind_param(stmt,2,session['hospital_name'])
        ibm_db.execute(stmt)
        acc=ibm_db.fetch_assoc(stmt)
        application_id+=str(acc['1'])
        doctorName=request.form['book'].strip()
        hospital_name=session['hospital_name']
        return render_template("appointment.html",doctor_name=doctorName,hospital_name=hospital_name,application_id=application_id,email=session['email'])
    msg="you signed out pls! login in"
    return render_template("login.html",msg=msg)

@app.route('/hospital/book/<id>',methods=['POST'])
def book(id):
    if 'email' in session:
        if request.method=="POST":
            email=request.form['email']
            id=id
            p_name=request.form['patientName']
            d_name=request.form['DoctorName']
            hospital=request.form['hospitalName']
            date=request.form['appointmentDate']
            slot=request.form['appointmentSlot']
            phone=request.form['phoneNumber']
            disease=request.form['diseaseName']
            link=request.form.get('document','')
            if "https" not in link:
                link="No Documents"
            query1="SELECT count(*) FROM APPOINTMENTS where DATE=? and HOSPITAL=? and DOCTOR_NAME=? and SLOT=?"
            stmt1=ibm_db.prepare(conn,query1)
            ibm_db.bind_param(stmt1,1,date)
            ibm_db.bind_param(stmt1,2,hospital)
            ibm_db.bind_param(stmt1,3,d_name)
            ibm_db.bind_param(stmt1,4,slot)
            ibm_db.execute(stmt1)
            acc=ibm_db.fetch_assoc(stmt1)
            if acc['1']==0:
                sql="INSERT INTO APPOINTMENTS VALUES(?,?,?,?,?,?,?,?,?,?)"
                stmt=ibm_db.prepare(conn,sql)
                ibm_db.bind_param(stmt,1,id)
                ibm_db.bind_param(stmt,2,p_name)
                ibm_db.bind_param(stmt,3,d_name)
                ibm_db.bind_param(stmt,4,hospital)
                ibm_db.bind_param(stmt,5,date)
                ibm_db.bind_param(stmt,6,slot)
                ibm_db.bind_param(stmt,7,email)
                ibm_db.bind_param(stmt,8,phone)
                ibm_db.bind_param(stmt,9,disease)
                ibm_db.bind_param(stmt,10,link)
                ibm_db.execute(stmt)  
                msg="you have successsfully booked slot , pls go back!"        
                return render_template("appointment.html",msg=msg,email=session['email'])
            msg="sry the slot is not available pls book another slot!"
            return render_template("appointment.html",doctor_name=d_name,hospital_name=session['hospital_name'],application_id=id,email=session['email'],msg=msg)
    msg="you signed out pls! login in"
    return render_template("login.html",msg=msg)



@app.route("/patient_search",methods=["GET","POST"])
def patient_search():
    if 'email' in session:
        if request.method=="POST":
            disease=request.form['disease'].strip().lower()
            if not disease.isalpha():
                msg="search  does not contains special characters :   "+str(disease)
                return render_template('patient_search.html',msg=msg)
            sql="SELECT HOSPITAL,NAME,FEE,EXPERIENCE,SPECIALIZATION from DOCTORS where SPECIALIZATION=?"
            stmt=ibm_db.prepare(conn,sql)
            ibm_db.bind_param(stmt,1,disease)
            ibm_db.execute(stmt)
            data = []
            while True:
                row = ibm_db.fetch_assoc(stmt)
                if not row:
                    break
                data.append(row)
            if len(data)!=0:
                return render_template('patient_search.html',data=data)
            msg="No Doctors Available for your search   :   "+str(disease)
            return render_template('patient_search.html',msg=msg)

        return render_template("patient_search.html")
    msg="you signed out pls! login in"
    return render_template("login.html",msg=msg)


@app.route("/search",methods=["POST"])
def search():
    if 'email' in session:
        if request.method=="POST":
            current_date = datetime.now()
            formatted_date = current_date.strftime('%Y-%m-%d')
            date=current_date.date()
            application_id=formatted_date.replace('-','')
            sql="SELECT count(*) FROM APPOINTMENTS where DATE=? and HOSPITAL=?"
            stmt=ibm_db.prepare(conn,sql)
            ibm_db.bind_param(stmt,1,date)
            ibm_db.bind_param(stmt,2,request.form['hospital'].strip())
            ibm_db.execute(stmt)
            acc=ibm_db.fetch_assoc(stmt)
            application_id+=str(acc['1'])
            doctorName=request.form['book'].strip()
            hospital_name=request.form['hospital'].strip()
            return render_template("appointment.html",doctor_name=doctorName,hospital_name=hospital_name,application_id=application_id,email=session['email'])
    msg="you signed out pls! login in"
    return render_template("login.html",msg=msg)


@app.route('/book/<id>',methods=['POST'])
def book_search(id):
    if 'email' in session:
        if request.method=="POST":
            email=request.form['email']
            id=id
            p_name=request.form['patientName']
            d_name=request.form['DoctorName']
            hospital=request.form['hospitalName']
            date=request.form['appointmentDate']
            slot=request.form['appointmentSlot']
            phone=request.form['phoneNumber']
            disease=request.form['diseaseName']
            link=request.form.get('document','')
            if "https" not in link:
                link="No Documents"
            query1="SELECT count(*) FROM APPOINTMENTS where DATE=? and HOSPITAL=? and DOCTOR_NAME=? and SLOT=?"
            stmt1=ibm_db.prepare(conn,query1)
            ibm_db.bind_param(stmt1,1,date)
            ibm_db.bind_param(stmt1,2,hospital)
            ibm_db.bind_param(stmt1,3,d_name)
            ibm_db.bind_param(stmt1,4,slot)
            ibm_db.execute(stmt1)
            acc=ibm_db.fetch_assoc(stmt1)
            if acc['1']==0:
                sql="INSERT INTO APPOINTMENTS VALUES(?,?,?,?,?,?,?,?,?,?)"
                stmt=ibm_db.prepare(conn,sql)
                ibm_db.bind_param(stmt,1,id)
                ibm_db.bind_param(stmt,2,p_name)
                ibm_db.bind_param(stmt,3,d_name)
                ibm_db.bind_param(stmt,4,hospital)
                ibm_db.bind_param(stmt,5,date)
                ibm_db.bind_param(stmt,6,slot)
                ibm_db.bind_param(stmt,7,email)
                ibm_db.bind_param(stmt,8,phone)
                ibm_db.bind_param(stmt,9,disease)
                ibm_db.bind_param(stmt,10,link)
                ibm_db.execute(stmt)  
                msg="you have successsfully booked slot , pls go back!"        
                return render_template("appointment.html",msg=msg,email=session['email'],doctor_name=d_name,hospital_name=hospital,application_id=id)
            msg="sry the slot is not available pls book another slot!"
            return render_template("appointment.html",doctor_name=d_name,hospital_name=hospital,application_id=id,email=session['email'],msg=msg)
    msg="you signed out pls! login in"
    return render_template("login.html",msg=msg)

#----------------------------------donor---------------------------------------------------

@app.route("/donor_home")
def donor_home():
    if 'email' in session:
        return render_template("donor_home.html")
    msg="you signed out pls! login in"
    return render_template("login.html",msg=msg)

@app.route("/donor_history")
def donor_history():
    if 'email' in session:
        sql="SELECT * FROM BANK where EMAIL=?"
        stmt=ibm_db.prepare(conn,sql)
        ibm_db.bind_param(stmt,1,session['email'])
        ibm_db.execute(stmt)
        data = []
        while True:
            row = ibm_db.fetch_assoc(stmt)
            if not row:
                break
            data.append(row)
        if len(data)!=0:
            return render_template('donor_history.html',data=data)
        return render_template("donor_history.html")
    msg="you signed out pls! login in"
    return render_template("login.html",msg=msg)

@app.route("/donor_hospital/<hospital_name>")
def donor_hospital(hospital_name):
    if 'email' in session:
        return render_template("donor_hospital.html",hospital_name=hospital_name,email=session['email'])
    msg="you signed out pls! login in"
    return render_template("login.html",msg=msg)


@app.route("/donor_hospital/slot",methods=["POST"])
def slot():
    if 'email' in session:
        if request.method=="POST":
            name=request.form['Name']
            hospital=request.form['hospitalName']
            hospital=hospital.replace('_',' ')
            phone=request.form['phoneNumber']
            email=request.form['email']
            group=request.form['group']
            address=request.form['Address']
            pin=request.form['pin']
            sql="INSERT INTO BANK VALUES(?,?,?,?,?,?,?)"
            stmt=ibm_db.prepare(conn,sql)
            ibm_db.bind_param(stmt,1,name)
            ibm_db.bind_param(stmt,2,email)
            ibm_db.bind_param(stmt,3,hospital)
            ibm_db.bind_param(stmt,4,group)
            ibm_db.bind_param(stmt,5,phone)
            ibm_db.bind_param(stmt,6,address)
            ibm_db.bind_param(stmt,7,pin)
            ibm_db.execute(stmt)  
            msg="you have successsfully booked slot , pls go back!"        
            return render_template("donor_hospital.html",msg=msg,email=session['email'],hospital_name=hospital)
    msg="you signed out pls! login in"
    return render_template("login.html",msg=msg)
    
@app.route("/patient_bank")
def patient_bank():
    if 'email' in session:
        sql="SELECT * FROM PUBLIC"
        stmt=ibm_db.prepare(conn,sql)
        ibm_db.execute(stmt)
        data = []
        while True:
            row = ibm_db.fetch_assoc(stmt)
            if not row:
                break
            data.append(row)
        return render_template("patient_bank.html",data=data)
    msg="you signed out pls! login in"
    return render_template("login.html",msg=msg)

#-----------------------------------doctor------------------------------------------------

@app.route("/doctor_home")
def doctor_home():
    if 'email' in session:
        query="SELECT NAME FROM DOCTORS where EMAIL=?"
        stmt=ibm_db.prepare(conn,query)
        ibm_db.bind_param(stmt,1,session['email'])
        ibm_db.execute(stmt)
        acc=ibm_db.fetch_assoc(stmt)
        if acc:   
            session['d_name']=acc['NAME']
            doctor_name=acc['NAME']
            current_date = datetime.now()
            date=current_date.date()
            sql="SELECT ID,PATIENT_NAME,HOSPITAL,SLOT,DISEASE,LINK FROM APPOINTMENTS where DATE=? and DOCTOR_NAME=?"
            stmt=ibm_db.prepare(conn,sql)
            ibm_db.bind_param(stmt,1,date)
            ibm_db.bind_param(stmt,2,doctor_name)
            ibm_db.execute(stmt)
            data = []
            while True:
                row = ibm_db.fetch_assoc(stmt)
                if not row:
                    break
                data.append(row)
            if len(data)!=0:
                return render_template("doctor_home.html",data=data)
            msg="NO APPOINTMENTS TODAY"
            return render_template("doctor_home.html",msg=msg)
    msg="you signed out pls! login in"
    return render_template("login.html",msg=msg)
    
@app.route("/check_by_date",methods=["GET","POST"])
def check_by_date():
    if 'email' in session:
        if request.method=="POST":
            date=request.form['date']
            sql="SELECT ID,PATIENT_NAME,HOSPITAL,SLOT,DISEASE,LINK FROM APPOINTMENTS where DATE=? and DOCTOR_NAME=?"
            stmt=ibm_db.prepare(conn,sql)
            ibm_db.bind_param(stmt,1,date)
            ibm_db.bind_param(stmt,2,session['d_name'])
            ibm_db.execute(stmt)
            data = []
            while True:
                row = ibm_db.fetch_assoc(stmt)
                if not row:
                    break
                data.append(row)
            if len(data)!=0:
                return render_template("check_by_date.html",data=data)
            msg="NO APPOINTMENTS on "+" : "+str(date)
            return render_template("check_by_date.html",msg=msg)
        
        return render_template("check_by_date.html")
    msg="you signed out pls! login in"
    return render_template("login.html",msg=msg)

#--------------------------------------reception------------------------------------------

@app.route('/reception_home')
def reception_home():
    if 'email' in session:
        current_date = datetime.now()
        date=current_date.date()
        sql="SELECT ID,PATIENT_NAME,DOCTOR_NAME,HOSPITAL,DATE,SLOT,DISEASE from APPOINTMENTS where HOSPITAL=? and DATE=?"
        stmt=ibm_db.prepare(conn,sql)
        ibm_db.bind_param(stmt,1,session['email'])
        ibm_db.bind_param(stmt,2,date)
        ibm_db.execute(stmt)
        data = []
        while True:
            row = ibm_db.fetch_assoc(stmt)
            if not row:
                break
            data.append(row)
        return render_template("reception_home.html",data=data)
    else:
        msg="you are signed out please"
        return render_template("login.html",msg=msg)

@app.route('/reception_donor')
def reception_donor():
    if 'email' in session:
        sql="SELECT NAME,GROUP,PHONE,ADDRESS,PINCODE from BANK where HOSPITAL=?"
        stmt=ibm_db.prepare(conn,sql)
        ibm_db.bind_param(stmt,1,session['email'])
        ibm_db.execute(stmt)
        data = []
        while True:
            row = ibm_db.fetch_assoc(stmt)
            if not row:
                break
            data.append(row)
        return render_template("reception_donor.html",data=data)
    else:
        msg="you are signed out please"
        return render_template("login.html",msg=msg)


@app.route('/reception_edit')
def reception_edit():
    if 'email' in session:
        email=session['email']
        sql="SELECT * FROM PUBLIC WHERE HOSPITAL=?"
        stmt=ibm_db.prepare(conn,sql)
        ibm_db.bind_param(stmt,1,email)
        ibm_db.execute(stmt)
        data = []
        while True:
            row = ibm_db.fetch_assoc(stmt)
            if not row:
                break
            data.append(row)
        return render_template("reception_edit.html",data=data)
    else:
        msg="you are signed out please"
        return render_template("login.html",msg=msg)



@app.route("/edit_blood",methods=['GET','POST'])
def edit_blood():
    if 'email' in session:
        if request.method=="POST":
            email=session['email']
            on=request.form['o-']
            op=request.form['o+']
            ap=request.form['a+']
            an=request.form['a-']
            bn=request.form['b-']
            bp=request.form['b+']
            abp=request.form['ab+']
            abn=request.form['ab-']
            sql="UPDATE PUBLIC SET ON=? , OP=?,AN =?,AP =?,BN =?,BP =?,ABN =?,ABP =? WHERE HOSPITAL=?"
            stmt=ibm_db.prepare(conn,sql)
            ibm_db.bind_param(stmt,1,on)
            ibm_db.bind_param(stmt,2,op)
            ibm_db.bind_param(stmt,3,an)
            ibm_db.bind_param(stmt,4,ap)
            ibm_db.bind_param(stmt,5,bn)
            ibm_db.bind_param(stmt,6,bp)
            ibm_db.bind_param(stmt,7,abn)
            ibm_db.bind_param(stmt,8,abp)
            ibm_db.bind_param(stmt,9,email)
            ibm_db.execute(stmt)
            sql="SELECT * FROM PUBLIC WHERE HOSPITAL=?"
            stmt=ibm_db.prepare(conn,sql)
            ibm_db.bind_param(stmt,1,email)
            ibm_db.execute(stmt)
            data = []
            while True:
                row = ibm_db.fetch_assoc(stmt)
                if not row:
                    break
                data.append(row)
            msg="you have successsfully updated!"
            return render_template("reception_edit.html",data=data,msg=msg)
        msg="something wen wrong please update it again!"        
        return render_template("reception_edit.html",msg=msg)
    else:
        msg="you are signed out please"
        return render_template("login.html",msg=msg)


@app.route('/reception_bank')
def reception_bank():
    if 'email' in session:
        sql="SELECT * FROM PUBLIC"
        stmt=ibm_db.prepare(conn,sql)
        ibm_db.execute(stmt)
        data = []
        while True:
            row = ibm_db.fetch_assoc(stmt)
            if not row:
                break
            data.append(row)
        return render_template("reception_bank.html",data=data)
    msg="you are signed out please"
    return render_template("login.html",msg=msg)


@app.route("/reception_check_by_date",methods=["GET","POST"])
def reception_check_by_date():
    if 'email' in session:
        if request.method=="POST":
            date=request.form['date']
            sql="SELECT ID,PATIENT_NAME,DOCTOR_NAME,DATE,SLOT,DISEASE FROM APPOINTMENTS where DATE=? and HOSPITAL=?"
            stmt=ibm_db.prepare(conn,sql)
            ibm_db.bind_param(stmt,1,date)
            ibm_db.bind_param(stmt,2,session['email'])
            ibm_db.execute(stmt)
            data = []
            while True:
                row = ibm_db.fetch_assoc(stmt)
                if not row:
                    break
                data.append(row)
            if len(data)!=0:
                return render_template("reception_check_by_date.html",data=data)
            msg="NO APPOINTMENTS ON  "+" : "+str(date)
            return render_template("reception_check_by_date.html",msg=msg)
        
        return render_template("reception_check_by_date.html")
    msg="you signed out pls! login in"
    return render_template("login.html",msg=msg)

#-------------------logout---------------------

@app.route("/logout")
def logout():
    session.pop("email",None)
    session.pop("hospital_name",None)
    session.pop("d_name",None)
    return redirect("/login")




if __name__=="__main__":
    app.run(host="0.0.0.0",debug=True)
