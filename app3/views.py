from django.core.files.storage import FileSystemStorage
from requests import session
import datetime
import random
from .models import *
from django.contrib.auth import authenticate,login
from django.shortcuts import render, redirect
import razorpay
from django.contrib.auth.models import User
from django.contrib import messages


razorpay_client = razorpay.Client(auth=('rzp_test_9zruMnoLDlsCLG','oXUZ9Mf5zhjoZsTFLc7RpABO'))


def index(request):
    return render(request,'index.html')

# Create your views here.
def login1(reguest):
    return render(reguest,'login1.html')


def contact(request):
    return render(request,'contact.html')


def checklogin(request):
    username=request.POST.get("username")
    password=request.POST.get("password")
    user=authenticate(request,username=username,password=password)
    if user is not None:
        login(request,user)
        if username == 'admin':
            return redirect("/dashboard/")
        elif username == 'delivery':
            return redirect("/search/")
        else:
            return redirect("/login1/")
    else:
        return redirect("/login1/")



def update_password(request):
    if request.method == "POST":
        username = request.POST.get("username")
        new_password = request.POST.get("new_password")
        confirm_password = request.POST.get("confirm_password")

        if new_password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect("update_password")

        try:
            user = User.objects.get(username=username)
            user.set_password(new_password)
            user.save()
            messages.success(request, "Password updated successfully.")
            return redirect("/login1/")  # Or wherever you want
        except User.DoesNotExist:
            messages.error(request, "User does not exist.")
            return redirect("/updatepassword/")

    return render(request, 'updatepassword.html')






def dashboard(request):
    v=countrytable.objects.all()
    return render(request,'dashboard.html', {"v":v})

def brands(request):
    vb=brandtable.objects.all()
    return render(request,'brands.html', {"vb":vb})

def category(request):
    vc=categorytable.objects.all()
    return render(request,'category.html', {"vc":vc})

def products(request):
    vp=productstable.objects.all()
    return render(request,'products.html', {"vp":vp})

def addcountry(request):
    return render(request,'addcountry.html')

def savecountry(request):
    c=countrytable()
    c.country=request.POST.get("country")
    c.status=request.POST.get("status")
    c.save()
    return redirect("/addcountry/")

def addbrands(request):
    return render(request,'addbrands.html')

def savebrands(request):
    b=brandtable()
    b.brand=request.POST.get("brand")
    b.status=request.POST.get("status")
    image = request.FILES['image']
    fs = FileSystemStorage()
    file = fs.save(image.name, image)
    url = fs.url(file)
    b.image = url
    b.save()
    return redirect("/addbrands/")

def addcategory(request):
    return render(request,'addcategory.html')

def savecategory(request):
    ca=categorytable()
    ca.category=request.POST.get("category")
    ca.status=request.POST.get("status")
    image = request.FILES['image']
    fs = FileSystemStorage()
    file = fs.save(image.name, image)
    url = fs.url(file)
    ca.image = url
    ca.save()
    return redirect("/addcategory/")

def addproducts(request):
    return render(request, 'addproducts.html')

def saveproducts(request):
    p=productstable()
    p.code=request.POST.get("code")
    p.name=request.POST.get("name")
    p.price=request.POST.get("price")
    p.total=request.POST.get("total")
    p.brand=request.POST.get("brand")
    p.category=request.POST.get("category")
    p.created=request.POST.get("created")
    p.updated=request.POST.get("updated")
    p.opening_stock=request.POST.get("opening_stock")
    p.current_stock=request.POST.get("current_stock")
    p.status=request.POST.get("status")
    image = request.FILES['image']
    fs = FileSystemStorage()
    file = fs.save(image.name, image)
    url = fs.url(file)
    p.image = url
    p.save()
    return redirect("/addproducts/")

def deleteproducts(request,id):
    dp=productstable.objects.get(id=id)
    dp.delete()
    return redirect("/products/")

def editproducts(request,id):
    ep=productstable.objects.get(id=id)
    return render(request, 'editproducts.html', {"ep": ep})

