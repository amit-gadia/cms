from flask import *
from datetime import *
from werkzeug import *
import mysql.connector
import os

ab=mysql.connector.connect(host="localhost",user="amit",password="password",database="erp",auth_plugin='mysql_native_password')
crs=ab.cursor(buffered=True)
app = Flask(__name__)
app.secret_key = "abc"

gg=[[]]

"""-----------------------------------------------------PAGE MAIN--------------------------------------------------------------------"""
@app.route('/')
def hello_worlda():
   if('user' in session and session.get('userrole')=='admin'):
      return render_template('adminmain.html',user=session.get('user'),userrole=session.get('userrole'))
      
   elif('user' in session and session.get('userrole')=='student'):
      return render_template('usermain.html',user=session.get('user'),userrole=session.get('userrole'))
            
   elif('user' in session and session.get('userrole')=='faculty'):
      return render_template('facultymain.html',user=session.get('user'),userrole=session.get('userrole'))
   else:
      return render_template('index.html')
@app.route('/login',methods=['POST'])
def hello_world():
   if(request.method=='POST'):
      a=request.form['u']
      b=request.form['p']
      sql="select role,name,user_id from users where user_id=%s and passwd=%s;"
      val=a,b
      crs.execute(sql,val)
      gg=crs.fetchall()
      print(gg)
      if(len(gg)!=0):
         sql="select course,branch from addmission where reg_no=%s;"
         ttt=gg[0][2]
         val=(ttt,)
         crs.execute(sql,val)
         ge=crs.fetchall()
         print(ge)
         try:
            if(len(gg)==1):
               print(gg)
               if(gg[0][0]=='admin'):
                  session['userid']=gg[0][2]
                  session['user']=gg[0][1]
                  session['userrole']=gg[0][0]
                  print(session)
                  return render_template('adminmain.html',user=gg[0][1],userrole=gg[0][0])
               elif(gg[0][0]=='student'):
                  
                  session['userid']=gg[0][2]
                  session['user']=gg[0][1]
                  session['userrole']=gg[0][0]
                  
                  session['branch']=ge[0][1]
                  session['code']=ge[0][0]+"+"+ge[0][1]
                  print(session.get('code'))
                  return render_template('usermain.html',user=gg[0][1],userrole=gg[0][0])
               elif(gg[0][0]=='faculty'):
                  
                  session['userid']=gg[0][2]
                  session['user']=gg[0][1]
                  session['userrole']=gg[0][0]
                  
                  return render_template('facultymain.html',user=gg[0][1],userrole=gg[0][0])
            else:
               erro="The User Id And else Password is Incorrect"
               return render_template('index.html',erro=erro)
         except:
            erro="The User Id And Password is Incorrect"
            return render_template('index.html',erro=erro)
      else:
         erro="The User Id And else Password is Incorrect"
         return render_template('index.html',erro=erro)

"""-----------------------------------------------------LOGOUT--------------------------------------------------------------------"""

@app.route('/logout')
def logout():
   
   session.pop('userid', None)
   session.pop('user', None)
   session.pop('userrole', None)
   session.pop('branch', None)
   session.pop('code', None)
   
   
   return hello_worlda()
"""-----------------------------------------------------LOGOUT--------------------------------------------------------------------"""

@app.route('/PROFILE')
def profile():
   useridd=session.get('userid', None)
   print(useridd+"user")
   b=['0','First Name','Last Name','DOB','Father Name','Father Occupation','Mother Name','Mother Occupation','Address','City','State','Number','Gender','Aadhar Number','Course','Branch','Blood Group','REG_ID','TRANSPORT','Bus Number','Pickup Point','HOSTEL','Room Number','Room Type']
   sql="select * from addmission where reg_no=%s;"
   val=(useridd,)
   crs.execute(sql,val)
   pro=(crs.fetchall())
   pro=(pro[0])
   print(pro)
   sql="select BUS_NUMBER,PICK_UP from transport_bus where STUDENT_ID=%s;"
   val=(useridd,)
   crs.execute(sql,val)
   buspro=list(crs.fetchall())
   sql="select room_no,type from hostel_room where stu_id=%s;"
   val=(useridd,)
   crs.execute(sql,val)
   hospro=list(crs.fetchall())
   
   if(len(buspro)==0 and len(hospro)!=0):
      a=pro+hospro[0]
      a=list(a)
      a.insert(18,'NO')
      
      a.insert(19,'NO')
      a.insert(20,'NO')
      
      a.insert(21,'YES')
   elif(len(hospro)==0 and len(buspro)==0):
      a=pro
      a=list(a)
      a.append('NO')
      a.append('NO')
      a.append('NO')
      a.append('NO')
      a.append('NO')
      a.append('NO')
   elif(len(hospro)==0 and len(buspro)!=0):
      a=pro+buspro[0]
      a=list(a)
      a.insert(18,'YES')
      a.append('NO')
      a.append('NO')
      a.append('NO')
   else:
      a=pro+buspro[0]+hospro[0]
   a=list(a)
   if(a[16]=='Ap'):
      a.pop(16)
      a.insert(16,'A+')
   if(a[16]=='An'):
      a.pop(16)
      a.insert(16,'A-')
   if(a[16]=='bp'):
      a.pop(16)
      a.insert(16,'B+')
   if(a[16]=='bp'):
      a.pop(16)
      a.insert(16,'B-')
   if(a[16]=='op'):
      a.pop(16)
      a.insert(16,'O+')
   if(a[16]=='op'):
      a.pop(16)
      a.insert(16,'O-')
   
   
   return render_template('admin_pro.html',t=len(b),c=b,d=a)  

