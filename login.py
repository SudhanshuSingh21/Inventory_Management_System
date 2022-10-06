from tkinter import*
from tkinter import font
from PIL import ImageTk
from tkinter import messagebox
import sqlite3
import os
import email_pass
import smtplib
import time
class login_system:
    def __init__(self,root):
        self.root=root
        self.root.title("Login System")
        self.root.geometry("1350x700+0+0")
        self.root.config(bg="#fafafa")

        self.otp=''
        #=========Images=============
        self.phone_img=ImageTk.PhotoImage(file="pictures/phone.png")
        self.lbl_phone_img=Label(self.root,image=self.phone_img,bd=0).place(x=200,y=50)

        #==========Login Frame==================
        self.employee_id=StringVar()
        self.password=StringVar()


        login_frame=Frame(self.root,bd=2,relief=RIDGE,bg="white")
        login_frame.place(x=650,y=90,width=350,height=460)
        
        title=Label(login_frame,text="Login System",font=("Elephant",30,"bold"),bg="white").place(x=0,y=30,relwidth=1)

        lbl_user_name=Label(login_frame,text="Employee ID",font=("Andalus",15),bg="white",fg="#767171").place(x=50,y=100)
        txt_user_name=Entry(login_frame,textvariable=self.employee_id,font=("times new roman",15),bg="#ECECEC").place(x=50,y=140)

        lbl_password=Label(login_frame,text="Password",font=("Andalus",15),bg="white",fg="#767171").place(x=50,y=200)
        txt_password=Entry(login_frame,textvariable=self.password,show='*',font=("times new roman",15),bg="#ECECEC").place(x=50,y=240)

        btn_login=Button(login_frame,text="Log In",command=self.login,font=("Arial Rounded MT Bold",15),bg="#00B0F0",cursor="hand2",activebackground="#00B0F0",fg="white",activeforeground="white").place(x=50,y=300,width=250,height=35)

        hr=Label(login_frame,bg="lightgray").place(x=50,y=370,width=250,height=2)
        or_=Label(login_frame,text="OR",bg="white",fg="lightgray",font=("times new roman",15,"bold")).place(x=150,y=355)

        #btn_forget=Button(login_frame,text="Forgot Password?",command=self.forget_window,font=("times new roman",13),bg="white",fg="#00759E",bd=0,cursor="hand2",activebackground="white",activeforeground="#00759E").place(x=100,y=390)

    
        #===================Animation Images===============
        self.im1=ImageTk.PhotoImage(file="pictures/im1.png")
        self.im2=ImageTk.PhotoImage(file="pictures/im2.png")
        self.im3=ImageTk.PhotoImage(file="pictures/im3.png")

        self.lbl_change_image=Label(self.root,bg="white")
        self.lbl_change_image.place(x=367,y=153,width=240,height=428)
        
        self.animate()
    #=========================All functions==================
    def animate(self):
        self.im=self.im1
        self.im1=self.im2
        self.im2=self.im3
        self.im3=self.im
        self.lbl_change_image.config(image=self.im)
        self.lbl_change_image.after(2000,self.animate)
    
    
    
    def login(self):
        con=sqlite3.connect(database='ims.db')
        cur=con.cursor()
        try:
            if self.employee_id.get()=="" or self.password.get()=="":
                messagebox.showerror("Error","All fields are required",parent=self.root)
            else:
                cur.execute("Select utype from employee where eid=? AND pass=?",(self.employee_id.get(),self.password.get()))
                user=cur.fetchone()
                if user==None:
                    messagebox.showerror("Error","Invalid Username or Password",parent=self.root)
                else:
                    if user[0]=="Admin":
                        self.root.destroy()
                        os.system("python dashboard.py")
                    else:
                        self.root.destroy()
                        os.system("python billing.py")
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to: {str(ex)}",parent=self.root)

    def forget_window(self):
        con=sqlite3.connect(database='ims.db')
        cur=con.cursor()
        try:
        
            if self.employee_id.get()=="":
                messagebox.showerror("Error","Employee ID must be required",parent=self.root)
            else:
                cur.execute("Select email from employee where eid=?",(self.employee_id.get(),))
                email=cur.fetchone()
                if email==None:
                    messagebox.showerror("Error","Invalid Employee ID, try again",parent=self.root)
                else:
                    #=============Forget Window=======================
                    self.var_otp=StringVar()
                    self.var_new_pass=StringVar()
                    self.var_conf_pass=StringVar()
                    #call send email function()
                    chk=self.send_eamil(email[0])
                    if chk=='f':
                        messagebox.showerror("Error","Connection Error, try again",parent=self.root)
                    else:

                        self.forget_win=Toplevel(self.root)
                        self.forget_win.title("Forgot Password")
                        self.forget_win.geometry("400x350+500+100")
                        self.forget_win.focus_force()
                        
                        title=Label(self.forget_win,text="Reset Password",font=("goudy old style",15,"bold"),bg='#3f51b5',fg="white").pack(side=TOP,fill=X)
                        lbl_reset=Label(self.forget_win,text="Enter OTP Sent on Registered Email",font=("times new roman",15)).place(x=20,y=60)
                        txt_reset=Entry(self.forget_win,textvariable=self.var_otp,font=("times new roman",15),bg="lightyellow").place(x=20,y=100,width=250,height=30)
                        
                        
                        self.btn_reset=Button(self.forget_win,text="SUBMIT",command=self.validate_otp,font=("times new roman",15),bg="lightblue",cursor="hand2")
                        self.btn_reset.place(x=280,y=100,width=100,height=30)

                        lbl_new_pass=Label(self.forget_win,text="New Password",font=("times new roman",15)).place(x=20,y=160)
                        txt_new_pass=Entry(self.forget_win,textvariable=self.var_new_pass,font=("times new roman",15),bg="lightyellow").place(x=20,y=190,width=250,height=30)

                        lbl_conf_pass=Label(self.forget_win,text="Cofirm Password",font=("times new roman",15)).place(x=20,y=225)
                        txt_conf_pass=Entry(self.forget_win,textvariable=self.var_conf_pass,font=("times new roman",15),bg="lightyellow").place(x=20,y=255,width=250,height=30)

                        self.btn_update=Button(self.forget_win,text="UPDATE",command=self.update_password,state=DISABLED,font=("times new roman",15),bg="lightblue",cursor="hand2")
                        self.btn_update.place(x=150,y=300,width=100,height=30)
    
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to: {str(ex)}",parent=self.root)

    def update_password(self):
        if self.var_new_pass.get()=="" or self.var_conf_pass.get()=="":
            messagebox.showerror("Error","Password is required",parent=self.forget_win)
        elif self.var_new_pass.get()!=self.var_conf_pass.get():
            messagebox.showerror("Error","New Password & Confirm Password should be same",parent=self.forget_win)
        else:
            con=sqlite3.connect(database='ims.db')
            cur=con.cursor()
            try:
                cur.execute("Update employee SET pass=? where eid=?",(self.var_new_pass.get(),self.employee_id.get()))
                con.commit()
                messagebox.showinfo("Success","Password updated succesfully")
                self.forget_win.destroy()
            except Exception as ex:
                messagebox.showerror("Error",f"Error due to: {str(ex)}",parent=self.root)
        

    def validate_otp(self):
        if int(self.otp)==int(self.var_otp.get()):
            self.btn_update.config(state=NORMAL)
            self.btn_reset.config(state=DISABLED)
        else:
            messagebox.showerror("Error","Invalid OTP, try again",parent=self.forget_win)


    def send_eamil(self,to_):
        s=smtplib.SMTP('smtp.gmail.com',587)
        s.starttls()
        email_=email_pass.email_
        pass_=email_pass.pass_

        s.login(email_,pass_)

        self.otp=int(time.strftime("%I%S%M"))+int(time.strftime("%S"))
        subj="IMS-Reset Password OTP"
        msg=f"Dear Sir/Madam,\n\nYour Reset OTP is {str(self.otp)}.\n\nWith Reagards,\nIMS Team"
        msg="Subject:{}\n\n{}".format(subj,msg)
        s.sendmail(email_,to_,msg)
        chk=s.ehlo()
        if chk[0]==250:
            return 's'
        else:
            return 'f'


root=Tk()
obj=login_system(root)
root.mainloop()