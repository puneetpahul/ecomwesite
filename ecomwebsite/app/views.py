from django.shortcuts import render,redirect
from django.views import View
from app.models import Product,Customer, Cart,OrderPlaced
from .forms import CustomerRegistrationForm,LoginForm, CustomerProfileForm
from django.db.models import Q
from django.http.response import JsonResponse
from django.contrib.auth.decorators import login_required  ## For Function Based View
from django.utils.decorators import method_decorator ## for class based views #


# def home(request):
#  return render(request, 'app/home.html')

class ProductView(View):
    def get(self,request):
        totalitem = 0
        topwears = Product.objects.filter(category = 'TW')
        bottomwears= Product.objects.filter(category = 'BW')
        mobiles = Product.objects.filter(category = 'M')
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
        return render(request, 'app/home.html',{'topwears':topwears,'bottomwears':bottomwears,'mobiles' : mobiles,'totalitem':totalitem})
 
# def product_detail(request):
#  return render(request, 'app/productdetail.html')
class ProductDetailView(View):
    def get(self,request,pk):
        totalitem = 0
        product = Product.objects.get(pk=pk)
        item_already_in_cart = False
        if request.user.is_authenticated:
            item_already_in_cart = Cart.objects.filter(Q(product=product.id) & Q(user=request.user)).exists()
            totalitem = len(Cart.objects.filter(user=request.user))
        return render(request, 'app/productdetail.html',{'product':product,'item_already_in_cart':item_already_in_cart,'totalitem':totalitem})



## This function will add product in card using form hidden field
@login_required
def add_to_cart(request):
    user = request.user
    product_id = request.GET.get('prod_id')
    product=Product.objects.get(id=product_id)
    Cart(user=user,product=product).save()
    return redirect('/')

## this function will shows and perform calculation about products in Cart model
@login_required
def show_cart(request):
    if request.user.is_authenticated:
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = 0.0
        shipping_amount = 70.0
        total_amount = 0.0
        cart_product = [p for p in Cart.objects.all() if p.user == request.user]
        if cart_product:
            for p in cart_product:
                tempamount = (p.quantiy * p.product.discounted_price) 
                amount += tempamount
                totalamount = amount + shipping_amount
            return render(request, 'app/addtocart.html',{'carts':cart,'totalamount':totalamount,'amount':amount})
        else:
            return render(request, 'app/emptycart.html')


#### Ajax 
@login_required
def plus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user= request.user))
        c.quantiy += 1
        c.save()
        amount = 0.0
        shipping_amount = 70.0
        cart_product = [p for p in Cart.objects.all() if p.user == request.user]
        
        for p in cart_product:
            tempamount = (p.quantiy * p.product.discounted_price) 
            amount += tempamount
            totalamount = amount + shipping_amount
        data = {
            'quantity': c.quantiy,
            'amount': amount,
            'totalamount': totalamount
            }
        
        
        return JsonResponse(data)


####  Minus Ajax 
@login_required
def minus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user= request.user))
        c.quantiy -= 1
        c.save()
        amount = 0.0
        shipping_amount = 70.0
        cart_product = [p for p in Cart.objects.all() if p.user == request.user]
        
        for p in cart_product:
            tempamount = (p.quantiy * p.product.discounted_price) 
            amount += tempamount
            totalamount = amount + shipping_amount
        minus_data = {
            'quantity': c.quantiy,
            'amount': amount,
            'totalamount': totalamount
            }
        return JsonResponse(minus_data)


####  remove cartAjax
@login_required
def remove_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user= request.user))
        
        c.delete()
        amount = 0.0
        shipping_amount = 70.0
        cart_product = [p for p in Cart.objects.all() if p.user == request.user]
        
        for p in cart_product:
            tempamount = (p.quantiy * p.product.discounted_price) 
            amount += tempamount
            totalamount = amount + shipping_amount
        remove_data = {
            'amount': amount,
            'totalamount': totalamount,
        }
        return JsonResponse(remove_data)


def buy_now(request):
 return render(request, 'app/buynow.html')


@login_required
def address(request):
    add = Customer.objects.filter(user=request.user)
    return render(request, 'app/address.html',{'add':add,'active':'btn-primary'})