"""-------------------------------------------------COURSE BRANCH PAGE------------------------------------------------------------------------"""
@app.route('/COURSE_BRANCH')
def admin_course():
   ct=0
   sql="select * from branch;"
   crs.execute(sql)
   branches=crs.fetchall()
   print(branches)
   sql="select * from course;"
   crs.execute(sql)
   courses=crs.fetchall()
   sql="select * from subject;"
   crs.execute(sql)
   subject=crs.fetchall()
   if(len(branches)<len(courses) and len(subject)<len(courses)):
      ct=len(courses)
   elif(len(branches)>len(courses) and len(subject)<len(branches)):
      ct=len(branches)
   elif(len(subject)>len(courses) and len(subject)>len(branches)):
      ct=len(subject)
   elif(len(branches)==len(courses)):
      ct=len(branches)
   elif(len(subject)==len(courses)):
      ct=len(courses)
   elif(len(subject)==len(branches)):
      ct=len(branches)
   print(ct)
   return render_template('admin_course.html',ss='/admbr',b=branches,c=courses,br=len(branches),co=len(courses),ct=ct,s=subject,sr=len(subject))  

@app.route('/admbr')
def admbr():
   return admin_course()
@app.route('/abc/<asp>')
def admin_abc(asp):
   sql="delete from branch where branch_name=%s;"
   val=(asp,)
   crs.execute(sql,val)
   ab.commit()
   return admin_course()
@app.route('/addsubject',methods=['POST'])
def admin_add_sub():
   crname=request.form['sname']
   
   sql="insert into subject(sub_name)values(%s);"
   val=(crname,)
   crs.execute(sql,val)
   ab.commit()
   return admbr()

@app.route('/addbranch',methods=['POST'])
def admin_add_branch():
   brname=request.form['bname']
   brfees=request.form['bfees']
   sql="insert into branch(branch_name,branch_fees) values(%s,%s);"
   val=(brname,brfees)
   crs.execute(sql,val)
   ab.commit()
   return admbr()
@app.route('/addcouuse',methods=['POST'])
def admin_add_course():
   crname=request.form['cname']

   sql="insert into course(course_name) values(%s);"
   val=(crname,)
   crs.execute(sql,val)
   ab.commit()
   return admbr()

@app.route('/abd/<asp>')
def admin_abd(asp):
   sql="delete from course where course_name=%s;"
   val=(asp,)
   crs.execute(sql,val)
   ab.commit()
   return admin_course()
@app.route('/sub/<asp>')
def admin_sub(asp):
   sql="delete from subject where sub_name=%s;"
   val=(asp,)
   crs.execute(sql,val)
   ab.commit()
   return admin_course()

"""--------------------------------------------BUS ROUTE PAGE-----------------------------------------------------------------------------"""
"""--------------------------------------------ADD bou ROOM PAGE-----------------------------------------------------------------------------"""
@app.route('/TRANSPORT')
def admin_chetransport():
   ct=0
   sql="select distinct bus_no from route_bus;"
   crs.execute(sql)
   bus_no=crs.fetchall()
   sql="select pick_pt from route;"
   crs.execute(sql)
   ppt=crs.fetchall()
   sql="select * from transport_bus;"
   crs.execute(sql)
   route=crs.fetchall()
   
   return render_template('stu_trans.html',ss='/admbr',p=ppt,pr=len(ppt),b=bus_no,c=route,br=len(bus_no),co=len(route))  
@app.route('/transport/<asp>')
def admin_trans(asp):
   sql="delete from transport_bus where STUDENT_ID=%s;"
   val=(asp,)
   crs.execute(sql,val)
   ab.commit()
   return admin_chetransport()

@app.route('/addbusinfo',methods=['POST'])
def admin_add_trans():
   pp=request.form['pp']
   stu=request.form['stu_id']
   sql="select name from users where user_id= %s;"
   val=(stu,)
   crs.execute(sql,val)
   reg=crs.fetchall()
   ee=reg[0][0]
   print(ee)
   sql="select bus_no,fees from route where pick_pt= %s;"
   val=(pp,)
   crs.execute(sql,val)
   rego=crs.fetchall()
   ef=rego[0][0]
   fe=rego[0][1]
   print(ef)
   
   print(fe)
   sql="insert into transport_bus(BUS_NUMBER,PICK_UP,STUDENT_ID,NAME,FEES) values(%s,%s,%s,%s,%s);"
   val=(ef,pp,stu,ee,fe)
   crs.execute(sql,val)
   ab.commit()
   return admin_chetransport()

@app.route('/BUS_ROUTE')
def admin_route():
   ct=0
   sql="select distinct bus_no from route_bus;"
   crs.execute(sql)
   bus_no=crs.fetchall()
   sql="select * from route;"
   crs.execute(sql)
   route=crs.fetchall()
   
   return render_template('bus_route.html',ss='/admbr',b=bus_no,c=route,br=len(bus_no),co=len(route))  
@app.route('/ascd/<asp>')
def admin_ascd(asp):
   sql="delete from route where pick_pt=%s;"
   val=(asp,)
   crs.execute(sql,val)
   ab.commit()
   return admin_route()

@app.route('/addbusno',methods=['POST'])
def admin_add_busno():
   crname=request.form['bno']

   sql="insert into route_bus(bus_no) values(%s);"
   val=(crname,)
   crs.execute(sql,val)
   ab.commit()
   return admin_route()
@app.route('/addroute',methods=['POST'])
def admin_add_busro():
   crname=request.form['Bus_No']
   pick_pt=request.form['point']
   fees=request.form['busfees']
   sql="insert into route(bus_no,pick_pt,fees) values(%s,%s,%s);"
   val=(crname,pick_pt,fees)
   crs.execute(sql,val)
   ab.commit()
   return admin_route()
"""--------------------------------------------ADD HOSTEL ROOM PAGE-----------------------------------------------------------------------------"""
@app.route('/HOSTEL_ROOM')
def admin_roon():
   ct=0
   sql="select distinct room_no,hostel_room.room_no from room_no left join hostel_room using(room_no) where hostel_room.room_no is NULL;"
   crs.execute(sql)
   bus_no=crs.fetchall()
   sql="select * from hostel_room;"
   crs.execute(sql)
   route=crs.fetchall()
   
   return render_template('hostel_room.html',ss='/admbr',b=bus_no,c=route,br=len(bus_no),co=len(route))  
@app.route('/arrd/<asp>')
def admin_arrd(asp):
   sql="delete from hostel_room where room_no=%s;"
   val=(asp,)
   crs.execute(sql,val)
   ab.commit()
   return admin_roon()

