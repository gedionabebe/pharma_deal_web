from django.shortcuts import render
from . import firebase
from .forms import loginForm, signupForm

# Create your views here.


def signup(request):
  form = signupForm(request.POST)
  signup_form =signupForm()
  test='Please enter a valid email and password'
  confirm='Please confirm password'
  global user
  
  if form.is_valid():
    email= form.cleaned_data['email']
    password= form.cleaned_data['password']
    confirm_password= form.cleaned_data['confirm_password']
    name= form.cleaned_data['name']
    address= form.cleaned_data['address']
    phone_number=  form.cleaned_data['phone_number']
    type_user= request.POST['kind']
    
    if password == confirm_password:
      try:
        user = firebase.auth.create_user_with_email_and_password(email,password) #returns a dictionary with the user information
        print('10000000000success0000000001',user['localId'])
        print(user['localId'])
        u_id=user['localId']
        
        if type_user == 'distributor':
            data= {'email':'%s'%email, 'name':'%s'%name, 'address':'%s'%address, 'phone_number':'%s'%phone_number, 'user_id':'%s'%u_id}
            firebase.database.child('Distributors').child('%s'%u_id).set(data)
            return render(request, 'home.html', {'user':user})
        elif type_user == 'pharmacy':
            data= {'email':'%s'%email, 'name':'%s'%name, 'address':'%s'%address, 'phone_number':'%s'%phone_number, 'user_id':'%s'%u_id}
            firebase.database.child('Pharmacies').child('%s'%u_id).set(data)
            return render(request, 'mine.html', {'user':user})



        
      except:
          return render(request, 'signup.html', {'signup_form':signup_form,'test':test})
    else:
      return render(request, 'signup.html', {'signup_form':signup_form,'confirm':confirm})
  
  else:
    print(form.errors)
    

  return render(request, 'signup.html', {'signup_form':signup_form})
def login(request):
  form= loginForm(request.POST)
  login_form= loginForm()
  incorrect='Incorrect Email or Passsword'
  global user
  distributors = firebase.database.child('Distributors').get().val()
  pharmacies = firebase.database.child('Pharmacies').get().val()


  if form.is_valid():
    email= form.cleaned_data['email']
    password= form.cleaned_data['password']
    try:
      user = firebase.auth.sign_in_with_email_and_password(email,password)
      print('10000000000success0000000001',user['localId'])
      u_id=user['localId']
      if u_id in distributors:

        return render(request, 'home.html', {'user':user})

      elif u_id in pharmacies:
        return render(request, 'mine.html', {'user':user})
    except:
      return render(request, 'login.html', {'login_form':login_form, 'incorrect':incorrect})
  else:
    print(form.errors)
  return render(request, 'login.html',{'login_form':login_form})