def updateproducts(request,id):
    up=productstable.objects.get(id=id)
    try:
        up.code=request.POST.get("ep_code")
        up.name=request.POST.get("ep_name")
        up.price=request.POST.get("ep_price")
        up.total=request.POST.get("ep_total")
        up.brand=request.POST.get("ep_brand")
        up.category=request.POST.get("ep_category")
        up.created=request.POST.get("ep_created")
        up.updated=request.POST.get("ep_updated")
        up.opening_stock=request.POST.get("ep_openind_stock")
        up.current_stock=request.POST.get("ep_current_stock")
        up.status=request.POST.get("ep_status")
        image = request.FILES['ep_image']
        fs = FileSystemStorage()
        file = fs.save(image.name, image)
        url = fs.url(file)
        up.image = url
        up.save()
        return redirect("/products/")
    except:
        up.code=request.POST.get("ep_code")
        up.name=request.POST.get("ep_name")
        up.price=request.POST.get("ep_price")
        up.total=request.POST.get("ep_total")
        up.brand=request.POST.get("ep_brand")
        up.category=request.POST.get("ep_category")
        up.created=request.POST.get("ep_created")
        up.updated=request.POST.get("ep_updated")
        up.opening_stock=request.POST.get("ep_openind_stock")
        up.current_stock=request.POST.get("ep_current_stock")
        up.status=request.POST.get("ep_status")
        up.save()
        return redirect("/products/")

def deletecategory(request,id):
    dc=categorytable.objects.get(id=id)
    dc.delete()
    return redirect("/category/")

def editcategory(request,id):
    ec=categorytable.objects.get(id=id)
    return render(request,'editcategory.html',{"ec":ec})

def updatecategory(request,id):
    uc=categorytable.objects.get(id=id)
    try:
        uc.category=request.POST.get("ec_category")
        uc.status=request.POST.get("ec_status")
        image = request.FILES['ec_image']
        fs = FileSystemStorage()
        file = fs.save(image.name, image)
        url = fs.url(file)
        uc.image=url
        uc.save()
        return redirect("/category/")
    except:
        uc.category = request.POST.get("ec_category")
        uc.status = request.POST.get("ec_status")
        uc.save()
        return redirect("/category/")

def deletebrands(request,id):
    db=brandtable.objects.get(id=id)
    db.delete()
    return redirect("/brands/")

def editbrands(request,id):
    eb=brandtable.objects.get(id=id)
    return render(request,'editbrands.html',{"eb":eb})

def updatebrands(request,id):
    ub=brandtable.objects.get(id=id)
    try:
        ub.brand=request.POST.get("eb_brand")
        ub.status=request.POST.get("eb_status")
        image = request.FILES['eb_image']
        fs = FileSystemStorage()
        file = fs.save(image.name, image)
        url = fs.url(file)
        ub.image = url
        ub.save()
        return redirect("/brands/")
    except:
        ub.brand = request.POST.get("eb_brand")
        ub.status = request.POST.get("eb_status")
        ub.save()
        return redirect("/brands/")

def deletecountry(request,id):
    d=countrytable.objects.get(id=id)
    d.delete()
    return redirect("/dashboard/")

def editcountry(request,id):
    e=countrytable.objects.get(id=id)
    return render(request,'editcountry.html',{"e":e})

def updatecountry(request,id):
    u=countrytable.objects.get(id=id)
    u.country=request.POST.get("e_country")
    u.status=request.POST.get("e_status")
    u.save()
    return redirect("/dashboard/")

def productsview(request):
    pv=productstable.objects.all()
    return render(request,'productsview.html',{"pv":pv})


def productcart(request):
    cart = carttable.objects.filter(session_key=request.session.session_key)
    cart_total = sum(i.totalprice() for i in cart)

    if not cart.exists():
        messages.info(request, "Your shopping cart is empty!")

    return render(request, 'productcart.html', {
        "cart": cart,
        "cart_total": cart_total
    })

def addtocart(request, id):
    if not request.session.session_key:
        request.session.create()
    session_key = request.session.session_key
    pc = productstable.objects.get(id=id)
    c, created = carttable.objects.get_or_create(product_id=pc.id, session_key=session_key)
    if not created:
        c.quantity += 1
        c.save()
    else:
        c.quantity = 1
        c.save()
    return redirect("/productcart/")