@app.route('/addroom',methods=['POST'])
def admin_add_room():
   crname=request.form['bno']

   sql="insert into room_no(room_no) values(%s);"
   val=(crname,)
   crs.execute(sql,val)
   ab.commit()
   return admin_roon()
@app.route('/addroominfo',methods=['POST'])
def admin_add_horo():
   crname=request.form['Bus_No']
   pick_pt=request.form['point']
   fees=request.form['busfees']
   stu_id=request.form['stu_id']
   local_guardian=request.form['local_guardian']
   address=request.form['address']
   goods_detailsM_P_E=request.form['goods_detailsM_P_E']
   sql="insert into hostel_room(room_no,type,fees,stu_id,local_guardian,address,goods_detailsM_P_E) values(%s,%s,%s,%s,%s,%s,%s);"
   val=(crname,pick_pt,fees,stu_id,local_guardian,address,goods_detailsM_P_E)
   crs.execute(sql,val)
   ab.commit()
   return admin_roon()
"""-------------------------------------------- FACULTY PAGE-----------------------------------------------------------------------------"""

@app.route('/FACULTY')
def admin_faculty(a="",b="",e=""):
   return render_template('admin_faculty.html',c=a,d=b,f=e)  
@app.route('/addfaculty',methods=['POST'])
def admin_add_faculty():
   frname=request.form['frname']
   lname=request.form['lname']
   dob=request.form['dob']
   bsd=request.form['bsd']
   msd=request.form['msd']
   fname=request.form['fname']
   address=request.form['address']
   Blood_group=request.form['Blood_group']
   city=request.form['city']
   state=request.form['state']
   number=request.form['number']
   gender=request.form['gender']
   sql1="select id from faculty;"
   crs.execute(sql1)
   id=crs.fetchall()
   if(len(id)!=0):
      userid=("fac"+frname+"@"+lname+str(id[-1][0]+1))
      pas=frname+"@"+lname
   else:
      userid=("fac"+frname+"@"+lname+str(1))
      pas=frname+"@"+lname
   sql="insert into users(name,user_id,passwd,role)values(%s,%s,%s,%s);"
   val=((frname+lname),userid,pas,'faculty')
   crs.execute(sql,val)
   sql="insert into faculty(frname,lname,dob,bsd,msd,fname,address,Blood_group,city,state,number,gender)values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);"
   val=(frname,lname,dob,bsd,msd,fname,address,Blood_group,city,state,number,gender)
   crs.execute(sql,val)
   ab.commit()
   return admin_faculty(userid,pas,(frname+lname))

"""-------------------------------------------- NOTICE PAGE-----------------------------------------------------------------------------"""

@app.route('/nottice',methods=['POST'])
def admin_add_notice():
   
   evename=request.form['evename']
   evedate=request.form['evedate']
   evetype=request.form['evetype']
   evedesc=request.form['evedesc']
   sql="insert into notice(name,details,date,category)values(%s,%s,%s,%s);"
   val=(evename,evedesc,evedate,evetype)
   crs.execute(sql,val)
   ab.commit()
   return admin_notice()

