from django.shortcuts import redirect, render, get_object_or_404
from django.contrib import messages
from hmartApp.models import Banner_list, Brand, Category, Product,Contact, Advertisem, Filter, Informations, Cart_item, Cart, Widsh_List
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required

# Create your views here.

def home(request, pk=None):
    banner_list = Banner_list.objects.all()
    products_new = Product.objects.all().order_by('-create_date')[:8]
    products = Product.objects.all()
    contacts = Contact.objects.all()

    category = Category.objects.all()
    products = Product.objects.all()
    
    brand_list = Brand.objects.all()
    advertisem_list = Advertisem.objects.all()

    if request.user.is_authenticated:
        products_wishlist = Widsh_List.objects.filter(owner_id = request.user.id)
        products_cart = Cart_item.objects.filter(cart__owner = request.user)
    else:
        products_cart = {}
        products_wishlist = {}

    context = {'products':products, 'products_wishlist':products_wishlist, 'products_cart':products_cart, 'category':category, 'products':products, 'banner_list':banner_list, 'products_new':products_new, 'contacts':contacts, 'brand_list':brand_list, 'advertisem_list':advertisem_list}
    return render(request=request, template_name='hmart/index.html', context=context)

def add_cart(request, pk):
    product = get_object_or_404(Product, pk=pk) 
    count = request.POST['count']
    print(count)
    if request.method == 'POST' and count:
        if product.count > int(count):
            c = product.count - int(count) 
            try:
                cart_owner = Cart.objects.get(owner = request.user)
            except:
                cart_owner = Cart.objects.create(owner=request.user, order=True)
            try: 
                count_item = Cart_item.objects.get(product_id=pk)
                count = count_item.count + int(count)
                price = product.price * int(count)
                Cart_item.objects.filter(product_id=pk).update(count = count, total = price)
                print('count if 3')
            except:
                price = product.price * int(count)
                Cart_item.objects.create(product_id=pk, count = count, cart = cart_owner, total = price)
                print('count if 4')
            
            prod = Product.objects.get(id = pk)
            prod.count = c
            prod.save()

            return redirect('cart')

        else:
            print(request)
            messages.success(request, '   Sklatda maxsulot soni kam!!!   ')


    return redirect('single_product', pk)    

def update_cart(request, pk):
    product = get_object_or_404(Product, pk=pk)
    product_count = product.count
    count = request.POST.get('count')
    cart_item = Cart_item.objects.get(product_id = pk)
    if request.method == 'POST':
        if cart_item.count > int(count):
            product.count = product_count + (cart_item.count - int(count))
            product.save()
            total = product.price * int(count)
            cart_item.count = count
            cart_item.total = total
            cart_item.save()
            return redirect('cart')
        else:
            if product.count > product_count + (cart_item.count - int(count)):
                product.count = product_count - (int(count) - cart_item.count)
                product.save()
                total = product.price * int(count)
                cart_item.count = count
                cart_item.total = total
                cart_item.save()
                return redirect('cart')
            elif product.count == product_count + (cart_item.count - int(count)):
                return redirect ('cart')
            else:
                messages.success(request, '   Sklatda maxsulot soni kam!!!   ')
    return redirect('cart')

def delete_cart(request, pk):
    product = Product.objects.get(pk = pk)
    Cart_item.objects.filter(product = product).delete()
    return redirect('cart')

def delete_wishlist(requst, pk):
    product = Product.objects.get(pk = pk)
    Widsh_List.objects.filter(product = product).delete()
    return redirect('wishlist')

def add_wishlist(request, pk):
    product = Product.objects.get(id=pk)
    widsh_Lists = Widsh_List.objects.filter(owner=request.user).values('product')
    
    if not product.id in list(map(lambda elem: elem['product'], list(widsh_Lists))):
        Widsh_List.objects.create(owner = request.user, product_id = pk)
    return redirect('single_product', pk)

