from django.shortcuts import redirect, render
from authentication import firebase
from .forms import ProductCreateForm
from django.core.files.storage import FileSystemStorage
import os
from pharma_deal_django.settings import BASE_DIR



def browse(request):

    if request.session['status'] == 'logged_in':
        
        products = firebase.database.child('Products').get().val()
        for product in products.values():
            print(product)
        return render(request, 'browse.html', {'products':products})
        

    return redirect('/authentication/')
def create(request):
    if request.session['status'] == 'logged_in':
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
            product_id = len(firebase.database.child('Products').get().val())+1
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

    return redirect('/authentication/')

def update(request,product_id):
    if request.session['status'] == 'logged_in':
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
    return redirect('/authentication/')
def delete(request,product_id):
    if request.session['status'] == 'logged_in':
        firebase.database.child('Products').child('pro_00%d'%product_id).remove()
        return redirect('/products/browse/')
    return redirect('/authentication/')
def inventory(request):
    if request.session['status'] == 'logged_in':
        user_id = request.session['user_id']
        
        try:
            user_inventory = firebase.database.child('Products').order_by_child('user_id').equal_to('%s'%user_id).get().val()

            return render(request, 'inventory.html', {'user_inventory':user_inventory})
        except:
            return redirect('/products/create')
    return redirect('/authentication/')





