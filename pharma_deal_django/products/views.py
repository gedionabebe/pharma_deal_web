
from django.shortcuts import redirect, render
from authentication import firebase
from .forms import ProductCreateForm
from django.core.files.storage import FileSystemStorage
import os
from pharma_deal_django.settings import BASE_DIR




#pharmacies = firebase.database.child('Pharmacies').get().val()

#global search_results
search_results = []

def browse(request):

    if request.session['status'] == 'logged_in':
        
        products = firebase.database.child('Products').get().val()
        for product in products.values():
            print(product)
        return render(request, 'browse.html', {'products':products})
        

    return redirect('/authentication/')
def create(request):
    if request.session['status'] == 'logged_in':
        #distributors = firebase.database.child('Distributors').get().val()
        if request.session['privilege'] == 'distributors':
            p_form = ProductCreateForm(request.POST)
            create_form = ProductCreateForm()
            if p_form.is_valid():
                product_name = p_form.cleaned_data['product_name']
                description = p_form.cleaned_data['description']
                brand = p_form.cleaned_data['brand']
                manufacturing_company = p_form.cleaned_data['manufacturing_company']
                form_of_preparation = p_form.cleaned_data['form_of_preparation']
                manufacturing_date = p_form.cleaned_data['manufacturing_date']
                expiry_date = p_form.cleaned_data['expiry_date']
                category = p_form.cleaned_data['category']
                price = int(p_form.cleaned_data['price'])
                product_image = request.FILES['pro_image']
                product_id = len(firebase.database.child('Products').get().val())+138
                user_id = request.session['user_id']

                path = os.path.join(BASE_DIR, 'media/image/%d'%product_id)
                filesys = FileSystemStorage(location='%s'%path, base_url='/media/image/%d'%product_id)
                imagename = filesys.save(product_image.name,product_image)
                storage_path = 'media/image/%s/%s'%(product_id,imagename)
                firebase.storage.child(storage_path).put(storage_path)
                url = firebase.storage.child('media/image/%s/%s'%(product_id,imagename)).get_url(None)

                data = {'product_id':'%s'%product_id,'product_name':'%s'%product_name,
                        'description':'%s'%description,'brand':'%s'%brand,
                        'manufacturing_company':'%s'%manufacturing_company,'form_of_preparation':'%s'%form_of_preparation,
                        'manufacturing_date':'%s'%manufacturing_date,'expiry_date':'%s'%expiry_date,
                        'category':'%s'%category,'price':'%s'%price,'product_image':'%s'%url,'user_id':'%s'%user_id,
                        }
                firebase.database.child('Products').child('pro_00%d'%product_id).set(data)
            return render(request, 'create.html', {'create_form':create_form})
        return redirect('/products/browse')
    return redirect('/authentication/')

def update(request,product_id):
    if request.session['status'] == 'logged_in':
        #distributors = firebase.database.child('Distributors').get().val()
        if request.session['privilege'] == 'distributors':
           # print('user_id',request.GET['owner_id'])
            if request.session['user_id'] == request.GET['owner_id']:
                
                print("----===10000000000000001===-------")
                products = firebase.database.child('Products').get()
                single_product={}
                for product in products.each():
                    if int(product.val()['product_id']) == product_id:
                        single_product = product

                name = single_product.val()['product_name']
                description = single_product.val()['description']
                price = int(single_product.val()['price'])
                category = single_product.val()['category']
                brand = single_product.val()['brand']
                manufacturing_company = single_product.val()['manufacturing_company']
                form_of_preparation = single_product.val()['form_of_preparation']
                manufacturing_date = single_product.val()['manufacturing_date']
                expiry_date = single_product.val()['expiry_date']
                product_id = int(single_product.val()['product_id'])
                user_id = request.session['user_id']
                url = single_product.val()['product_image']

                previous_data = {
                    'product_name':'%s'%name,'description':'%s'%description,
                    'brand':'%s'%brand,
                    'manufacturing_company':'%s'%manufacturing_company,'form_of_preparation':'%s'%form_of_preparation,
                    'manufacturing_date':'%s'%manufacturing_date,'expiry_date':'%s'%expiry_date,
                    'category':'%s'%category,'price':'%s'%price,
                            }
                u_form = ProductCreateForm(request.POST)
                update_form = ProductCreateForm(initial= previous_data)
                
                if u_form.is_valid():
                    product_name = u_form.cleaned_data['product_name']
                    description = u_form.cleaned_data['description']
                    brand = u_form.cleaned_data['brand']
                    manufacturing_company = u_form.cleaned_data['manufacturing_company']
                    form_of_preparation = u_form.cleaned_data['form_of_preparation']
                    manufacturing_date = u_form.cleaned_data['manufacturing_date']
                    expiry_date = u_form.cleaned_data['expiry_date']
                    category = u_form.cleaned_data['category']
                    price = int(u_form.cleaned_data['price'])
                    product_image = request.FILES.get('pro_image')

                    if product_image != None:
                        path = os.path.join(BASE_DIR, 'media/image/%d'%product_id)
                        filesys = FileSystemStorage(location='%s'%path, base_url='/media/image/%d'%product_id)
                        imagename = filesys.save(product_image.name,product_image)
                        storage_path = 'media/image/%s/%s'%(product_id,imagename)
                        firebase.storage.child(storage_path).put(storage_path)
                        url = firebase.storage.child('media/image/%s/%s'%(product_id,imagename)).get_url(None)

                    data = {'product_id':'%s'%product_id,'product_name':'%s'%product_name,
                            'description':'%s'%description,'brand':'%s'%brand,
                            'manufacturing_company':'%s'%manufacturing_company,'form_of_preparation':'%s'%form_of_preparation,
                            'manufacturing_date':'%s'%manufacturing_date,'expiry_date':'%s'%expiry_date,
                            'category':'%s'%category,'price':'%s'%price,'product_image':'%s'%url,'user_id':'%s'%user_id,
                            }
                    firebase.database.child('Products').child('pro_00%d'%product_id).update(data)
                    return redirect('/products/inventory/')
                return render(request, 'update.html', {'update_form':update_form, 'single_product':single_product})
            return redirect('/products/inventory')    
        return redirect('/products/browse')
    return redirect('/authentication/')
