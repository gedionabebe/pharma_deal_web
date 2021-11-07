import pyrebase
from django.shortcuts import render

from django.http import HttpResponse
from authentication import firebase



def showpro(request):
    
    url = request.POST.get('url')
    user_id = request.session['user_id'] 

    print("Hello")
    try:
        user = firebase.auth.refresh(request.session['refreshidtoken'])
        distributors = firebase.database.child('Distributors').get(user['idToken']).val()
        pharmacies = firebase.database.child('Pharmacies').get(user['idToken']).val()
        
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
            firebase.database.child(x).child(user_id).update({'url':url},user['idToken'])
            
            
        img_url = firebase.database.child(x).child(user_id).child('url').get(user['idToken']).val()
        
        name = firebase.database.child(x).child(user_id).child('name').get(user['idToken']).val()

        privilage = x
        

        return render(request , 'profile.html', {'i': img_url, 'n' : name , 'priv': privilage})
    except Exception as e: 
        print (e)
        return render(request, 'unauthorized.html')

    
    # message = "oops user is logged out"
    # return render(request,"Profile.htm",{"mes":message})


    