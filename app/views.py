from django.shortcuts import render,redirect, HttpResponseRedirect,get_object_or_404
from django.http import HttpResponse
from .models import Category,SubCategory,Product,ProductImage,Profile,AddToCart,Order,Review
from django.db.models import Q
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.models import User
# Create your views here.

def homepage(request):
    categories = Category.objects.all()
    return render(request,"index.html",{"categories":categories})

def Create_category(request):
    if request.method == "POST":
        cat_name=request.POST.get("cat_name")
        # print(dir(request))
        cat_image=request.FILES.get('Cat_image')
        category_instance = Category.objects.create(
            name = cat_name,
            image = cat_image
            )
        category_instance.save()
        return HttpResponseRedirect("/")
    return render(request,"create_category.html")

def edit_category(request,id):
    category_instance =Category.objects.get(id=id)
    if request.method == 'POST':
        category_instance.name=request.POST['cat_name']
        if "category_image" in request.FILES:
            category_instance.image = request.POST['cat_image']
        category_instance.save()
        return redirect("/")
    return render(request,"edit_cat.html",{'category':category_instance})

def delete_cat(request,id):
    category_instance=Category.objects.get(id=id)

    if request.method =='POST':
        category_instance.delete()
        return redirect("/")
    return render(request,"delete_category.html",{"category":category_instance})

def sub_category(request,id):
    
    category_instance = get_object_or_404(Category,id=id)
    subcategories = SubCategory.objects.filter(category=category_instance)
    print(subcategories)
    return render(request,"subcategory.html",{"category":category_instance,"subcategories":subcategories})

def create_subcategory(request,id):
    Category_instance= Category.objects.get(id=id)
    if request.method=='POST':
        category_name=request.POST.get('category_name')
        category_image = request.FILES.get("subcategory_image")  
        # category_image=request.FILES.get("subcategory_images")

        sub_category_instance = SubCategory.objects.create(
            category=Category_instance,
            name = category_name,
            image = category_image)
        sub_category_instance.save()
        return HttpResponseRedirect('/')
    return render(request,"create_sub_category.html",{"category":Category_instance})

def edit_sub_cat(request,subcategory_id):
    subcategory=get_object_or_404(SubCategory,id=subcategory_id)
    if request.method=='POST':
        subcategory.name=request.POST.get("name")
        category_id=request.POST.get('category')
        if category_id:
            category=get_object_or_404(Category,id=category_id)
            subcategory.category=category
        if 'image ' in request.FILES:
            subcategory.image=request.FILES['image'] 
        if 'delete_image' in request.POST and subcategory.image:
            subcategory.image.delete()
        subcategory.save()
        return redirect("/")
    categories=Category.objects.all()
    return render(request,"edit_Sub_category.html",{"subcategory":subcategory,"categories":categories})           

def product_list_page(request,subcategory_id):
    subcategory=get_object_or_404(SubCategory,id=subcategory_id)
    products=Product.objects.filter(subcategory=subcategory)
    return render(request,'product_list.html',{'subcategory':subcategory,'products':products,})

def product_detail(request,product_id):
    product= get_object_or_404(Product,id=product_id)
    images=product.images.first()
    return render(request,"product_detail.html",{"product":product,"images":images})

def create_product(request, subcategory_id):
    subcategory = get_object_or_404(SubCategory, id=subcategory_id) 
    category = subcategory.category  
    
    if request.method == 'POST':
       
        product_name = request.POST.get('product_name')
        product_price = request.POST.get('product_price')
        product_description = request.POST.get('product_description')
        color = request.POST.get('color')
        material = request.POST.get('material')
        stock = request.POST.get('stock')

        product = Product(
            product_name=product_name,
            product_price=product_price,
            product_description=product_description,
            color=color,
            material=material,
            stock=stock,
            subcategory=subcategory,  
            category=category, 
        )
        product.save()
       
        images = request.FILES.getlist('images')  
        for image in images:
            ProductImage.objects.create(product=product, image=image)

        return HttpResponseRedirect(f'/products_list_page/{subcategory_id}')
        # return redirect('product_list_page', subcategory_id=subcategory_id)

    return render(request, 'create_product.html', {'subcategory_id': subcategory_id, 'subcategory': subcategory}) 

def view_cart(request):
    if request.user.is_authenticated:
        cart_items=AddToCart.objects.filter(user=request.user) 

        for item in cart_items:
            item.product_images=item.product.images.first()
            item.total_price=item.product.product_price*item.quantity
        total_amount=sum(item.total_price for item in cart_items)
        return render(request,"cart.html",{"cart_items":cart_items,"total_amount":total_amount})
    else:
        return redirect("userlogin")    



def search_bar(request):
    query=request.GET.get('q','')
    data=Product.objects.none()
    if query:
        data=Product.objects.filter(Q(product_name_icontains=query))
    return render(request,"search.html",{'products':data,'query':query})    

