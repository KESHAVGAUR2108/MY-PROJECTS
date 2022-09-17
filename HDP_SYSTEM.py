#HEART DISEASE PREDICTION SYSTEM

from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk      #to display image
from functools import partial
import mysql.connector
from predictionModel import Modelpredict

#module to validate login details entered by the user
def Validate(win,uid,pd,rl):
    userid = uid.get()
    pwd = pd.get()
    role = rl.get()

    #connecting to database
    mydb = mysql.connector.connect(host='localhost',user='root',password = 'keshav21@',database='hdp_system')
    mycursor = mydb.cursor(buffered= True)

    #checking details entered by the user
    #user whose details match with the record in database will allowed to use the system
    if role==1:
        mycursor.execute("select userid,Password from user where Role = 'Administrator'")      #query to fetch details from database
        loginDetails = mycursor.fetchone()              #fetching data from mycursor buffer

        if userid == loginDetails[0] and pwd == loginDetails[1] : 
            admin_dep(win)
        else :
            messagebox.showerror('Error',message='Invalid credentials')
    
    elif role == 2:
        flag = False
        mycursor.execute("select userid,Password from user where Role = 'Doctor'")
        loginDetails = mycursor.fetchall()

        for i in loginDetails:
            if userid == i[0] and pwd == i[1]:
                flag = True
                break
        if flag == True :
            doctor_dep(win)
        else:
                messagebox.showerror('Error',message='Invalid credentials')
    else :
        messagebox.showerror('Error',message='Please fill all the details.')
    
    mydb.close()    #closing database


#module to generate login interface
def login():
    
    #creating window
    top = Tk(className=' Heart Disease Prediction System')
    top['bg'] =   '#FAFAFA' #'#A9E2F3'  #background colour

    #dimension of the window
    top.geometry("800x500")
    #displaying image
    side_img = Image.open("sideImage.png")
    resize_img = side_img.resize((800,500),Image.ANTIALIAS)
    final_img = ImageTk.PhotoImage(resize_img)
    side_logo = Label(top,image = final_img,bg='#FAFAFA').place(x=-10,y=0)

    logo_img = Image.open("logo.png")
    resize_logo = logo_img.resize((123,123),Image.ANTIALIAS)
    logo_final = ImageTk.PhotoImage(resize_logo)
    logo = Label(top,image = logo_final,bg='#FAFAFA').place(x=352,y=52)

    #displaying message
    msg = Label(top,text = "USER LOGIN",font = 'Times 20 bold',fg = '#FAFAFA',bg='#819FF7',width = 100)
    msg.pack()
    
    userid = StringVar()
    pwd = StringVar()

    #created a form to take user id,password and role form the user
    l1 = Label(top,text = "User id : ",font = 'Times 13',bg='#FAFAFA').place(x=296,y=181)
    e1 = Entry(top,textvariable=userid).place(x=369,y=185,width=182)
    
    l2 = Label(top,text = "Password : ",font = 'Times 13 ',bg='#FAFAFA').place(x=294,y=220)
    e2 = Entry(top,textvariable=pwd,show='*').place(x=374,y=222,width=182)

    l3 = Label(top,text="Role : ",font = 'Times 13',bg='#FAFAFA').place(x=296,y=253)
    radio = IntVar()
    R1 = Radiobutton(top,text = "Administrator",font = 'Times 13',bg='#FAFAFA',variable = radio,value=1).place(x=359,y=255)
    R2 = Radiobutton(top,text = "Doctor",font = 'Times 13',bg='#FAFAFA',variable = radio,value=2).place(x=490,y=255)
  
    #login button
    validate = partial(Validate,top,userid,pwd,radio)
    btn = Button(top,text = "Login",font = 'Times 13 bold',bg= "cyan",command = validate).place(x=376,y=305,width=73,height=23)
    top.mainloop() 


