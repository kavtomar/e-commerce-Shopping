from django.shortcuts import render, redirect
from .models import Product, Contact, Order, OrderUpdate
from math import ceil
from datetime import datetime
from django.contrib import messages
import json
from django.views.decorators.csrf import csrf_exempt
from .paytm import checksum

from django.shortcuts import HttpResponse
from .forms import NewUserForm2
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
MERCHANT_KEY = 'kbzk1DSbJiV_O3p5'
# Create your views here.

def index(request):
    allProds = []
    catprods = Product.objects.values('category', 'id')
    cats = {item['category'] for item in catprods}
    for cat in cats:
        prod = Product.objects.filter(category=cat)
        n = len(prod)
        nSlides = n // 4 + ceil((n / 4) - (n // 4))
        allProds.append([prod, range(1, nSlides), nSlides])
    params = {'allProds': allProds}
    return render(request, 'shop/index.html', params)

def searchMatch(query, item):
    if query in item.desc.lower() or query in item.product_name.lower() or query in item.category.lower()  :
        return True
    else:
        return False
def search(request):
    query = request.GET.get('search')
    allProds = []
    catprods = Product.objects.values('subcategory', 'id')
    cats = {item['subcategory'] for item in catprods}
    for cat in cats:
        prodtemp = Product.objects.filter(subcategory=cat.lower())
        prod = [item for item in prodtemp if searchMatch(query, item)]
        n = len(prod)
        nSlides = n // 4 + ceil((n / 4) - (n // 4))
        if len(prod) != 0:
            allProds.append([prod, range(1, nSlides), nSlides])
    params = {'allProds': allProds, "msg": ""}
    if len(allProds) == 0 or len(query)<4:
        params = {'msg': "Please make sure to enter relevant search query"}
    return render(request, 'shop/search.html', params)


def about(request):
    return render(request, 'shop/about.html')

def contact(request):
    if request.method == "POST":
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        phone = request.POST.get('phone', '')
        review = request.POST.get('review', '')
        contact = Contact(name=name, email=email, phone=phone, review=review, date=datetime.today())
        contact.save()
        messages.success(request, 'Your request has been sent!')

    return render(request, 'shop/contact.html')

def tracker(request):
    if request.method == "POST":
        orderId = request.POST.get('orderId', '')
        email = request.POST.get('email', '')
        try:
            order = Order.objects.filter(order_id=orderId, email= email)
            if len(order)>0:
                update = OrderUpdate.objects.filter(order_id = orderId)
                updates = []
                for item in update:
                    updates.append({'text': item.update_desc, 'time': item.timestamp})
                    response = json.dumps( {"status":"success", "updates": updates, "itemJson":  order[0].items_json},
                                          default=str)
                return HttpResponse(response)
            else:
                return HttpResponse('{"status":"noitem"}')
        except Exception as e:
            return HttpResponse('{"status":"error"}')
    return render(request, 'shop/tracker.html')



def productView(request, myid):
    # Fetch product Using ID
    product = Product.objects.filter(id=myid)
    return render(request, 'shop/products.html', {'product':product[0]})

# @login_required(login_url='/shop/login/')
def checkout(request):
    if request.method == "POST":
        items_json = request.POST.get('items_json', '')
        amount = request.POST.get('amount', '')
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        phone = request.POST.get('phone', '')
        address = request.POST.get('address1', '') + " " + request.POST.get('address2', '')
        city = request.POST.get('city', '')
        state = request.POST.get('state', '')
        zip_code = request.POST.get('zip_code', '')
        order = Order(items_json=items_json,amount=amount,name=name, email=email, phone=phone ,address=address,
                       city=city, state=state, zip_code=zip_code)
        order.save()
        update = OrderUpdate(order_id = order.order_id, update_desc="The order has been placed.")
        update.save()

        thank = True
        id = order.order_id
        return render(request, 'shop/checkout.html', {'thank': thank, 'id': id})
        # messages.success(request, 'Your order has been placed!')
        #Request Paytm to transfer amount to your account
        param_dict = {
            "MID": "",
            "WEBSITE": "WEBSTAGING",
            "INDUSTRY_TYPE_ID": "RETAIL",
            "CHANNEL_ID": "WEB",
            "ORDER_ID": str(order.order_id),
            "CUST_ID": email,
            "TXN_AMOUNT": str(amount),
            "CALLBACK_URL": " http://127.0.0.1:8000/shop/handlerequest/",

           }

        param_dict['CHECKSUMHASH'] = checksum.generateSignature(param_dict, MERCHANT_KEY)
        return render(request, 'shop/paytm.html', {'param_dict': param_dict})
    return render(request, 'shop/checkout.html')

