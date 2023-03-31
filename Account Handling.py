############################################################### REQUIRED LIBRARIES AND CONNECTIONS ###############################################################

import tkinter
import customtkinter
import mysql.connector
import random
import math

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
permanentPoints = 0
taskList = [["Get 10 Headshots", 50], ["Interact with the bomb for 5 rounds", 50], ["Get 10 Kills", 10]]
rewardList = [["Reward 1", 100, False], ["Reward 2", 50, False], ["Reward 3", 75, False]]
#################################################################################################################################################
def newUser(username, password, email):
    global permanentUsername 
    permanentUsername = username
    global permanentPassword 
    permanentPassword = password
    print(permanentUsername, permanentPassword)
    cursor = db.cursor(buffered = True)
    cursor.execute("USE userdata")
    idCount = cursor.execute("SELECT userid FROM projectdata")
    idCountResult = cursor.fetchall()
    tempId = random.randint(1000000, 9999999)
    if idCountResult == None:
        while idCountResult[0] == tempId:
            tempId = random.randint(1000000, 9999999)
    insertNew = ("INSERT INTO projectdata (userid, username, password, email) VALUES (%s, %s, %s, %s)")
    cursor.execute(insertNew, (tempId, username, password, email))
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
    print("Deleting User")
    cursor.execute("USE userdata")
    deleteUserBegin = ("DELETE FROM projectdata WHERE username = %s")
    deleteUserEnd = (cursor.execute(deleteUserBegin, (username)))
    db.commit()
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
app.resizable(False, False)
landingPage = tkinter.Frame(app, height = 1080, width = 1920, bg = "#2b2b2b", bd = 1)
landingPage.place(x = 0, y = 0)

homePage = tkinter.Frame(app, height = 1080, width = 1920, bg = "#2b2b2b", bd = 1)
homePage.place(x = 0, y = 0)

steamPage = tkinter.Frame(app, height = 1080, width = 1920, bg = "#2b2b2b", bd = 1)
steamPage.place(x = 0, y = 0)

settingsPage = tkinter.Frame(app, height = 1080, width = 1920, bg = "#2b2b2b", bd = 1)
settingsPage.place(x = 0, y = 0)

def changeFrame(frameIndex):
    if frameIndex == 1:
        landingPage.tkraise()
        print("Landing")
    elif frameIndex == 2:
        homePage.tkraise()
        print("Home")
    elif frameIndex == 3:
        settingsPage.tkraise()
        print("Settings")

##############################################################################################################################################################
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
                    global permanentUsername 
                    permanentUsername = username
                    global permanentPassword 
                    permanentPassword = password
                    changeFrame(2)
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
        changeFrame(2)

def changeError(newError):
    errorLabel.configure(text = newError)
def openSettings():
    settingsPage.tkraise()
def openLanding():
    landingPage.tkraise()
    changeError("You have been returned to the Landing Page!")
def openHome():
    homePage.tkraise()
def deleteAccountFunction():
    print(permanentUsername)
    landingPage.tkraise()
    deleteUser(permanentUsername)
    changeError("You have deleted your account!")
