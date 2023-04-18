import payloadparser
import importlib
############################################################### REQUIRED LIBRARIES AND CONNECTIONS ###############################################################
#import gamestate
#mport logger
#import map
#import player
#import provider

kills = 0
money = 0
bomb = 0
round = 0
roundWins = 0
armour = 0

playRecommendList = [
    "Rush bombsite / 3 2 Split",
    "Play for picks",
    "Play support"
]
ecoRecommendList = [
    "Save",
    "Half Buy / Force Buy",
    "Full Buy"
]
bombRecommendList = [
    "Carry",
    "Drop",
]

playRecommend = ""
ecoRecommend = ""
bombRecommend = ""
armourRecommend = ""

from steam import Steam
from decouple import config
import tkinter
import customtkinter
import mysql.connector
import random
import math

def generalRecommendation():
    importlib.reload(payloadparser)
    global round
    global round
    round = payloadparser.globalRound
    global kills
    kills = payloadparser.globalKills
    global armour
    armour = payloadparser.globalArmour
    global money
    money = payloadparser.globalMoney
    global playRecommend
    global ecoRecommend
    global bombRecommend
    global armourRecommend
    #RECOMMEND PLAY
    print(round, kills)
    if round == 0:
        playRecommend = "Error with loading - Player must not be in game."
    elif round == 1:
        playRecommend = playRecommendList[0]
    elif round == 2 and kills > 2:
        playRecommend = playRecommendList[1]
    elif round == 2 and kills < 2:
        playRecommend = playRecommendList[2]
    elif round < 5 and kills > round + 2:
        playRecommend = playRecommendList[1]
    elif round < 5 and kills < round + 2:
        playRecommend = playRecommendList[2]
    elif round > 5 and kills > round + 1:
        playRecommend = playRecommendList[1]
    elif round > 5 and kills < round + 1:
        playRecommend = playRecommendList[2]
    #RECOMMEND ECO
    print(round, money)
    if round == 1:
        ecoRecommend = ecoRecommendList[0]
    elif round == 2 and money > 3000:
        ecoRecommend = ecoRecommendList[0]
    elif round == 2 and money < 3000:
        ecoRecommend = ecoRecommendList[2]
    elif round == 3 and money > 3000:
        ecoRecommend = ecoRecommendList[1]
    elif round == 3 and money < 3000:
        ecoRecommend = ecoRecommendList[2]
    elif round > 3 and money < 2000:
        ecoRecommend = ecoRecommendList[0]
    elif round > 3 and money < 5000:
        ecoRecommend = ecoRecommendList[1]
    elif round > 3 and money > 5000:
        ecoRecommend = ecoRecommendList[2]
    else:
        ecoRecommend = "Error with loading - Player must not be in game."
    #ARMOUR RECOMMEND
    if armour > 49:
        armourRecommend = "True"
    else:
        armourRecommend = "False"

    recommend1Label.configure(text = "Play Recommendation: " + playRecommend)
    recommend2Label.configure(text = "Eco Recommendation: " + ecoRecommend)
    recommend3Label.configure(text = "Bomb Recommendation: " + bombRecommend)
    armourRecommendLabel.configure(text = "Buy Armour: " + armourRecommend)

    

