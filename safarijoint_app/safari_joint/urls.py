"""safari_joint URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin

from django.conf.urls.static import static

from django.conf.urls import url
from django.views.generic.base import TemplateView
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
import os.path
from django.conf import *
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.conf import *
from django.views.generic import RedirectView

from django.contrib.auth import views as auth_views
#from safari_joint.forms import IteneraryForm1, IteneraryForm2, IteneraryForm3, IteneraryForm4, IteneraryForm5, IteneraryForm6, IteneraryForm7, IteneraryForm8, IteneraryForm9, IteneraryForm10
#from safari_joint.views import PostPicturesModelFormView,ShowThumbnail,ThumbnailOptions,thumbnail_foreign_key, HomePage,FeedsView,IndividualPartnersView,TermsAndConditions,CreateATrip,AllPartnerTripsView, PartnersView,PartnerRewiewVote,DeletePartnerPic, PartnersSignupView,  UserRegistrationView,Logout,AboutUs, BookingView,AllTripsView,LemoshoSevenDays,LemoshoEightDays,MaranguFiveDays,MaranguSixDays,MachameSixDays,MachameSevenDays,RongaiSixDays,RongaiSevenDays,UmbweSixDays,UmbweSevenDays, NorthernCircuitEightDays,NorthernCircuitNineDays,SafariOneDay,SafariTwoDay, SafariThreeDay, SafariFourDay, SafariFiveDay, SafariSixDay, SafariSevenDay, SafarievenCultural, AboutTanzania, SafariPacklist, AnimalsMigration, kilimanjaroPacklist, kilimanjaroTips, WhenToClimbKilimanjaro, FAQView
from safari_joint.views import AccomodationDiscountingView, AccomodationDiscountUpdateView, AccomodationDiscountDelete,TripDiscountUpdateView,TripDiscountDelete,AllPartnerFeedsView,ContactUsForm,PartnerBookings,TripBookingsSearches,TripDiscountingView,  ShowThumbnail,PostPicturesModelFormView,PartnerLogoFormView,IndexSearchResults, TripSearch,IndexAccomodationSearch,UserProfile,PartnerFeedbackForm, OneDayTrips, AllTripTags, TripUpdateFormView,AccomodationTypeUpdateForm,UserProfileUpdateFormView, PartnerProfileUpdateForm, AccomodationPartners,AllMonthTripsView,  TourOperatorPartners ,ThankYouForBookingAccomodation,AccomodationWhereYouAreGoing, AccomodationBookingView, AllPartnerAccomodation,  AvailableAccomodationView, SearchPartner,SearchAccomodationInArea, HomePage,FeedsView,ThankYouForBooking, IndividualPartnersView,TermsAndConditions,CreateATrip,AllPartnerTripsView, PartnersView,PartnerRewiewVote, DeletePartnerPic, PartnersSignupView,  UserRegistrationView,Logout,AboutUs, BookingView,AllTripsView, AboutTanzania, SafariPacklist, AnimalsMigration, kilimanjaroPacklist, kilimanjaroTips, WhenToClimbKilimanjaro, FAQView
#from safari_joint.views import TripItenerarySuggestionForm,
"Rename the links they are mistakenly arranged"

from django.contrib.auth.views import password_reset
from django.contrib.auth.views import password_reset_done
from django.contrib.auth.views import password_reset_confirm
from django.contrib.auth.views import password_reset_complete



urlpatterns = [
    url(r'^admin/', admin.site.urls),
#index searches urls
    url(r'^index-search-trip/', view = IndexSearchResults, name = 'index-trip-search'),
    url(r'^index-search-accomodation/', view = IndexAccomodationSearch, name = 'index-accomodation-search'), 

    url(regex=r'^give-feedback-(?P<partner_id>\d+)/$', view = PartnerFeedbackForm, name = 'partner-feedback-form-with-id'),
    url(regex=r'^give-feedback/$', view = PartnerFeedbackForm, name = 'partner-feedback-form'),


    url(regex=r'^home/$', view = HomePage, name= 'home-page'),
    url(regex=r'^about-tanzania/$', view = AboutTanzania, name= 'about-tanzania'),
    url(regex=r'^tanzania-safari-packList/$', view = SafariPacklist, name= 'safari-pack-list'),
    url(regex=r'^animal-migrations/$', view = AnimalsMigration, name= 'animals-migration'),
    url(regex=r'^kilimanjaro-pack-list/$', view = kilimanjaroPacklist, name= 'kilimanjaro-packlist'),
    url(regex=r'^kilimanjaro-climbing-tips/$', view = kilimanjaroTips, name= 'kilimanjaro-tips'),
    url(regex=r'^when-to-climb-kilimanjaro/$', view = WhenToClimbKilimanjaro, name= 'when-to-climb-kilimanjaro'),
    url(regex=r'^faq/$', view = FAQView, name= 'FAQ-view'),
    url(regex=r'^terms-and-conditions/$', view = TermsAndConditions, name= 'terms-and-conditions'),
    url(regex=r'^register/$', view = UserRegistrationView, name= 'user-registration-view'),
    url(regex=r'^logout/$', view = Logout, name= 'logout-page'),
    url(regex=r'^about-us/$', view = AboutUs,  name='about-us'),
    url(regex=r'^feeds/$', view = FeedsView,  name='feeds-view'),
    url(regex=r'^profile/(?P<user_id>\d+)/$', view = UserProfile,  name='user-profile'),
    url(regex=r'^user/(?P<user_id>\d+)/update/$', view = UserProfileUpdateFormView,  name='user-profile-update'), 
    url(regex=r'^contactemail/$', view = ContactUsForm,  name='contact-us-form'),

#partners
    url(regex=r'^partners/$', view = PartnersView,  name='partners-view'),
    url(regex=r'^all-reviews/(?P<partner_id>\d+)/$', view = AllPartnerFeedsView,  name='all-partner-feeds-view'),
    url(regex=r'^parners-sign-up/$', view = PartnersSignupView,  name='partners-signup-view'),
    url(regex=r'^parners-sign-up/(?P<partner_id>\d+)/$', view = PartnersSignupView,  name='partners-signup-view'),
    url(regex=r'^parners-profile-update/(?P<partner_id>\d+)/$', view = PartnerProfileUpdateForm,  name='partner-profile-update-form'),
    url(regex=r'^about-partner-(?P<partner_id>\d+)/$', view =  IndividualPartnersView, name='individual-partners-view'),
    url(regex=r'^vote-up-(?P<partner_id>\d+)/$', view =  PartnerRewiewVote, name='partner-rewiew-vote'),
    url(regex=r'^delete/(?P<picture_id>\d+)/$', view =  DeletePartnerPic, name='delete-partner-pic'),
    url(regex=r'^tour-operators/$', view =  TourOperatorPartners, name='tour-operator-partner'),
    url(regex=r'^accomodation-providers/$', view =  AccomodationPartners, name='accomodation-partners'),
#    url(regex=r'^about-partner-(?P<username>[\w-]+)/$', view =  IndividualPartnersView, name='individual-partners-view'),

#upload partner logo
    #url(regex=r'^upload-logo/$', view =  PartnerLogoFormView, name='partner-logo-form-view'),
    url(regex=r'^upload-a-logo/(?P<partner_id>\d+)/$', view =  PartnerLogoFormView, name='partner-logo-form-view'),

#trip booking
    url(regex=r'^Booking_trip/(?P<trip_id>\d+)/$', view =  BookingView, name='booking-view'),
    url(regex=r'^thank_you_for_booking/(?P<trip_id>\d+)/$', view = ThankYouForBooking, name='thank-you-for-booking-view'),


#create a trip

    url(regex=r'^create_trip/(?P<partner_id>\d+)/$', view =  CreateATrip, name='create-a-trip'),
    url(regex=r'^all-trips/(?P<partner_id>\d+)/$', view = AllPartnerTripsView,  name='all-partners-trips-view'),
    url(regex=r'^all-trips-this-month/$', view = AllMonthTripsView,  name='all-month-trips-view'), 
    url(regex=r'^all-one-day-trips/$', view = OneDayTrips,  name='all-one-day-trips-view'),
    url(regex=r'^all-trips/$', view = AllTripsView,  name='all-trips-view'),
    url(regex=r'^trip-(?P<trip_id>\d+)-update/$', view = TripUpdateFormView,  name='trip-update-form-view'),


#create a room/ accomodation

    url(regex=r'^create_a_room/(?P<partner_id>\d+)/$', view =  AvailableAccomodationView, name='available-accomodation-view'),
    url(regex=r'^all_available_accomodation-type/(?P<partner_id>\d+)/$', view =  AllPartnerAccomodation, name='all-partner-accomodation-type'),
    url(regex=r'^accomodation-in-area/(?P<trip_id>\d+)/$', view = AccomodationWhereYouAreGoing, name='accomodation-where-you-are-going'),
    url(regex=r'^update_room/(?P<room_id>\d+)/$', view = AccomodationTypeUpdateForm, name=' accomodation-type-update-form'),

#Accomodation Booking

    url(regex=r'^Booking_a_room/(?P<room_id>\d+)/$', view =  AccomodationBookingView, name='accomodation-booking-view'),
    url(regex=r'^thank_you_for_booking_a_room/(?P<room_id>\d+)/$', view = ThankYouForBookingAccomodation, name='thank-you-for-booking-accomodation'),


#partner Bookings
    url(regex=r'^your-bookings/(?P<partner_id>\d+)/$', view = PartnerBookings, name='partner-bookings-view'),
    url(regex=r'^get-bookings/(?P<partner_id>\d+)/$', view = TripBookingsSearches, name='trip-bookings-searches-view'),


#login views
    url(r'^login/$', auth_views.login, name='login'),
    url(r'^', include('django.contrib.auth.urls')),


#trip Itinearies
#    url(regex=r'^itineary/(?P<tag_id>\d+)/$', view = TripItenerarySuggestionForm.as_view(), name='trip-itenerary-suggestion-form'),
    url(regex=r'^all-tags/$', view = AllTripTags, name='all-trip-tags'),



#password reset


    url(r'^accounts/password/reset/$', auth_views.password_reset, {'post_reset_redirect' : '/accounts/password/reset/done/'}),
    #url(r'^user/password/reset/$',  {'password_reset_form': EmailValidationOnForgotPassword},name="password_reset"),
    url(r'^accounts/password/reset/done/$', auth_views.password_reset_done),
    url(r'^accounts/password/reset/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$', auth_views.password_reset_confirm, {'post_reset_redirect' : '/accounts/password/done/'}),
    url(r'^accounts/password/done/$', auth_views.password_reset_complete),


#seraching platiform
    url(r'^search/', view = SearchPartner, name = 'partner-search'),
    url(r'^search-accomodation-in-area/', view = SearchAccomodationInArea, name = 'search-accomodation-in-area'),
    url(r'^search-a-trip/', view = TripSearch, name = 'trip-search'),

#discount handling mechanisms
    url(r'^create_discount/(?P<trip_id>\d+)/$', view =  TripDiscountingView, name='trip-discounting-view'),
    url(r'^update_discount/(?P<discount_id>\d+)/$', view =  TripDiscountUpdateView, name='trip-discounting-update-view'),
    url(r'^delete_discount/(?P<discount_id>\d+)/$', view =  TripDiscountDelete, name='trip-discounting-delete-view'),


    url(r'^create_room_discount/(?P<room_id>\d+)/$', view =  AccomodationDiscountingView, name='accomodation-discounting-view'),
    url(r'^update_room_discount/(?P<discount_id>\d+)/$', view =  AccomodationDiscountUpdateView, name='accomodation-discounting-update-view'),
    url(r'^delete_room_discount/(?P<discount_id>\d+)/$', view =  AccomodationDiscountDelete, name='room-discounting-delete-view'),

#formtools view

#TripItenerarySuggestionForm.as_view([IteneraryForm1, IteneraryForm2, IteneraryForm3, IteneraryForm4, IteneraryForm5, IteneraryForm6, IteneraryForm7, IteneraryForm8, IteneraryForm9, IteneraryForm10])

#    url(regex=r'^itineary/(?P<id>\d+)/$', view =  TripItenerarySuggestionForm.as_view([IteneraryForm1, IteneraryForm2, IteneraryForm3, IteneraryForm4, IteneraryForm5, IteneraryForm6, IteneraryForm7, IteneraryForm8, IteneraryForm9, IteneraryForm10]), name='atineary-creation-view'),


#Examples
    url(r'^modelform_example/$', view =  PostPicturesModelFormView, name = 'modelform_example'),
    url(r'^modelform_example/(?P<image_id>\d+)/$', view =  PostPicturesModelFormView, name='modelform_example'),
    url(r'^show_thumbnail/(?P<image_id>\d+)/$', view =  ShowThumbnail, name='show_thumbnail'),
#    url(r'^$', view = ThumbnailOptions, name='thumbnail_options'),
#    url(r'^show_foreignkey_thumbnail/$', view = thumbnail_foreign_key, name='thumbnail_foreign_key'),
#    url(r'^show_foreignkey_thumbnail/(?P<instance_id>\d+)/$', view = thumbnail_foreign_key, name='thumbnail_foreign_key'),

]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)

#urlpatterns += staticfiles_urlpatterns()