def remove(request,id):
    r=carttable.objects.get(id=id)
    r.delete()
    return redirect("/productcart/")

def checkout(request):
    checkout1=carttable.objects.filter(session_key=request.session.session_key)
    checkout_total=sum(i.totalprice() for i in checkout1)
    currency = 'INR'
    amount = int(checkout_total) * 100
    checkout_total1=checkout_total+6

    # Create a Razorpay Order
    razorpay_order = razorpay_client.order.create(dict(amount=amount, currency=currency,payment_capture='0'))
    # order id of newly created order.
    razorpay_order_id = razorpay_order['id']
    callback_url = 'paymenthandler'
    now = datetime.datetime.now()
    generated_order_id = f"ORD{now.strftime('%Y%m%d')}{random.randint(1000, 9999)}"

    # we need to pass these details to frontend.
    context = {}
    context['razorpay_order_id'] = razorpay_order_id
    context['razorpay_merchant_key'] = 'rzp_test_9zruMnoLDlsCLG'
    context['razorpay_amount'] = amount
    context['currency'] = currency
    context['callback_url'] = callback_url
    context['checkout1']=checkout1
    context['checkout_total1']=checkout_total1
    context['order_id'] = generated_order_id

    return render(request,'checkout.html',context)




def save(request):
    payment_method=request.POST.get("payment-method")
    checkout1 = carttable.objects.filter(session_key=request.session.session_key)
    total_price=sum(i.totalprice() for i in checkout1)
    if payment_method == "cod":
        s = checkouttable()
        s.session_key = request.session.session_key
        s.firstname = request.POST.get("firstname")
        s.lastname = request.POST.get("lastname")
        s.address = request.POST.get("address")
        s.place = request.POST.get("place")
        s.landmark = request.POST.get("landmark")
        s.shippingcharge = request.POST.get("shippingcharge")
        s.order_id = request.POST.get("order_id")
        s.phone = request.POST.get("phone")
        s.payment_method = payment_method
        s.status = "pending"
        s.total_price=total_price
        s.save()
        for i in checkout1:
            ob=checkoutitems()
            ob.checkout_id=s.id
            ob.product_id=i.product.id
            ob.quantity=i.quantity
            ob.session_key=i.session_key
            ob.save()
        checkout1.delete()
        return redirect("/")
    else:
        checkout1 = carttable.objects.filter(session_key=request.session.session_key)
        checkout_total = sum(i.totalprice() for i in checkout1)
        s = checkouttable()
        s.session_key = request.session.session_key
        s.firstname = request.POST.get("firstname")
        s.lastname = request.POST.get("lastname")
        s.address = request.POST.get("address")
        s.place = request.POST.get("place")
        s.landmark = request.POST.get("landmark")
        s.shippingcharge = request.POST.get("shippingcharge")
        s.order_id = request.POST.get("order_id")
        s.phone = request.POST.get("phone")
        s.payment_method = payment_method
        s.status = "pending"
        s.total_price=checkout_total
        payment_id = request.POST.get('payment_id', '')
        signature = request.POST.get('razorpay_signature', '')
        params_dict = {
            'razorpay_payment_id': payment_id,
            'razorpay_signature': signature
        }
        # verify the payment signature.
        amount = int(checkout_total) *100  # Rs. 200
        razorpay_client.payment.capture(payment_id, amount)
        s.save()
        for i in checkout1:
            ob=checkoutitems()
            ob.checkout_id=s.id
            ob.product_id=i.product.id
            ob.quantity=i.quantity
            ob.session_key=i.session_key
            ob.save()
        checkout1.delete()
        return redirect("/")




def vieworders(request):
    vo = checkouttable.objects.filter(status='pending')
    return render(request, 'vieworders.html', {'vo': vo})


def delivery(request):
    d=deliverytable.objects.all()
    return render(request,'delivery.html',{"d":d})

def adddelivery(request):
    return render(request, 'adddelivery.html')


