from django.shortcuts import render,redirect,HttpResponseRedirect
from authentication import firebase
import string,random



def review_and_rate(request):
    if request.session['status'] == 'logged_in':
        if request.POST['transaction_status'] == 'accepted':
            if request.POST['pharma_id'] == request.session['user_id']:
                status = request.POST['transaction_status']
                pharma_id = request.POST['pharma_id']
                product_id = request.POST['product_id']
                review_input = request.POST.get('review_and_rate')
                owner_name = request.POST.get('owner_name')
                product_name = request.POST.get('product_name')
                cost = request.POST.get('cost')
                url = request.GET['url']
                print(url)
                #next = request.POST.get('next')
                if review_input != None:
                    review_id = ''.join(random.choices(string.ascii_lowercase + string.digits,k=7))
                    user_review = request.POST['review_and_rate']
                    user_rating = request.POST['rating']
                    user_name = request.POST['user_name']
                    data ={'review_id':'rev00%s'%review_id,'pharmacy_id':'%s'%pharma_id,'product_id':'%s'%product_id,
                           'user_review':'%s'%user_review,'user_rating':'%s'%user_rating,'user_name':'%s'%user_name,
                    }
                    try:
                        user = firebase.auth.refresh(request.session['refreshidtoken'])
                        firebase.database.child('reviews_and_ratings').child('rev00%s'%review_id).set(data,user['idToken'])
                        print('-===============100000001======-------')
                        #print(review_id,user_review,user_rating)
                        return redirect('/transaction/cart_check/')
                    except:
                        return render(request, 'unauthorized.html')

                return render(request, 'rate_and_review.html',{'pharma_id':pharma_id,'product_id':product_id,'status':status,'owner_name':owner_name,'product_name':product_name,'cost':cost,'img_url':url})

    return redirect('/authentication/')


