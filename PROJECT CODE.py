from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
import random
from datetime import date as D
import mysql.connector as mysql

#MySQL connection establishment
con=mysql.connect(user='root',host='localhost',passwd='Krish159',database='my_travel_app')
cur=con.cursor()

#Window 
root=Tk()
root.geometry('1000x600')
root.title('My Travel App-Login Page')
root.iconbitmap('icon.ico')
root.configure(bg='#d5edef')

#login page image and resize
image = Image.open("loginpage.gif")
resize_image = image.resize((400, 450)) 
img = ImageTk.PhotoImage(resize_image)
label1 = Label(image=img)
label1.image = img
label1.grid(row=0,column=0,ipadx=10,ipady=50,rowspan=5,sticky=W)

#login page entries
login=Label(text='LOGIN PAGE',fg='blue',bg='light blue',font=('Arial',30))
login.grid(row=0,column=2,columnspan=2,sticky=W,padx=75)

username=Label(text='Mobile Number:',font=('Arial',20))
username_entry=Entry(root)
username.grid(row=1,column=2,sticky=W)
username_entry.grid(row=1,column=3,sticky=W)

pswd=Label(text='Password:',font=('Arial',20))
pswd_entry=Entry(root)
pswd.grid(row=2,column=2,sticky=W)
pswd_entry.grid(row=2,column=3,sticky=W)