"""--------------------------------------------TIMETABLE PAGE-----------------------------------------------------------------------------"""
@app.route('/admin_tt',methods=['POST'])
def admin_add_time():
   
   note00=request.form['note00']
   note01=request.form['note01']
   note02=request.form['note02']
   note03=request.form['note03']
   note04=request.form['note04']
   note05=request.form['note05']
   note06=request.form['note06']
   note07=request.form['note07']
   note10=request.form['note10']
   note11=request.form['note11']
   note12=request.form['note12']
   note13=request.form['note13']
   note14=request.form['note14']
   note15=request.form['note15']
   note16=request.form['note16']
   note17=request.form['note17']
   note20=request.form['note20']
   note21=request.form['note21']
   note22=request.form['note22']
   note23=request.form['note23']
   note24=request.form['note24']
   note25=request.form['note25']
   note26=request.form['note26']
   note27=request.form['note27']
   note30=request.form['note30']
   note31=request.form['note31']
   note32=request.form['note32']
   note33=request.form['note33']
   note34=request.form['note34']
   note35=request.form['note35']
   note36=request.form['note36']
   note37=request.form['note37']   
   note40=request.form['note40']
   note41=request.form['note41']
   note42=request.form['note42']
   note43=request.form['note43']
   note44=request.form['note44']
   note45=request.form['note45']
   note46=request.form['note46']
   note47=request.form['note47']
   note50=request.form['note50']
   note51=request.form['note51']
   note52=request.form['note52']
   note53=request.form['note53']
   note54=request.form['note54']
   note55=request.form['note55']
   note56=request.form['note56']
   note57=request.form['note57']
   subnote00=request.form['subnote00']
   subnote01=request.form['subnote01']
   subnote02=request.form['subnote02']
   subnote03=request.form['subnote03']
   subnote04=request.form['subnote04']
   subnote05=request.form['subnote05']
   subnote06=request.form['subnote06']
   subnote07=request.form['subnote07']
   subnote10=request.form['subnote10']
   subnote11=request.form['subnote11']
   subnote12=request.form['subnote12']
   subnote13=request.form['subnote13']
   subnote14=request.form['subnote14']
   subnote15=request.form['subnote15']
   subnote16=request.form['subnote16']
   subnote17=request.form['subnote17']
   subnote20=request.form['subnote10']
   subnote21=request.form['subnote11']
   subnote22=request.form['subnote12']
   subnote23=request.form['subnote13']
   subnote24=request.form['subnote14']
   subnote25=request.form['subnote15']
   subnote26=request.form['subnote16']
   subnote27=request.form['subnote17']
   subnote30=request.form['subnote10']
   subnote31=request.form['subnote11']
   subnote32=request.form['subnote12']
   subnote33=request.form['subnote13']
   subnote34=request.form['subnote14']
   subnote35=request.form['subnote15']
   subnote36=request.form['subnote16']
   subnote37=request.form['subnote17']
   subnote40=request.form['subnote10']
   subnote41=request.form['subnote11']
   subnote42=request.form['subnote12']
   subnote43=request.form['subnote13']
   subnote44=request.form['subnote14']
   subnote45=request.form['subnote15']
   subnote46=request.form['subnote16']
   subnote47=request.form['subnote17']
   subnote50=request.form['subnote10']
   subnote51=request.form['subnote11']
   subnote52=request.form['subnote12']
   subnote53=request.form['subnote13']
   subnote54=request.form['subnote14']
   subnote55=request.form['subnote15']
   subnote56=request.form['subnote16']
   subnote57=request.form['subnote17']
   subcode=request.form['sub_code']
   print(subcode)
   sql="delete from timetable where classcode=%s;"
   val=(subcode,)
   crs.execute(sql,val)
   sql="insert into timetable(sub_name,fac_name,ab,classcode) values(%s,%s,%s,%s);"
   val=[(note00,subnote00,'subnote00',subcode),
        (note01,subnote01,'subnote01',subcode),
        (note02,subnote02,'subnote02',subcode),
        (note03,subnote03,'subnote03',subcode),
        (note04,subnote04,'subnote04',subcode),
        (note05,subnote05,'subnote05',subcode),
        (note06,subnote06,'subnote06',subcode),
        (note07,subnote07,'subnote07',subcode),
        (note10,subnote10,'subnote10',subcode),
        (note11,subnote11,'subnote11',subcode),
        (note12,subnote12,'subnote12',subcode),
        (note13,subnote13,'subnote13',subcode),
        (note14,subnote14,'subnote14',subcode),
        (note15,subnote15,'subnote15',subcode),
        (note16,subnote16,'subnote16',subcode),
        (note17,subnote17,'subnote17',subcode),
        (note20,subnote20,'subnote20',subcode),
        (note21,subnote21,'subnote21',subcode),
        (note22,subnote22,'subnote22',subcode),
        (note23,subnote23,'subnote23',subcode),
        (note24,subnote24,'subnote24',subcode),
        (note25,subnote25,'subnote25',subcode),
        (note26,subnote26,'subnote26',subcode),
        (note27,subnote27,'subnote27',subcode),
        (note30,subnote30,'subnote30',subcode),
        (note31,subnote31,'subnote31',subcode),
        (note32,subnote32,'subnote32',subcode),
        (note33,subnote33,'subnote33',subcode),
        (note34,subnote34,'subnote34',subcode),
        (note35,subnote35,'subnote35',subcode),
        (note36,subnote36,'subnote36',subcode),
        (note37,subnote37,'subnote37',subcode),
        (note40,subnote40,'subnote40',subcode),
        (note41,subnote41,'subnote41',subcode),
        (note42,subnote42,'subnote42',subcode),
        (note43,subnote43,'subnote43',subcode),
        (note44,subnote44,'subnote44',subcode),
        (note45,subnote45,'subnote45',subcode),
        (note46,subnote46,'subnote46',subcode),
        (note47,subnote47,'subnote47',subcode),
        (note50,subnote50,'subnote50',subcode),
        (note51,subnote51,'subnote51',subcode),
        (note52,subnote52,'subnote52',subcode),
        (note53,subnote53,'subnote53',subcode),
        (note54,subnote54,'subnote54',subcode),
        (note55,subnote55,'subnote55',subcode),
        (note56,subnote56,'subnote56',subcode),
        (note57,subnote57,'subnote57',subcode)]
   crs.executemany(sql,val)
   ab.commit()
   return admin_add_timetable()

"""--------------------------------------------EXAM PAGE-----------------------------------------------------------------------------"""
@app.route('/EXAM')
def admin_exam():
   return render_template('admin_exam.html')
"""--------------------------------------------h_t PAGE-----------------------------------------------------------------------------"""

@app.route('/H_T_FACILITY')
def admin_h_t(a="",b="",c="",d=""):
   print(c)
   return render_template('admin_h_t.html',gg=a,ag=b,bg=c,cg=d)

@app.route('/add_h_t_stu',methods=['POST'])
def admin_h_t_stu():
   cfees=request.form['cfess']
   rno=request.form['rnoname']
   sql="insert into fees(stu_id,fees_details)values(%s,%s);"
   val=(rno,cfees)
   crs.execute(sql,val)
   ab.commit()
   return stu_search_fees(rno)

@app.route('/stu_search_h_t',methods=['POST'])
def stu_admin_h_t(stu=""):
   fee=0
   print(stu)
   stu=request.form['rnoname']
   sql="select * from addmission where reg_no=%s;"
   val=(stu,)
   crs.execute(sql,val)
   a=crs.fetchall()
   g=a[0][-1]
   h=a[0][1]
   t=a[0][-4]
   j=a[0][-3]
   print(a[0][-4])
   return admin_h_t(g,h,t,j)
"""--------------------------------------------LIBRARY PAGE-----------------------------------------------------------------------------"""

@app.route('/LIBRARY')
def admin_library(a="",b="",c="",d="",dd=[]):
   print(dd)
   return render_template('admin_library.html',gg=a,ag=b,bg=c,cg=d,de=dd,lend=len(dd))
@app.route('/add_lib_stu',methods=['POST'])
def admin_library_stu():
   cfees=request.form['cfess']
   rno=request.form['rnoname']
   sub_date=date.today()
   due_date=date.today()+timedelta(7)
   sql="insert into library(stu_id,book_id,issue_date,submit_date)values(%s,%s,%s,%s);"
   val=(rno,cfees,sub_date,due_date)
   crs.execute(sql,val)
   return stu_search_library(rno)

@app.route('/stu_search_library',methods=['POST'])
def stu_search_library(stu=""):
   fee=0
   if(stu==""):
      stu=request.form['rnoname']
   sql="select * from addmission where reg_no=%s;"
   val=(stu,)
   crs.execute(sql,val)
   a=crs.fetchall()
   g=a[0][-1]
   h=a[0][1]
   t=a[0][-4]
   j=a[0][-3]
   print(a[0][-4])
   sql="select * from library where stu_id=%s;"
   val=(stu,)
   crs.execute(sql,val)
   dd=crs.fetchall()
   ab.commit()
   return admin_library(g,h,t,j,dd)
