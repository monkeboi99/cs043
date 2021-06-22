from database import Simpledb
db=Simpledb('data.txt')

dude=''

while True:
    if dude =='':
        print ('add, find, delete, update, or quit? (enter the first letter of your command)')
        dude=input()
        
    if dude == 'a':
        print('Enter a name.')
        name1=input()
        print('Enter a phone number.')
        number1=input()
        db.insert(name1, number1)
        dude=''
        
    if dude=='f':
        print('Enter a name.')
        name2=input()
        bot=db.select_one(name2)
        if bot==None:
            print('Not found')
        else:
            print(bot)
        dude=''
        
    if dude=='d':
        print('Enter a name.')
        name3=input()
        db.delete(name3)
        dude=''
        
    if dude=='u':
        print('Enter a name.')
        name4=input()
        foundornot=db.select_one(name4)
        if foundornot==None:
            print('Not found')
        else:
            print('Enter a new phone number.')
            number2=input()
            db.update(name4,number2)
        dude=''
        
    if dude=='q':
        break
        
        
        
    
    
