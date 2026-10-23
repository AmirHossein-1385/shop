def filter_by_price(products, request):
    min_price = request.GET.get('min-price', '').strip()
    max_price = request.GET.get('max-price', '').strip()

    if 'min-price' not in request.GET and 'max-price' not in request.GET:
        return products, None

    if not min_price or not max_price:
        return products, None

    try:
        min_price = int(min_price)
        max_price = int(max_price)
    except ValueError:
        return products, 'لطفاً قیمت معتبر وارد کنید'

    if min_price < 0 or max_price < 0:
        return products, 'قیمت منفی نامعتبر می‌باشد'

    if min_price > max_price:
        return products, 'حداقل قیمت نمی‌تواند از حداکثر بیشتر باشد'

    products = products.filter(
        new_price__range=(min_price, max_price)
    )

    return products, None