@app.route('/abcbook/<asp>/<reg>')
def admin_abce(asp,reg):
   print(asp,reg)
   sql="delete from library where book_id=%s;"
   val=(asp,)
   crs.execute(sql,val)
   ab.commit()
   return stu_search_library(reg)


@app.route('/VIEW_LIBRARY')
def view_library():
   
   stuu=session.get('userid')
   sql="select * from library where stu_id=%s;"
   val=(stuu,)
   crs.execute(sql,val)
   dd=crs.fetchall()
   ab.commit()
   return render_template('stu_library.html',de=dd,lend=len(dd))


"""--------------------------------------------HOSTEL PAGE-----------------------------------------------------------------------------"""
@app.route('/HOSTEL')
def admin_hostel():
   return render_template('admin_hostel.html')


@app.route('/FEES')
def admin_fees(a="",b="",c="",d="",fee=0,tot=0,h="",tt="",ac="",hss=0,toth=0,tran=0,tott=0):
   r=tot-fee
   hr=toth-hss
   tr=tott-tran
   """ts,hs,hr,tr,tt,ht"""
   return render_template('admin_fees.html',gg=a,ag=b,bg=c,cg=d,f=fee,t=tot,r=r,hf=h,tf=tt,ack=ac,ht=toth,hs=hss,hr=hr,ts=tran,tt=tott,tr=tr)

@app.route('/add_fees_stu',methods=['POST'])
def admin_fees_stu():
   cfees=request.form['cfess']
   rno=request.form['rnoname']
   sql="insert into fees(stu_id,fees_details)values(%s,%s);"
   val=(rno,cfees)
   crs.execute(sql,val)
   ab.commit()
   return stu_search_fees(rno)
@app.route('/add_hosfees_stu',methods=['POST'])
def add_hosfees_stu():
   cfees=request.form['cfess']
   rno=request.form['rnoname']
   sql="select * from hostel_room where stu_id=%s;"
   val=(rno,)
   crs.execute(sql,val)
   hos=crs.fetchall()
   print(hos)
   hf=""
   if(len(hos)==1):
      sql="insert into hostel_fees(stu_id,fees_details)values(%s,%s);"
      val=(rno,cfees)
      crs.execute(sql,val)
      ab.commit()
      ack="SUCCESS IN HOSTEL FEES"
   else:
      
      ack="NO HOSTEL "
   
   return stu_search_fees(rno,ack)
@app.route('/add_transfees_stu',methods=['POST'])
def add_transfees_stu():
   cfees=request.form['cfess']
   rno=request.form['rnoname']
   sql="select * from transport_bus where STUDENT_ID=%s;"
   val=(rno,)
   crs.execute(sql,val)
   trans=crs.fetchall()
   print(trans)
   tf=""
   if(len(trans)==1):
      ack="SUCCESS IN TRANSPORT FEES"
      sql="insert into transport_fees(stu_id,fees_details)values(%s,%s);"
      val=(rno,cfees)
      crs.execute(sql,val)
      ab.commit()
   else:
      ack="NO TRANSPORT"
   
   return stu_search_fees(rno,ack)

@app.route('/stu_search_fees',methods=['POST'])
def stu_search_fees(stu="",ack=""):
   fee=0
   hosfee=0
   tranfee=0
   toth=0
   tott=0
   print(stu)
   stu=request.form['rnoname']
   sql="select * from addmission where reg_no=%s;"
   val=(stu,)
   crs.execute(sql,val)
   a=crs.fetchall()
   g=a[0][-1]
   h=a[0][1]
   t=a[0][-4]
   j=a[0][-3]
   print(a[0][-4])
   sql="select * from transport_bus where STUDENT_ID=%s;"
   val=(stu,)
   crs.execute(sql,val)
   trans=crs.fetchall()
   print(trans)
   tf=""
   if(len(trans)==1):
      tf="YES"
   else:
      tf="NO"
   sql="select * from hostel_room where stu_id=%s;"
   val=(stu,)
   crs.execute(sql,val)
   hos=crs.fetchall()
   print(hos)
   hf=""
   if(len(hos)==1):
      hf="YES"
   else:
      hf="NO"

   sql="select * from branch where branch_name=%s;"
   val=(j,)
   crs.execute(sql,val)
   ee=crs.fetchall()
   print(ee)
   tot=int(ee[0][2])
   sql="select * from fees where stu_id=%s;"
   val=(stu,)
   crs.execute(sql,val)
   
   dd=crs.fetchall()
   for i in range(len(dd)):
      fee=fee+int(dd[i][2])
   if(len(hos)==1):
      sql="select fees from hostel_room where stu_id=%s;"
      val=(stu,)
      crs.execute(sql,val)
      ee=crs.fetchall()
      print(ee)
      toth=int(ee[0][0])
      sql="select * from hostel_fees where stu_id=%s;"
      val=(stu,)
      crs.execute(sql,val)
      
      dd=crs.fetchall()
      print(dd)
      for i in range(len(dd)):
         hosfee=hosfee+int(dd[i][2])

   if(len(trans)==1):
      sql="select FEES from transport_bus where STUDENT_ID=%s;"
      val=(stu,)
      crs.execute(sql,val)
      ee=crs.fetchall()
      print(ee)
      tott=int(ee[0][0])
      sql="select * from transport_fees where stu_id=%s;"
      val=(stu,)
      crs.execute(sql,val)
      
      dd=crs.fetchall()
      print(dd)
      for i in range(len(dd)):
         tranfee=tranfee+int(dd[i][2])

      
      
   return admin_fees(g,h,t,j,fee,tot,hf,tf,ack,hosfee,toth,tranfee,tott)
