import time
import os
import hashlib
PIV = 0
global MASTER_key_username
global MASTER_key_password 
MASTER_key_username = ""
MASTER_key_password = ""
os.system("clear")
with open("cve", "r") as FILE_F:
    FILLOUT = FILE_F.readlines()
    FILLOUT = "".join(FILLOUT)
    if(FILLOUT == ""):
       PIV = 0
    if(FILLOUT != ""):
        PIV = 1
def Decision_unit(Raw):
    if(Raw == 0):
       return "ok"
    if(Raw == 1):
        with open("credentials.txt", "r") as Senior_Password:
           Senior_password_raw = Senior_Password.readlines()
           Senior_password_raw = "".join(Senior_password_raw)
           Senior_length = len(Senior_password_raw)
           Octave_key = 0
           for i in range(0,Senior_length):
               Checkup_buffer = Senior_password_raw[i]
               if(Checkup_buffer == ":"):
                 Octave_key = i
                 break
           Octave_key = Octave_key + 1
           Master_of_all_KEY = Senior_password_raw[Octave_key:]
           return Master_of_all_KEY
Octave_Dec = Decision_unit(PIV)
print(Octave_Dec)
if(Octave_Dec == "ok"):
    MASTER_key_password = "admin"
    MASTER_key_username = "admin"
    Check_buffer_key = hashlib.sha256("admin".encode()).hexdigest()
else:
    Check_buffer_key = Octave_Dec                
print("ZNTP Password Manager 1.0")
Passowrd_fillout_raw = input("ZNTP_OLD_PASSWORD:")
if(hashlib.sha256(Passowrd_fillout_raw.encode()).hexdigest() != Check_buffer_key):
    print("ZNTP: Wrong password try again!!")
else:
    print("password is confirmed")
def Password_session():
    while True:
        Ava_commands = ["help","chp","vhp","exit","cls"]
        User_session = input(">")
        if(User_session not in Ava_commands and  User_session != ""):
            print("ZNTP: commands is not reconginzed")
        if(User_session == "help"):
            print("chp : changes the current operator password")
            print("vhp : Shows the current password of the opertor")
            print("exit: closing the current operator session")
            print("cls : clears the console")
        if(User_session == "chp"):
            def Exp_secu():
                while True:
                    New_username = input("ZNTP: New username >")
                    if(New_username == ""):
                        print("ZNTP: Username cannot be empty")
                        Exp_secu()
                    New_pass_pin = input("ZNTP: New password >")
                    Reap_pass_pin = input("ZNTP: Confirm New password >")
                    if(Reap_pass_pin != New_pass_pin):
                        print("ZNTP : Confirmation was not authorized")
                    if(Reap_pass_pin == New_pass_pin):
                        break
                with open("credentials.txt", "w") as pass_point:
                    pass_point.writelines(New_username+":"+ hashlib.sha256(Reap_pass_pin.encode()).hexdigest())
            Exp_secu()    
        if(User_session == "vhp"):
            with open("credentials.txt", "r") as View_point:
                View_point_raw = View_point.readlines()
                View_point_cooked = "".join(View_point_raw)
                print("[",View_point_raw,"]")
        if(User_session == "cls"):
            print("\033c")
        if(User_session == "exit"):
            exit()                                    
Password_session()        
               