### Mobile ###
def mobile(request,data=None):
    if data == None:
        mobiles = Product.objects.filter(category = 'M')
    elif data == 'Redmi' or data == 'Samsung':
        mobiles = Product.objects.filter(category = 'M').filter(brand=data)
    elif data == 'below':
        mobiles = Product.objects.filter(category = 'M').filter(discounted_price__lte = 10000)
    elif data == 'above':
        mobiles = Product.objects.filter(category='M').filter(discounted_price__gte = 10000)
    return render(request, 'app/mobile.html',{'mobiles' : mobiles})

### TopWear ###
def topwear(request,data=None):
    if data == None:
        topwears = Product.objects.filter(category = 'TW')
    elif data == 'Addidas' or data == 'Puma':
        topwears = Product.objects.filter(category = 'TW').filter(brand=data)
    elif data == 'below':
        topwears = Product.objects.filter(category = 'TW').filter(discounted_price__lte = 500)
    elif data == 'above':
        topwears = Product.objects.filter(category='TW').filter(discounted_price__gte = 500)
    return render(request, 'app/topwear.html',{'topwears' :topwears })

### bottomWear ###
def bottomwear(request,data=None):
    if data == None:
        bottomwears = Product.objects.filter(category = 'BW')
    elif data == 'lee' or data == 'Maruti':
        bottomwears = Product.objects.filter(category = 'BW').filter(brand=data)
    elif data == 'below':
        bottomwears = Product.objects.filter(category = 'BW').filter(discounted_price__lte = 500)
    elif data == 'above':
        bottomwears = Product.objects.filter(category='BW').filter(discounted_price__gte = 500)
    return render(request, 'app/bottomwear.html',{'bottomwears' : bottomwears})

### laptop ###
def laptop(request,data=None):
    if data == None:
        laptops = Product.objects.filter(category = 'L')
    elif data == 'Dell' or data == 'HP':
        laptops = Product.objects.filter(category = 'L').filter(brand=data)
    elif data == 'below':
        laptops = Product.objects.filter(category = 'L').filter(discounted_price__lte = 30000)
    elif data == 'above':
        laptops = Product.objects.filter(category='L').filter(discounted_price__gte = 30000)
    return render(request, 'app/laptop.html',{'laptops' : laptops})




from django.contrib import messages
class CustomerRegistrationView(View):
    def get(self,request):
        form = CustomerRegistrationForm()
        return render(request, 'app/customerregistration.html',{'form':form})
    def post(self,request):
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            messages.success(request,'Congratulations !! Registered successfully')
            form.save()
        return render(request, 'app/customerregistration.html',{'form':form})

    
@login_required
def checkout(request):
    user = request.user
    add = Customer.objects.filter(user=user)
    cart_items = Cart.objects.filter(user=user)
    amount = 0.0
    shipping_amount = 70.0
    totalamount = 0.0
    cart_product = [p for p in Cart.objects.all() if p.user == request.user]
    if cart_product:  
        for p in cart_product:
            tempamount = (p.quantiy * p.product.discounted_price) 
            amount += tempamount
        totalamount = amount + shipping_amount

    return render(request, 'app/checkout.html',{'add':add,'totalamount':totalamount,'cart_items':cart_items})

@login_required
def paymentdone(request):
    user = request.user
    custid = request.GET.get('custid')
    customer = Customer.objects.get(id=custid)
    cart = Cart.objects.filter(user=user)
    for c in cart:
        OrderPlaced(user=user,customer=customer,product =c.product,quantiy=c.quantiy).save()
        c.delete()
    return redirect("orders")

@login_required
def orders(request):
    op=OrderPlaced.objects.filter(user=request.user)
    return render(request, 'app/orders.html',{'order_placed': op})




# def profile(request):
#  return render(request, 'app/profile.html')

@method_decorator(login_required,name ='dispatch')
class ProfileView(View):
    def get(self,request):
        form = CustomerProfileForm()
        return render(request, 'app/profile.html',{'form':form,'active':'primary'})
    def post(self,request):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            user = request.user
            name = form.cleaned_data['name']
            locality = form.cleaned_data['locality']
            city = form.cleaned_data['city']
            state = form.cleaned_data['state']
            zipcode = form.cleaned_data['zipcode']
            reg = Customer(user=user,name=name,locality=locality,city=city,state=state,zipcode=zipcode)
            reg.save()
            messages.success(request,'Conguratulation profile Updated successfully' )
        return render(request, 'app/profile.html',{'form':form,'active':'primary'})    