def delete(request,product_id):
    if request.session['status'] == 'logged_in':
        #distributors = firebase.database.child('Distributors').get().val()
        if request.session['privilege'] == 'distributors':
            if request.session['user_id'] == request.POST.get('owner_id'): 
                firebase.database.child('Products').child('pro_00%d'%product_id).remove()
                return redirect('/products/browse/')
            return redirect('/produts/inventory')
        return redirect('/products/browse')
    return redirect('/authentication/')
def inventory(request):
    if request.session['status'] == 'logged_in':
        #distributors = firebase.database.child('Distributors').get().val()
        if request.session['privilege'] == 'distributors':
            
            user_id = request.session['user_id']
            
            try:
                user_inventory = firebase.database.child('Products').order_by_child('user_id').equal_to('%s'%user_id).get().val()
                print(user_inventory)

                return render(request, 'inventory.html', {'user_inventory':user_inventory})
            except:
                return redirect('/products/create')
        return redirect('/products/browse')
    return redirect('/authentication/')

def search(request):
    if request.session['status'] == 'logged_in':
        search_input= request.POST['search']
        s_input = search_input
        products = firebase.database.child('Products').get().val()
        if search_input != None:
            search_input = str(search_input).split(' ')
            search_result = []
            global search_results
            search_results = search_result

            filters = ['is','the','a','an','is','was','were','and']
            no_reslut = 'Sorry no results found for your search'
            filtered_input = list(filter(lambda each: each not in filters, search_input))
            iter_filter = iter(filtered_input)
            print('filter:--++--',filtered_input)
            #val = next(iter_filter,'*end*')
            #print('each',val)
            for val in filtered_input:
                print('each',val)
                for product in products.values():
                    for detailed in product.values():
                        print('tester',detailed)
                        if val != '*end*':
                            if val.casefold() in detailed.casefold():
                                if product not in search_result:
                                    search_result.append(product)
                            
            print(search_result)
            return render(request, 'search_result.html', {'search_result':search_result, 'no_reslut':no_reslut,'input':s_input})
        return redirect('/products/browse')


    
    return redirect('/authentication/')

def filters(request):
    if request.session['status'] == 'logged_in':
        no_reslut = 'Sorry no results found'
        if request.POST.get('filter') :
            print(request.POST['filter'])
            
            filter_parameters = request.POST['filter']
            f_para = filter_parameters.replace('_',' ').capitalize()
            filtered_result = firebase.database.child('Products').order_by_child('category').equal_to('%s'%filter_parameters).get().val()
            print(filtered_result)
            return render(request, 'filtered_results.html', {'filtered_result':filtered_result, 'no_result':no_reslut,'input':f_para})
        elif request.POST.get('filter_search'):
            filter_parameters = request.POST['filter_search']
            f_para = filter_parameters.replace('_',' ').capitalize()
            filtered_results = []
            print(search_results)
            for items in search_results:
                if items['category'] == filter_parameters:
                    if items not in filtered_results:
                        filtered_results.append(items)
            print(filtered_results)
            return render(request, 'filtered_results.html', {'filtered_results':filtered_results, 'no_result':no_reslut,'input':f_para})





    return redirect('/authentication/')


def single_product(request,product_id):
    if request.session['status'] == 'logged_in':
        product = firebase.database.child('Products').child('pro_00%s'%product_id).get().val()
        reviews = firebase.database.child('reviews_and_ratings').order_by_child('product_id').equal_to('%s'%product_id).get().val()
        print(product)

        return render(request,'single_product.html',{'product':product,'reviews':reviews})
    

    return redirect('/authentication/')