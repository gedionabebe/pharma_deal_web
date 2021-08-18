from django import forms

categories = [
    ('drug','Drug'),
    ('medical_equipment','Medical Equipment'),
    ('accessories','Accessories'),
]

class ProductCreateForm(forms.Form):
    product_name = forms.CharField(label='Name')
    description = forms.CharField(label= 'Description', widget=forms.Textarea(attrs={"rows":5,"cols":20}))
    brand = forms.CharField(label= 'Brand')
    manufacturing_company = forms.CharField(label= 'Manufacturing company')
    form_of_preparation = forms.CharField(label= 'Form of preparation')
    manufacturing_date = forms.CharField(label= 'Manufacturing date')
    expiry_date = forms.CharField(label= 'Expiry date')
    price = forms.CharField(label= 'Price')
    category = forms.CharField(label='Category', widget=forms.Select(choices=categories))
class filterform(forms.Form):
    filter_category = forms.CharField(label='Filter', widget=forms.Select(choices=categories))