def detail_product(request, pk):
    banner_list = Banner_list.objects.all()
    product = get_object_or_404(Product, pk = pk)
    informations = get_object_or_404(Informations, product_id = pk)

    products = Product.objects.filter(category = product.category)

    if request.user.is_authenticated:
        products_wishlist = Widsh_List.objects.filter(owner_id = request.user.id)
        products_cart = Cart_item.objects.filter(cart__owner = request.user)
    else:
        products_cart = {}
        products_wishlist = {}
    
    context = {'products_wishlist':products_wishlist,'products_cart':products_cart,'product':product, 'products':products, 'informations':informations, 'banner_list':banner_list}
    return render(request=request, template_name='hmart/single-product.html', context=context)


def about(request):
    if request.user.is_authenticated:
        products_wishlist = Widsh_List.objects.filter(owner_id = request.user.id)
        products_cart = Cart_item.objects.filter(cart__owner = request.user)
    else:
        products_cart = {}
        products_wishlist = {}
    context = {'products_wishlist':products_wishlist, 'products_cart':products_cart}

    return render(request=request, template_name='hmart/about.html', context = context)

def detail_brand(request, pk):
    categories = Category.objects.all()
    brands = Brand.objects.all()    
    brand = Brand.objects.get(pk = pk)
    products = Product.objects.filter(brand = brand)
    product = Product.objects.all()
    all = product.count()
    if request.user.is_authenticated:
        products_wishlist = Widsh_List.objects.filter(owner_id = request.user.id)
        products_cart = Cart_item.objects.filter(cart__owner = request.user)
    else:
        products_cart = {}
        products_wishlist = {}

    if request.method == 'POST':
        if request.POST.get('start_price') and request.POST.get('end_price'):
            start_price=request.POST.get('start_price')
            end_price = request.POST.get('end_price')
            products = Product.objects.filter(price__gte = start_price , price__lte = end_price)
        elif request.POST.get('start_price'):
            start_price=request.POST.get('start_price')
            products = Product.objects.filter(price__gte = start_price)
        else:
            end_price = request.POST.get('end_price')
            products = Product.objects.filter(price__lte = end_price)

        paginator = Paginator(object_list=products, per_page=1)
        page_number = request.GET.get('page')
        page_objects = paginator.get_page(page_number)
    else:
        paginator = Paginator(object_list=products, per_page=1)
        page_number = request.GET.get('page')
        page_objects = paginator.get_page(page_number)

    context = {'products_wishlist':products_wishlist, 'products_cart':products_cart, 'brands':brands, 'categories':categories, 'page_objects':page_objects, 'products':products, 'all':all}
    return render(request=request, template_name='hmart/brand-detail.html', context = context)

def detail_category(request, pk):
    categories = Category.objects.all()
    brands = Brand.objects.all()    
    category = Category.objects.get(pk=pk)
    product = Product.objects.all()
    all = product.count()
    products = Product.objects.filter(category = category)

    if request.user.is_authenticated:
        products_wishlist = Widsh_List.objects.filter(owner_id = request.user.id)
        products_cart = Cart_item.objects.filter(cart__owner = request.user)
    else:
        products_cart = {}
        products_wishlist = {}

    if request.method == 'POST':
        if request.POST.get('start_price') and request.POST.get('end_price'):
            start_price=request.POST.get('start_price')
            end_price = request.POST.get('end_price')
            products = Product.objects.filter(price__gte = start_price , price__lte = end_price)
            
        elif request.POST.get('start_price'):
            start_price=request.POST.get('start_price')
            products = Product.objects.filter(price__gte = start_price)
        else:
            end_price = request.POST.get('end_price')
            products = Product.objects.filter(price__lte = end_price)
            

        paginator = Paginator(object_list=products, per_page=1)
        page_number = request.GET.get('page')
        page_objects = paginator.get_page(page_number)
    else:
        paginator = Paginator(object_list=products, per_page=1)
        page_number = request.GET.get('page')
        page_objects = paginator.get_page(page_number)

    context = {'products_wishlist':products_wishlist, 'products_cart':products_cart, 'brands':brands, 'categories':categories, 'page_objects':page_objects, 'products':products, 'all':all}
    return render(request=request, template_name='hmart/category-detail.html', context=context)

