from django.db import models
from django.contrib.auth.models import User

# Create your models here.
def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    #return 'user_{0}/{1}'.format(instance.user.id, filename)
    return 'user_{0}/{1}'.format(1, filename)


class Cryptocurrency(models.Model):
    symbol = models.CharField(max_length=30)
    name = models.CharField(max_length=30)
    logo = models.ImageField(upload_to=user_directory_path)

    def __str__(self):              # __unicode__ on Python 2
        return self.symbol

class Address(models.Model):
    owner = models.ForeignKey(User,on_delete=models.CASCADE)
    cryptocurrency = models.ForeignKey(Cryptocurrency,on_delete=models.CASCADE)
    name = models.CharField(max_length=30)
    address = models.CharField(max_length=500)

    def __str__(self):              # __unicode__ on Python 2
        return self.address

class Lectura(models.Model):
    POOLS = (
    (0, "total"),
    (1, "ahashpool"),
    (2, "zergpool"),
    (3, "zpool"),
    (4, "hashrefinery"),
    )
    cryptocurrency = models.ForeignKey(Cryptocurrency,on_delete=models.CASCADE)
    address = models.ForeignKey(Address,on_delete=models.CASCADE)
    pool = models.IntegerField(choices=POOLS)
    cash = models.FloatField()
    total_balance = models.FloatField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):              # __unicode__ on Python 2
        return str(self.cash)

    def add_new(self,address,pool_id,total,currency,total_balance):
        lec = Lectura()
        lec.address = address
        lec.cryptocurrency = address.cryptocurrency
        lec.pool = pool_id
        lec.cash = total
        lec.total_balance = total_balance
        lec.save()

    def get_pool_url(self):
        if self.pool == 1:
            return "https://www.ahashpool.com/wallet.php?wallet="
        if self.pool == 2:
            return "http://www.zergpool.com/?address="
        if self.pool == 3:
            return "http://zpool.ca/?address="
        if self.pool == 4:
            return "https://pool.hashrefinery.com/?address="
        else:
            return "./"





class PriceSnapshot(models.Model):
    cryptocurrency = models.ForeignKey(Cryptocurrency,on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    price = models.FloatField()

    def __str__(self):              # __unicode__ on Python 2
        return self.symbol

    def add_new(self,price,cryptocurrency):
        p = PriceSnapshot()
        p.cryptocurrency = cryptocurrency
        p.price = price
        p.save()