def createuser(request):
    if request.method=='POST':
        username = request.POST['username']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        password = request.POST['password']
        email = request.POST['email']
        phone_number = request.POST['phone_number']
        is_vendor = request.POST['is_vendor'] 
        if User.objects.filter(username=username).exists():
            return HttpResponse("Error: Username already exists. Please enter another username.")
      
        user = User.objects.create(username=username,
                                   first_name=first_name,
                                   last_name=last_name,
                                   email=email,)
        user.set_password( password)
        user.save()
        profile_instance=Profile.objects.create(phone_no=phone_number,is_vendor=is_vendor,user=user)
        profile_instance.save()
        return redirect("/")
    return render(request,"createuser.html")

def userlogin(request):
    if request.method =='POST':
        username=request.POST['username']
        password=request.POST['password']
        user = authenticate(username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect("/")
        else:
            return render(request,'userlogin.html')
    return render(request,"userlogin.html")

def userlogout(request):
    logout(request)
    return redirect('/')

def get_pro(request):
    if request.user.is_authenticated:
        try:
            profile_instance=request.user.profile
            is_vendor=profile_instance.is_vendor
        except Profile.DoesNotExist:
            is_vendor=False
        return render(request,"profile.html",{"user":request.user,"is_vendor":is_vendor})
    else:
        return redirect("userlogin")   
         
def add_to_cart(request, product_id):
    product = Product.objects.get(id=product_id)
    quantity = int(request.POST.get('quantity', 1)) 

    if product.stock == 0:
        return HttpResponse("this product is out of stock")

    if quantity > product.stock:
        
        return HttpResponse(f"Only {product.stock} items are available.")

   
    cart_item, created = AddToCart.objects.get_or_create(user=request.user, product=product)

    if not created:
        
        cart_item.quantity += quantity
    else:
      
        cart_item.quantity = quantity
    
   
    cart_item.save()
    return redirect("cart") 

def proceed_order(request):
    cart_items=AddToCart.objects.filter(user=request.user)
    if not cart_items:
        return HttpResponse("your cart is empty")
    total_amount=0
    for item in cart_items:
        product=item.product
        quantity=item.quantity
        total_amount+=product.product_price*quantity
        item.total_price=product.product_price*quantity

    if request.method=='POST':
        for item in cart_items:
            product=item.product
            quantity=item.quantity
            if product.stock>=quantity:
                product.stock-=quantity
                product.save()

                delivery_date=request.POST.get('delivery_date')
                order=Order.objects.create(
                    user=request.user,
                    product=product,
                    price=product.product_price,
                    quantity=quantity,
                    shipping_address=request.POST.get('shipping_address'),
                    payment_method=request.POST.get('payment_method'),
                    delivery_date=delivery_date,
                    status='confirmed'
                )    
                order.save()
        cart_items.delete()
        return redirect("order_confirmation",order_id=order.id)
    return render(request,"proceed_order.html",{"cart_items":cart_items,"total_amount":total_amount})

def order_confirmation(request,order_id):
    order=get_object_or_404(Order,id=order_id)
    total_price=order.quantity*order.price
    return render(request,"order_Confirmation.html",{'order':order,'total_price':total_price,'delivery_date':order.delivery_date})
   

def Buy_Now(request, product_id):
    if not request.user.is_authenticated:
        return redirect('userlogin')

    product = get_object_or_404(Product, id=product_id)

    if product.stock <= 0:
        return HttpResponse("This product is out of stock.")

    if request.method == "POST":
        quantity = int(request.POST.get('quantity', 1)) 
        if quantity > product.stock:
            return HttpResponse("Not enough stock available.")

        shipping_address = request.POST.get('shipping_address')
        payment_method = request.POST.get('payment_method')
        delivery_date = request.POST.get('delivery_date')
        # delivery_date = request.POST.get('delivery_date', timezone.now() + timezone.timedelta(days=7))

        
        order = Order.objects.create(
            user=request.user,
            product=product,
            quantity=quantity,
            price=product.product_price,
            shipping_address=shipping_address,
            payment_method=payment_method,
            delivery_date=delivery_date,
            status='confirmed'
        )

       
        product.stock -= quantity
        product.save()

        return redirect('order_confirmation', order_id=order.id)

    return render(request, 'proceed_order.html', {
        'product': product,
        'is_buy_now': True  
    })

def add_review(request, product_id):
    if request.method == 'POST':
        
        product = get_object_or_404(Product, id=product_id)

        rating = request.POST.get('rating')
        review_text = request.POST.get("review_text")

       
        if rating is None or not rating.isdigit() or int(rating) not in range(1, 6):
            return HttpResponse("Invalid rating.")

       
        if not review_text or len(review_text.strip()) == 0:
            return HttpResponse("Review not availaible")

      
        review = Review(
            product=product,
            user=request.user,
            rating=int(rating),
            review_text=review_text )
        review.save()
        
        
        return redirect('product_detail', product_id=product.id)

   
    product = get_object_or_404(Product, id=product_id)
    return render(request, "add_review.html", {'product': product})






            









    