def booking_page():
  #CREATION OF BOOKING PAGE
  booking_page=Toplevel(root)
  booking_page.title('Booking Page-My Travel App')
  booking_page.iconbitmap('icon.ico')
  booking_page.geometry('750x400')
  booking_page.configure(bg='#03fffb')

  head_lbl=Label(booking_page,text='ARE YOU READY TO TRAVEL',font=('Georgia',30))
  head_lbl.grid(row=1,column=1,columnspan=10,padx=10,pady=10)

  dept_label=Label(booking_page,text='Depart from',font=('Bold',15))
  dept_label.grid(row=3,column=1,padx=30)
  depts="Select distinct departure_venue from flights;"
  cur.execute(depts)
  dept_list=[]
  depts=cur.fetchone()
  while depts!=None:
      dept_list.append(depts[0])
      depts=cur.fetchone()
  
  dept_ins=StringVar(booking_page)
  dept_ins.set(dept_list[0])
  dept=OptionMenu(booking_page,dept_ins,*dept_list)
  dept.grid(row=3,column=2)

  arr_label=Label(booking_page,text='Arrive to',font=('Bold',15))
  arr_label.grid(row=3,column=4,padx=30,ipadx=50)
  cur.execute("select distinct arrival_venue from flights;")
  arr_list=[]
  arrs=cur.fetchone()
  while arrs!=None:
      arr_list.append(arrs[0])
      arrs=cur.fetchone()
  
  arr_ins=StringVar(booking_page)
  arr_ins.set(arr_list[0])
  arr=OptionMenu(booking_page,arr_ins,*arr_list)
  arr.grid(row=3,column=5)

  time_lbl=Label(booking_page,text='Select Departure Date',font=('Bold',15))
  timedate_list=['01','02','03','04','05','06','07','08','09','10','11','12','13','14','15','16','17','18','19','20','21','22','23','24','25','26','27','28','29','30','31']
  timedate_ins=StringVar(booking_page)
  timedate_ins.set('date')
  timedate=OptionMenu(booking_page,timedate_ins,*timedate_list)
  timedate.grid(row=4,column=2)

  timemon_list=['01','02','03','04','05','06','07','08','09','10','11','12']
  timemon_ins=StringVar(booking_page)
  timemon_ins.set('month')
  timemonth=OptionMenu(booking_page,timemon_ins,*timemon_list)
  time_lbl.grid(row=4,column=1)
  timedate.grid(row=4,column=2)
  timemonth.grid(row=4,column=3)

  seat_lbl=Label(booking_page,text='Select number of seats:',font=('Bold',15))
  seat_lbl.grid(row=4,column=4)
  seat_list=['1','2','3','4','5','6','7','8','9','10']
  seat_ins=StringVar(booking_page)
  seat_ins.set('1')
  num_seat=OptionMenu(booking_page,seat_ins,*seat_list)
  num_seat.grid(row=4,column=5)

  def flights():
    if dept_ins.get()==arr_ins.get():
      messagebox.showwarning('Same Locations','Departure Location and Arrival Destination are same,Please Change')
    check_avail="Select * from flights where departure_venue='{}' and arrival_venue='{}'and departure_time like \"%{}-{}%\" and seats>{};".format(dept_ins.get(),arr_ins.get(),timemon_ins.get(),timedate_ins.get(),seat_ins.get())    
    
    cur.execute(check_avail)
    flight_avl=cur.fetchall()
    
    if len(flight_avl)==0:
      messagebox.showinfo('Flight availability','No flights available for your desired destination')
    else:  
      flight=Toplevel()
      flight.title('Flights')
      flight.iconbitmap('icon.ico')
      flight.geometry('1100x500')
      flightlist=flight_avl
      flight_no=Label(flight,text='Flight No.',font=('Calibri',10))
      dist=Label(flight,text='|',font=('Calibri',10))
      flight_no.grid(row=1,column=1,padx=10,pady=10)
      dist.grid(row=1,column=2)
      flight_details=Label(flight,text='Airline    |    Departure_venue    |     Arrival venue    |      Departure Time     |      Arrival Time      |       Seats Available     |       Duration   |    Price (INR) ' ,font=('Arial',10))
      flight_details.grid(row=1,column=3)
      rowflight=2
      columnflight=1
      air_id=[]
      for i in flightlist:
        num=i[0]
        air_id.append(num)
        det=''
        for j in range(1,8):
            if j!=4:

              det+=(str(i[j])+'            |            ')
              
            else:
              det+=(str(i[j])+'  |   ')
        det+=str(i[8])
        flight_1=Label(flight,text=num,font=('Calibri',10))
        dist_2=Label(flight,text='|',font=('Calibri',10))
        flight_det_1=Label(flight,text=det,font=('Calibri',10))
        flight_1.grid(row=rowflight,column=columnflight,padx=10,pady=10)
        dist.grid(row=rowflight,column=columnflight+1)
        flight_det_1.grid(row=rowflight,column=columnflight+1,columnspan=10)
        rowflight+=1


      def payment():
       seats=seat_ins.get()
       payment=Toplevel()
       payment.title('Payment Window-my travel app')
       payment.iconbitmap('icon.ico')
       payment.geometry('500x500')
       
       paylabel=Label(payment,text='Payment',font=('Arial',30))
       paylabel.grid(row=1,column=1,columnspan=10,padx=250,pady=10)

       pay_flight_lbl=Label(payment,text='Airline ID/Flight Number',font=('Arial',15))
       pay_fli_price_lbl=Label(payment,text='Price per seat',font=('Arial',15))
       pay_seat_lbl=Label(payment,text='Number of seats',font=('Arial',15))
       total_amt_lbl=Label(payment,text='Total Amount',font=('Arial',15))
       gst_lbl=Label(payment,text='GST',font=('Arial',15))
       total_pay_lbl=Label(payment,text='Total Payable amount',font=('Arial',15))
       
       pay_flight_lbl.grid(row=2,column=1)
       pay_fli_price_lbl.grid(row=3,column=1)
       pay_seat_lbl.grid(row=4,column=1)
       total_amt_lbl.grid(row=5,column=1)
       gst_lbl.grid(row=6,column=1)
       total_pay_lbl.grid(row=7,column=1)
       
       fare="Select price from flights where air_id={}".format(airnum_ins.get())
       cur.execute(fare)
       fl_fare=cur.fetchone()
       air_id_num=fl_fare[0]
       payment_flight=Label(payment,text=airnum_ins.get(),font=('Arial',15))
       pay_fli_price=Label(payment,text=air_id_num,font=('Arial',15))
       pay_seat=Label(payment,text=seats,font=('Arial',15))
       amt=int(air_id_num)*int(seats)
       total_pay=Label(payment,text=str(amt),font=('Arial',15))
       gst=Label(payment,text='5%',font=('Arial',15))
       amt=1.05*int(amt)
       total_amt=Label(payment,text=str(amt),font=('Arial',15))

       payment_flight.grid(row=2,column=2)
       pay_fli_price.grid(row=3,column=2)
       pay_seat.grid(row=4,column=2)
       total_pay.grid(row=5,column=2)
       gst.grid(row=6,column=2)
       total_amt.grid(row=7,column=2)

       card_num=Label(payment,text='Enter card number:',font=('Arial',15))
       card_holder=Label(payment,text='Enter card holder name:',font=('Arial',15))
       card_cvv=Label(payment,text='Enter CVV:',font=('Arial',15))

       card_num_ent=Entry(payment)
       card_holder_ent=Entry(payment)
       card_cvv_ent=Entry(payment)

       card_num.grid(row=9,column=1)
       card_num_ent.grid(row=9,column=2)
       card_holder.grid(row=10,column=1)
       card_holder_ent.grid(row=10,column=2)
       card_cvv.grid(row=11,column=1)
       card_cvv_ent.grid(row=11,column=2)

       def generate_otp():
         if card_num_ent.get()=='0123456789' and card_cvv_ent.get()=='123' and card_holder_ent.get()=='ABCXYZ': 
           otp_rec=random.randint(100000,999999)
           otp_rec=str(otp_rec)
           otp=Toplevel()
           otp.title('Fake Bank of India-Payment Page')
           otp.geometry('1000x500')
           otp.iconbitmap('monopoly_icon.gif')
           otp_title=Label(otp,text='FAKE BANK OF INDIA(FBI)',font=('Arial',30))
           otp_title.grid(row=1,column=1,columnspan=10,padx=250,pady=10)
           otp_lbl=Label(otp,text='Enter otp',font=('Arial',15))
           otp_ent=Entry(otp)
           otp_lbl.grid(row=2,column=1)
           otp_ent.grid(row=2,column=2)
           
           def pay_complete():
             if otp_ent.get()==otp_rec:
               name=username_entry.get()
               pswd=pswd_entry.get()
               pnr=str(random.randint(100000,999999))
               name_file=name+'mytravelapp'+pnr+'.txt'
               file=open(name_file,'a')
               file.write('MY TRAVEL APP')
               file.write(str('Booking time:'+str(D.today())))
               file.write('\n')
               file.write(str('Flight Number'+str(airnum_ins.get())))
               file.write('\n')
               file.write(pnr)
               file.write('\n')
               for i in flightlist:
                 if i[0]==airnum_ins.get():
                   file.write(str(i))
                   file.write('\n')
               file.write('Total seats ='+seats)
               file.write('\n')
               file.write('Total amount='+str(amt))
               file.write('\n')
               file.close()
               x=messagebox.showinfo('BOOKING CONFIRMED','Flight ticket downloaded')
               booking_page.destroy()
               payment.destroy()
               otp.destroy()
               flight.destroy()
               username_entry.delete(0,END)
               pswd_entry.delete(0,END)
             else:
               x=messagebox.showwarning('Payment unsuccessful','Incorrect OTP! Payment aborted')
               payment.destroy()
               otp.destroy()
             
           pay_comp=Button(otp,text='PAY',command=pay_complete)
           pay_comp.grid(row=3,column=1)

           msg_box='OTP for payment of INR'+str(amt)+'is:'+otp_rec
           messagebox.showinfo('Fake Bank of India-OTP Payment',msg_box)

       gen_otp=Button(payment,text='Generate OTP',command=generate_otp)
       gen_otp.grid(row=12,column=1,padx=50)
       

      airnum_list=air_id
      airnum_ins=StringVar(flight)
      airnum_ins.set(air_id[0])
      airnum=OptionMenu(flight,airnum_ins,*airnum_list)
      airnum.grid(row=rowflight,column=1)
                      
      pay=Button(flight,text='PAY',font=('Arial',15),fg='Blue',command=payment)
      pay.grid(row=rowflight,column=2,columnspan=2)
    
    
  search_bar=Button(booking_page,text='Search',command=flights)
  search_bar.grid(row=5,column=1,columnspan=6)
  
  