@csrf_exempt
def handlerequest(request):
    # Paytm will send you post request here
    form = request.POST
    response_dict ={}
    for i in form.keys():
        response_dict[i] = form[i]
        if i == 'CHECKSUMHASH':
            checksum = form[i]
    verify = checksum.verify_signature(response_dict, MERCHANT_KEY, checksum)
    if verify:
        if response_dict['RESPCODE'] =='01':
            print('order successfull')
        else:
            print('order is not successful because' + response_dict['RESPMSG'])
    return render(request,'shop/paymentstatus.html', {'response': response_dict})



def privacy(request):
    return render(request, 'shop/privacy.html')

def faq(request):
    return render(request, 'shop/faq.html')


def watches(request):
    allProds = []
    catprods = Product.objects.values('subcategory', 'id')
    cats = {item['subcategory'] for item in catprods}
    for cat in cats:
        prod = Product.objects.filter(subcategory=cat.lower())
        if cat.__contains__('watch'):
            n = len(prod)
            nSlides = n // 4 + ceil((n / 4) - (n // 4))
            allProds.append([prod, range(1, nSlides), nSlides])
    params = {'allProds': allProds}
    return render(request,'shop/watches.html', params)

def households(request):
    allProds = []
    catprods = Product.objects.values('subcategory', 'id')
    cats = {item['subcategory'] for item in catprods}
    for cat in cats:
        prod = Product.objects.filter(subcategory=cat)
        if cat.__contains('household'):
            n = len(prod)
            nSlides = n // 4 + ceil((n / 4) - (n // 4))
            allProds.append([prod, range(1, nSlides), nSlides])
    params = {'allProds': allProds}
    return render(request,'shop/household.html', params)


def fashion(request):
    allProds = []
    catprods = Product.objects.values('category', 'id')
    cats = {item['category'] for item in catprods}
    for cat in cats:
        prod = Product.objects.filter(category=cat)
        if cat == 'Fashion Wears':
            n = len(prod)
            nSlides = n // 4 + ceil((n / 4) - (n // 4))
            allProds.append([prod, range(1, nSlides), nSlides])
    params = {'allProds': allProds}
    return render(request,'shop/fashion.html', params)

def footwears(request):
    allProds = []
    catprods = Product.objects.values('category', 'id')
    cats = {item['category'] for item in catprods}
    for cat in cats:
        prod = Product.objects.filter(category=cat)
        if cat == 'Footwears':
            n = len(prod)
            nSlides = n // 4 + ceil((n / 4) - (n // 4))
            allProds.append([prod, range(1, nSlides), nSlides])
    params = {'allProds': allProds}
    return render(request,'shop/footwears.html', params)

def electronics(request):
    allProds = []
    catprods = Product.objects.values('category', 'id')
    cats = {item['category'] for item in catprods}
    for cat in cats:
        prod = Product.objects.filter(category=cat)
        if cat == 'Electronics':
            n = len(prod)
            nSlides = n // 4 + ceil((n / 4) - (n // 4))
            allProds.append([prod, range(1, nSlides), nSlides])
    params = {'allProds': allProds}
    return render(request,'shop/electronics.html', params)

def households(request):
    allProds = []
    catprods = Product.objects.values('subcategory', 'id')
    cats = {item['subcategory'] for item in catprods}
    for cat in cats:
        prod = Product.objects.filter(subcategory=cat.lower())
        if cat.__contains__('household'):
            n = len(prod)
            nSlides = n // 4 + ceil((n / 4) - (n // 4))
            allProds.append([prod, range(1, nSlides), nSlides])
    params = {'allProds': allProds}
    return render(request,'shop/household.html', params)

def register_request(request):
	if request.method == "POST":
		form = NewUserForm2(request.POST)
		if form.is_valid():
			user = form.save()
			login(request, user)
			messages.success(request, "Registration successful." )
			return redirect("/shop/")
		messages.error(request, "Unsuccessful registration. Invalid information.")
	form = NewUserForm2
	return render (request=request, template_name="shop/register.html", context={"register_form":form})

def login_request(request):
	if request.method == "POST":
		form = AuthenticationForm(request, data=request.POST)
		if form.is_valid():
			username = form.cleaned_data.get('username')
			password = form.cleaned_data.get('password')
			user = authenticate(username=username, password=password)
			if user is not None:
				login(request, user)
				messages.info(request, f"You are now logged in as {username}.")
				return redirect("/shop/")
			else:
				messages.error(request,"Invalid username or password.")
		else:
			messages.error(request,"Invalid username or password.")
	form = AuthenticationForm()
	return render(request=request, template_name="shop/login.html", context={"login_form":form})

def logout_request(request):
	logout(request)
	messages.info(request, "You have successfully logged out.")
	return redirect("/shop/")