################################################################################################
# Creating the landing page's interface, nothing complex it terms of algorithmic work at use. Basic inputs.
################################################################################################
registerButton = customtkinter.CTkButton(
    master=landingPage,
    text="Register",
    command=registerNewAccount
)
loginButton = customtkinter.CTkButton(
    master=landingPage,
    text="Login",
    command=loginAccount
)
firstScreenLabel = customtkinter.CTkLabel(
    master=landingPage,
    text="Welcome to Practice.GG",
    font=("Arial", 40)
)
error = "No Errors Yet!"
errorLabel = customtkinter.CTkLabel(
    master=landingPage,
    text=error,
    font=("Arial", 20)
)
usernameInput = customtkinter.CTkEntry(
    master=landingPage,
    width=175,
    placeholder_text="Username",
    height=30,
    corner_radius=10,
)
passwordInput = customtkinter.CTkEntry(
    master=landingPage,
    width=175,
    placeholder_text="Password",
    height=30,
    corner_radius=10,
)
emailInput = customtkinter.CTkEntry(
    master=landingPage,
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

################################################################################################
homePageLabel = customtkinter.CTkLabel(
    master=homePage,
    text="Practice.GG Hub",
    font=("Arial", 40)
)
tabUserSettings = customtkinter.CTkButton(
    master=homePage,
    text="Account Settings",
    command=openSettings
)
tabLFG = customtkinter.CTkButton(
    master=homePage,
    text="Looking For Group",
    #command=registerNewAccount
)
tabRecommendedSettings= customtkinter.CTkButton(
    master=homePage,
    text="Recommended Settings",
    #command=registerNewAccount
)
tabCSGO = customtkinter.CTkButton(
    master=homePage,
    text="View CSGO Data",
    #command=registerNewAccount
)
leaderboardTitleLabel = customtkinter.CTkLabel(
    master=homePage,
    text="Current Session Leaderboard",
    font=("Arial", 40)
)
leaderboardLabel = customtkinter.CTkLabel(
    master=homePage,
    text="Current Session Leaderboard",
    font=("Arial", 40)
)
currentTaskTitleLabel = customtkinter.CTkLabel(
    master=homePage,
    text="Current Tasks",
    font=("Arial", 40)
)
currentTaskLabel = customtkinter.CTkLabel(
    master=homePage,
    text=taskList[random.randrange(0, len(taskList) - 1)][0],
    font=("Arial", 40)
)
currentPointsLabel = customtkinter.CTkLabel(
    master=homePage,
    text=("Points: " + str(permanentPoints)),
    font=("Arial", 40)
)
homePageLabel.place(relx=0.5, rely=0.075, anchor=tkinter.CENTER)
leaderboardTitleLabel.place(relx=0.65, rely=0.65, anchor=tkinter.CENTER)

currentTaskTitleLabel.place(relx=0.35, rely=0.65, anchor=tkinter.CENTER)
currentTaskLabel.place(relx=0.35, rely=0.7, anchor=tkinter.CENTER)

tabUserSettings.place(relx=0.2, rely=0.15, anchor=tkinter.CENTER)
tabLFG.place(relx=0.4, rely=0.15, anchor=tkinter.CENTER)
tabRecommendedSettings.place(relx=0.6, rely=0.15, anchor=tkinter.CENTER)
tabCSGO.place(relx=0.8, rely=0.15, anchor=tkinter.CENTER)
################################################################################################
################################################################################################
settingsLabel = customtkinter.CTkLabel(
    master=settingsPage,
    text="Account Settings",
    font=("Arial", 40)
)
changeUsername = customtkinter.CTkButton(
    master=settingsPage,
    text="Change Username",
    #command=registerNewAccount
)
changePassword = customtkinter.CTkButton(
    master=settingsPage,
    text="Change Password",
    #command=registerNewAccount
)
logoutAccount = customtkinter.CTkButton(
    master=settingsPage,
    text="Logout",
    command=openLanding
)
usernameInputChange = customtkinter.CTkEntry(
    master=settingsPage,
    width=175,
    placeholder_text="New Username",
    height=30,
    corner_radius=10,
)
passwordInputChange = customtkinter.CTkEntry(
    master=settingsPage,
    width=175,
    placeholder_text="New Password",
    height=30,
    corner_radius=10,
)
emailInputChange = customtkinter.CTkEntry(
    master=settingsPage,
    width=225,
    placeholder_text="New Email Address",
    height=30,
    corner_radius=10,
)
changeEmail= customtkinter.CTkButton(
    master=settingsPage,
    text="Change Email",
    #command=registerNewAccount
)
deleteAccount = customtkinter.CTkButton(
    master=settingsPage,
    text="Delete Account",
    command=deleteAccountFunction
)
settingsToHome = customtkinter.CTkButton(
    master=settingsPage,
    text="Return Home",
    command=openHome
)
settingsLabel.place(relx=0.5, rely=0.075, anchor=tkinter.CENTER)

changeUsername.place(relx=0.5, rely=0.2, anchor=tkinter.CENTER)
changePassword.place(relx=0.5, rely=0.4, anchor=tkinter.CENTER)
changeEmail.place(relx=0.5, rely=0.6, anchor=tkinter.CENTER)

usernameInputChange.place(relx=0.5, rely=0.24, anchor=tkinter.CENTER)
passwordInputChange.place(relx=0.5, rely=0.44, anchor=tkinter.CENTER)
emailInputChange.place(relx=0.5, rely=0.64, anchor=tkinter.CENTER)

deleteAccount.place(relx=0.95, rely=0.05, anchor=tkinter.CENTER)
logoutAccount.place(relx=0.95, rely=0.1, anchor=tkinter.CENTER)
settingsToHome.place(relx=0.95, rely=0.15, anchor=tkinter.CENTER)

################################################################################################
landingPage.tkraise()
app.mainloop()
#################################################################################################################################################
