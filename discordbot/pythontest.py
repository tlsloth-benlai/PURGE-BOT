import random 
list = ["stop pranking","LIAR","i can see your fats","leifsen im conducting an interview here"]
message = "yo"
person = input("Hey bro, are you fat or very fat?: ")
while person is not "FAT" or person is not "VERY FAT":
    person = input("Hey bro, are you fat or very fat?: ")
    if person == "FAT":
        print("hey, its okay bro. Weight is an issue that we all struggle on. Don't be so harsh on yourself.")
        break
    elif person == "VERY FAT":
        print("WOAH CALM DOWN THERE BIG BERTHA")
        break
    else:
        randomnumber = random.randint(0,4)
        print(f"{list[randomnumber]}")

