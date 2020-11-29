"""This Program is the coursework for GCSE Computer Science
Created By Henry Milner. It is a program to help a youth club Count
Coins they have collected Once the User enters the weight of a bag of
coins, it tells them how many coins to add or remove The Volunteer can
also access their account to view the Total  or Volunteer Information
This Program uses Modules like csv, easygui etc.
"""

#This imports the Needed Modules for the Program
import time
from datetime import datetime
import csv
import sys
from easygui import *
###############-VARIABLE SETUP-#########################
def varsetup():
    #This function Sets up variables and lists/tuples that will be used throughout the program
    retry = True
    #Creating Lists for allowed coin types and for correct bag weights (See 'Analysis' file to see these)
    cvalues = ("1p", "2p", "5p", "10p", "20p", "50p", "£1", "£2")
    bvalues = (356, 356, 325, 325, 250, 160, 175, 120)
    sessiontotal = 0
    sessionright = 0
    sessionwrong = 0
    attemps = 0
    uservalues(retry, cvalues, bvalues, sessiontotal, sessionright, sessionwrong, attemps)
###############-USER VALUES-############################
def uservalues(retry, cvalues, bvalues, sessiontotal, sessionright, sessionwrong, attemps):
    #This Function lets the User decide what they want to do
    #It is essentially the Main menu for the program
    fchoices = ["Volunteer Functions", "Team Leader Functions", "Exit Program"]
    option = buttonbox("Choose a Function", title="Function Choice",choices= fchoices)
    if option == fchoices[0]:
        volunteerlogin(retry, cvalues, bvalues, sessiontotal, sessionright, sessionwrong, attemps)
    if option == fchoices[1]:
        leaderabilitieslogin()
    if option == fchoices[2]:
        exit()
###############-VOLUNTEER ABILITIES-####################
def volunteerabilities(retry, cvalues, bvalues, sessiontotal, currentuser, sessionright, sessionwrong,attemps):
    #This Funtion Obtains The Bag's Coin Type and Weight
    ctype = enterbox("Enter The Coin Type: ", title = "Coin Type")
    bweight = enterbox("Enter the Weight of the Bag of " + ctype + "'s In Grams: ", title= "Bag Weight")
    validation(retry, cvalues, bvalues, sessiontotal, ctype, bweight, currentuser, sessionright, sessionwrong,attemps)
###############-USER VALIDATION-########################
def validation(retry, cvalues, bvalues, sessiontotal, ctype, bweight, currentuser, sessionright, sessionwrong, attemps):
    #This Function Validates the Users Inputs (From 'volunteerabilities' Function)
    while retry == True:
        #If the entered Coin type Fits to the allowed coin types, it progresses
        if ctype in cvalues:
            weightammend(retry, ctype, bweight, cvalues, bvalues, sessiontotal, currentuser,sessionright, sessionwrong, attemps)
            retry = False
        #If the entered Coin type Doesn't Fit in the allowed coin types, it Notifies the user
        else:
            msgbox("Please Enter a Valid Coin Type", title = "Error")
            #This asks the user whether they want to start again
            #It uses Boolean to cary on or end the program
            startagain = ynbox("Would You Like to Start Again: ", title="Start Again?")
            if startagain == True:
                uservalues(retry, cvalues, bvalues, sessiontotal, sessionright, sessionwrong, attemps)
            else:
                exit()
            retry = False