def get_login_entry():
  ans=messagebox.askyesno('Confirmation','Do you confirm entry of credentials')
  if ans:
    userid=username_entry.get()
    pswd_rec=pswd_entry.get()
    if userid.isdigit() and len(userid)==10:
      login_confirm="Select password,customer_name from travellers where customer_id={}".format(int(userid))
      cur.execute(login_confirm)
      saved_pswd=cur.fetchone()
      if userid=='' and pswd_rec=='':
        messagebox.showwarning('Empty Entry','Please fill in the requirements')
      elif saved_pswd==None:
        messagebox.showinfo('Signup', 'You are not registered please register')
      elif pswd_rec!=saved_pswd[0]:
        chng_pswd=messagebox.askyesno('Wrong Password','Incorrect password do you want to change?')
        if chng_pswd:
          chng_pswd_win=Toplevel()
          chng_pswd_win.geometry('300x150')
          chng_pswd_win.iconbitmap('icon.ico')
          pagelbl=Label(chng_pswd_win,text='Password Reset',font=('Arial',20))
          pagelbl.grid(row=1,column=1,columnspan=2)
          emailid_reg=Label(chng_pswd_win,text='Enter Email:')
          emailid_ent=Entry(chng_pswd_win)
          pswd_new=Label(chng_pswd_win,text='Enter new password:')
          pswd_newent=Entry(chng_pswd_win)

          emailid_reg.grid(row=2,column=1)
          emailid_ent.grid(row=2,column=2,ipadx=20)
          pswd_new.grid(row=3,column=1)
          pswd_newent.grid(row=3,column=2,ipadx=20)

          def confirmchange():
            cur.execute("Select email_id from travellers where customer_id={};".format(int(username_entry.get())))
            eml=cur.fetchone()
            if emailid_ent.get()==eml[0]:
              cur.execute("Update travellers set password='{}' where customer_id={};".format(pswd_newent.get(),int(username_entry.get())))
              con.commit()
              messagebox.showinfo('Password updated','Please login')
              chng_pswd_win.destroy()
            else:
              messagebox.showerror('Invalid email','Sorry could not authenticate email, Incorrect email id')
          confirm_button=Button(chng_pswd_win,text='Confirm',command=confirmchange)
          confirm_button.grid(row=4,column=1,columnspan=2)
          
          
      elif pswd_rec==saved_pswd[0]:
        messagebox.showinfo('SUCCESS','You are logged in successfully as {}'.format(saved_pswd[1]))
        booking_page()
      else:
        messagebox.showerror('Incorrect credential','Please fill in correct credentials')
    else:
      if userid.isdigit()==False:
        messagebox.showwarning('Incorrect character','Mobile number contains 10digits(0-9) only')
        username_entry.delete(0,END)
      else:
        messagebox.showwarning('Incorrect Number','Mobile number is of 10 digits')
  
