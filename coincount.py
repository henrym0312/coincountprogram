"""This Program is the coursework for GCSE Computer Science
Created By Henry Milner. It is a program to help a youth club Count
Coins they have collected Once the User enters the weight of a bag of
coins, it tells them how many coins to add or remove The Volunteer can
also access their account to view the Total  or Volunteer Information
This Program uses Modules like csv, easygui etc.
"""

# This imports the Needed Modules for the Program
import time
from datetime import datetime
import csv
from easygui import *

'------------------------------- Setting Up Variables ------------------------------'


# This function Sets up variables and lists/tuples that will be used throughout the program
def varsetup():
    retry = True
    # Creating Lists for allowed coin types and for correct bag weights (See 'Analysis' file to see these)
    cvalues = ("1p", "2p", "5p", "10p", "20p", "50p", "£1", "£2")
    bvalues = (356, 356, 325, 325, 250, 160, 175, 120)
    sessiontotal = 0
    sessionright = 0
    sessionwrong = 0
    attemps = 0
    uservalues(retry, cvalues, bvalues, sessiontotal, sessionright,
               sessionwrong, attemps)


'------------------------------- User Value Inputs ------------------------------'


# This Function lets the User decide what they want to do
def uservalues(retry, cvalues, bvalues, sessiontotal, sessionright,
               sessionwrong, attemps):
    # It is essentially the Main menu for the program
    fchoices = ["Volunteer Functions", "Team Leader Functions", "Exit Program"]
    option = buttonbox("Choose a Function", title="Function Choice", choices=fchoices)
    if option == fchoices[0]:
        volunteerlogin(retry, cvalues, bvalues, sessiontotal, sessionright,
                       sessionwrong, attemps)
    if option == fchoices[1]:
        leaderabilitieslogin()
    if option == fchoices[2]:
        exit()


'------------------------------- Volunteer Abilities ------------------------------'


# This Funtion Obtains The Bag's Coin Type and Weight
def volunteerabilities(retry, cvalues, bvalues, sessiontotal, currentuser,
                       sessionright, sessionwrong, attemps):
    ctype = enterbox("Enter The Coin Type: ", title="Coin Type")
    bweight = enterbox("Enter the Weight of the Bag of " + ctype + "'s In Grams: ", title="Bag Weight")
    validation(retry, cvalues, bvalues, sessiontotal, ctype, bweight,
               currentuser, sessionright, sessionwrong, attemps)


'------------------------------- Validating user Input ------------------------------'


# This Function Validates the Users Inputs (From 'volunteerabilities' Function)
def validation(retry, cvalues, bvalues, sessiontotal, ctype, bweight,
               currentuser, sessionright, sessionwrong, attemps):
    while retry:
        # If the entered Coin type Fits to the allowed coin types, it progresses
        if ctype in cvalues:
            weightammend(retry, ctype, bweight, cvalues, bvalues, sessiontotal, currentuser,
                         sessionright, sessionwrong, attemps)
            retry = False
        # If the entered Coin type Doesn't Fit in the allowed coin types, it Notifies the user
        else:
            msgbox("Please Enter a Valid Coin Type", title="Error")
            # This asks the user whether they want to start again
            # It uses Boolean to cary on or end the program
            startagain = ynbox("Would You Like to Start Again: ", title="Start Again?")
            if startagain:
                uservalues(retry, cvalues, bvalues, sessiontotal,
                           sessionright, sessionwrong, attemps)
            else:
                exit()
            retry = False


'------------------------------- Weight ammendment output ------------------------------'