###############-WEIGHT AMMENDMENT-######################
def weightammend(retry, ctype, bweight, cvalues, bvalues, sessiontotal, currentuser, sessionright, sessionwrong, attemps):
    #This Function Tells the user how many coins to add or remove, or if it is correct then Adds it to the total
    cindex = cvalues.index(ctype)
    correctbweight = bvalues[cindex]
    #'bagamount' is the monetery value of each bag for each coin type
    #'onecoinweight' is the weight of one coin for each coin type
    bagamount = [1, 1, 5, 5, 10, 10, 20, 20]
    onecoinweight = [3.56, 7.12, 3.25, 6.5, 5, 8, 8.75, 12]
    #This if statement is for when the entered bag weight is CORRECT
    #It adds the monetary value to the correct user and to the 'coincountfile.txt'
    if int(bweight) == int(correctbweight):
        msgbox("Bag Weight Is Correct (£ "+str(bagamount[cindex])+" Added To Total)", "Correct")
        sessiontotal = sessiontotal + bagamount[cindex]
        attemps = attemps + 1
        sessionright = sessionright+1
        time.sleep(1)
        csvreadandwrite(sessiontotal, currentuser, sessionright, sessionwrong, attemps)
        time.sleep(2)
        startagain = ynbox("Would You Like to Start Again: ", title="Start Again?")
        if startagain == True:
            uservalues(retry, cvalues, bvalues, sessiontotal, sessionright, sessionwrong, attemps)
        else:
            exit()
    #This if statement is for when the entered bag weight is HIGHER than the Correct weight
    #It notifies the user much many coins to REMOVE FROM the bag, then asks to start again
    if int(bweight) > correctbweight:
        sessionwrong = sessionwrong + 1
        attemps = attemps + 1
        outbag = int(bweight) - int(correctbweight)
        outcoin = round(outbag / onecoinweight[cindex])
        msgbox("Remove: "+str(outcoin)+ " Coin/s From Bag", title = "Remove")
        time.sleep(2)
        startagain = ynbox("Would You Like to Start Again: ", title="Start Again?")
        if startagain == True:
            uservalues(retry, cvalues, bvalues, sessiontotal, sessionright, sessionwrong, attemps)
        else:
            exit()
    #This if statement is for when the entered bag weight is LOWER than the Correct weight
    #It notifies the user much many coins to ADD TO the bag, then asks to start again
    if int(bweight) < correctbweight:
        sessionwrong = sessionwrong + 1
        attemps = attemps + 1
        outbag = int(correctbweight) - int(bweight)
        outcoin = round(outbag / onecoinweight[cindex])
        msgbox("Add: "+str(outcoin)+ " Coin/s To Bag", title = "Add")
        time.sleep(2)
        startagain = ynbox("Would You Like to Start Again: ", title="Start Again?")
        if startagain == True:
            uservalues(retry, cvalues, bvalues, sessiontotal, sessionright, sessionwrong, attemps)
        else:
            exit()
###############-CSV CHANGER-############################
def csvreadandwrite(sessiontotal, currentuser, sessionright, sessionwrong, attemps):
    #This Ammends the 'coincount.txt' file
    file = open("coincountfile.txt", "r")
    #Reads the file into a list, then adds the total ('sessiontotal'), Then writes it back into the file
    read = int(file.read())
    file.close()
    csvinput = read + sessiontotal
    csvinput = str(csvinput)
    file = open("coincountfile.txt", "w")
    file.write(csvinput)
    file.close()

    #This ammends the 'volunteers.csv' file
    with open('volunteers.csv', newline='') as f:
        #Reads the data into a list, then finds the current user inside the file
        #Then ammends the whole list with the changed user info
        #rewrites the file
        reader = csv.reader(f)
        data = list(reader)
    for i in range(1, len(data)):
        if data[i][0] == currentuser:
            csvuser = data[i]
            usertotal = data[i][1]
            totalammend = int(sessiontotal) + int(usertotal)
            totalpercentage = (sessionright/attemps)*100
            deldata = data.index(csvuser)
            del data[deldata]
            csvuserammended = currentuser
            data.append([csvuserammended, totalammend, totalpercentage])
            file = open('volunteers.csv', 'w+', newline='')
            with file:
                write = csv.writer(file)
                write.writerows(data)
###############-LEADER LOGIN-###########################
def leaderabilitieslogin():
    #This Function allows a Leader to log in to their account
    #'leaders' tuple is the team leader username's allowed
    leaders = ("Henry", "Alex", "Elliott", "Karina")
    for i in range(0, 4):
        leaderusern = enterbox("Enter Username", "Username Enter")
        leaderpassword = passwordbox("Enter Password", title = "Volunteer Password")
        if leaderusern in leaders and leaderpassword == "admin":
            leaderabilities()
            break
        else:
            #This lets the user have 3 attemps at entering a correct UN and PW
            attemps = 2- i
            msgbox("Incorrect Password or username\n (You have " + str(attemps) + " Attemps Left)")