login_button=Button(root,text='Login',font=('Arial',18),command=get_login_entry)
login_button.grid(row=3,column=1,columnspan=4,padx=170)

#Sign up window function
def signup_window():
  signup_window = Toplevel()
  signup_window.title('My Travel App-Signup Page')
  signup_window.iconbitmap('icon.ico')
  #signup_window.geometry('{}x{}'.format(signup_window.winfo_screenwidth(),signup_window.winfo_screenheight()))
  signup_window.geometry('1000x600')
  signup_window.configure(bg='#03fffb')

  def handle_entry_key_press(event):   
    x=event.char
    if event.keycode==8:                               #KEYCODE 8 IS FOR 'blank space key'
      pass
    elif not x.isdigit():
      messagebox.showwarning('incorrect input','Please Enter numerical characters only (0-9)')


  username=Label(signup_window,text='Enter your name:',font=('Arial',20))
  username_entry=Entry(signup_window)
  username.grid(row=1,column=1)
  username_entry.grid(row=1,column=2,sticky=W)
  
  mobile=Label(signup_window,text='Mobile Number:',font=('Arial',20))          #username label and entry
  mobile_entry=Entry(signup_window)
  mobile.grid(row=2,column=1)
  mobile_entry.grid(row=2,column=2,sticky=W)
  mobile_entry.bind('<Key>', handle_entry_key_press)
  
  pswd=Label(signup_window,text='Password:',font=('Arial',20))                    #Password label and entry
  pswd_entry=Entry(signup_window)
  pswd.grid(row=3,column=1)
  pswd_entry.grid(row=3,column=2,sticky=W)

  dob=Label(signup_window,text='DOB',font=('Arial',20))
  dob.grid(row=4,column=1)

  date_list=['1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17','18','19','20','21','22','23','24','25','26','27','28','29','30','31']
  date_ins=StringVar(signup_window)
  date_ins.set('Select date')
  date=OptionMenu(signup_window,date_ins,*date_list)
  date.grid(row=4,column=2)

  mon_list=['1','2','3','4','5','6','7','8','9','10','11','12']
  mon_ins=StringVar(signup_window)
  mon_ins.set('Select month')
  month=OptionMenu(signup_window,mon_ins,*mon_list)
  month.grid(row=4,column=3)

  yr_list=[1945, 1946, 1947, 1948, 1949, 1950, 1951, 1952, 1953, 1954, 1955, 1956, 1957, 1958, 1959, 1960, 1961, 1962, 1963, 1964, 1965, 1966, 1967, 1968, 1969, 1970, 1971, 1972, 1973, 1974, 1975, 1976, 1977, 1978, 1979, 1980, 1981, 1982, 1983, 1984, 1985, 1986, 1987, 1988, 1989, 1990, 1991, 1992, 1993, 1994, 1995, 1996, 1997, 1998, 1999, 2000, 2001, 2002, 2003, 2004, 2005, 2006]
  yr_ins=StringVar(signup_window)
  yr_ins.set('Select Year')
  year=OptionMenu(signup_window,yr_ins,*yr_list)
  year.grid(row=4,column=4)

  city_lbl=Label(signup_window,text='Enter your location',font=('Arial',20))
  city_list=['Kolkata','Mumbai','Varanasi','Delhi']
  cntry_list=['India']
  city_ins=StringVar(signup_window)
  cntry_ins=StringVar(signup_window)
  city_ins.set('Select City')
  cntry_ins.set('Select Country')
  city=OptionMenu(signup_window,city_ins,*city_list)
  cntry=OptionMenu(signup_window,cntry_ins,*cntry_list)
  city_lbl.grid(row=5,column=1)
  city.grid(row=5,column=2)
  cntry.grid(row=5,column=3)

  email_lbl=Label(signup_window,text='Enter Email',font=('Arial',20))
  email=Entry(signup_window)
  email_lbl.grid(row=6,column=1)
  email.grid(row=6,column=2,ipadx=30,sticky=W)

  def register_confirm():
    if mobile_entry.get().isdigit() and ('@' in email.get()):
      print(mobile_entry.get())
      exe_phn="Select * from travellers where customer_id={};".format(int(mobile_entry.get()))
      cur.execute(exe_phn)
      num_list=cur.fetchone()
      print(num_list)
      exe_em="Select * from travellers where email_id='{}';".format(email.get())
      cur.execute(exe_phn)
      em_list=cur.fetchone()
      print(em_list)
      if num_list!=None:
        messagebox.showwarning('Old credential','Mobile number already registered')
      elif em_list!= None:
        messagebox.showwarning('Old credential','Email ID already registered')
      else:
        if len(mobile_entry.get())==10:
          if date_ins.get()=='Select date' or mon_ins.get()=='Select month' or yr_ins.get()=='Select Year' or pswd_entry.get()=='' or city_ins.get()=='Select City' or cntry_ins.get()=='Select Country' or email.get()=='':
            messagebox.showwarning('Incomplete Credentials','Please fill in all necessary details')
          else:  
            dob_sql="{}-{}-{}".format(int(yr_ins.get()),int(mon_ins.get()),int(date_ins.get()))
            exe="insert into travellers values({},'{}',{},'{}','{}','{}','{}','{}');".format(int(mobile_entry.get()),username_entry.get(),mobile_entry.get(),dob_sql,city_ins.get(),cntry_ins.get(),email.get(),pswd_entry.get())
            cur.execute(exe)
            con.commit()
            messagebox.showinfo('Registration Success','Welcome! Registered successfully. \n Please LOGIN')
            signup_window.destroy()
        else:
            mobile_entry.delete(0,END)
            messagebox.showinfo('Incorrect Credential','Mobile number is of 10 digits only')
    elif '@'not in email.get():
            email.delete(0,END)
            messagebox.showinfo('Incorrect Credential','Invalid Email ID')   
    else:
      mobile_entry.delete(0,END)
      messagebox.showinfo('Incorrect Credential','Mobile number contains no alphabets or special characters, please enter digits(0-9) only.')
      
  reg_button=Button(signup_window,text='Register',font=('Arial',20),command=register_confirm)
  reg_button.grid(row=7,column=1,padx=200,columnspan=3)

# back to login from signup
  login_change=Button(signup_window,text='Already a member! Sign in here',font=('Arial',18),command=root.deiconify)
  login_change.grid(row=8,column=1,columnspan=3,padx=170)

#signup icon
signup_change=Button(root,text='New member! Sign up here',font=('Arial',18),command=signup_window)
signup_change.grid(row=4,column=1,columnspan=3,padx=170)

root.mainloop()
