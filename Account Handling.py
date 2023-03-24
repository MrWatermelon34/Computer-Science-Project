############################################################### REQUIRED LIBRARIES AND CONNECTIONS ############################################################### 

 

import tkinter 

import customtkinter 

import mysql.connector 

 

db = mysql.connector.connect( 

    host = "localhost", 

    user = "rootuser", 

    passwd = "20Phoenixclose!", 

) 

 

############################################################### DATABASE HANDLING ############################################################### 

#Places a new user into the database, inputting all items but the ID - the ID is calculated through measuring how many columns already exist and incrementing that by 1. 

#The process of each function is relatively similar in terms of the retrieval, update and deletion of data - the only physical part changing being the SQL command: 

#cursor: Enables the ability to 'surf' the database, making any changes that are needed. 

#cursor.execute(): Executes any SQL within the brackets. 

#At the times where an SQL command is assigned to a variable with no 'cursor.execute', it is due to passed parameters needing to be inserted, changed or deleted rather than fixed data in the database. 

################################################################################################################################################# 

# IDENTIFIERS # 

permanentUsername = "" 

permanentPassword = "" 

################################################################################################################################################# 

def newUser(username, password, email): 

    cursor = db.cursor(buffered = True) 

    cursor.execute("USE userdata") 

    idCount = cursor.execute("SELECT userid FROM projectdata") 

    idCountResult = cursor.fetchall() 

    insertNew = ("INSERT INTO projectdata (userid, username, password, email) VALUES (%s, %s, %s, %s)") 

    cursor.execute(insertNew, (len(idCountResult), username, password, email)) 

    db.commit() 

#Any checks that need to be completed within the database (existing usernames, overriding emails) is done here. 

def checkDatabase(data1, data2): 

    cursor = db.cursor(buffered = True) 

    cursor.execute("USE userdata") 

    usernames = cursor.execute("SELECT username FROM projectdata") 

    usernamesResult = cursor.fetchall() 

    tempData1 = "('" + data1 + "',)" 

    data1 = tempData1 

    for username in usernamesResult: 

        strUsername = repr(username) 

        if strUsername == data1: 

            return(True) 

    cursor.execute("USE userdata") 

    emails = cursor.execute("SELECT email FROM projectdata") 

    emailsResult = cursor.fetchall() 

    tempData2 = "('" + data2 + "',)" 

    data2 = tempData2 

    for email in emailsResult: 

        strEmail = repr(email) 

        if strEmail == data2: 

            return(True) 

    return(False) 

#If a user wants to delete their account, the process is completed here. 

def deleteUser(username): 

    cursor = db.cursor(buffered = True) 

    cursor.execute("USE userdata") 

    deleteUserBegin = ("DELETE FROM projectdata WHERE username = %s") 

    deleteUserEnd = (cursor.execute(deleteUserBegin, (username))) 

    db.commit() 

    print() 

#If a user wants to change any details with their account, that too is completed here. 

def changeUser(change, oldData, newData): 

    if change == 1: 

        cursor = db.cursor(buffered = True) 

        cursor.execute("USE userdata") 

        updateUserBegin = ("UPDATE projectdata SET username = %s WHERE username = %s") 

        updateUserEnd = (cursor.execute(updateUserBegin, (oldData, newData))) 

        db.commit() 

        return() 

    elif change == 2: 

        cursor = db.cursor(buffered = True) 

        cursor.execute("USE userdata") 

        updateUserBegin = ("UPDATE projectdata SET email = %s WHERE email = %s") 

        updateUserEnd = (cursor.execute(updateUserBegin, (oldData, newData))) 

        db.commit() 

        return() 

#newUser("username1", "password1", "emailadress") 

############################################################### INITIAL USER INTERFACE HANDLING ############################################################### 

# Modes: system (default), light, dark 

customtkinter.set_appearance_mode("dark") 

# Themes: blue (default), dark-blue, green 

customtkinter.set_default_color_theme("green") 

 

app = customtkinter.CTk()  # create CTk window like you do with the Tk window 

app.geometry("1920x1080") 