# This Function Tells the user how many coins to add or remove, or if it is correct then Adds it to the total
def weightammend(retry, ctype, bweight, cvalues, bvalues, sessiontotal,
                 currentuser, sessionright, sessionwrong, attemps):
    cindex = cvalues.index(ctype)
    correctbweight = bvalues[cindex]
    # 'bagamount' is the monetery value of each bag for each coin type
    # 'onecoinweight' is the weight of one coin for each coin type
    bagamount = [1, 1, 5, 5, 10, 10, 20, 20]
    onecoinweight = [3.56, 7.12, 3.25, 6.5, 5, 8, 8.75, 12]
    # This if statement is for when the entered bag weight is CORRECT
    # It adds the monetary value to the correct user and to the 'coincountfile.txt'
    if int(bweight) == int(correctbweight):
        msgbox("Bag Weight Is Correct (£ " + str(bagamount[cindex]) + " Added To Total)", "Correct")
        sessiontotal = sessiontotal + bagamount[cindex]
        attemps = attemps + 1
        sessionright = sessionright + 1
        time.sleep(1)
        csvreadandwrite(sessiontotal, currentuser, sessionright, attemps)
        time.sleep(2)
        startagain = ynbox("Would You Like to Start Again: ", title="Start Again?")
        if startagain:
            uservalues(retry, cvalues, bvalues, sessiontotal, sessionright, sessionwrong, attemps)
        else:
            exit()
    # This if statement is for when the entered bag weight is HIGHER than the Correct weight
    # It notifies the user much many coins to REMOVE FROM the bag, then asks to start again
    if int(bweight) > correctbweight:
        sessionwrong = sessionwrong + 1
        attemps = attemps + 1
        outbag = int(bweight) - int(correctbweight)
        outcoin = round(outbag / onecoinweight[cindex])
        msgbox("Remove: " + str(outcoin) + " Coin/s From Bag", title="Remove")
        time.sleep(2)
        startagain = ynbox("Would You Like to Start Again: ", title="Start Again?")
        if startagain:
            uservalues(retry, cvalues, bvalues, sessiontotal, sessionright, sessionwrong, attemps)
        else:
            exit()
    # This if statement is for when the entered bag weight is LOWER than the Correct weight
    # It notifies the user much many coins to ADD TO the bag, then asks to start again
    if int(bweight) < correctbweight:
        sessionwrong = sessionwrong + 1
        attemps = attemps + 1
        outbag = int(correctbweight) - int(bweight)
        outcoin = round(outbag / onecoinweight[cindex])
        msgbox("Add: " + str(outcoin) + " Coin/s To Bag", title="Add")
        time.sleep(2)
        startagain = ynbox("Would You Like to Start Again: ", title="Start Again?")
        if startagain:
            uservalues(retry, cvalues, bvalues, sessiontotal, sessionright, sessionwrong, attemps)
        else:
            exit()


'------------------------------- Changing the CSV ------------------------------'


# This function amends the 'coincount.txt' file
def csvreadandwrite(sessiontotal, currentuser, sessionright, attemps):  # This Ammends the 'coincount.txt' file
    file = open("coincountfile.txt", "r")
    # Reads the file into a list, then adds the total ('sessiontotal'), Then writes it back into the file
    read = int(file.read())
    file.close()
    csvinput = read + sessiontotal
    csvinput = str(csvinput)
    file = open("coincountfile.txt", "w")
    file.write(csvinput)
    file.close()

    # This amends the 'volunteers.csv' file
    with open('volunteers.csv', newline='') as f:
        # Reads the data into a list, then finds the current user inside the file
        # Then ammends the whole list with the changed user info
        # rewrites the file
        reader = csv.reader(f)
        data = list(reader)
    for i in range(1, len(data)):
        if data[i][0] == currentuser:
            csvuser = data[i]
            usertotal = data[i][1]
            totalammend = int(sessiontotal) + int(usertotal)
            totalpercentage = (sessionright / attemps) * 100
            deldata = data.index(csvuser)
            del data[deldata]
            csvuserammended = currentuser
            data.append([csvuserammended, totalammend, totalpercentage])
            file = open('volunteers.csv', 'w+', newline='')
            with file:
                write = csv.writer(file)
                write.writerows(data)


'------------------------------- Leader Login ------------------------------'


# This Function allows a Leader to log in to their account
def leaderabilitieslogin():
    """This uses the values in 'volunteeraccounts.csv' and
        compares them with the users input"""
    leadusern = []
    leadpass = []
    with open("leaderaccounts.csv", "r") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for lines in csv_reader:
            leadusern.append(lines[0])
    with open("leaderaccounts.csv", "r") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for lines in csv_reader:
            leadpass.append(lines[1])
    for i in range(0, 3):
        leaderusern = enterbox("Enter Username", "Username Enter")
        leaderpassword = passwordbox("Enter Password", title="Leader Password")
        if leaderusern in leadusern and leaderpassword in leadpass:
            leaderabilities()
            break
        else:
            # This lets the user have 3 attemps at entering a correct UN and PW
            attemps = 2 - i
            msgbox("Incorrect Password or username\n (You have "
                   + str(attemps) + " Attemps Left)")


