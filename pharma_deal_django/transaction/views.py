import pyrebase
from django.shortcuts import render

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
    Cost = request.POST.get('cost')
    url = request.POST.get('url')
    try:
        user_id = request.session['user_id']  

        data = {
            'medicine': Medicine,
            'distributor': Distributor,
            'pharmacy': Pharmacy,
            'cost': Cost,
            'status': "pending",
            'url' : url,
        }
        db.child('transaction').child(millis).set(data)
       
        return render(request,"check.htm")
    except KeyError:
        message = "oops user is logged out"
        return render(request,"create.htm",{"mes":message})

def check(request):
    
    import datetime
    
    timestamps = db.child('transaction').shallow().get().val()
    #shallow is used to get the key
    lis_time = []
    for i in timestamps:
        lis_time.append(i)
    lis_time.sort(reverse = False)
    print(lis_time)
    req = []
    for i in lis_time:
        pharma = db.child('transaction').child(i).child('pharmacy').get().val()
        name = db.child('transaction').child(i).child('distributor').get().val()
       
        req.append(pharma)
    print(req)
    
    date=[]
    for i in lis_time:
        i = float(i)
        dat = datetime.datetime.fromtimestamp(i).strftime('%H:%M:%S %d-%m-%y')
        date.append(dat)
    print(date)

            #combined list
    comb_lis = zip(lis_time,date,req)
    # name = db.child('users').child(a).child('detail').child('name').get().val()

    return render(request,"check.htm",{'comb_lis': comb_lis})

def post_check(request):
    import datetime
    
    time = request.GET.get('z')
    
    user_id = request.session['user_id']  

    pharmacy = db.child('transaction').child(time).child('pharmacy').get().val()
    medicine = db.child('transaction').child(time).child('medicine').get().val()
    cost = db.child('transaction').child(time).child('cost').get().val()
    img_url = db.child('transaction').child(time).child('url').get().val()
    
    i = float(time)
    dat = datetime.datetime.fromtimestamp(i).strftime('%H:%M:%S %d-%m-%y')

    return render(request , 'post_check.htm', {'p': pharmacy,'m':medicine,'c':cost,'d': dat , 'i': img_url, 't':time})

def accept(request):
    key = request.POST.get('key')
    
    print(key)
    
    db.child("transaction").child(key).update({'status':'accepted'})
    return render(request , 'post_check.htm')

def decline(request):
    key = request.POST.get('key')
    
    print(key)
    db.child("transaction").child(key).update({'status':'declined'})
    return render(request , 'post_check.htm')




def cart(request):
    
    import datetime
    
    timestamps = db.child('transaction').shallow().get().val()
    #shallow is used to get the key
    lis_time = []
    for i in timestamps:
        lis_time.append(i)
    lis_time.sort(reverse = False)
    print(lis_time)
    req = []
    for i in lis_time:
        pharma = db.child('transaction').child(i).child('pharmacy').get().val()
        name = db.child('transaction').child(i).child('distributor').get().val()
       
        req.append(pharma)
    print(req)
    
    date=[]
    for i in lis_time:
        i = float(i)
        dat = datetime.datetime.fromtimestamp(i).strftime('%H:%M:%S %d-%m-%y')
        date.append(dat)
    print(date)

            #combined list
    comb_lis = zip(lis_time,date,req)
    # name = db.child('users').child(a).child('detail').child('name').get().val()

    return render(request,"cart.htm",{'comb_lis': comb_lis})

def cart_check(request):
    import datetime
    
    time = request.GET.get('z')
    
    user_id = request.session['user_id']  

    pharmacy = db.child('transaction').child(time).child('pharmacy').get().val()
    medicine = db.child('transaction').child(time).child('medicine').get().val()
    cost = db.child('transaction').child(time).child('cost').get().val()
    img_url = db.child('transaction').child(time).child('url').get().val()
    status = db.child('transaction').child(time).child('status').get().val()
    
    i = float(time)
    dat = datetime.datetime.fromtimestamp(i).strftime('%H:%M:%S %d-%m-%y')

    return render(request , 'cart_check.htm', {'p': pharmacy,'m':medicine,'c':cost,'d': dat , 'i': img_url, 't':time,'s':status})