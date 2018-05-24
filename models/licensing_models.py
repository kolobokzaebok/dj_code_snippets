from django.db import models
from django.urls import reverse
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError
import random, string


class Company(models.Model):
    name = models.CharField(max_length=250)
    logo = models.FileField()
    class Meta:
        db_table = "Company"

    def get_absolute_url(self):
        return reverse('sales:company_detail', kwargs={'pk': self.pk})

    def __str__(self):
        return self.name


class PurchaseOrder(models.Model):
    PRO = 'Pro'
    ARM = 'Arm'
    IO = 'Io'
    ENC = 'Enc'
    VW = 'Vw'
    company = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=250)
    balance = models.PositiveIntegerField(validators=[MinValueValidator(1)])  # TODO: rename to initial_order
    created = models.DateTimeField(auto_now=False, auto_now_add=True)
    LICENSE_TYPE = (
        (PRO, 'Professional'),
        (ARM, 'Embedded'),
        (IO, 'I/O'),
        (ENC, 'Encoder'),
        (VW, 'VideoWall')
    )
    license_type = models.CharField(
        max_length=4,
        choices=LICENSE_TYPE,
        default=PRO
    )

    class Meta:
        db_table = "PurchaseOrder"

    def get_absolute_url(self):
        return reverse('sales:purchaseorder_detail', kwargs={'pk': self.pk})

    def __str__(self):
        return self.name

    @property
    def total_channels(self):
        total = self.license_set.aggregate(models.Sum('channels'))
        if total.get('channels__sum') == None:
            return 0
        else:
            return total.get('channels__sum')

    @property
    def balance_left(self):
        return self.balance - self.total_channels


class License(models.Model):
    po = models.ForeignKey(PurchaseOrder, on_delete=models.SET_NULL, null=True)
    license_key = models.CharField(max_length=50, blank=True)
    enabled = models.BooleanField(default=True)
    generated = models.DateTimeField(auto_now=False, auto_now_add=True)
    channels = models.PositiveIntegerField(validators=[MinValueValidator(1)])

    class Meta:
        db_table = "License"

    def __str__(self):
        return self.license_key

    @staticmethod
    def key_generator():
        def step1(size=4, chars=string.ascii_uppercase + string.digits):
            return "".join(random.choice(chars) for _ in range(size))
        def step2():
            return "-".join([step1() for _ in range(4)])
        result = step2()
        while License.objects.filter(license_key=result).exists():
            result = step2()
        return result

    def clean(self):
        if self.channels > self.po.balance_left:
            raise ValidationError('Number of channels exceeds available order balance ')

    def save(self, *args, **kwargs):
        if not self.license_key:
            self.license_key = self.key_generator()
        super().save(*args, **kwargs)  # Call the "real" save() method.