#module for admin department
def admin_dep(win):
    win.destroy()
    new_window = Tk(className=' ADMINISTRATION DEPARTMENT')
    new_window['bg'] = '#E6E6E6'

    new_window.geometry('1355x768')
    #interface creation
    logout = partial(logOut,new_window)

    l1 = Label(new_window,text='Welcome To Administration Department',fg='white',font='Times 23 bold',bg='#0080FF',width=100)
    l1.pack() 

    b1 = Button(new_window,text = 'Log out',command = logout,font='Times 12 bold',fg = 'white',bg = '#585858')
    b1.pack(side=TOP,anchor=E)

    l2 = Label(new_window,text='NOTE : You have access to User Account Management, Patient Details and Lab test info. (Table name : user, patient_details, lab_test_info)',font='Times 13 italic bold')
    l2.pack()

    l3 = Label(new_window,text = 'AUTHENTICATION AND AUTHORIZATION',font='Times 14',bg = '#E6E6E6').place(x=435,y=120)
    l4 = Label(new_window,text = 'QUERY (View users/Add/Delete) :  ',font='Times 13',bg='#E6E6E6').place(x = 436,y=190)
  
    textBox = Text(new_window,font = 'Times 14',width=60,height=5)
    textBox.place(x=438,y=217)

    process_query = partial(Process_query,textBox,new_window)   #processing the sql query entered by the admin
                                                                #sql query will be processed in Process_query() 
    
    btn = Button(new_window,text = 'PROCESS',command = process_query,font = 'Times 12',fg='white',bg='#0B0B61').place(x=590, y=340,height=22)
    new_window.mainloop()

#module to process database queries
def Process_query(query,new_window,caller = 1):

    #creating interfaces for showing output of the query
    frame = Frame(new_window) 
    q = ''

    #for each caller output textbox will be at different location and of different size based on the interface
    #each caller has some specific queries except admin
    if caller==1:
        q = query.get(1.0,'end-1c')

        l5 = Label(new_window,text='OUTPUT :: ',font='Times 13 bold',bg = '#E6E6E6').place(x = 443,y=380)
        frame.place(x=443,y=420) 
        textBox = Text(frame,width=80,height=8,wrap=NONE)

    elif caller==2:
        #storing patient details entered by the user in the database
        q = "insert into patient_details values ('"+str(query[0].get())+"','"+str(query[1].get())+"','"+str(query[4].get())+"','"+str(query[3].get())+"','"+str(query[5].get())+"','"
        
        if query[2].get()==3:
            q = q + 'M'+"')"
        elif query[2].get()==4:    
            q = q + 'F'+"')"
        
        l5 = Label(new_window,text='OUTPUT :: ',font='Times 15 bold',bg = '#E6E6E6').place(x = 296,y=370)   
        frame.place(x=421,y=373)
        textBox = Text(frame,width=90,height=15,wrap=NONE)

    elif caller==3:
        #storing lab info. eneterd by the user in the database
        q = "insert into lab_test_info values ('"+str(query[0].get())+"','"+str(query[1].get())+"','"+str(query[2].get())+"','"+str(query[3].get())+"','"+str(query[4].get())+"','"+str(query[5].get())+"','"+str(query[6].get())+"','"+str(query[7].get())+"','"+str(query[8].get())+"','"+str(query[9].get())+"',NULL)"  

        l5 = Label(new_window,text='OUTPUT :: ',font='Times 15 bold',bg = '#E6E6E6').place(x = 296,y=530)   
        frame.place(x=421,y=535)
        textBox = Text(frame,width=90,height=7,wrap=NONE)
    elif caller==4:
        #query to fetch patient details from database
        q = "select * from patient_details where name = '"+str(query.get())+"'"
        l5 = Label(new_window,text='OUTPUT :: ',font='Times 15 bold',bg = '#E6E6E6').place(x=710,y=286)   
        frame.place(x=825,y=286)
        textBox = Text(frame,width=60,height=10,wrap=NONE)

    mydb = mysql.connector.connect(host='localhost',user='root',password = 'keshav21@',database='hdp_system')
    mycursor = mydb.cursor(buffered= True)

    #to process the query
    try:
        mycursor.execute(q) 
        mydb.commit()
        result = mycursor.fetchall() 
        if len(result) == 0:
            textBox.insert(END,'No result found.')
        else:

            header =  mycursor.column_names
            
            i=0

            head = ''
            for i in range(len(header)):
                head += str.ljust(header[i],20,' ')
            
            textBox.insert(END,head+'\n')
                
            j=0
            for r in result:
                for j in range(len(header)):
                    textBox.insert(END,str.ljust(str(r[j]),20,' '))
                textBox.insert(END,'\n')  

    except mysql.connector.errors.ProgrammingError as error:
        textBox.insert(END,error)
    except TypeError:
        textBox.insert(END,'Query processed successfully.')
    except Exception as error:
        textBox.insert(END,error)
    mydb.close()

    #Add a horizontal scrollbar
    sb = Scrollbar(frame)
    sb.pack(side =RIGHT,fill= Y)

    #Add a horizontal scrollbar
    sb_h = Scrollbar(frame,orient=HORIZONTAL)
    sb_h.pack(side=BOTTOM,fill=X)
        
    textBox.config(xscrollcommand=sb_h.set,yscrollcommand=sb.set)

    textBox.pack(side = TOP,expand = True)    
    
    sb_h.config(command=textBox.xview)
    sb.config(command=textBox.yview)

