from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save


class Urls(models.Model):
    url = models.CharField(max_length=255)

    def __str__(self):
        return self.url


class CruxHistory(models.Model):
    url = models.ForeignKey(Urls, on_delete=models.CASCADE)
    date = models.DateField(auto_now=False, auto_now_add=False)
    clsm = models.FloatField(null=True, default=None)
    clsd = models.FloatField(null=True, default=None)
    lcpm = models.FloatField(null=True, default=None)
    lcpd = models.FloatField(null=True, default=None)
    fidm = models.FloatField(null=True, default=None)
    fidd = models.FloatField(null=True, default=None)
    inpm = models.FloatField(null=True, default=None)
    inpd = models.FloatField(null=True, default=None)
    ttfbm = models.FloatField(null=True, default=None)
    ttfbd = models.FloatField(null=True, default=None)
    fcpm = models.FloatField(null=True, default=None)
    fcpd = models.FloatField(null=True, default=None)

    class Meta:
        unique_together = [("url", "date")]
        get_latest_by = "date"

    def __str__(self):
        return f"{self.url},{self.date},{self.clsm},{self.clsd}"


class CruxWeeklyHistory(models.Model):
    url = models.ForeignKey(Urls, on_delete=models.CASCADE)
    lastdate = models.DateField(auto_now=False, auto_now_add=False)
    clsm = models.FloatField(null=True, default=None)
    clsd = models.FloatField(null=True, default=None)
    lcpm = models.FloatField(null=True, default=None)
    lcpd = models.FloatField(null=True, default=None)
    fidm = models.FloatField(null=True, default=None)
    fidd = models.FloatField(null=True, default=None)
    inpm = models.FloatField(null=True, default=None)
    inpd = models.FloatField(null=True, default=None)
    ttfbm = models.FloatField(null=True, default=None)
    ttfbd = models.FloatField(null=True, default=None)
    fcpm = models.FloatField(null=True, default=None)
    fcpd = models.FloatField(null=True, default=None)

    class Meta:
        unique_together = [("url", "lastdate")]
        get_latest_by = "lastdate"

    def __str__(self):
        return f"{self.url},{self.lastdate},{self.clsm},{self.clsd}"


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    urls = models.ManyToManyField(Urls, through="ProfileUrl")

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()


class ProfileUrl(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    url = models.ForeignKey(Urls, on_delete=models.CASCADE)
    email_alert = models.BooleanField(default=False)
    sensitivity = models.IntegerField(default=2)

    def __str__(self):
        return f"{self.url.url}"


class Annotations(models.Model):
    profileurl = models.ForeignKey(ProfileUrl, on_delete=models.CASCADE)
    date = models.DateField(auto_now=False, auto_now_add=False)
    annotation_title = models.CharField(max_length=10)
    annotation_text = models.CharField(max_length=255)
