from firebase import firebase

firebase = firebase.FirebaseApplication('https://purge-credits-database.firebaseio.com', None)
def setup(id):
    result = firebase.patch(f'/members/{id}',None)
    print(result)       
    #add credits to users
    cred = firebase.patch(f'/members/{id}',{"credits":50})
    print(cred)
    #add inventory
    firebase.patch(f'/members/{id}',{"purge":0})
    firebase.patch(f'/members/{id}',{"disperse":0})
    firebase.patch(f'/members/{id}',{"splooge":0})
    firebase.patch(f'/members/{id}',{"yo":0}) 
    


def checkuser(memberid):
    #get firebase server
    fmemberid = firebase.get(f'members/{memberid}',None)
    if fmemberid != None:
        return True
    else:
        return False

def loaddata():
    data = firebase.get('members',None)
    return data

def purchase(memberid,usercred,item):
    firebase.patch(f'/members/{memberid}',{"credits":usercred})
    #get item
    numofitems = int(firebase.get(f'/members/{memberid}/{item}',None)) + 1
    firebase.patch(f'/members/{memberid}',{f"{item}":numofitems})

def decreasestock(memberid,item):
    #get item   
    numofitems = int(firebase.get(f'/members/{memberid}/{item}',None)) - 1
    firebase.patch(f'/members/{memberid}',{f'{item}':numofitems})

def increasecredit(memberid,amt):
    #get usercred
    usercred = int(firebase.get(f'/members/{memberid}/credits',None)) + int(amt)
    firebase.patch(f'/members/{memberid}',{"credits":usercred})

def decreasecredit(memberid,amt):
    usercred = int(firebase.get(f'/members/{memberid}/credits',None)) - int(amt)
    firebase.patch(f'/members/{memberid}',{"credits":usercred})

