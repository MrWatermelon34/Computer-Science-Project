############################################################### REQUIRED LIBRARIES AND CONNECTIONS ###############################################################
#import gamestate
#mport logger
#import map
#import player
#import provider

#List created, later used to determine which play is recommended to the user.
playRecommendList = [
    "Rush bombsite / 3 2 Split",
    "Play for picks",
    "Play support"
]

#List created, later used to determine which eco is recommended to the user.
ecoRecommendList = [
    "Save",
    "Half Buy / Force Buy",
    "Full Buy"
]

#List created, unused but could be used to determine the bomb carry recommendation to the user.
bombRecommendList = [
    "Carry",
    "Drop",
]

#Strings created, later used toe be presented to the user through Tkinter labels.
playRecommend = ""
ecoRecommend = ""
bombRecommend = ""
armourRecommend = ""

#All neccessary imports to make the project compatible with Steam.
from steam import Steam
from decouple import config
#All neccessary imports to make the project's UI.
import tkinter
import customtkinter
#Neccessary import to establish a connection between a SQL Database and the project.
import mysql.connector
#Miscellaneous imports. 
import random
import math

#Integer values later used in storing data between the live CSGO match and the project.
kills = 0
money = 0
bomb = 0
round = 0
roundWins = 0
armour = 0

#Function called upon page refresh, recommends several gameplay factors to the user.
def generalRecommendation():
    #References the previous integer values.
    global armour
    global kills
    global money
    global round

    #References the previous string values.
    global playRecommend
    global ecoRecommend
    global bombRecommend
    global armourRecommend
    
    #Opens the text file which the sever writes data to.
    #Reads each line and assigns the integer from each line of the text file to their respective positions in dataList.
    with open("data.txt", "r") as dataFile:
        dataList = ["", "", "", ""]
        count = 0
        for line in dataFile:
            currentData = int(line)
            dataList[count] = currentData
            count += 1
    dataFile.close()

    #Assigns the values retrieved from the text file to the globally accessed variables, turning them to strings.
    armour = dataList[0]
    kills = dataList[1]
    money = dataList[2]
    round = dataList[3]

    #Check complete to ensure data is retrieved successfully.
    print(armour, kills, money, round)


    #Series of checks complete to find which statement fits the player's current state within CSGO.
    #Will assign playRecommend and ecoRecommend to values from their respective lists announced earlier.
    #RECOMMEND PLAY
    if round == 0:
        #Error handling.
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
        #Error handling.
        ecoRecommend = "Error with loading - Player must not be in game."
    
    #Simple check to recommend the player buy armour if its value is under 50, and not if it's over.
    #ARMOUR RECOMMEND
    if armour < 50:
        armourRecommend = "True"
    else:
        armourRecommend = "False"

    #Tkinter label to display how many kills a user has during the match, pulled from the live CSGO match and stored in the 'kills' variable.
    currentKillsLabel.configure(text = "Kils: " + str(kills))

    #Tkinter label to display how much money a user has during the match, pulled from the live CSGO match and stored in the 'kills' variable.
    currentMoneyLabel.configure(text = "Money: $" + str(money))

    #Tkinter labels used to display the recommendations to the user visually.
    recommend1Label.configure(text = "Play Recommendation: " + playRecommend)
    recommend2Label.configure(text = "Eco Recommendation: " + ecoRecommend)
    recommend3Label.configure(text = "Bomb Recommendation: " + bombRecommend)
    armourRecommendLabel.configure(text = "Buy Armour: " + armourRecommend)

    
