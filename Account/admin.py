from django.contrib import admin

# Register your models here.
from .models import Users, Books, Video, Course, CouponPurchase, CoursePurchaseCoupon, CoursePurchaseRequest, LNMOnline, EmailSubscription, Post, Events

admin.site.register(Users)
admin.site.register(Video),
admin.site.register(Books),
admin.site.register(Course)
admin.site.register(CouponPurchase)
admin.site.register(CoursePurchaseRequest)
admin.site.register(CoursePurchaseCoupon)
admin.site.register(LNMOnline)
admin.site.register(EmailSubscription)
admin.site.register(Post)
admin.site.register(Events)
