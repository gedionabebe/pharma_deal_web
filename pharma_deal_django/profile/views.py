import pyrebase
from django.shortcuts import render

from django.http import HttpResponse
from authentication import firebase



def showpro(request):
    
    url = request.POST.get('url')
    user_id = request.session['user_id'] 

    print("Hello")

    distributors = firebase.database.child('Distributors').get().val()
    pharmacies = firebase.database.child('Pharmacies').get().val()
    
    for i in distributors:
        if i == user_id:
            #print ("distributor")
            x = 'Distributors'
            print(x)
            
       
        
    for i in pharmacies:
        if i == user_id:
            #print ("pharmacies")
            x = 'Pharmacies'
            
            print (x)


    if 'prof' in request.POST:
        firebase.database.child(x).child(user_id).update({'url':url})
        
        
    img_url = firebase.database.child(x).child(user_id).child('url').get().val()
    
    name = firebase.database.child(x).child(user_id).child('name').get().val()

    privilage = x
    

    return render(request , 'Profile.htm', {'i': img_url, 'n' : name , 'priv': privilage})

    
    # message = "oops user is logged out"
    # return render(request,"Profile.htm",{"mes":message})


    