'''
LT
HTL 2022
Databank-Guessing-Game
'''

# imports
import random
import mysql.connector as mariadb

mydb = None
mycursor = None


# function to create a databank
def database_setup():
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

    mycursor.execute("USE guessing_game_high_score")
    mycursor.execute("""CREATE TABLE IF NOT EXISTS highscore
                    (name VARCHAR(100) PRIMARY KEY,
                     guesses_nr INT)""")

    # some example to check if it worked
    sql = "INSERT IGNORE INTO highscore (name, guesses_nr) VALUES (%s,%s)"
    val = [
        ('Sepp', 101),
        ('Franz', 111),
        ('Ignazius', 121)
    ]

    mycursor.executemany(sql, val)
    mydb.commit()


# function to show highscore from databank
def show_highscore(mycursor):
    print()
    mycursor.execute("SELECT * FROM highscore ORDER BY guesses_nr")
    print("#########################################")
    print("###### The current highscore list  ######")
    print("#########################################")
    print("#{0:^19}#{1:^19}#".format("Name", "Number of guesses"))
    print("#########################################")
    for name, guesses_nr in mycursor:
        print("#{0:^19}#{1:^19}#".format(name, guesses_nr))
    print("#########################################")
    print()


# function to check if the user is already in the databank
def check_duplicate(userName):
    mycursor = mydb.cursor()

    sql = "SELECT name FROM highscore WHERE(name = %s)"
    val = [(userName)]  # you have to insert a list or a tuple so you have to make it a list with []

    mycursor.execute(sql, val)

    myresult = mycursor.fetchone()

    if myresult == None:
        return 0

    else:
        return 1


# function to update the highscore, if the new score is better than the old one
def update_highscore(name, number):
    mycursor = mydb.cursor()
    check = check_duplicate(name)

    if check == 0:
        # puts name and score in databank
        sql = "INSERT IGNORE INTO highscore (name, guesses_nr) VALUES (%s,%s)"
        val = [(name, number)]

        mycursor.executemany(sql, val)
        mydb.commit()

    else:
        sql = "SELECT guesses_nr FROM highscore WHERE(name = %s)"
        val = [(name)]

        mycursor.execute(sql, val)

        myresult = mycursor.fetchone()

        for i in myresult:
            if i > number:
                print("Your new best is:", number)

                sql = "UPDATE highscore SET guesses_nr = %s WHERE name = %s"
                val = [(number, name)]

                mycursor.executemany(sql, val)
                mydb.commit()

            else:
                print("Your Highscore is: ", i)


# function to get a random number from 0-10 -> returns only the number of trys
def randNum():
    counter = 0
    userGuess = 11
    randomNum = random.randint(0, 10)

    while (userGuess != randomNum):
        userGuess = int(input("Guess a number 0-10: "))

        if userGuess > randomNum:
            print("Too large.")

        elif userGuess < randomNum:
            print("Too small.")

        elif userGuess == randomNum:
            print("The right number was:", randomNum, "\nYou needed:", counter, "trys\nCongrats!")

        # error1
        else:
            print("error1: invalid input")

        counter += 1
    return counter


######### main program starts here ##########
database_setup()
print("### Welcome to the guessing game! ###")

# definitions & declarations
guessCounter = 0

print("Type in 0 to play the game\nType in 1 to show the highscore\nType in 2 to quit")
userInputOption1 = int(input("Input: "))

if userInputOption1 == 0:
    userName = str(input("Pick a username: "))

    # runs the random Number function
    guessCounter = randNum()

    # puts all the stuff in the databank
    update_highscore(userName, guessCounter)

elif userInputOption1 == 1:
    show_highscore(mycursor)


elif userInputOption1 == 2:
    print("Bye.")

else:
    # error2
    print("error2: invalid input")
