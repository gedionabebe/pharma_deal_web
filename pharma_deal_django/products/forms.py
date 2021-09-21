from django import forms

categories = [
    ('drug','Drug'),
    ('medical_equipment','Medical Equipment'),
    ('accessories','Accessories'),
]

class ProductCreateForm(forms.Form):
    product_name = forms.CharField(label='Product Name', widget=forms.TextInput(attrs={'style':'width:400px;', 'class':'form-control'}))
    description = forms.CharField(label= 'Description', widget=forms.Textarea(attrs={"rows":5,"cols":20,'style':'width:400px;','class':'form-control'}))
    brand = forms.CharField(label= 'Brand', widget=forms.TextInput(attrs={'style':'width:400px;','class':'form-control'}))
    manufacturing_company = forms.CharField(label= 'Manufacturing company', widget=forms.TextInput(attrs={'style':'width:400px;','class':'form-control'}))
    form_of_preparation = forms.CharField(label= 'Form of preparation', widget=forms.TextInput(attrs={'style':'width:400px;','class':'form-control'}))
    manufacturing_date = forms.CharField(label= 'Manufacturing date', widget=forms.TextInput(attrs={'style':'width:400px;','class':'form-control'}))
    expiry_date = forms.CharField(label= 'Expiry date', widget=forms.TextInput(attrs={'style':'width:400px;','class':'form-control'}))
    price = forms.CharField(label= 'Price', widget=forms.TextInput(attrs={'style':'width:400px;','class':'form-control'}))
    category = forms.CharField(label='Choose a Category', widget=forms.Select(choices=categories,attrs={'style':'width:200px;','class':'form-control'}))
class filterform(forms.Form):
    filter_category = forms.CharField(label='Filter', widget=forms.Select(choices=categories))