@app.route('/VIEW_FEES')
def view_fees():
   fee=0
   hosfee=0
   tranfee=0
   toth=0
   tott=0
   stu=session.get('branch')
   
   stuu=session.get('userid')
   stu
   sql="select * from transport_bus where STUDENT_ID=%s;"
   val=(stuu,)
   crs.execute(sql,val)
   trans=crs.fetchall()
   print(trans)
   tf=""
   if(len(trans)==1):
      tf="YES"
   else:
      tf="NO"
   sql="select * from hostel_room where stu_id=%s;"
   val=(stuu,)
   crs.execute(sql,val)
   hos=crs.fetchall()
   print(hos)
   hf=""
   if(len(hos)==1):
      hf="YES"
   else:
      hf="NO"
   sql="select * from branch where branch_name=%s;"
   val=(stu,)
   crs.execute(sql,val)
   ee=crs.fetchall()
   print(ee)
   tot=int(ee[0][2])
   fee=0
   sql="select * from fees where stu_id=%s;"
   val=(stuu,)
   crs.execute(sql,val)
   dd=crs.fetchall()
   for i in range(len(dd)):
      fee=fee+int(dd[i][2])

   if(len(hos)==1):
      sql="select fees from hostel_room where stu_id=%s;"
      val=(stuu,)
      crs.execute(sql,val)
      ee=crs.fetchall()
      print(ee)
      toth=int(ee[0][0])
      sql="select * from hostel_fees where stu_id=%s;"
      val=(stuu,)
      crs.execute(sql,val)
      
      dd=crs.fetchall()
      print(dd)
      for i in range(len(dd)):
         hosfee=hosfee+int(dd[i][2])

   if(len(trans)==1):
      sql="select FEES from transport_bus where STUDENT_ID=%s;"
      val=(stuu,)
      crs.execute(sql,val)
      ee=crs.fetchall()
      print(ee)
      tott=int(ee[0][0])
      sql="select * from transport_fees where stu_id=%s;"
      val=(stuu,)
      crs.execute(sql,val)
      
      dd=crs.fetchall()
      print(dd)
      for i in range(len(dd)):
         tranfee=tranfee+int(dd[i][2])
         
   r=tot-fee
   hr=toth-hosfee
   tr=tott-tranfee
   return render_template('stu_fees.html',f=fee,t=tot,r=r,hf=hf,tf=tf,ht=toth,hs=hosfee,hr=hr,ts=tranfee,tt=tott,tr=tr)
@app.route('/stu_fees',methods=['POST'])
def stu_view_fees(stu=""):
   fee=0
   print(stu)
   stu=request.form['rnoname']
   sql="select * from addmission where reg_no=%s;"
   val=(stu,)
   crs.execute(sql,val)
   a=crs.fetchall()
   g=a[0][-1]
   h=a[0][1]
   t=a[0][-4]
   j=a[0][-3]
   print(a[0][-4])
   sql="select * from branch where branch_name=%s;"
   val=(j,)
   crs.execute(sql,val)
   ee=crs.fetchall()
   print(ee)
   tot=int(ee[0][2])
   sql="select * from fees where stu_id=%s;"
   val=(stu,)
   crs.execute(sql,val)
   
   dd=crs.fetchall()
   for i in range(len(dd)):
      fee=fee+int(dd[i][2])
   return view_fees(g,h,t,j,fee,tot)

"""--------------------------------------------NOTICE PAGE-----------------------------------------------------------------------------"""


@app.route('/ADMIN_NOTICE')
def admin_notice():
   sql="select * from notice order by id desc;"
   crs.execute(sql)
   note=crs.fetchall()
   return render_template('admin_notice.html',c=note,t=len(note))
@app.route('/NOTICE')
def stu_notice():
   sql="select * from notice order by id desc;"
   crs.execute(sql)
   note=crs.fetchall()
   return render_template('stunotice.html',c=note,t=len(note))
"""--------------------------------------------CODE_REG PAGE-----------------------------------------------------------------------------"""

@app.route('/CODE_REG')
def admin_result():
   
   ctr=0
   sql="select * from branch;"
   crs.execute(sql)
   branches=crs.fetchall()
   sql="select * from course;"
   crs.execute(sql)
   courses=crs.fetchall()
   sql="select * from code;"
   crs.execute(sql)
   code=crs.fetchall()
   return render_template('admin_result.html',b=branches,c=courses,br=len(branches),co=len(courses),codee=code,lencode=len(code))

@app.route('/accd/<asp>')
def admin_abcd(asp):
   sql="delete from code where code=%s;"
   val=(asp,)
   crs.execute(sql,val)
   ab.commit()
   return admin_result()
@app.route('/def')
def admin_result1():
   ctr=0
   return render_template('abc.html')
"""--------------------------------------------USERS PAGE-----------------------------------------------------------------------------"""

@app.route('/USERS')
def admin_room():
   sql="select * from users;"
   crs.execute(sql)
   note=crs.fetchall()
   print(note)
   return render_template('admin_users.html',c=note,t=len(note))
"""--------------------------------------------VIEW_ATTENDANCE PAGE-----------------------------------------------------------------------------"""

@app.route('/VIEW_ATTENDANCE')
def admin_attenddd():
   idd=(session.get('userid'))
   sql="select * from attendance where stuid=%s;"
   val=(idd,)
   crs.execute(sql,val)
   note=crs.fetchall()
   print(note,idd)
   return render_template('stu_ass.html',c=note,t=len(note))

"""--------------------------------------------VIEW_ASSIGNMENT PAGE-----------------------------------------------------------------------------"""

@app.route('/VIEW_ASSIGNMENT')
def admin_attassign():
   idd=(session.get('code'))
   sql="select * from assignment where code=%s;"
   val=(idd,)
   crs.execute(sql,val)
   note=crs.fetchall()
   
   print(note,idd)
   return render_template('stu_att.html',c=note,t=len(note))
DOWNLOAD_DIRECTORY = "C:\\Users\\DELL\\AppData\\Local\\Programs\\Python\\Python38-32\\New_folder\\uploads\\"
@app.route('/download/<file>')
def down(file):
   print(file)
   return send_from_directory(DOWNLOAD_DIRECTORY, file, as_attachment=True)
app.config['UPLOAD_FOLDER'] = 'C:\\Users\\DELL\\AppData\\Local\\Programs\\Python\\Python38-32\\New_folder\\uploads'

