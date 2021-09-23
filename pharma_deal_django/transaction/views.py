import pyrebase
from django.shortcuts import render,redirect

from django.http import HttpResponse
from authentication import firebase


db = firebase.database

def post_create(request):

    import time 
    from datetime import datetime, timezone
    import pytz
    tz = pytz.timezone('Africa/Addis_Ababa')
    time_now = datetime.now(timezone.utc).astimezone(tz)
    millis = int(time.mktime(time_now.timetuple()))
    print("mill" + str(millis)) 
    Medicine = request.POST.get('medicine')
    Distributor = request.POST.get('distributor')
    Pharmacy = request.session["user_id"]
    distributor_info = db.child('Distributors').child('%s'%Distributor).get().val()['phone_number']
    pharmacy_info = db.child('Pharmacies').child('%s'%Pharmacy).get().val()['phone_number']
   

    pn =  firebase.database.child('Pharmacies').child('%s'%Pharmacy).get().val()['name']
    print(pn)
    product_id = request.POST.get('product_id') 
    Cost = request.POST.get('cost')
    url = request.POST.get('url')
    
    try:
        user_id = request.session['user_id']  

        data = {
            'medicine': Medicine,
            'distributor': Distributor,
            'pharmacy': Pharmacy,
            'product_id': product_id,
            'cost': Cost,
            'status': "pending",
            'url' : url,
            'pharam_name':pn,
            'pharma_info':pharmacy_info,
            'distributor_info':distributor_info,
        }
        db.child('transaction').child(millis).set(data)
       
        return redirect('/transaction/cart_check')
    except KeyError:
        message = "oops user is logged out"
        return render(request,"create.htm",{"mes":message})


def post_check(request):
    if request.session['status'] == 'logged_in' and request.session['privilege'] == 'distributors':
        import datetime
        
        user_id = request.session['user_id']  

        timestamps = db.child('transaction').shallow().get().val()
        #shallow is used to get the key
        lis_time = []
        for i in timestamps:
            lis_time.append(i)
        lis_time.sort(reverse = False)
        print(lis_time)
        ph = []
        me = []
        co = []
        img = []
        stat = []
        p_name= []
        p_info = []
        for i in lis_time:
            pharmacy = db.child('transaction').child(i).child('pharmacy').get().val()
            medicine = db.child('transaction').child(i).child('medicine').get().val()
            cost = db.child('transaction').child(i).child('cost').get().val()
            img_url = db.child('transaction').child(i).child('url').get().val()
            status = db.child('transaction').child(i).child('status').get().val() 
            Distributor_id = db.child('transaction').child(i).child('distributor').get().val()
            pharma_name = db.child('transaction').child(i).child('pharam_name').get().val()
            pharma_info = db.child('transaction').child(i).child('pharma_info').get().val()
            # if status == 'pending' and user_id == Distributor_id:
            if user_id == Distributor_id:
                ph.append(pharmacy)
                me.append(medicine)
                co.append(cost)
                img.append(img_url)
                stat.append(status)
                p_name.append(pharma_name)
                p_info.append(pharma_info)
    
        date=[]
        for i in lis_time:
            i = float(i)
            dat = datetime.datetime.fromtimestamp(i).strftime('%H:%M:%S %d-%m-%y')
            date.append(dat)
        print(date)
        comb_lis = zip(lis_time,date,ph,me,co,img,p_name,stat,p_info)
        return render(request,"post_check.htm",{'comb_lis': comb_lis})
    else :
        return render(request,"login.html")
    
    

def accept(request):
    key = request.POST.get('lis_time')
    
    print(key)
    
    db.child("transaction").child(key).update({'status':'accepted'})
    return redirect('/transaction/post_check')

def decline(request):
    key = request.POST.get('lis_time')
    
    print(key)
    db.child("transaction").child(key).update({'status':'declined'})
    return redirect('/transaction/post_check')



def cart_check(request):
    if request.session['status'] == 'logged_in' and request.session['privilege'] == 'pharmacies':
        import datetime
        
        user_id = request.session['user_id']  

        timestamps = db.child('transaction').shallow().get().val()
        #shallow is used to get the key
        lis_time = []
        for i in timestamps:
            lis_time.append(i)
        lis_time.sort(reverse = False)
        print(lis_time)
        ph = []
        me = []
        co = []
        img = []
        stat = []
        did = []
        pid = []
        p_name= []
        dist_info = []
        for i in lis_time:
            pharmacy = db.child('transaction').child(i).child('pharmacy').get().val()
            medicine = db.child('transaction').child(i).child('medicine').get().val()
            cost = db.child('transaction').child(i).child('cost').get().val()
            img_url = db.child('transaction').child(i).child('url').get().val()
            status = db.child('transaction').child(i).child('status').get().val() 
            Distributor_id = db.child('transaction').child(i).child('distributor').get().val()
            product_id = db.child('transaction').child(i).child('product_id').get().val()
            pharma_name = db.child('transaction').child(i).child('pharam_name').get().val()
            distributor_info = db.child('transaction').child(i).child('distributor_info').get().val()
            if pharmacy == user_id:
                me.append(medicine)
                co.append(cost)
                img.append(img_url)
                stat.append(status)
                did.append(Distributor_id)
                ph.append(pharmacy)
                pid.append(product_id)
                p_name.append(pharma_name)
                dist_info.append(distributor_info)
    
        date=[]
        for i in lis_time:
            i = float(i)
            dat = datetime.datetime.fromtimestamp(i).strftime('%H:%M:%S %d-%m-%y')
            date.append(dat)
        print(date)
        comb_lis = zip(lis_time,date,me,co,img,stat,did,ph,pid,p_name,dist_info)
        print('items:--' ,comb_lis)
        return render(request,"cart_check.htm",{'comb_lis': comb_lis})
    else :
        return render(request,"login.html")
    
    
    