'------------------------------- Leader abilities ------------------------------'


# This Function Lets the leader View The Total or View Volunteer Information
def leaderabilities():
    now = datetime.now()
    optionchoices = ["View Total", "View Volunteer Info.",
                     "View One Volunteer", "Add Account",
                     "Delete Account", "Exit Program"]
    option = buttonbox("Choose a Function", title="Function Choice", choices=optionchoices)

    if option == optionchoices[0]:
        # This Tells The User the Total Amount of money counted by all Volunteers
        file = open("coincountfile.txt", "r")
        # Reads File into variable, then outputs it along with the Current Time
        total = str(file.read())
        totalp = "£" + total + ".00"
        dt = now.strftime("%d/%m/%Y %H:%M:%S")  # Current Time
        msgbox("The Total Amount of Money Counted so far is: " + str(totalp) + "\n(Last Updated  " + dt + ")")
        logout = ynbox("Would you like to log out of the admin account?: ", title="Logout?")
        if logout:
            varsetup()
        if not logout:
            leaderabilities()

    if option == optionchoices[1]:
        # This Tells the User All the information from every volunteer
        dt = now.strftime("%d/%m/%Y %H:%M:%S")  # Current Time
        with open('volunteers.csv', newline='') as f:
            reader = csv.reader(f)
            # Reads Data into list, then prints the whole list
            data = [list(row) for row in reader]
            msgbox(
                msg=f'{data[0][0]}| {data[0][1]}| {data[0][2]}\n'
                    f'{data[1][0]}| {data[1][1]}| {data[1][2]}\n'
                    f'{data[2][0]}| {data[2][1]}| {data[2][2]}\n'
                    f'{data[3][0]}| {data[3][1]}| {data[3][2]}\n'
                    f'{data[4][0]}| {data[4][1]}| {data[4][2]}\n\n'
                    f'(Last Updated {dt})',
                title='Info.'
            )
            logout = ynbox(
                "Would you like to log out of the admin account?: ",
                title="Logout?")
            if logout:
                varsetup()
            if not logout:
                leaderabilities()

    if option == optionchoices[2]:
        # This lets the User View One Volunteers info.
        f = open("volunteers.csv", "r")
        reader = csv.reader(f)
        data = []
        # Reads the csv into list
        for row in reader:
            data.append(row)
        whichv = enterbox("Which Volunteer Would you like to view?", title="Volunteer Picker")
        for i in range(0, len(data)):
            # Searches For User, from the name and prints it if it is found
            if whichv == data[i][0]:
                onevol = str(data[i][0]) + "     |     " + str(data[i][1]) + "     |    " + str(data[i][2])
                msgbox("Volunteer|Total Counted|Accuracy (%)\n" + onevol)
                startagain = ynbox("Would You Like to Start Again: ", title="Start Again?")
                if startagain:
                    leaderabilities()
                else:
                    exit()
        if whichv not in data:
            msgbox("Volunteer Does Not Exist.", title="Not Found")
    if option == optionchoices[3]:
        addchoices = ["Add A Volunteer Account", "Add A Team Leader Account"]
        aoption = buttonbox("Choose An Option", title="Add Option", choices=addchoices)

        if aoption == addchoices[0]:
            whichu = enterbox("What is the name of the Volunteer You Would Like to Add?",
                              title="Volunteer Name")
            whichp = enterbox("What is the password for the Account?",
                              title="Volunteer Password")
            data = [whichu, whichp]
            print(data)
            with open('volunteeraccounts.csv', 'a') as fd:
                fd.write("\n" + str(data[0]) + "," + str(data[1]))
            data1 = [whichu, 0, 0]
            with open('volunteers.csv', 'a') as fd:
                fd.write("\n" + str(data1[0]) + "," + str(data1[1]) + "," + str(data1[2]))
            msgbox("User is added to the server", title="Added")
            logout = ynbox(
                "Would you like to log out of the admin account?: ",
                title="Logout?")
            if logout:
                varsetup()
            if not logout:
                leaderabilities()
        if aoption == addchoices[1]:
            whichu = enterbox("What is the name of the Team Leader You Would Like to Add?",
                              title="Volunteer Name")
            whichp = enterbox("What is the password for the Account?",
                              title="Volunteer Password")
            data = [whichu, whichp]
            print(data)
            with open('leaderaccounts.csv', 'a') as fd:
                fd.write("\n" + str(data[0]) + "," + str(data[1]))
            msgbox("User is added to the server", title="Added")
            logout = ynbox(
                "Would you like to log out of the admin account?: ",
                title="Logout?")
            if logout:
                varsetup()
            if not logout:
                leaderabilities()
    if option == optionchoices[4]:
        # Reads the data into a list, then finds the  user inside the file
        # Then ammends the whole list with the changed user info
        deluseroptions = ["Volunteer", "Team Leader"]
        deluservol = buttonbox("What would you like to delete?", title="Delete",
                               choices=deluseroptions)
        deluser = enterbox("Which user do you want to delete",
                           title="User Deletion")
        if deluservol == deluseroptions[0]:
            with open('volunteeraccounts.csv', newline='') as f:
                reader = csv.reader(f)
                data = list(reader)
                for i in range(0, len(data)):
                    if deluser in data[i]:
                        del data[i]
                        file = open('volunteeraccounts.csv', 'w+', newline='')
                        with file:
                            write = csv.writer(file)
                            write.writerows(data)
            with open('volunteers.csv', newline='') as f:
                reader = csv.reader(f)
                data1 = list(reader)
                print(data1)
                for i in range(0, len(data1)):
                    print(i)
                    if deluser in data1[i]:
                        del data1[i]
                        file = open('volunteers.csv', 'w+', newline='')
                        with file:
                            write = csv.writer(file)
                            write.writerows(data1)
            msgbox("Account Removed Form Server.", title="Removed")
            logout = ynbox(
                "Would you like to log out of the admin account?: ",
                title="Logout?")
            if logout:
                varsetup()
            if not logout:
                leaderabilities()
        if deluservol == deluseroptions[1]:
            with open('leaderaccounts.csv', newline='') as f:
                reader = csv.reader(f)
                data = list(reader)
                for i in range(0, len(data)):
                    if deluser in data[i]:
                        del data[i]
                        file = open('leaderaccounts.csv', 'w+', newline='')
                        with file:
                            write = csv.writer(file)
                            write.writerows(data)
            msgbox("Account Removed Form Server.", title="Removed")
            logout = ynbox(
                "Would you like to log out of the admin account?: ",
                title="Logout?")
            if logout:
                varsetup()
            if not logout:
                leaderabilities()
    if option == optionchoices[5]:
        exit()


'------------------------------- Volunteer Login ------------------------------'


# This Function allows a Volunteer to log in to their account
def volunteerlogin(retry, cvalues, bvalues, sessiontotal, sessionright,
                   sessionwrong, attemps):
    """This uses the values in 'volunteeraccounts.csv' and
        compares them with the users input"""

    volusern = []
    volpass = []
    with open("volunteeraccounts.csv", "r") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for lines in csv_reader:
            volusern.append(lines[0])
    with open("volunteeraccounts.csv", "r") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for lines in csv_reader:
            volpass.append(lines[1])

    i: int
    for i in range(0, 3):
        volunteerusern = enterbox("Enter Username", "Username Enter")
        volunteerpassword = passwordbox("Enter Password", title="Volunteer Password")
        if volunteerusern in volusern and volunteerpassword in volpass:
            currentuser = volunteerusern
            volunteerabilities(retry, cvalues, bvalues, sessiontotal,
                               currentuser, sessionright, sessionwrong, attemps)
            break
        else:
            # This lets the user have 3 attemps at entering a correct UN and PW
            attemps = 2 - i
            msgbox("Incorrect Password or username\n (You have " + str(attemps) + " Attemps Left)")


'------------------------------- Startup ------------------------------'

# This Starts The program
varsetup()