###############-LEADER ABILITIES-#######################
def leaderabilities():
    #This Function Lets the leader View The Total or View Volunteer Information
    now = datetime.now()
    optionchoices = ["View Total", "View Volunteer Info.", "View One Volunteer", "Exit Program"]
    option = buttonbox("Choose a Function", title="Function Choice", choices=optionchoices)

    if option == optionchoices[0]:
        #This Tells The User the Total Amount of money counted by all Volunteers
        file = open("coincountfile.txt", "r")
        #Reads File into variable, then outputs it along with the Current Time
        total = str(file.read())
        totalp = "£" + total + ".00"
        dt = now.strftime("%d/%m/%Y %H:%M:%S") #Current Time
        msgbox("The Total Amount of Money Counted so far is: " + str(totalp) + "\n(Last Updated  " + dt + ")")
        logout = ynbox("Would you like to log out of the admin account?: ", title="Logout?")
        if logout == True:
            varsetup()
        if logout == False:
            leaderabilities()

    if option == optionchoices[1]:
        #This Tells the User All the information from every volunteer
        dt = now.strftime("%d/%m/%Y %H:%M:%S") #Current Time
        with open('volunteers.csv', newline='') as f:
            reader = csv.reader(f)
            #Reads Data into list, then prints the whole list
            data = [list(row) for row in reader]
            msgbox(msg = str(data[0][0])+"| "+str(data[0][1])+"| "+str(data[0][2])+"\n"+str(data[1][0])+"| "+str(data[1][1])+"| "+str(data[1][2])+"\n"+str(data[2][0])+"| "+str(data[2][1])+"| "+str(data[2][2])+"\n"+str(data[3][0])+"| "+str(data[3][1])+"| "+str(data[3][2])+"\n"+str(data[4][0])+"| "+str(data[4][1])+"| "+str(data[4][2]) + "\n\n(Last Updated  " + dt + ")", title = "Info.")
            logout = ynbox("Would you like to log out of the admin account?: ", title="Logout?")
            if logout == True:
                varsetup()
            if logout == False:
                leaderabilities()

    if option == optionchoices[2]:
        #This lets the User View One Volunteers info.
        f = open("volunteers.csv", "r")
        reader = csv.reader(f)
        data = []
        #Reads the csv into list
        for row in reader:
            data.append(row)
        whichv = enterbox("Which Volunteer Would you like to view?", title="Volunteer Picker")
        for i in range(0,len(data)):
            #Searches For User, from the name and prints it if it is found
            if whichv == data[i][0]:
                onevol = str(data[i][0])+"     |     "+str(data[i][1])+"     |    "+str(data[i][2])
                msgbox("Volunteer|Total Counted|Accuracy (%)\n"+onevol)
                startagain = ynbox("Would You Like to Start Again: ", title="Start Again?")
                if startagain == True:
                    leaderabilities()
                else:
                    exit()
        if whichv not in data:
            msgbox("Volunteer Does Not Exist.", title="Not Found")

    if option == optionchoices[3]:
        exit()
###############-VOLUNTEER LOGIN-########################
def volunteerlogin(retry, cvalues, bvalues, sessiontotal, sessionright, sessionwrong, attemps):
    #This Function allows a Volunteer to log in to their account
    #'volunteers' tuple is the team leader username's allowed
    volunteers = ("Henry", "Alex", "Elliott", "Karina")
    i: int
    for i in range(0, 4):
        volunteerusern = enterbox("Enter Username", "Username Enter")
        volunteerpassword = passwordbox("Enter Password", title = "Volunteer Password")
        if volunteerusern in volunteers and volunteerpassword == "password":
            currentuser = volunteerusern
            volunteerabilities(retry, cvalues, bvalues, sessiontotal, currentuser, sessionright, sessionwrong, attemps)
            break
        else:
            #This lets the user have 3 attemps at entering a correct UN and PW
            attemps = 2 - i
            msgbox("Incorrect Password or username\n (You have "+str(attemps)+" Attemps Left)")



        ###############-STARTUP-########################
###############-START PROGRAM-#########################
#This Starts The program
varsetup()