#module to show doctor department interface
def doctor_dep(win):

    win.destroy()
    new_window = Tk(className=' DIAGNOSIS DEPARTMENT')
    new_window['bg'] = '#E6E6E6'

    width,height = str(new_window.winfo_screenwidth()),str(new_window.winfo_screenheight()) 
    new_window.geometry(width+'x'+height)

    l1 = Label(new_window,text='Welcome To Diagnosis Department',fg='red',font='Times 23 bold',bg='white',width=100)
    l1.pack() 

    logout = partial(logOut,new_window)
    b1 = Button(new_window,text = 'Log out',command = logout,font='Times 12 bold',fg = 'white',bg = '#585858').place(x = 1292,y = 43,height = 24)

    Patient_Details = partial(patient_Details,new_window)
    l3 = Label(new_window,text='For adding patient details  :: ',font='Times 14 italic bold',bg = '#E6E6E6').place(x = 400,y=150)    
    b1 = Button(new_window,text = 'CLICK HERE',command = Patient_Details ,font='Times 13',bg = 'orange',height=1).place(x = 780,y = 151)

    lab_Test = partial(Lab_Test,new_window)
    l3 = Label(new_window,text='For adding Lab test information  :: ',font='Times 14 italic bold',bg = '#E6E6E6').place(x = 400,y=220)    
    b1 = Button(new_window,text = 'CLICK HERE',command = lab_Test,font='Times 13',bg = 'white',height=1).place(x = 780,y = 221)

    l3 = Label(new_window,text='For Report Generation  :: ',font='Times 14 italic bold',bg = '#E6E6E6').place(x = 400,y=290)    
   
    generate_report = partial(Generate_Report,new_window)
    b1 = Button(new_window,text = 'CLICK HERE',command = generate_report,font='Times 13',bg = 'red',height=1).place(x = 780,y = 290)
    new_window.mainloop()

#module for logout
def logOut(win):
    win.destroy()
    login()

