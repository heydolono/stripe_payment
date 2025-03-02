import stripe
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from .models import Item, Order

stripe.api_key = settings.STRIPE_TEST_SECRET_KEY


def create_order_checkout_session(request, id):
    order = get_object_or_404(Order, pk=id)
    line_items = []
    for item in order.items.all():
        line_items.append({
            'price_data': {
                'currency': item.currency,
                'product_data': {
                    'name': item.name,
                },
                'unit_amount': int(item.price * 100),
            },
            'quantity': 1,
        })
    discounts = []
    if order.discount:
        if order.discount.amount_off:
            discount_obj = stripe.Coupon.create(
                amount_off=int(order.discount.amount_off * 100), currency="usd"
            )
        else:
            discount_obj = stripe.Coupon.create(
                percent_off=float(order.discount.percent_off)
            )
        discounts.append({'coupon': discount_obj.id})
    tax_rates = []
    if order.tax:
        tax_rate = stripe.TaxRate.create(
            display_name=order.tax.name,
            inclusive=False,
            percentage=float(order.tax.percentage),
        )
        tax_rates.append(tax_rate.id)
    checkout_session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=line_items,
        discounts=discounts,
        mode='payment',
        success_url='http://localhost:8000/success/',
        cancel_url='http://localhost:8000/cancel/',
    )
    return JsonResponse({'id': checkout_session.id})

def create_checkout_session(request, id):
    item = get_object_or_404(Item, pk=id)
    checkout_session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[
            {
                'price_data': {
                    'currency': item.currency,
                    'product_data': {
                        'name': item.name,
                    },
                    'unit_amount': int(item.price * 100),
                },
                'quantity': 1,
            },
        ],
        mode='payment',
        success_url='http://localhost:8000/success/',
        cancel_url='http://localhost:8000/cancel/',
    )
    return JsonResponse({
        'id': checkout_session.id
    })


def item_detail(request, id):
    item = get_object_or_404(Item, pk=id)
    context = {
        'item': item,
        'stripe_publishable_key': settings.STRIPE_TEST_PUBLISHABLE_KEY,
    }
    return render(request, 'store/item_detail.html', context)


def order_detail(request, order_id):
    order = get_object_or_404(Order, pk=order_id)
    total_price = sum(item.price for item in order.items.all())
    currency = order.items.first().currency if order.items.exists() else "USD"
    context = {
        'order': order,
        'total_price': total_price,
        'currency': currency,
        'stripe_publishable_key': settings.STRIPE_TEST_PUBLISHABLE_KEY,
    }
    return render(request, 'store/order_detail.html', context)