def savedelivery(request):
    sd = deliverytable()
    sd.name = request.POST.get("name")
    sd.mobile = request.POST.get("mobile")
    sd.vehicle = request.POST.get("vehicle")
    sd.vehicle_number = request.POST.get("vehicle_number")
    sd.save()
    return redirect("/adddelivery/")


def deletedelivery(request,id):
    dd=deliverytable.objects.get(id=id)
    dd.delete()
    return redirect("/delivery/")

def editdelivery(request,id):
    ed=deliverytable.objects.get(id=id)
    return render(request,'editdelivery.html',{"ed":ed})

def updatedelivery(request,id):
    ud=deliverytable.objects.get(id=id)
    ud.name=request.POST.get("ed_name")
    ud.mobile=request.POST.get("ed_mobile")
    ud.vehicle=request.POST.get("ed_vehicle")
    ud.vehicle_number=request.POST.get("ed_vehicle_number")
    ud.save()
    return redirect("/delivery/")




def outfordelivery(request):
    delivery_list = deliverytable.objects.all()
    return render(request, 'outfordelivery.html', {"delivery_list": delivery_list})


def save_assigned_delivery(request):
    selected_delivery_id = request.POST.get("delivery_id")
    delivery_obj = deliverytable.objects.get(id=selected_delivery_id)

    session_key = request.session.session_key

    try:
        checkout = checkouttable.objects.filter(session_key=session_key).latest("id")
        order_id = checkout.order_id
    except checkouttable.DoesNotExist:
        order_id = None

    ofd = outfordeliverytable()
    ofd.delivery = delivery_obj
    ofd.session_key = session_key
    ofd.order_id = order_id
    ofd.save()

    return redirect("/outfordelivery/")


def deliverylogin(request):
    dl=outfordeliverytable.objects.all()
    return render(request,'deliverylogin.html',{"dl":dl})

def search_delivery(request):
    if request.method == "POST":
        search_name = request.POST.get("search_name")
        deliveries = deliverytable.objects.filter(name__icontains=search_name)
        order_ids = outfordeliverytable.objects.filter(delivery__in=deliveries).values('order_id')
        return render(request, 'search_results.html', {"order_ids": order_ids, "search_name": search_name})
    return render(request, 'search.html')



def update_status(request):
    if request.method == "POST":
        order_id = request.POST.get('order_id')
        new_status = request.POST.get('status')

        try:
            order = checkouttable.objects.get(order_id=order_id)
            order.status = new_status
            order.save()
        except checkouttable.DoesNotExist:
            pass

        return redirect("/search/")


def savecontact(request):
    sc=contacttable()
    sc.name=request.POST.get("name")
    sc.email=request.POST.get("email")
    sc.subject=request.POST.get("subject")
    sc.message=request.POST.get("message")
    sc.save()
    return render(request,'index.html')


def viewcontact(request):
    vc=contacttable.objects.all()
    return render(request,'viewcontact.html',{"vc":vc})

def cancelledproducts(request):
    cp = checkouttable.objects.filter(status='completed')
    return render(request, 'cancelledproducts.html', {'cp': cp})


def cancel_order(request,order_id):
    try:
        order = checkouttable.objects.get(order_id=order_id)
        order.status = 'completed'
        order.save()
    except checkouttable.DoesNotExist:
        pass
    return redirect("/vieworders/")


def myorders(request):
    # Make sure the session exists
    if not request.session.session_key:
        request.session.create()

    session_key = request.session.session_key

    # Filter orders only for this user's session
    mo = checkoutitems.objects.filter(session_key=session_key)

    return render(request, 'myorders.html', {'mo': mo})

from django.shortcuts import get_object_or_404

def cancelorder(request, order_id):
    # Make sure the user session exists
    if not request.session.session_key:
        request.session.create()
    session_key = request.session.session_key
    order = get_object_or_404(checkouttable, order_id=order_id, session_key=session_key)
    if order.status == "pending":
        order.status = "completed"
        order.save()
    checkoutitems.objects.filter(checkout=order).delete()
    return redirect("/myorders/")