#module to take patient details from user using form interface
def patient_Details(win):

    win.destroy()

    #interface designing
    patient_window = Tk(className=' PATIENT DETAILS PORTAL')
    patient_window['bg'] = '#E6E6E6'
    
    patient_window.geometry('1355x768')

    #displaying message
    msg = Label(patient_window,text = "PATIENT DETAILS ",font = 'Times 20 bold',fg = '#FAFAFA',bg='#819FF7',width = 100)
    msg.pack()   
   
    goback = partial(goBack,patient_window)
    b1 = Button(patient_window,text = 'Go back',command = goback,font='Times 12',bg = 'blue')
    b1.pack(side=TOP,anchor=E)     

    pid,name,cntct,dob,doc = StringVar(),StringVar(),StringVar(),StringVar(),StringVar()
    sex = IntVar()
    list = []

    l1 = Label(patient_window,text = "Fill this form to add patient details :: ",font = 'Times 16 bold',bg='black',fg='white').place(x=475,y=53)   

    l2 = Label(patient_window,text = "Enter Patient ID : ",font = 'Times 12 bold',bg='#E6E6E6').place(x=296,y=107)
    e1 = Entry(patient_window,textvariable=pid,width=35).place(x=450,y=110)
    list.append(pid)
    l3 = Label(patient_window,text = "Name : ",font = 'Times 12 bold',bg='#E6E6E6').place(x=296,y=137)
    e2 = Entry(patient_window,textvariable=name,width=35).place(x=450,y=140)    
    list.append(name)
    l4 = Label(patient_window,text = "Sex : ",font = 'Times 12 bold',bg='#E6E6E6').place(x=296,y=167)
    R1 = Radiobutton(patient_window,text = "Male",font = 'Times 12',bg='#E6E6E6',variable=sex,value=3).place(x=445,y=169)
    R2 = Radiobutton(patient_window,text = "Female",font = 'Times 12',bg='#E6E6E6',variable=sex,value=4).place(x=550,y=169)
    list.append(sex)
    l5 = Label(patient_window,text = "Contact No. : ",font = 'Times 12 bold',bg='#E6E6E6').place(x=296,y=197)
    e4 = Entry(patient_window,textvariable=cntct,width=35).place(x=450,y=200) 
    list.append(cntct)
    l6 = Label(patient_window,text = "Date Of Birth : ",font = 'Times 12 bold',bg='#E6E6E6').place(x=296,y=227)
    e5 = Entry(patient_window,textvariable=dob,width=35).place(x=450,y=230) 
    list.append(dob)
    l7 = Label(patient_window,text = "Date Of CheckUp : ",font = 'Times 12 bold',bg='#E6E6E6').place(x=296,y=257)
    e6 = Entry(patient_window,textvariable=doc,width=35).place(x=450,y=260)
    list.append(doc)

    process_query = partial(Process_query,list,patient_window,2)
    
    btn = Button(patient_window,text = 'PROCESS',command = process_query,font = 'Times 12',fg='white',bg='#0B0B61').place(x=500, y=315,height=22)
    patient_window.mainloop()    

