from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.db.models import Sum
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib import messages
from .forms import *
from .filters import filter_by_price
# Create your views here.

def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.all()

    if category_slug:
        category = Category.objects.get(slug=category_slug)
        products = products.filter(category=category)

    products, error = filter_by_price(products, request)

    if error:
        messages.error(request, error)

    paginator = Paginator(products, 6)
    page_number = request.GET.get('page')
    products = paginator.get_page(page_number)

    context = {
        'categories': categories,
        'category': category,
        'products': products,
    }

    return render(request, 'shop/product_list.html', context)


# def product_list(request,category_slug=None):
#     category = None
#     categories = Category.objects.all()
#     products = Product.objects.all()
#     if category_slug:
#         category = Category.objects.get(slug=category_slug)
#         products = products.filter(category=category)
#
#     paginator = Paginator(products,6)
#     page_number = request.GET.get('page')
#     products = paginator.get_page(page_number)
#
#     context = {
#         'categories':categories,
#         'category':category,
#         'products':products,
#     }
#     return render(request, 'shop/product_list.html',context)


def product_detail(request,id ,slug):
    product = get_object_or_404(Product,id=id,slug=slug)
    similar_products = Product.objects.exclude(id=id).filter(Q(category=product.category) | Q(description=product.description))
    form = CommentForm()
    if request.user.is_authenticated:
        is_save = product in request.user.saved_products.all()
    else:
        is_save = False
    context = {
        'product':product,
        'similar_products':similar_products,
        'is_save':is_save,
        'form':form,
    }
    return render(request, 'shop/detail.html',context)

def cheapest_product(request):
    return render(request,'shop/cheapest_products.html')

def expensive_products(request):
    return render(request,'shop/most_expensive_products.html')

def latest_products(request):
    return render(request,'shop/latest_products.html')

def filter_products(request):
    min_price = request.GET.get('min-price','').strip()
    max_price = request.GET.get('max-price','').strip()
    products = Product.objects.none()

    if not min_price or not max_price:
        messages.error(request,'لطفاً حداقل و حداکثر قیمت را وارد کنید')

    else:
        try:
            min_price = int(min_price)
            max_price = int(max_price)
            if min_price < 0 or max_price < 0:
                messages.error(request,'قیمت منفی نامعتبر می باشد')

            elif min_price > max_price:
                messages.error(request,'قیمت حداقل نمی تواند از حداکثر بیشتر باشد')
            else:
                products = Product.objects.filter(new_price__range=(min_price,max_price))

        except ValueError:
            messages.error(request, 'لطفاً قیمت معتبر وارد کنید')


    context = {
          'products':products,
    }
    return render(request,'shop/price_filter.html',context)


@login_required
def save_product(request,product_id):
    user = request.user
    product = get_object_or_404(Product,id=product_id)
    if product in user.saved_products.all():
        user.saved_products.remove(product)
        save = False
    else:
        user.saved_products.add(product)
        save = True

    return JsonResponse({'save':save})


def list_saved_products(request):
    user = request.user
    products = user.saved_products.all()
    context = {
        'products':products,
        'user':user,
    }
    return render(request,'shop/saved_products.html',context)


def apply_code(request):
    if request.method == 'POST':
        code = request.POST.get('code')
        discount_code = DiscountCode.objects.filter(code=code).first()
        if not discount_code:
            messages.error(request, 'Discount code not found')
            return redirect('cart:card_detail')

        today = timezone.localdate()
        if discount_code.end_date < today:
            messages.error(request, 'Discount code expired')
            return redirect('cart:card_detail')

        current_code = request.session.get('discount_code')

        if current_code == discount_code.code:
            messages.error(request, 'This code has already been applied.')
        else:
            if DiscountUsage.objects.filter(discount=discount_code, user=request.user).exists():
                messages.error(request, 'You have already used the discount code.')
                return redirect('cart:card_detail')
            request.session['discount_code'] = discount_code.code
            messages.success(request, 'Discount code applied successfully')

    return redirect('cart:card_detail')


def search(request):
    query = request.GET.get('query')
    products = None
    if query:
        products = Product.objects.filter(Q(name__icontains=query) | Q(description__icontains=query))

    context = {
        'products':products,
    }
    return render(request, 'shop/search.html',context)


@login_required
def comment(request,product_id):
    product = get_object_or_404(Product,id=product_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.product = product
            comment.save()
            return redirect('shop:product_detail',product.id,product.slug)

    else:
        form = CommentForm()
    context = {
        'form':form,
        'product':product,
    }
    return render(request, 'shop/detail.html',context)


def best_selling_products(request):
    products = Product.objects.annotate(total_sold=Sum('order_items__quantity',filter=Q(order_items__order__paid=True))).order_by('-total_sold')[:5]
    return render(request,'shop/best_selling_products.html',{'products':products})


def discounted_products(request,category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(off__gt=0)
    if category_slug:
        category = Category.objects.get(slug=category_slug)
        products = products.filter(category=category)

    products,error = filter_by_price(products,request)

    if error:
        messages.error(request, error)

    context = {
        'products':products,
        'categories':categories,
        'category':category,
        'error':error,
    }
    return render(request, 'shop/discounted products.html', context)


def about(request):
    return render(request,'shop/about.html')

def contact(request):
    return render(request,'shop/contact.html')