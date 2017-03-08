from django.contrib import admin
#from safari_joint.models import *
from django.contrib.auth.models import User


from django.contrib import admin
from safari_joint.models import *


#from image_cropping.admin import ImageCroppingMixin
from image_cropping import ImageCroppingMixin


class MyModelAdmin(ImageCroppingMixin, admin.ModelAdmin):
    pass
admin.site.register(FunPictures, MyModelAdmin)

class PartnersModelAdmin(ImageCroppingMixin, admin.ModelAdmin):
    pass
admin.site.register(PartnersModel, PartnersModelAdmin)

class MyModelAdmin(ImageCroppingMixin, admin.ModelAdmin):
    pass
admin.site.register(PartnerLogo, MyModelAdmin)


class TripBookingAdmin(admin.ModelAdmin):
    fields = ['trip_booked', 'day_of_booking', 'full_name', 'email_address', 'phone_number', 'your_country', 'additional_note']
    readonly_fields = ['trip_booked', 'day_of_booking', 'full_name', 'email_address', 'phone_number', 'your_country', 'additional_note']

class AccomodationBookingAdmin(admin.ModelAdmin):
    fields = ['room_booked', 'reservation_placed_on', 'arrival_date', 'depature_date', 'your_name', 'email_address', 'phone_number', 'country']
    readonly_fields = ['room_booked', 'reservation_placed_on', 'arrival_date', 'depature_date', 'your_name', 'email_address', 'phone_number', 'country']


admin.site.register(TripBooking,TripBookingAdmin)
admin.site.register(PageContents)
admin.site.register(TripIteneraryChart)
admin.site.register(TripItenerary)
admin.site.register(TeamModel)
admin.site.register(TripAvailableDates)
admin.site.register(FeedsModel)
admin.site.register(FAQS)
admin.site.register(TripIdentificationTag)
admin.site.register(Service)
admin.site.register(AvailableAccomodation)
admin.site.register(AccomodationBookingModel, AccomodationBookingAdmin)
admin.site.register(TripDiscount)
admin.site.register(Paragraphs)