def loginAccount(): 

    tempUsername = "('" + usernameInput.get() + "',)" 

    tempPassword = "('" + passwordInput.get() + "',)" 

    cursor = db.cursor(buffered = True) 

    cursor.execute("USE userdata") 

    usernameFetch = cursor.execute("SELECT username FROM projectdata") 

    usernames = cursor.fetchall() 

    for username in usernames: 

        strUsername = repr(username) 

        if strUsername == tempUsername: 

            selectedPasswordFetchBegin = ("SELECT password FROM projectdata WHERE username = %s") 

            selectedPasswordFetchEnd = (cursor.execute(selectedPasswordFetchBegin, (usernameInput.get(),))) 

            selectedPassword = cursor.fetchall() 

            for password in selectedPassword: 

                strPassword = repr(password) 

                if strPassword == tempPassword: 

                    changeError("Welcome back " + usernameInput.get() + "!") 

permanentUsername = usernameInput.get() 

permanentPassword = passwordInput.get() 

secondApp = customtkinter.CTk()   

 

                    return() 

                else: 

                    changeError("Your password is incorrect!") 

                    return() 

     

    changeError("Your username is incorrect!") 

    return() 

 

 

def registerNewAccount(): 

    if len(usernameInput.get()) > 10: 

        changeError("Username too long!") 

        return() 

    elif len(usernameInput.get()) == 0: 

        changeError("You must have a username!") 

        return() 

    if len(passwordInput.get()) > 10 or len(passwordInput.get()) < 10 or len(passwordInput.get()) == 0: 

        changeError("Password must be 10 characters long!") 

        return() 

    email = emailInput.get() 

    foundEmailSymbol = False 

    for character in range(0, len(email)): 

        if email[character] == '@': 

            foundEmailSymbol = True 

    if not foundEmailSymbol: 

        changeError("Email must contain @ symbol!") 

        return() 

    #changeError("No Errors Yet!") 

    if checkDatabase(usernameInput.get(), emailInput.get()): 

        changeError("Email or Username already in use!") 

    else: 

        newUser(usernameInput.get(), passwordInput.get(), emailInput.get()) 

        changeError("You have registered successfully! Press 'login' to enter your account.") 

def changeError(newError): 

    errorLabel.configure(text = newError) 

# Creating the landing page's interface, nothing complex it terms of algorithmic work at use. Basic inputs. 

registerButton = customtkinter.CTkButton( 

    master=app, 

    text="Register", 

    command=registerNewAccount 

) 

loginButton = customtkinter.CTkButton( 

    master=app, 

    text="Login", 

    command=loginAccount 

) 

firstScreenLabel = customtkinter.CTkLabel( 

    master=app, 

    text="Welcome to Practice.GG", 

    font=("Arial", 40) 

) 

error = "No Errors Yet!" 

errorLabel = customtkinter.CTkLabel( 

    master=app, 

    text=error, 

    font=("Arial", 20) 

) 

usernameInput = customtkinter.CTkEntry( 

    master=app, 

    width=175, 

    placeholder_text="Username", 

    height=30, 

    corner_radius=10, 

) 

passwordInput = customtkinter.CTkEntry( 

    master=app, 

    width=175, 

    placeholder_text="Password", 

    height=30, 

    corner_radius=10, 

) 

emailInput = customtkinter.CTkEntry( 

    master=app, 

    width=225, 

    placeholder_text="Email Address", 

    height=30, 

    corner_radius=10, 

) 

firstScreenLabel.place(relx=0.5, rely=0.2, anchor=tkinter.CENTER) 

errorLabel.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER) 

 

passwordInput.place(relx=0.5, rely=0.335, anchor=tkinter.CENTER) 

usernameInput.place(relx=0.5, rely=0.3, anchor=tkinter.CENTER) 

emailInput.place(relx=0.5, rely=0.37, anchor=tkinter.CENTER) 

 

registerButton.place(relx=0.46, rely=0.41, anchor=tkinter.CENTER) 

loginButton.place(relx=0.54, rely=0.41, anchor=tkinter.CENTER) 

 

app.mainloop() 

################################################################################################################################################# 