#module to take lab_test_info from user using form interface
def Lab_Test(win):
    
    win.destroy()
    #designing interface
    labtest_window = Tk(className=' LAB TEST INFO PORTAL')
    labtest_window['bg'] = '#E6E6E6'

    labtest_window.geometry('1357x768')

    #displaying message
    msg = Label(labtest_window,text = "LAB TEST INFO ",font = 'Times 20 bold',fg = '#FAFAFA',bg='#819FF7',width = 100)
    msg.pack()   
   
    goback = partial(goBack,labtest_window)
    b1 = Button(labtest_window,text = 'Go back',command = goback,font='Times 12',bg = 'blue')
    b1.pack(side=TOP,anchor=E)

    pid,cpt,rbp,chl,fbs,recg,mhr,eang,op,slp = StringVar(),StringVar(),StringVar(),StringVar(),StringVar(),StringVar(),StringVar(),StringVar(),StringVar(),StringVar()
    list = []

    l1 = Label(labtest_window,text = "Fill this form to add patient lab test info :: ",font = 'Times 16 bold',bg='black',fg='white').place(x=475,y=53)
    
    l2 = Label(labtest_window,text = "Enter Patient ID : ",font = 'Times 12 bold',bg='#E6E6E6').place(x=296,y=107)
    e1 = Entry(labtest_window,textvariable=pid,width=35).place(x=450,y=110)
    list.append(pid)
    l3 = Label(labtest_window,text = "Chest Pain Type : ",font = 'Times 12 bold',bg='#E6E6E6').place(x=296,y=137)
    e2 = Entry(labtest_window,textvariable=cpt,width=35).place(x=450,y=140)    
    list.append(cpt)
    l4 = Label(labtest_window,text = "Resting BP : ",font = 'Times 12 bold',bg='#E6E6E6').place(x=296,y=167)
    e3 = Entry(labtest_window,textvariable=rbp,width=35).place(x=450,y=170)
    list.append(rbp)
    l5 = Label(labtest_window,text = "Cholesterol : ",font = 'Times 12 bold',bg='#E6E6E6').place(x=296,y=197)
    e4 = Entry(labtest_window,textvariable=chl,width=35).place(x=450,y=200) 
    list.append(chl)
    l6 = Label(labtest_window,text = "Fasting BS : ",font = 'Times 12 bold',bg='#E6E6E6').place(x=296,y=227)
    e5 = Entry(labtest_window,textvariable=fbs,width=35).place(x=450,y=230) 
    list.append(fbs)
    l7 = Label(labtest_window,text = "Resting ECG : ",font = 'Times 12 bold',bg='#E6E6E6').place(x=296,y=257)
    e6 = Entry(labtest_window,textvariable=recg,width=35).place(x=450,y=260)
    list.append(recg)
    l8 = Label(labtest_window,text = "Max HR : ",font = 'Times 12 bold',bg='#E6E6E6').place(x=296,y=287)
    e7 = Entry(labtest_window,textvariable=mhr,width=35).place(x=450,y=290)
    list.append(mhr)
    l9 = Label(labtest_window,text = "Exercise Angina : ",font = 'Times 12 bold',bg='#E6E6E6').place(x=296,y=317)
    e8 = Entry(labtest_window,textvariable=eang,width=35).place(x=450,y=320)
    list.append(eang)
    l10 = Label(labtest_window,text = "Old peak : ",font = 'Times 12 bold',bg='#E6E6E6').place(x=296,y=350)
    e9 = Entry(labtest_window,textvariable=op,width=35).place(x=450,y=352)
    list.append(op)
    l11 = Label(labtest_window,text = "ST slope : ",font = 'Times 12 bold',bg='#E6E6E6').place(x=296,y=380)
    e10 = Entry(labtest_window,textvariable=slp,width=35).place(x=450,y=383)
    list.append(slp)
    process_query = partial(Process_query,list,labtest_window,3)
    
    name = StringVar()
    btn = Button(labtest_window,text = 'ADD',command = process_query,font = 'Times 12',fg='white',bg='#0B0B61').place(x=450, y=420,height=25)   
    l = Label(labtest_window,text = "Enter name of the patient to find patient ID :: ",font = 'Times 13 bold',bg = '#E6E6E6').place(x=708,y=164)
    e = Entry(labtest_window,textvariable=name,width = 35).place(x=1092,y=167)
    
    find = partial(Process_query,name,labtest_window,4)
    
    btn2 = Button(labtest_window,text = 'FIND',command = find,font = 'Times 12',fg='white',bg='#0B0B61').place(x=1098,y=210,height=25) 
    labtest_window.mainloop()  

#module for goback button
def goBack(window):
    doctor_dep(window)

