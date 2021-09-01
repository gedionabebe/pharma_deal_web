from django.shortcuts import render,redirect
from authentication import firebase



def review_and_rate(request):
    if request.session['status'] == 'logged_in':
        if request.POST['transaction_status'] == 'accepted':
            if request.POST['pharma_id'] == request.session['user_id']:
                status = request.POST['transaction_status']
                pharma_id = request.POST['pharam_id']
                product_id = request.POST['product_id']
                review_input = request.POST.get('review_and_rate')
                
                if review_input != None:
                    review_id = len(firebase.database.child('review_and_ratings').get().val())+138
                    user_review = request.POST['review']
                    user_rating = request.POST['rating']
                    data ={'review_id':'rev00%s'%review_id,'pharmacy_id':'%s'%pharma_id,'product_id':'%s'%product_id,
                           'user_review':'%s'%user_review,'user_rating':'%s'%user_rating
                    }
                    firebase.database.child('reviews_and_ratings').child('rev00%d'%review_id).set(data)

                return render(request, 'rate_and_review.html',{'pharma_id':pharma_id,'product_id':product_id,'status':status})

    return redirect('/authentication/')