"""--------------------------------------------STUDENT PAGE-----------------------------------------------------------------------------"""
app.route('/STUDENTT')
def stu_add_assign():
   return "hELLO"


@app.route('/STUDENT')
def admin_student(ag="",bg="",eg=""):
   sql="select * from branch;"
   crs.execute(sql)
   branches=crs.fetchall()
   sql="select * from course;"
   crs.execute(sql)
   courses=crs.fetchall()
   return render_template('admin_student.html',b=branches,c=courses,br=len(branches),co=len(courses),cg=ag,dg=bg,fg=eg)

@app.route('/addstudent',methods=['POST'])
def admin_add_stu():
   frname=request.form['frname']
   lname=request.form['lname']
   dob=request.form['dob']
   fname=request.form['fname']
   fo=request.form['fo']
   mname=request.form['mname']
   mo=request.form['mo']
   address=request.form['address']
   Blood_group=request.form['Blood_group']
   city=request.form['city']
   state=request.form['state']
   number=request.form['number']
   gender=request.form['gender']
   
   addno=request.form['addno']
   course=request.form['course']
   branch=request.form['branch']

   sql1="select id from addmission;"
   crs.execute(sql1)
   id=crs.fetchall()
   if(len(id)!=0):
      userid=("stu"+frname+"@"+lname+str(id[-1][0]+1))
      pas=frname+"@"+lname
   else:
      userid=("stu"+frname+"@"+lname+str(1))
      pas=frname+"@"+lname
   sql="insert into users(name,user_id,passwd,role)values(%s,%s,%s,%s);"
   val=((frname+lname),userid,pas,'student')
   crs.execute(sql,val)
   sql="insert into addmission(frname,lname,dob,f_name,f_occ,m_name,m_occ,address,city,state,mob_no,gender,aadhar,course,branch,bg,reg_no)values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);"
   val=(frname,lname,dob,fname,fo,mname,mo,address,city,state,number,gender,addno,course,branch,Blood_group,userid)
   crs.execute(sql,val)
   ab.commit()
   return admin_student(userid,pas,(frname+lname))
"""--------------------------------------------TIME_TABLE PAGE-----------------------------------------------------------------------------"""

@app.route('/TIME_TABLE')
def admin_add_timetable():
   sql="select name from users where role='faculty'";
   crs.execute(sql)
   note=crs.fetchall()
   sql="select * from code;";
   crs.execute(sql)
   code=crs.fetchall()
   sql="select sub_name from subject;"
   crs.execute(sql)
   subnote=crs.fetchall()
   sql="select distinct classcode from timetable;"
   crs.execute(sql)
   classnote=crs.fetchall()
   return render_template('admin_timetable.html',b=['Monday','Tuesday','Wednesday','Thrusday','Friday','Saturday'],notee=note,classnotee=classnote,codee=code,lencode=len(code),lenclassnotee=len(classnote),lenote=len(note),subnotee=subnote,sublenote=len(subnote))

@app.route('/STU_TIME_TABLE')
def view_timetable():
   code=session.get('code')
   print(code)
   
   sql="select * from timetable where classcode=%s;"
   val=(code,)
   crs.execute(sql,val)
   tt=crs.fetchall()
   ff=tt[0][4]
   print(ff)
   c={}
   for i in tt:
      c[i[3]+"a"]=i[1]
      c[i[3]+"b"]=i[2]
   return render_template('stu_time.html',dataa=c,b=['Monday','Tuesday','Wednesday','Thrusday','Friday','Saturday'],kke=ff)

@app.route('/stu_tt',methods=['POST'])
def stu_data(code):   
   code=request.form['code']
   print(code)
   
   sql="select * from timetable where classcode=%s;"
   val=(code,)
   crs.execute(sql,val)
   tt=crs.fetchall()
   ff=tt[0][4]
   print(ff)
   b={}
   for i in tt:
      b[i[3]+"a"]=i[1]
      b[i[3]+"b"]=i[2]
   return view_timetable(b,ff)
@app.route('/FAC_TIME_TABLE')
def fac_view_timetable(data={},kk=""):
   sql="select distinct sub_name from timetable;"
   crs.execute(sql)
   classcode=crs.fetchall()
   print(classcode)
   print(data,kk)
   return render_template('fac_time.html',dataa=data,b=['Monday','Tuesday','Wednesday','Thrusday','Friday','Saturday'],classcodee=classcode,lenclasscode=len(classcode),kke=kk)

@app.route('/stu_fac',methods=['POST'])
def fac_data():   
   fac=request.form['fac']
   
   sql="select * from timetable where sub_name=%s;"
   val=(fac,)
   crs.execute(sql,val)
   tt=crs.fetchall()
   kk=fac
   print(tt)
   b={}
   for i in tt:
      b[i[3]+"a"]=i[1]
      b[i[3]+"b"]=i[2]
      b[i[3]+"c"]=i[4]
   print(b)
   return fac_view_timetable(b,kk)

@app.route('/HELLO',methods=['POST'])
def adview_timetable():
   codr=request.form['ame']
   return "HELLo"

"""--------------------------------------------TIME_TABLE PAGE-----------------------------------------------------------------------------"""



"""--------------------------------------------TIME_TABLE PAGE-----------------------------------------------------------------------------"""








@app.route('/TRANSPORT')
def admin_transport():
   return render_template('admin_transport.html')  

@app.route('/ADD_ATTENDANCE')
def fac_att(ab=[],classs="",dcode=[]):
   sql="select * from code;";
   crs.execute(sql)
   code=crs.fetchall()
   strr="+".join(dcode)
   sql="select * from subject;"
   crs.execute(sql)
   subject=crs.fetchall()
   print(subject)
   return render_template('fac_att.html',codee=code,lencode=len(code),stt=strr,lenab=(len(ab)),a=ab,classs=classs,subject=subject,lensubject=len(subject),lenclasss=len(classs),dcode=dcode)