def shop(request):
    categories = Category.objects.all()
    brands = Brand.objects.all()
    products = Product.objects.all()
    all = products.count()
    if request.method == 'POST':
        if request.POST.get('start_price') and request.POST.get('end_price'):
            start_price=request.POST.get('start_price')
            end_price = request.POST.get('end_price')
            products = Product.objects.filter(price__gte = start_price , price__lte = end_price)
        elif request.POST.get('start_price'):
            start_price=request.POST.get('start_price')
            products = Product.objects.filter(price__gte = start_price)
        else:
            end_price = request.POST.get('end_price')
            products = Product.objects.filter(price__lte = end_price)

        paginator = Paginator(object_list=products, per_page=3)
        page_number = request.GET.get('page')
        page_objects = paginator.get_page(page_number)
    else:
        paginator = Paginator(object_list=products, per_page=3)
        page_number = request.GET.get('page')
        page_objects = paginator.get_page(page_number)       

    if request.user.is_authenticated:
        products_wishlist = Widsh_List.objects.filter(owner_id = request.user.id)
        products_cart = Cart_item.objects.filter(cart__owner = request.user)
    else:
        products_cart = {}
        products_wishlist = {}

    context = {'products_wishlist':products_wishlist, 'products_cart':products_cart, 'brands':brands, 'page_objects':page_objects, 'categories':categories, 'all':all}
    return render(request=request, template_name='hmart/shop-left-sidebar.html', context=context)

@login_required(login_url='login')
def cart(request):   
    products = Cart_item.objects.filter(cart__owner = request.user)
    if request.user.is_authenticated:
        products_wishlist = Widsh_List.objects.filter(owner_id = request.user.id)
        products_cart = Cart_item.objects.filter(cart__owner = request.user)
    else:
        products_cart = {}
        products_wishlist = {}

    context = {'products_wishlist':products_wishlist, 'products_cart':products_cart, 'products':products}
    return render(request=request, template_name='hmart/cart.html', context=context)

@login_required(login_url='login')
def checkout(request):
    if request.user.is_authenticated:
        products_wishlist = Widsh_List.objects.filter(owner_id = request.user.id)
        products_cart = Cart_item.objects.filter(cart__owner = request.user)
    else:
        products_cart = {}
        products_wishlist = {}
    context = {'products_wishlist':products_wishlist, 'products_cart':products_cart}
    return render(request=request, template_name='hmart/checkout.html', context=context)


def contact(request):
    if request.method == 'POST' and request.user.is_authenticated:
        owner = request.user
        subject = request.POST.get('subject')
        body = request.POST.get('body')
      
        Contact.objects.create(owner=owner, subject=subject, body=body)
        return redirect('contact')

    if request.user.is_authenticated:
        products_wishlist = Widsh_List.objects.filter(owner_id = request.user.id)
        products_cart = Cart_item.objects.filter(cart__owner = request.user)
    else:
        products_cart = {}
        products_wishlist = {}

    context = {'products_wishlist':products_wishlist, 'products_cart':products_cart}
    return render(request=request, template_name='hmart/contact.html', context=context)

@login_required(login_url='login')
def wishlist(request):
    if request.user.is_authenticated:
        products_wishlist = Widsh_List.objects.filter(owner_id = request.user.id)
        products_cart = Cart_item.objects.filter(cart__owner = request.user)
    else:
        products_cart = {}
        products_wishlist = {}
    context = {'products_wishlist':products_wishlist, 'products_cart':products_cart}
    return render(request=request, template_name='hmart/wishlist.html', context=context)
