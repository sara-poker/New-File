from django.db import models


# Create your models here.

class Country(models.Model):
    class Meta:
        verbose_name = 'کشور'
        verbose_name_plural = 'کشور ها'

    name = models.CharField(verbose_name='اسم',max_length=50)
    persian_name = models.CharField(max_length=60, verbose_name='اسم فارسی', blank=True, null=True)
    country_id = models.CharField(max_length=3, verbose_name='آیدی_کشور', blank=True, null=True)
    continent = models.CharField(max_length=13, verbose_name='قاره', blank=True, null=True)
    population = models.IntegerField(verbose_name='جمعیت', blank=True, null=True)
    flag = models.CharField(max_length=60, verbose_name='قاره', blank=True, null=True)

    def __str__(self):
        return self.name


class Vpn(models.Model):
    class Meta:
        verbose_name = 'فیلتر شکن'
        verbose_name_plural = 'فیلتر شکن ها'

    PLATFORM_CHOICE = (
        ('Android', 'Android'),
        ('Telegram', 'Telegram'),
        ('Windows', 'Windows'),
        ('Chrome', 'Chrome'),
        ('Ios', 'Ios')
    )

    CHOICE = (
        ('Free', 'Free'),
        ('Limited Free', 'Limited Free'),
        ('Non-free', 'Non-free')
    )

    name = models.CharField(verbose_name='اسم',max_length=100)
    platform = models.CharField(max_length=10, verbose_name='پلتفرم', choices=PLATFORM_CHOICE)
    vpn_maker = models.CharField(max_length=100, verbose_name='نام سازنده', blank=True, null=True)
    vpn_country = models.ForeignKey(Country, verbose_name='کشور سازنده', related_name='vpn_country',
                                    on_delete=models.PROTECT, blank=True, null=True)
    vpn_normal_user_fee = models.CharField(max_length=12, verbose_name='وضعیت رایگان بودن', choices=CHOICE, null=True,
                                           blank=True)

    def __str__(self):
        return self.name


class Test(models.Model):
    class Meta:
        verbose_name = 'نتیجه تست'
        verbose_name_plural = 'نتایج تست ها'

    STATUS_CHOICE = (
        ('Filter', 'Filter'),
        ('Without Filter', 'Without Filter')
    )

    FILTER_CHOICE = (
        ('Drop After Connect', 'Drop After Connect'),
        ('Drop Pack Filter', 'Drop Pack Filter'),
        ('Fast And Stable', 'Fast And Stable'),
        ('Full Filter', 'Full Filter'),
        ('Low Speed Or UnStable', 'Low Speed Or UnStable')
    )

    date = models.IntegerField(verbose_name="تاریخ")
    time = models.CharField(verbose_name="ساعت",max_length=15)
    city = models.CharField(verbose_name='شهر',max_length=40)
    vpn = models.ForeignKey(Vpn, related_name='vpns', on_delete=models.PROTECT)
    oprator = models.CharField(max_length=30, verbose_name='اپراتور')
    status = models.CharField(max_length=18, verbose_name='وضعیت', choices=STATUS_CHOICE)
    filter = models.CharField(max_length=38, verbose_name='فیلترینگ', choices=FILTER_CHOICE)
    server_ip = models.CharField(verbose_name='آیپی سرور', blank=True, null=True,max_length=60)
    server_host = models.CharField(verbose_name='هاست سرور', blank=True, null=True,max_length=200)
    server_isp = models.CharField(verbose_name='ارائه دهنده سرور', blank=True, null=True,max_length=100)
    server_country = models.ForeignKey(Country, verbose_name='کشور سرور', related_name='server_country',
                                       on_delete=models.PROTECT, blank=True, null=True)
    server_region = models.CharField(verbose_name='منطقه سرور', blank=True, null=True,max_length=150)
    server_city = models.CharField(verbose_name='شهر سرور', blank=True, null=True,max_length=80)
    server_Latitude = models.CharField(verbose_name='عرض جغرافیایی سرور', blank=True, null=True,max_length=200)
    server_Longitude = models.CharField(verbose_name='طول جغرافیایی سرور', blank=True, null=True,max_length=200)
    ping_speed = models.IntegerField(verbose_name='سرعت پینگ', blank=True, null=True)
    ttl = models.IntegerField(verbose_name='حجم بسته', blank=True, null=True)
    proxy_port = models.CharField(max_length=7, verbose_name='پورت پروکسی', blank=True, null=True)
    proxy_secret = models.CharField(verbose_name='رمز پروکسی', blank=True, null=True,max_length=200)

    def __str__(self):
        return self.vpn.name + "|" + self.city + "|" + str(self.date)


class Isp(models.Model):
    class Meta:
        verbose_name = 'ارائه دهنده خدمات'
        verbose_name_plural = 'ارائه دهندگان خدمات'

    CLOUD_CHOICE = (
        ('True', 'True'),
        ('False', 'False')
    )

    name = models.CharField(verbose_name='اسم', blank=True, null=True,max_length=80)
    url = models.CharField(max_length=30, verbose_name='آدرس', blank=True, null=True)
    country = models.ForeignKey(Country, verbose_name='کشور', related_name='country', on_delete=models.PROTECT,
                                blank=True, null=True)
    cloud = models.CharField(max_length=18, verbose_name='وضعیت', choices=CLOUD_CHOICE, blank=True, null=True)

    def __str__(self):
        return self.name