#Check complete to ensure that if this file is called in another, it is never ran as it would result in duplicating windows.
if __name__ == '__main__':
    #Establishing connection to a local database.
    db = mysql.connector.connect(
        host = "localhost",
        user = "rootuser",
        passwd = "20Phoenixclose!",
    )
    #steam://rungame/730/76561202255233023/+csgo_download_match%20CSGO-qCmju-aHFpW-FAaoS-B4uAd-9EacP

    #Retrieves the Steam ID from the .env file located within the project folder.
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
    #Obselete lists, plan was to be used as a basic rewards and task idea for the project but was not developed.
    taskList = [["Get 10 Headshots", 50], ["Interact with the bomb for 5 rounds", 50], ["Get 10 Kills", 10]]
    rewardList = [["Reward 1", 100, False], ["Reward 2", 50, False], ["Reward 3", 75, False]]
    #################################################################################################################################################
    #Function called upon the user pressing the register button.
    def newUser(username, password, email):
        #Global variables are used to be referenced by functions for check purposes.
        global permanentUsername 
        permanentUsername = username
        global permanentPassword 
        permanentPassword = password
        print(permanentUsername, permanentPassword)
        #Opening the database.
        cursor = db.cursor(buffered = True)
        cursor.execute("USE userdata")
        #Assigning a random ID to the user - use is obselete as the ID is never referenced, but could be used as primary key for browsing other tables.
        idCount = cursor.execute("SELECT userid FROM projectdata")
        idCountResult = cursor.fetchall()
        tempId = random.randint(1000000, 9999999)
        if idCountResult == None:
            while idCountResult[0] == tempId:
                tempId = random.randint(1000000, 9999999)
        #Inserts all user data into the database.
        insertNew = ("INSERT INTO projectdata (userid, username, password, email) VALUES (%s, %s, %s, %s)")
        cursor.execute(insertNew, (tempId, username, password, email))
        db.commit()
    #Any checks that need to be completed within the database (existing usernames, overriding emails) is done here.
    def checkDatabase(data1, data2):
        cursor = db.cursor(buffered = True)
        cursor.execute("USE userdata")
        usernames = cursor.execute("SELECT username FROM projectdata")
        usernamesResult = cursor.fetchall()
        #Additional characters assigned to ensure that tempData1 has the same string layout as the usernames that are retrieved from the database.
        tempData1 = "('" + data1 + "',)"
        data1 = tempData1
        #Loops through all retrieved usernames to complete check. Returns early if a username already exists within the database.
        for username in usernamesResult:
            strUsername = repr(username)
            if strUsername == data1:
                return(True)
        #Same checks complete prior are then done for the email - if an email already exists, the check will return true as an matching item is in the database.
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
    #If a user wants to change their username, that is completed here.
    def changeUsernameFunction():
        print("Change Username")
        global permanentUsername
        #Rather than assigning new characters to a string - as was done before - unnecessary characters are now stripped from the string.
        localUsername = str(permanentUsername).replace("(", "")
        localUsername = localUsername.replace(")", "")
        localUsername = localUsername.replace("'", "")
        localUsername = localUsername.replace(",", "")
        cursor = db.cursor(buffered = True)
        usernames = cursor.execute("SELECT username FROM projectdata")
        usernamesResult = cursor.fetchall()
        tempData1 = "('" + usernameInputChange.get() + "',)"
        data = tempData1
        #Check complete to ensure new username is the required length.
        print(len(usernameInputChange.get()))
        if len(usernameInputChange.get()) > 10 or len(usernameInputChange.get()) == 0:
            settingsErrorLabel.configure(text = "Username cannot be 0 or more than 10 characters long!")
            return()
        #Check done to ensure entered username does not exist in the database.
        for username in usernamesResult:
            strUsername = repr(username)
            print(strUsername, data)
            if strUsername == data:
                settingsErrorLabel.configure(text = "Username already exists!")
                return()
        #Updates complete to change a username located in the database. Ensures future logging in remains consistent with new username.
        print(usernameInputChange.get(), permanentUsername, type(usernameInputChange.get()))
        updateUserBegin = ("UPDATE projectdata SET username = %s WHERE username = %s")
        updateUserEnd = (cursor.execute(updateUserBegin, (str(usernameInputChange.get()), localUsername)))
        db.commit()
        settingsErrorLabel.configure(text = "Your username has switched from " + localUsername + " to " + str(usernameInputChange.get()))
        permanentUsername = usernameInputChange.get()

    #Function called upon a user changing their password.
    def changePasswordFunction():
        print("Change Password")
        global permanentPassword
        global permanentUsername
        #Stripping of username and password global variables.
        localUsername = str(permanentUsername).replace("(", "")
        localUsername = localUsername.replace(")", "")
        localUsername = localUsername.replace("'", "")
        localUsername = localUsername.replace(",", "")
        localPassword = str(permanentPassword).replace("(", "")
        localPassword = localPassword.replace(")", "")
        localPassword = localPassword.replace("'", "")
        localPassword = localPassword.replace(",", "")
        cursor = db.cursor(buffered = True)
        #Ensures the password remains consistent with character rules previously defined.
        if len(passwordInputChange.get()) > 10 or len(passwordInputChange.get()) < 10:
            settingsErrorLabel.configure(text = "Password must be 10 characters long!")
            return()
        #As there will only be one username in the table that is the same, no checks on the username required.
        updateUserBegin = ("UPDATE projectdata SET password = %s WHERE username = %s")
        updateUserEnd = (cursor.execute(updateUserBegin, (str(passwordInputChange.get()), localUsername)))
        db.commit()
        #Update presented to the user.
        settingsErrorLabel.configure(text = "Your password has switched from " + localPassword + " to " + str(passwordInputChange.get()))
        permanentUsername = passwordInputChange.get()

    #Function called to change a user's email.
    def changeEmailFunction():
        print("Change Email")
        global permanentUsername
        localUsername = str(permanentUsername).replace("(", "")
        localUsername = localUsername.replace(")", "")
        localUsername = localUsername.replace("'", "")
        localUsername = localUsername.replace(",", "")
        cursor = db.cursor(buffered = True)
        foundEmailSymbol = False
        #Check done to ensure email contains an @ symbol.
        #Basic check but ensures that the email can logically be an email.
        for character in range(0, len(emailInputChange.get())):
            if emailInputChange.get()[character] == '@':
                foundEmailSymbol = True
        #Returns following error if no @ symbol is found and no update occurs.
        if not foundEmailSymbol:
            settingsErrorLabel.configure(text = "Email must contain @ symbol!")
            return()
        #Contacts the database to change the email of the row which cooinsides with the user's username.
        updateUserBegin = ("UPDATE projectdata SET email = %s WHERE username = %s")
        updateUserEnd = (cursor.execute(updateUserBegin, (str(emailInputChange.get()), localUsername)))
        db.commit()
        settingsErrorLabel.configure(text = "You have successfully changed your email!")
        permanentUsername = passwordInputChange.get()



    ############################################################### INITIAL USER INTERFACE HANDLING ###############################################################
    #Process of creating a tkinter window - visualisation of the project to the user.
    customtkinter.set_appearance_mode("dark")
    customtkinter.set_default_color_theme("green")

    app = customtkinter.CTk()
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
    #Obselete function, was to be sued to change the frame of the Tkinter window but was not used.
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
    #Function called whenever a user presses the login button on the landing screen.
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
        #Loops through usernames until one is found which is equal to the input field
        for username in usernames:
            strUsername = repr(username)
            if strUsername == tempUsername: #Username found which is equal to input field.
                #Process of selecting the password which is on the same row as the user's username.
                selectedPasswordFetchBegin = ("SELECT password FROM projectdata WHERE username = %s")
                selectedPasswordFetchEnd = (cursor.execute(selectedPasswordFetchBegin, (usernameInput.get(),)))
                selectedPassword = cursor.fetchall()
                for password in selectedPassword:
                    strPassword = repr(password)
                    if strPassword == tempPassword: #Check done to ensure the retrieved password is the same as the entered one.
                        changeError("Welcome back " + usernameInput.get() + "!")
                        permanentUsername = username
                        permanentPassword = password
                        #Selects group data to assign to the user.
                        groupMemberFetchBegin = ("SELECT groupname FROM projectdata WHERE username = %s")
                        groupMemberFetchEnd = (cursor.execute(groupMemberFetchBegin, (usernameInput.get(),)))
                        groupMemberFetch = cursor.fetchall()
                        print(repr(groupMemberFetch[0]))
                        #Strips any extra characters to ensure the data is readable for the user.
                        groupMemberFetch = str(groupMemberFetch[0]).replace("(", "")
                        groupMemberFetch = groupMemberFetch.replace(")", "")
                        groupMemberFetch = groupMemberFetch.replace(",", "")
                        groupMember = groupMemberFetch
                        lfgGroupLabel.configure(text = "You are a member of: " + groupMember)
                        print("Group: " + groupMember)
                        changeFrame(2)
                        return()
                    else: #If the password does not equal the one retrieved from the database, user is presented with an error.
                        changeError("Your password is incorrect!")
                        return()
        #If the username does not exist in the database, user is presented with an error.
        changeError("Your username is incorrect!")
        return()
    #Function called when a user presses the button to register for a new account.
    def registerNewAccount():
        #Checks done to ensure entered data is in line with character policy.
        if len(usernameInput.get()) > 10: #Username length.
            changeError("Username too long!")
            return()
        elif len(usernameInput.get()) == 0: #Username length.
            changeError("You must have a username!")
            return()
        if len(passwordInput.get()) > 10 or len(passwordInput.get()) < 10 or len(passwordInput.get()) == 0: #Password length.
            changeError("Password must be 10 characters long!")
            return()
        email = emailInput.get()
        foundEmailSymbol = False
        for character in range(0, len(email)): #Email @ symbol - ensures email contains an @ symbol to ensure email can actually be an email.
            if email[character] == '@':
                foundEmailSymbol = True
        if not foundEmailSymbol:
            changeError("Email must contain @ symbol!")
            return()
        #changeError("No Errors Yet!")
        if checkDatabase(usernameInput.get(), emailInput.get()): #If username already exists, error is returned to the user.
            changeError("Email or Username already in use!")
        else:
            newUser(usernameInput.get(), passwordInput.get(), emailInput.get()) #Calls new user function to insert entered data into the database.
            changeError("You have registered successfully! Press 'login' to enter your account.")
            changeFrame(2)
    #################################################################################################################################################
    #Error handler which changes the error label to whatever string is passed through the function as a parameter
    def changeError(newError):
        errorLabel.configure(text = newError)
    #Functions which are used to open new pages of the project using the raise function of tkinter.
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
    #Function to create a group.
    def createGroupFunction():
        global groupMember
        #Check done to ensure group name has an actual value other than ''.
        if len(groupName.get()) == 0:
            lfgErrorLabel.configure(text = "Group name must contain at least 1 character!")
            return()
        #Check done to ensure the user is not already part of a group.
        if groupMember != "None":
            lfgErrorLabel.configure(text = "You are already part of a group!")
            return()
        #Character adding done to ensure the check is compatible with the entered group name.
        groupNameCompatible = "('" + groupName.get() + "',)"
        print(groupName.get(), groupLimitVar.get(), groupGameVar.get(), groupFocusVar.get())
        cursor = db.cursor(buffered = True)
        cursor.execute("USE userdata")
        groupFetch = cursor.execute("SELECT name FROM groupdata")
        dbGroupNames = cursor.fetchall()
        #Check done to ensure group name does not already exist within the database.
        for dbGroupName in dbGroupNames:
            if repr(dbGroupName) == groupNameCompatible:
                lfgErrorLabel.configure(text = "A group with this name already exists!")
                return()
        #If group name does not exist within the database then a new group row is inserted into the database with all data assosiated with the group.
        lfgErrorLabel.configure(text = "You have successfully created the group: " + groupName.get())
        insertNew = ("INSERT INTO groupdata (name, game, focus, grouplimit, membercount) VALUES (%s, %s, %s, %s, %s)")
        cursor.execute(insertNew, (groupName.get(), groupGameVar.get(), groupFocusVar.get(), int(groupLimitVar.get()), 1))
        db.commit()
        #groupname column updated in the projectdata table which consists of all user data.
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

    #Function called when user wants to join a group.
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