@app.route('/admin_att',methods=['POST'])
def admin_att():
   ttr=[]
   codr=request.form['sub_code']
   print(codr)
   bbb=codr.partition('+')
   cr=bbb[0]
   br=bbb[-1]
   print(cr,br)
   sql="select frname,lname,reg_no from addmission where course=%s and branch=%s;";
   val=(cr,br)
   btr=[]
   crs.execute(sql,val)
   code=crs.fetchall()
   for i in code:
      b=list(i)
      btr.append(b[2])
   for i in code:
      b=list(i)
      ttr.append("".join(b[0]+b[1]))
   return fac_att(ttr,codr,btr)



@app.route('/add_fees_stu',methods=['POST'])
def fac_att_stu():
   cfees=request.form['cfess'] 
   rno=request.form['rnoname']
   sql="insert into fees(stu_id,fees_details)values(%s,%s);"
   val=(rno,cfees)
   crs.execute(sql,val)
   ab.commit()
   return stu_search_fees(rno)

@app.route('/attdata',methods=['POST'])
def fac_attdata():
   cfees=request.form['abb']
   date=request.form['date']
   time=request.form['time']
   classs=request.form['acb']
   subject=request.form['subject']
   
   print()
   print(cfees,date,time,classs,subject)
   abc=cfees.split('+')
   for i in range(len(abc)):
      dfees=request.form[abc[i]]
      print(dfees,abc[i])
      sql="insert into attendance(class,time,sub,date,stuid,state)values(%s,%s,%s,%s,%s,%s);"
      val=(classs,time,subject,date,abc[i],dfees)
      crs.execute(sql,val)
   ab.commit()
   return fac_att()
@app.route('/adm_cb',methods=['POST'])
def fac_attr_stu():
   branch=request.form['branch']
   course=request.form['course']
   code=course+"+"+branch
   sql="insert into code(branch,course,code)values(%s,%s,%s);"
   val=(branch,course,code)
   crs.execute(sql,val)
   ab.commit()
   return admin_result()
@app.route('/stu_search_fees',methods=['POST'])
def fac_stu_att(stu=""):
   fee=0
   print(stu)
   stu=request.form['rnoname']
   sql="select * from addmission where reg_no=%s;"
   val=(stu,)
   crs.execute(sql,val)
   a=crs.fetchall()
   g=a[0][-1]
   h=a[0][1]
   t=a[0][-4]
   j=a[0][-3]
   print(a[0][-4])
   sql="select * from branch where branch_name=%s;"
   val=(j,)
   crs.execute(sql,val)
   ee=crs.fetchall()
   print(ee)
   tot=int(ee[0][2])
   sql="select * from fees where stu_id=%s;"
   val=(stu,)
   crs.execute(sql,val)
   
   dd=crs.fetchall()
   for i in range(len(dd)):
      fee=fee+int(dd[i][2])
   return admin_fees(g,h,t,j,fee,tot)
@app.route('/ADD_ASSIGNMENT')
def fac_att_ign():
   sql="select distinct classcode from timetable;"
   crs.execute(sql)
   classcode=crs.fetchall()
   return render_template('faculty_add_assignment.html',classcodee=classcode,lenclasscode=len(classcode))




app.config['UPLOAD_FOLDER'] = 'C:\\Users\\DELL\\AppData\\Local\\Programs\\Python\\Python38-32\\New_folder\\uploads'
@app.route('/fac_add_assign',methods=['POST'])
def fac_add_assign():
   code=request.form['code']
   tname=request.form['tname']
   sname=request.form['sname']
   duedate=request.form['duedate']
   note=request.form['note']
   f=request.files['fame']
   f.save(os.path.join(app.config['UPLOAD_FOLDER'],f.filename))
   a=f.filename
   fc_code=session.get('userid')
   sql="insert into assignment(code,tname,sname,duedate,note,a,fc_code) values(%s,%s,%s,%s,%s,%s,%s)"
   val=(code,tname,sname,duedate,note,a,fc_code)
   crs.execute(sql,val)
   ab.commit()
   
   return fac_att_ign()



@app.route('/stu_search_fees',methods=['POST'])
def fac_stu_assign(stu=""):
   fee=0
   print(stu)
   stu=request.form['rnoname']
   sql="select * from addmission where reg_no=%s;"
   val=(stu,)
   crs.execute(sql,val)
   a=crs.fetchall()
   g=a[0][-1]
   h=a[0][1]
   t=a[0][-4]
   j=a[0][-3]
   print(a[0][-4])
   sql="select * from branch where branch_name=%s;"
   val=(j,)
   crs.execute(sql,val)
   ee=crs.fetchall()
   print(ee)
   tot=int(ee[0][2])
   sql="select * from fees where stu_id=%s;"
   val=(stu,)
   crs.execute(sql,val)
   
   dd=crs.fetchall()
   for i in range(len(dd)):
      fee=fee+int(dd[i][2])
   return admin_fees(g,h,t,j,fee,tot)

@app.route('/loadurl',methods=['POST'])
def Url_fetching():
   if('user' in session and session.get('userrole')=='admin'):
      admin=request.form['abc']
      return render_template('adminmain.html',frame="/"+admin,user=session.get('user'),userrole=session.get('userrole'))
   else:
      return hello_worlda()
@app.errorhandler(405)
def eoorr(eno):
   session.pop('user', None)
   session.pop('userrole', None)
   return hello_worlda()
@app.route('/loadstu',methods=['POST'])
def Url_stu_fetching():
   if('user' in session and session.get('userrole')=='student'):
      stu=request.form['abc']
      return render_template('usermain.html',frame="/"+stu,user=session.get('user'),userrole=session.get('userrole'))
   else:
      return hello_worlda()
   
@app.route('/loadfac',methods=['POST'])
def Url_fac_fetching():
   if('user' in session and session.get('userrole')=='faculty'):
      fac=request.form['abc'] 
      return render_template('facultymain.html',frame="/"+fac,user=session.get('user'),userrole=session.get('userrole'))
   else:
      return hello_worlda()
   
if __name__ == '__main__':
   app.run(host="0.0.0.0")
   app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
print(crs.fetchall())
