from django.db import models


class Item(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3, default='usd')


class Discount(models.Model):
    name = models.CharField(max_length=255)
    amount_off = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )
    percent_off = models.DecimalField(
        max_digits=5, decimal_places=2, null=True, blank=True
    )


class Tax(models.Model):
    name = models.CharField(max_length=255)
    percentage = models.DecimalField(max_digits=5, decimal_places=2)


class Order(models.Model):
    items = models.ManyToManyField(Item)
    discount = models.ForeignKey(
        Discount, null=True, blank=True, on_delete=models.SET_NULL
    )
    tax = models.ForeignKey(
        Tax, null=True, blank=True, on_delete=models.SET_NULL
    )

    def get_total_price(self):
        total = sum(item.price for item in self.items.all())
        if self.discount:
            if self.discount.amount_off:
                total -= self.discount.amount_off
            elif self.discount.percent_off:
                total -= total * (self.discount.percent_off / 100)
        if self.tax:
            total += total * (self.tax.percentage / 100)

        return round(total, 2)