if __name__ == '__main__':
    db = mysql.connector.connect(
        host = "localhost",
        user = "rootuser",
        passwd = "20Phoenixclose!",
    )
    #steam://rungame/730/76561202255233023/+csgo_download_match%20CSGO-qCmju-aHFpW-FAaoS-B4uAd-9EacP
    KEY = config("STEAM_API_KEY")
    steam = Steam(KEY)

    print("test")

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
    groupMember = ""
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
    def changeUsernameFunction():
        print("Change Username")
        global permanentUsername
        localUsername = str(permanentUsername).replace("(", "")
        localUsername = localUsername.replace(")", "")
        localUsername = localUsername.replace("'", "")
        localUsername = localUsername.replace(",", "")
        cursor = db.cursor(buffered = True)
        usernames = cursor.execute("SELECT username FROM projectdata")
        usernamesResult = cursor.fetchall()
        tempData1 = "('" + usernameInputChange.get() + "',)"
        data = tempData1
        print(len(usernameInputChange.get()))
        if len(usernameInputChange.get()) > 10 or len(usernameInputChange.get()) == 0:
            settingsErrorLabel.configure(text = "Username cannot be 0 or more than 10 characters long!")
            return()
        for username in usernamesResult:
            strUsername = repr(username)
            print(strUsername, data)
            if strUsername == data:
                settingsErrorLabel.configure(text = "Username already exists!")
                return()
        print(usernameInputChange.get(), permanentUsername, type(usernameInputChange.get()))
        updateUserBegin = ("UPDATE projectdata SET username = %s WHERE username = %s")
        updateUserEnd = (cursor.execute(updateUserBegin, (str(usernameInputChange.get()), localUsername)))
        db.commit()
        settingsErrorLabel.configure(text = "Your username has switched from " + localUsername + " to " + str(usernameInputChange.get()))
        permanentUsername = usernameInputChange.get()

    def changePasswordFunction():
        print("Change Password")
        global permanentPassword
        global permanentUsername
        localUsername = str(permanentUsername).replace("(", "")
        localUsername = localUsername.replace(")", "")
        localUsername = localUsername.replace("'", "")
        localUsername = localUsername.replace(",", "")
        localPassword = str(permanentPassword).replace("(", "")
        localPassword = localPassword.replace(")", "")
        localPassword = localPassword.replace("'", "")
        localPassword = localPassword.replace(",", "")
        cursor = db.cursor(buffered = True)
        if len(passwordInputChange.get()) > 10 or len(passwordInputChange.get()) < 10:
            settingsErrorLabel.configure(text = "Password must be 10 characters long!")
            return()
        updateUserBegin = ("UPDATE projectdata SET password = %s WHERE username = %s")
        updateUserEnd = (cursor.execute(updateUserBegin, (str(passwordInputChange.get()), localUsername)))
        db.commit()
        settingsErrorLabel.configure(text = "Your password has switched from " + localPassword + " to " + str(passwordInputChange.get()))
        permanentUsername = passwordInputChange.get()

    def changeEmailFunction():
        print("Change Email")
        global permanentUsername
        localUsername = str(permanentUsername).replace("(", "")
        localUsername = localUsername.replace(")", "")
        localUsername = localUsername.replace("'", "")
        localUsername = localUsername.replace(",", "")
        cursor = db.cursor(buffered = True)
        foundEmailSymbol = False
        for character in range(0, len(emailInputChange.get())):
            if emailInputChange.get()[character] == '@':
                foundEmailSymbol = True
        if not foundEmailSymbol:
            settingsErrorLabel.configure(text = "Email must contain @ symbol!")
            return()
        updateUserBegin = ("UPDATE projectdata SET email = %s WHERE username = %s")
        updateUserEnd = (cursor.execute(updateUserBegin, (str(emailInputChange.get()), localUsername)))
        db.commit()
        settingsErrorLabel.configure(text = "You have successfully changed your email!")
        permanentUsername = passwordInputChange.get()



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

    lfgPage = tkinter.Frame(app, height = 1080, width = 1920, bg = "#2b2b2b", bd = 1)
    lfgPage.place(x = 0, y = 0)

    csgoDataPage = tkinter.Frame(app, height = 1080, width = 1920, bg = "#2b2b2b", bd = 1)
    csgoDataPage.place(x = 0, y = 0)

    settingsPage = tkinter.Frame(app, height = 1080, width = 1920, bg = "#2b2b2b", bd = 1)
    settingsPage.place(x = 0, y = 0)
    #################################################################################################################################################
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
        global permanentUsername 
        global permanentPassword 
        global groupMember
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
                        permanentUsername = username
                        permanentPassword = password
                        groupMemberFetchBegin = ("SELECT groupname FROM projectdata WHERE username = %s")
                        groupMemberFetchEnd = (cursor.execute(groupMemberFetchBegin, (usernameInput.get(),)))
                        groupMemberFetch = cursor.fetchall()
                        print(repr(groupMemberFetch[0]))
                        groupMemberFetch = str(groupMemberFetch[0]).replace("(", "")
                        groupMemberFetch = groupMemberFetch.replace(")", "")
                        groupMemberFetch = groupMemberFetch.replace(",", "")
                        groupMember = groupMemberFetch
                        lfgGroupLabel.configure(text = "You are a member of: " + groupMember)
                        print("Group: " + groupMember)
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
    #################################################################################################################################################
    def changeError(newError):
        errorLabel.configure(text = newError)
    def openSettings():
        settingsPage.tkraise()
    def openLanding():
        landingPage.tkraise()
        changeError("You have been returned to the Landing Page!")
    def openHome():
        homePage.tkraise()
    def openLFG():
        lfgPage.tkraise()
    def openCSData():
        generalRecommendation()
        csgoDataPage.tkraise()
    def deleteAccountFunction():
        print(permanentUsername)
        landingPage.tkraise()
        deleteUser(permanentUsername)
        changeError("You have deleted your account!")
    #################################################################################################################################################
    def createGroupFunction():
        global groupMember
        if len(groupName.get()) == 0:
            lfgErrorLabel.configure(text = "Group name must contain at least 1 character!")
            return()
        if groupMember != "None":
            lfgErrorLabel.configure(text = "You are already part of a group!")
            return()
        groupNameCompatible = "('" + groupName.get() + "',)"
        print(groupName.get(), groupLimitVar.get(), groupGameVar.get(), groupFocusVar.get())
        cursor = db.cursor(buffered = True)
        cursor.execute("USE userdata")
        groupFetch = cursor.execute("SELECT name FROM groupdata")
        dbGroupNames = cursor.fetchall()
        for dbGroupName in dbGroupNames:
            if repr(dbGroupName) == groupNameCompatible:
                lfgErrorLabel.configure(text = "A group with this name already exists!")
                return()
        lfgErrorLabel.configure(text = "You have successfully created the group: " + groupName.get())
        insertNew = ("INSERT INTO groupdata (name, game, focus, grouplimit, membercount) VALUES (%s, %s, %s, %s, %s)")
        cursor.execute(insertNew, (groupName.get(), groupGameVar.get(), groupFocusVar.get(), int(groupLimitVar.get()), 1))
        db.commit()
        updateUserBegin = ("UPDATE projectdata SET groupname = %s WHERE username = %s")
        localUsername = str(permanentUsername).replace("(", "")
        localUsername = localUsername.replace(")", "")
        localUsername = localUsername.replace("'", "")
        localUsername = localUsername.replace(",", "")
        updateUserEnd = (cursor.execute(updateUserBegin, (str(groupName.get()), localUsername)))
        db.commit()
        print(localUsername, groupName.get())
        groupMember = groupName.get()
        lfgGroupLabel.configure(text = groupName.get())
        return()

    def joinGroupFunction():
        global groupMember
        global permanentUsername
        if len(groupName.get()) == 0:
            lfgErrorLabel.configure(text = "Group name must contain at least 1 character!")
            return()
        if groupMember != "None":
            lfgErrorLabel.configure(text = "You are already part of a group!")
            return()
        groupNameCompatible = "('" + groupName.get() + "',)"
        cursor = db.cursor(buffered = True)
        cursor.execute("USE userdata")
        groupFetch = cursor.execute("SELECT name FROM groupdata")
        dbGroupNames = cursor.fetchall()
        for dbGroupName in dbGroupNames:
            if repr(dbGroupName) == groupNameCompatible:
                memberCountBegin = ("SELECT membercount FROM groupdata WHERE name = %s")
                memberCountEnd = cursor.execute(memberCountBegin, (groupName.get(),))
                memberCountFetch = cursor.fetchall()
                memberLimitBegin = ("SELECT grouplimit FROM groupdata WHERE name = %s")
                memberLimitEnd = cursor.execute(memberLimitBegin, (groupName.get(),))
                memberLimitFetch = cursor.fetchall()

                memberLimitFetch = str(memberLimitFetch[0]).replace("(", "")
                memberLimitFetch = memberLimitFetch.replace(")", "")
                memberLimitFetch = memberLimitFetch.replace(",", "")
                memberLimitFetch = int(memberLimitFetch)

                memberCountFetch = str(memberCountFetch[0]).replace("(", "")
                memberCountFetch = memberCountFetch.replace(")", "")
                memberCountFetch = memberCountFetch.replace(",", "")
                memberCountFetch = int(memberCountFetch)
                print(memberLimitFetch, memberCountFetch)

                if memberCountFetch != memberLimitFetch: 
                    updateGroupBegin = ("UPDATE groupdata SET membercount = %s WHERE name = %s")
                    updateGroupEnd = (cursor.execute(updateGroupBegin, (memberCountFetch + 1, groupName.get())))
                    db.commit()
                    lfgErrorLabel.configure(text = "You have successfully joined " + groupName.get())
                    groupMember = groupName.get()
                    updateUserBegin = ("UPDATE projectdata SET groupname = %s WHERE username = %s")
                    localUsername = str(permanentUsername).replace("(", "")
                    localUsername = localUsername.replace(")", "")
                    localUsername = localUsername.replace("'", "")
                    localUsername = localUsername.replace(",", "")
                    print(localUsername, groupName.get())
                    updateUserEnd = (cursor.execute(updateUserBegin, (str(groupName.get()), localUsername)))
                    db.commit()
                    lfgGroupLabel.configure(text = "You are a member of: " + groupName.get())
                    return()
                else:
                    lfgErrorLabel.configure(text = groupName.get() + " has reached full capacity!")

    def leaveGroupFunction():
        global permanentUsername
        global groupMember
        localGroupMember = str(groupMember).replace("'", "")
        localUsername = str(permanentUsername).replace("(", "")
        localUsername = localUsername.replace(")", "")
        localUsername = localUsername.replace("'", "")
        localUsername = localUsername.replace(",", "")
        print("Group leaving: " + localGroupMember)
        if localGroupMember == "None":
            lfgErrorLabel.configure(text = "You are not part of any group!")
            return()

        cursor = db.cursor(buffered = True)

        memberCountBegin = ("SELECT membercount FROM groupdata WHERE name = %s")
        memberCountEnd = cursor.execute(memberCountBegin, (localGroupMember,))
        memberCountFetch = cursor.fetchall()

        memberCountFetch = str(memberCountFetch[0]).replace("(", "")
        memberCountFetch = memberCountFetch.replace(")", "")
        memberCountFetch = memberCountFetch.replace(",", "")
        memberCountFetch = int(memberCountFetch)

        updateGroupBegin = ("UPDATE groupdata SET membercount = %s WHERE name = %s")
        updateGroupEnd = (cursor.execute(updateGroupBegin, (memberCountFetch - 1, localGroupMember)))
        db.commit()
        updateUserBegin = ("UPDATE projectdata SET groupname = %s WHERE username = %s")
        updateUserpEnd = (cursor.execute(updateUserBegin, (None, localUsername)))
        db.commit()
        lfgErrorLabel.configure(text = "No errors yet!")
        lfgGroupLabel.configure(text = "Not part of a group!")#
        groupMember = "None"
        return()

    #################################################################################################################################################
    # Creating the landing page's interface, nothing complex it terms of algorithmic work at use. Basic inputs.
    #################################################################################################################################################
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

    ################################################################################################################################################################################################
    ################################################################################################################################################################################################
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
        command=openLFG
    )
    tabRecommendedSettings= customtkinter.CTkButton(
        master=homePage,
        text="Recommended Settings",
        #command=registerNewAccount
    )
    tabCSGO = customtkinter.CTkButton(
        master=homePage,
        text="View CSGO Data",
        command=openCSData
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
    ################################################################################################################################################################################################
    ################################################################################################################################################################################################
    settingsLabel = customtkinter.CTkLabel(
        master=settingsPage,
        text="Account Settings",
        font=("Arial", 40)
    )
    settingsErrorLabel = customtkinter.CTkLabel(
        master=settingsPage,
        text="No Errors Yet!",
        font=("Arial", 20)
    )
    changeUsername = customtkinter.CTkButton(
        master=settingsPage,
        text="Change Username",
        command=changeUsernameFunction
    )
    changePassword = customtkinter.CTkButton(
        master=settingsPage,
        text="Change Password",
        command=changePasswordFunction
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
        command=changeEmailFunction
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
    settingsErrorLabel.place(relx=0.5, rely=0.75, anchor=tkinter.CENTER)

    changeUsername.place(relx=0.5, rely=0.2, anchor=tkinter.CENTER)
    changePassword.place(relx=0.5, rely=0.4, anchor=tkinter.CENTER)
    changeEmail.place(relx=0.5, rely=0.6, anchor=tkinter.CENTER)

    usernameInputChange.place(relx=0.5, rely=0.24, anchor=tkinter.CENTER)
    passwordInputChange.place(relx=0.5, rely=0.44, anchor=tkinter.CENTER)
    emailInputChange.place(relx=0.5, rely=0.64, anchor=tkinter.CENTER)

    deleteAccount.place(relx=0.95, rely=0.05, anchor=tkinter.CENTER)
    logoutAccount.place(relx=0.95, rely=0.1, anchor=tkinter.CENTER)
    settingsToHome.place(relx=0.95, rely=0.15, anchor=tkinter.CENTER)
    ################################################################################################################################################################################################
    ################################################################################################################################################################################################
    lfgLabel = customtkinter.CTkLabel(
        master=lfgPage,
        text="Looking For Group",
        font=("Arial", 40)
    )
    lfgGroupLabel = customtkinter.CTkLabel(
        master=lfgPage,
        text="Not part of a group!",
        font=("Arial", 20)
    )
    lfgErrorLabel = customtkinter.CTkLabel(
        master=lfgPage,
        text="No Errors Yet!",
        font=("Arial", 20)
    )
    createGroup = customtkinter.CTkButton(
        master=lfgPage,
        text="Create Group",
        command=createGroupFunction
    )
    leaveGroup = customtkinter.CTkButton(
        master=lfgPage,
        text="Leave Group",
        command=leaveGroupFunction
    )
    joinGroup = customtkinter.CTkButton(
        master=lfgPage,
        text="Join Group",
        command=joinGroupFunction
    )
    groupName = customtkinter.CTkEntry(
        master=lfgPage,
        width=175,
        placeholder_text="Enter Group Name",
        height=30,
        corner_radius=10,
    )
    groupLimitVar = customtkinter.StringVar(value="4")
    groupLimit = customtkinter.CTkOptionMenu(
        master=lfgPage,
        values=["4", "8"],
        #command=print("Groupped", groupLimitVar),
        variable = groupLimitVar
    )
    groupFocusVar = customtkinter.StringVar(value="Casual")
    groupFocus = customtkinter.CTkOptionMenu(
        master=lfgPage,
        values=["Competitive", "Casual"],
        #command=print("Focused", groupFocusVar),
        variable = groupFocusVar
    )
    groupGameVar = customtkinter.StringVar(value="CSGO")
    groupGame = customtkinter.CTkOptionMenu(
        master=lfgPage,
        values=["CSGO"],
        #command=print("Focused", groupFocusVar),
        variable = groupGameVar
    )
    lfgToHome = customtkinter.CTkButton(
        master=lfgPage,
        text="Return Home",
        command=openHome
    )
    lfgLabel.place(relx=0.5, rely=0.075, anchor=tkinter.CENTER) 
    lfgErrorLabel.place(relx=0.5, rely=0.75, anchor=tkinter.CENTER)
    lfgGroupLabel.place(relx=0.5, rely=0.60, anchor=tkinter.CENTER)

    createGroup.place(relx=0.5, rely=0.325, anchor=tkinter.CENTER)

    groupName.place(relx=0.2, rely=0.50, anchor=tkinter.CENTER)
    groupFocus.place(relx=0.4, rely=0.50, anchor=tkinter.CENTER)
    groupGame.place(relx=0.6, rely=0.50, anchor=tkinter.CENTER)
    groupLimit.place(relx=0.8, rely=0.50, anchor=tkinter.CENTER)

    leaveGroup.place(relx=0.95, rely=0.05, anchor=tkinter.CENTER)
    joinGroup.place(relx=0.95, rely=0.10, anchor=tkinter.CENTER)
    lfgToHome.place(relx=0.95, rely=0.15, anchor=tkinter.CENTER)
    ################################################################################################################################################################################################
    csLabel = customtkinter.CTkLabel(
        master=csgoDataPage,
        text="Live CSGO Data!",
        font=("Arial", 40)
    )
    csToHome = customtkinter.CTkButton(
        master=csgoDataPage,
        text="Return Home",
        command=openHome
    )
    csRefresh = customtkinter.CTkButton(
        master=csgoDataPage,
        text="Refresh Page Data",
        command=openCSData
    )
    currentKillsLabel = customtkinter.CTkLabel(
        master=csgoDataPage,
        text="Kills: " + str(kills),
        font=("Arial", 20)
    )
    currentMoneyLabel = customtkinter.CTkLabel(
        master=csgoDataPage,
        text="Money: " + str(money),
        font=("Arial", 20)
    )
    currentBombLabel = customtkinter.CTkLabel(
        master=csgoDataPage,
        text="Bomb Interactions: " + str(bomb),
        font=("Arial", 20)
    )
    recommend1Label = customtkinter.CTkLabel(
        master=csgoDataPage,
        text="Play Recommendation: " + playRecommend,
        font=("Arial", 20)
    )
    recommend2Label = customtkinter.CTkLabel(
        master=csgoDataPage,
        text="Eco Recommendation: " + ecoRecommend,
        font=("Arial", 20)
    )
    recommend3Label = customtkinter.CTkLabel(
        master=csgoDataPage,
        text="Bomb Recommendation: " + bombRecommend,
        font=("Arial", 20)
    )
    armourRecommendLabel = customtkinter.CTkLabel(
        master=csgoDataPage,
        text="Buy Armour: " + armourRecommend,
        font=("Arial", 20)
    )
#playerKills, playerRounds, playerBomb
    csLabel.place(relx=0.5, rely=0.075, anchor=tkinter.CENTER) 

    csRefresh.place(relx=0.95, rely=0.1, anchor=tkinter.CENTER)
    csToHome.place(relx=0.95, rely=0.15, anchor=tkinter.CENTER)

    currentKillsLabel.place(relx=0.2, rely=0.2, anchor=tkinter.CENTER)
    currentMoneyLabel.place(relx=0.2, rely=0.3, anchor=tkinter.CENTER)
    currentBombLabel.place(relx=0.2, rely=0.4, anchor=tkinter.CENTER)
    recommend1Label.place(relx=0.2, rely=0.6, anchor=tkinter.CENTER)
    recommend2Label.place(relx=0.2, rely=0.75, anchor=tkinter.CENTER)
    recommend3Label.place(relx=0.2, rely=0.9, anchor=tkinter.CENTER)
    armourRecommendLabel.place(relx=0.7, rely=0.5, anchor=tkinter.CENTER)
    ################################################################################################################################################################################################
    landingPage.tkraise()
    app.mainloop()
    #################################################################################################################################################