#module for showing the prediction result
def Report(window,id):
    
    pid = id.get()

    #designing interface
    mydb = mysql.connector.connect(host='localhost',user='root',password = 'keshav21@',database='hdp_system')
    mycursor = mydb.cursor(buffered= True)

    frame = Frame(window)
    l = Label(window,text='OUTPUT :: ',font='Times 15 bold',bg = '#E6E6E6').place(x =80,y=280)   
    frame.place(x=200,y=286)
    textBox = Text(frame,width=60,height=10,wrap=NONE)

    try:
        #query to fetch lab info of the patient
        query = "select PatientID,ChestPainType,RestingBP,Cholesterol,FastingBS,RestingECG,MaxHR,ExerciseAngina,OldPeak,ST_Slope from lab_test_info where PatientID = '" + pid +"'"
        
        mycursor.execute(query)
        result = mycursor.fetchone()

        if result == None :
            textBox.insert(END,'Lab test reports of the entered ID does not exist.')
        else:  
            mycursor.execute("select year(from_days(datediff(current_date(),DOB))),Sex from patient_details where PatientID = '"+str(pid)+"'")
            age = mycursor.fetchone()

            r = result + age
            prediction_result = Modelpredict(r)

            #updating the prediction result in the database        
            if prediction_result==1:
                query = "update lab_test_info set HeartDisease = 'Y' where PatientID = '"+str(pid)+"'"
                textBox.insert(END,"Patient with patient ID '"+str(pid)+"' has Heart Disease.")
            elif prediction_result==0:
                query = "update lab_test_info set HeartDisease = 'N' where PatientID = '"+str(pid)+"'"
                textBox.insert(END,"Patient with patient ID '"+str(pid)+"' does not have Heart Disease.")
            mycursor.execute(query)
            mydb.commit()
            mydb.close()
    except mysql.connector.errors.ProgrammingError as error:
        textBox.insert(END,error) 

    #Add a horizontal scrollbar
    sb = Scrollbar(frame)
    sb.pack(side =RIGHT,fill= Y)

    #Add a horizontal scrollbar
    sb_h = Scrollbar(frame,orient=HORIZONTAL)
    sb_h.pack(side=BOTTOM,fill=X)
        
    textBox.config(xscrollcommand=sb_h.set,yscrollcommand=sb.set)

    textBox.pack(side = TOP,expand = True)    
    
    sb_h.config(command=textBox.xview)
    sb.config(command=textBox.yview)

#module for report generation 
def Generate_Report(win):
    
    win.destroy()
    #designing interface
    reportWin = Tk(className=' REPORT GENERATION')
    reportWin['bg'] = '#E6E6E6'

    reportWin.geometry('1355x768')

    #displaying message
    msg = Label(reportWin,text = "REPORT GENERATION ",font = 'Times 20 bold',fg = '#FAFAFA',bg='#819FF7',width = 100)
    msg.pack()   
   
    goback2 = partial(goBack,reportWin)
    b1 = Button(reportWin,text = 'Go back',command = goback2,font='Times 12',bg = 'blue')
    b1.pack(side=TOP,anchor=E)    

    pid,name = StringVar(),StringVar()

    l1 = Label(reportWin,text = "Enter patient ID : ",font = 'Times 16 bold',bg = '#E6E6E6').place(x=78,y=164)
    e = Entry(reportWin,textvariable=pid,width = 30).place(x=247,y=170)

    report = partial(Report,reportWin,pid)

    btn = Button(reportWin,text = 'Report',command = report,font = 'Times 12',fg='white',bg='#0B0B61').place(x=255, y=220,height=25)    

    l2 = Label(reportWin,text = "Enter name of the patient to find patient ID :: ",font = 'Times 14 bold',bg = '#E6E6E6').place(x=708,y=164)
    e2 = Entry(reportWin,textvariable=name,width = 35).place(x=1092,y=167)
    
    find = partial(Process_query,name,reportWin,4)
    
    btn2 = Button(reportWin,text = 'FIND',command = find,font = 'Times 12',fg='white',bg='#0B0B61').place(x=1098,y=210,height=25)
    
    reportWin.mainloop()

if __name__ == '__main__' :
    login()     #calling login module