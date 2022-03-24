'''
LT
HTL 2022
Databank-Guessing-Game
'''

#imports
import random
import mysql.connector as mariadb

mydb = None
mycursor = None

#keep the db-setup seperate from the rest of the code!
def database_setup():
    #optional add the database name below to auto connect
    global mydb
    mydb = mariadb.connect(
        host="localhost",
        user="lucas",
        password="lucas",
        database="guessing_game_high_score"
    )

    global mycursor
    mycursor = mydb.cursor()

    mycursor.execute("CREATE DATABASE IF NOT EXISTS guessing_game_high_score")
    #check if it worked?
    #mycursor.execute("SHOW DATABASES")
    #for x in mycursor:
    #    print(x)
    
    mycursor.execute("USE guessing_game_high_score")    
    mycursor.execute("""CREATE TABLE IF NOT EXISTS highscore
                    (name VARCHAR(100) PRIMARY KEY,
                     guesses_nr INT)""")
    #check if it worked?
    #mycursor.execute("SHOW TABLES")
    #for x in mycursor:
    #    print(x)
    
    #add some dummy user to the table ACHTUNG %s hat mit dem cursor
    #zu tun und nicht mit python!!!
    #IGNORE ist für Einträge die schon existieren
    sql = "INSERT IGNORE INTO highscore (name, guesses_nr) VALUES (%s,%s)"
    val =[
        ('Sepp', 101),
        ('Franz', 111),
        ('Ignazius', 121)
        ]
        
    mycursor.executemany(sql,val)
    mydb.commit()
    
    #check if it worked?
    #mycursor.execute("SELECT * FROM highscore")
    #for x in mycursor:
    #    print(x)
        

def show_highscore(mycursor):
    print()
    mycursor.execute("SELECT * FROM highscore ORDER BY guesses_nr")
    print("#########################################")
    print("###### The current highscore list  ######")
    print("#########################################")
    print("#{0:^19}#{1:^19}#".format("Name","Number of guesses"))
    print("#########################################")
    for name, guesses_nr in mycursor:
        print("#{0:^19}#{1:^19}#".format(name, guesses_nr))
    print("#########################################")
    print()








####### What Lucas did #######

#function to check if the user is already in the databank
def check_duplicate(userName):
    mycursor = mydb.cursor()
    
    sql = "SELECT name FROM highscore WHERE(name = %s)"
    val = [(userName)] #you have to insert a list or a tuple so you have to make it a list with []
    
    mycursor.execute(sql,val)
    
    myresult = mycursor.fetchone()
    
    if myresult == None:
        return 0
    
    else:
        return 1



#function to update the highscore, if the new score is better than the old one
def update_highscore(name, number):
    
    mycursor = mydb.cursor()
    
    #checks if the user is already in the databank
    check = check_duplicate(name)
    
    #return 0 = user is not in databank
    if check == 0:
        
        #puts name and score in databank
        sql = "INSERT IGNORE INTO highscore (name, guesses_nr) VALUES (%s,%s)"
        val = [(name, number)]

        mycursor.executemany(sql,val)
        mydb.commit()
    
    
    #return 1 = user is in databank
    else:
        
        #output = trys
        sql = "SELECT guesses_nr FROM highscore WHERE(name = %s)"
        val = [(name)]
    
        mycursor.execute(sql,val)
    
        myresult = mycursor.fetchone()

        #if the new attempt got less trys than the old one, the new number of attempts gets replaced with the old number of attempts
        for i in myresult:
              if i > number:
                  print("Your new best is:", number)
              
                  sql = "UPDATE highscore SET guesses_nr = %s WHERE name = %s"
                  val = [(number,name)]
              
                  mycursor.executemany(sql,val)
                  mydb.commit()
                
              else:
                  print("Your Highscore is: ",i)
        
       

#function to get a random number from 0-10 -> returns only the number of trys
def randNum():
    counter = 0
    userGuess = 11
    randomNum = random.randint(0,10)
    
    while (userGuess != randomNum):
        userGuess = int(input("Guess a number 0-10: "))
        
        #input = too high
        if userGuess > randomNum:
            print("Too large.")
        
        #input = too low
        elif userGuess < randomNum:
            print("Too small.")
        
        #input = the right number
        elif userGuess == randomNum:
            print("The right number was:",randomNum,"\nYou needed:",counter,"trys\nCongrats!")
        
        #error1
        else:
            print("error1: invalid input")
        
        counter += 1
    return counter


    
    
    
    
    
    
######### main program starts here ##########
database_setup()
print("### Welcome to the guessing game! ###")


#definitions & declarations
guessCounter = 0

#Choose between playing(0) - show highscore(1) - quit(2)
print("Type in 0 to play the game\nType in 1 to show the highscore\nType in 2 to quit")
userInputOption1 = int(input("Input: "))


if userInputOption1 == 0:
    userName = str(input("Pick a username: "))
    
    #runs the random Number function
    guessCounter = randNum()
    
    #puts all the stuff in the databank
    update_highscore(userName, guessCounter)
    
elif userInputOption1 == 1:
    show_highscore(mycursor)


elif userInputOption1 == 2:
    print("Bye.")
    
else:
    print("error2: invalid input")
