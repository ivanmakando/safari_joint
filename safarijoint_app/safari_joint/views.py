from django.template import *
from django.contrib.auth import *
from django.http import *
from django.contrib.auth.models import *
#from django.core.context_processors import csrf
from django.http import HttpResponseRedirect
#from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as django_logout
#from django.contrib.auth import login as django_login, authenticate
#from django.utils import timezone
#from random import sample
from django.shortcuts import *
from django.utils import timezone
from django.views.decorators import csrf
from django.views.decorators.csrf import csrf_protect
from django.utils import timezone
from safari_joint.forms import *
from safari_joint.models import *
from django.contrib.auth.models import User
from django.views.generic.edit import FormView
from django.core.mail import EmailMessage

#from image_cropping.utils import get_backend
from easy_thumbnails.files import get_thumbnailer
from datetime import date
from django.contrib import messages
from formtools.wizard.views import SessionWizardView, WizardView

try:
    from django.utils import simplejson as json
except ImportError:
    import json
from django.views.decorators.http import require_POST

def PostPicturesModelFormView(request, image_id=None):
    image = get_object_or_404(FunPictures, pk = image_id) if image_id else None
    form = FunPicturesForm(instance = image)
    if request.method == "POST":
        form = FunPicturesForm(request.POST, request.FILES, instance=image)
        if form.is_valid():
            image = form.save()
            return HttpResponseRedirect(reverse('modelform_example', args=(image.pk,)))
    return render(request, 'image_crop/modelform_example.html', {'form': form, 'image': image})

def ShowThumbnail(request, image_id):
    image = get_object_or_404(FunPictures, pk=image_id)
#    thumbnail_url = get_backend().get_thumbnail_url(image.image_field, {
#        'size': (430, 360),
#        'box': image.cropping,
#        'crop': True,
#        'detail': True,
#    }).url
#    thumbnail_url = get_thumbnailer(image.image).get_thumbnail({
#        'size': (430, 360),
#        'box': image.cropping,
#        'crop': True,
#        'detail': True,
#    }).url
    thumbnail_url = get_backend().get_thumbnail_url(image.image_field, {
        'size': (430, 360),
        'box': image.cropping,
        'crop': True,
        'detail': True,
    })
    return render(request, 'image_crop/thumbnail.html', {'thumbnail_url': thumbnail_url})

def ThumbnailOptions(request):
    try:
        image = PostPicturesModel.objects.all()[0]
    except (PostPicturesModel.DoesNotExist, IndexError,):
        image = None
    return render(request, 'image_crop/thumbnail_options.html', {'image': image})

def thumbnail_foreign_key(request, instance_id=None):
    if not instance_id:
        try:
            imagefk = ImageFK.objects.all()[0]
        except (ImageFK.DoesNotExist, IndexError,):
            imagefk = None
    else:
        try:
            imagefk = ImageFK.objects.get(pk=instance_id)
        except ImageFK.DoesNotExist:
            imagefk = None
    return render(request, 'image_crop/thumbnail_foreign_key.html', {'imagefk': imagefk})


def random_booking_chars():
    time = timezone.now()
#    date = date.today()
    serial_chars = get_random_string( length = 4, allowed_chars = 'TZA123456789BCDEFGHIJKLMNOPQRSTUVWXYZ' )
    date_string =str(time.minute+time.second*time.microsecond)
    ultimate_booking_chars = serial_chars+date_string+"SM"
    return ultimate_booking_chars

def Logout(request):
    django_logout(request)
    return HttpResponseRedirect('/home')

@csrf_protect
def HomePage(request):
    feeds = FeedsModel.objects.all().order_by('-feed_posted_on')
    user = request.user
    tags = TripIdentificationTag.objects.all()
    dates = TripAvailableDates.objects.all().order_by('-depature_date')
    partner = PartnersModel.objects.all().order_by('-company_review')[:12]
    this_month = timezone.now()
    full_month_name = this_month.strftime("%B")
    #page = PageContents.objects.get(id = 24)
    best_sell = TeamModel.objects.get(id = 2)
#    if request.method == 'POST':
#        form = TripSearchForm(request.POST)
#        if form.is_valid():
#            depature_date_data = form.cleaned_data['trip_depature_date']
#            trip_tag_data = form.cleaned_data['the_trip_tag']
#whein it starts to fail again chabge id in the trip tag into tag_name!
#            results = TripAvailableDates.objects.filter(depature_date__contains = depature_date_data, trip_tag__id__contains = trip_tag_data)

#            return render (request, 'search/index-search.html', {'results':results})

#    else:
    form = TripSearchForm()
    form1 = AccomodationSearch()
    return render (request, 'index.html', {'form': form, 'form1':form1, 'partner':partner, 'tags':tags,  'user':user, 'feeds':feeds, 'dates':dates, 'full_month_name':full_month_name, 'best_sell':best_sell})

@csrf_protect
def IndexSearchResults(request):
    if request.method == 'POST':
        depature_date_data = request.POST['depature_date_data']
        trip_tag_data = request.POST['trip_tag_data']
    else:
        depature_date_data = ''
        trip_tag_data = ''
#whein it starts to fail again chabge id in the trip tag into tag_name!
    results = TripAvailableDates.objects.filter(depature_date__contains = depature_date_data, trip_tag__id__contains = trip_tag_data)
    return render (request, 'search/index-search-trip.html', {'results':results})
@csrf_protect
def IndexAccomodationSearch(request):
#    results = []
    if request.method =='POST':
        room_type_data = request.POST['room_type_data']
        destination_data = request.POST['destination_data']
    else:
        room_type_data = ''
        destination_data = ''
    results = AvailableAccomodation.objects.filter(accomodation_type__contains = room_type_data, owner_company__company_location__contains = destination_data)
    return render (request, 'search/index-search-accomodation.html', {'results':results, 'room_type_data':room_type_data})


def UserProfile(request, user_id):
    logged_in_user = request.user
    syst_user = User.objects.get(id = user_id)
    company = syst_user.partnersmodel_set.all()
    trips = syst_user.tripavailabledates_set.all()
    rooms = syst_user.availableaccomodation_set.all()
    page = PageContents.objects.get(id = 41)
    values = RequestContext(request, {
        'syst_user':syst_user,
        'logged_in_user':logged_in_user,
#        'user':user,
        'page':page,
        'company':company,
        'trips':trips,
        'rooms':rooms
    })
    return render_to_response('user-page.html', values)

@csrf_protect
def AvailableAccomodationView(request, partner_id):
    page = PageContents.objects.get(id = 39)
    user = request.user
    partner = PartnersModel.objects.get(id = partner_id)
    if request.method == 'POST':
        form = AvailableAccomodationForm(request.POST, request.FILES)
        if form.is_valid():
            accomodation = form.save(commit = False)
            accomodation.owner_company = partner
            accomodation.user = user
            accomodation.original_price = form.cleaned_data['price_USD']
            accomodation.save()
            form.save_m2m()
            return HttpResponseRedirect(reverse('individual-partners-view', args=(partner.id,)))
    else:
        form = AvailableAccomodationForm()

    return render(request, 'create_accomodation.html', {'form': form, 'user': user, 'partner': partner, 'page': page})

def AllPartnerAccomodation(request, partner_id):
    partner = PartnersModel.objects.get(id = partner_id)
    user = request.user
    page = PageContents.objects.get(id = 40)
    rooms = partner.availableaccomodation_set.all()
    variables = RequestContext(request, {
        'partner':partner,
        'user': user,
        'page':page,
        'rooms':rooms
    })
    return render_to_response('all-accomodation-type.html', variables)

@csrf_protect
def TripSearch(request):
    tags = TripIdentificationTag.objects.all()
    if request.method == 'GET':
        leaving_date = request.POST['depature_date']
        tag = request.POST['trip_tag']
        trip = TripAvailableDates.objects.filter(depature_date = leaving_date, trip_tag = tag)
        return HttpResponseRedirect('/all-trips')
    return render_to_response (request, 'index.html', {'tags':tags})



@csrf_protect
def SearchPartner(request):
    if request.method == 'POST':
        search_text = request.POST['search_text']
    else:
        search_text = ''
    partners = PartnersModel.objects.filter(company_name__contains = search_text)
    return render_to_response('search/ajax_search.html', {'partners':partners})

@csrf_protect
def SearchAccomodationInArea(request):
    if request.method == 'POST':
        search_text = request.POST['search_text']
    else:
        search_text = ''
    partners = PartnersModel.objects.filter(company_name__contains = search_text)
    #return render(request, 'search/ajax_search_a_hotel.html', {'partners':partners})
    return render_to_response('search/ajax_search_a_hotel.html', {'partners':partners})


@csrf_protect
def UserRegistrationView(request):
    if request.method == 'POST':
        form  = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/login')
    else:
        form  = UserRegistrationForm()

    return render(request, 'registration/register.html', {'form':form})

def AboutUs(request):
    user = request.user
    page = PageContents.objects.get(id = 2)
    paragraph = page.paragraphs_set.all()
    #team = TeamModel.objects.get(id = 1)
    return render(request, 'hybrid-page.html', {'user': user, 'page':page, 'paragraph':paragraph})

def BookingView(request, trip_id):
    trip = TripAvailableDates.objects.get(id = trip_id)
    partner = trip.partner_concerned
    user_in_trip = trip.user
    get_this_email = user_in_trip.partnersmodel_set.all()
    user = request.user
    page = PageContents.objects.get(id = 3)
    receipt_serial_gen = random_booking_chars()

    if request.method == 'POST':
        form = TripBookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit = False)
            booking.trip_booked = trip
            booking.trip_owner_partner = trip.partner_concerned
            booking.receipt_serial = receipt_serial_gen
            #to_mail = booking.save()

            subject = "Trip Booked"
            from_email = form.cleaned_data['email_address']
            the_content = trip

            message = [{
                'Receipt Identification Number (Keep this a secreat)': receipt_serial_gen,
                'Name of Trip': the_content.trip_name,
                'Trip Serial': the_content.trip_serial,
                'deparure': the_content.depature_date,
                'returning': the_content.returning_date,
                'price in Us Dollars': the_content.trip_price,
                'Trip tag': the_content.trip_tag,
            }]
            for r in get_this_email:
                this_partner_email = r.created_by.email
            send_mail(subject,from_email, message, [this_partner_email , 'ivanphilipg@gmail.com'], fail_silently = True)
            booking.save()

            #return HttpResponseRedirect('/thank_you_for_booking')
            return HttpResponseRedirect(reverse('thank-you-for-booking-view', args=(trip.id,)))
    else:
        form = TripBookingForm()

    return render (request, 'booking.html', {'form':form, 'user':user, 'trip':trip, 'page':page})


def AccomodationBookingView(request, room_id):
    room_acc = AvailableAccomodation.objects.get(id = room_id)
    room_availability = room_acc.availability()
    room_related_bookings = room_acc.accomodationbookingmodel_set.all()
    today_date = date.today
    room = room_acc
    room_available_on = room_acc.available_date()
    partner = room.owner_company
    user_in_trip = room.user
    get_this_email = user_in_trip.partnersmodel_set.all()
    user = request.user
    page = PageContents.objects.get(id = 3)
    receipt_serial_gen = random_booking_chars()

    if request.method == 'POST':
        form = AccomodationBookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit = False)
#cheking room availability of room and date
            user_arrival_date = form.cleaned_data.get('arrival_date')
            booking.room_owner_partner = room.owner_company
            booking.receipt_serial = receipt_serial_gen
            if room_availability == False:
                if user_arrival_date < room_available_on:
                    raise forms.ValidationError ("Sorry Currently this room is fully booked. This room will be available again from " + str(room_available_on) + " Please try another room.")
                else:
                    booking.room_booked = room
            else:
                booking.room_booked = room
            subject = "Trip Booked"
            from_email = form.cleaned_data['email_address']
            the_content = room

#sending email (some datas) are obtained from above!
            if the_content.airport_transport == True:
                status = 'Included'
            else:
                status = 'Not Included'
            message = [{
                'Receipt Identification Number (Keep this a secreat)': receipt_serial_gen,
                'Room Type': the_content.accomodation_type,
                'Room Product Serial Number': the_content.room_serial_number,
                'Owner Company': the_content.owner_company,
                'price in Us Dollars': the_content.price_USD,
                'Airport Transport': status
            }]
            for r in get_this_email:
                this_partner_email = r.created_by.email
            send_mail(subject,from_email, message, [this_partner_email , 'ivanphilipg@gmail.com'], fail_silently = True)

            booking.save()
            return HttpResponseRedirect(reverse('thank-you-for-booking-accomodation', args=(room.id,)))
    else:
        form = AccomodationBookingForm()

    return render (request, 'accomodation-booking.html', {'form':form, 'user':user, 'room':room, 'page':page})


def ThankYouForBooking(request, trip_id):
    user = request.user
    page = PageContents.objects.get(id = 38)
    trip = TripAvailableDates.objects.get(id = trip_id)
    partner = PartnersModel.objects.all()
    values = RequestContext(request, {
        'user':user,
        'page': page,
        'trip': trip,
        'partner' : partner
    })
    return render_to_response('thank-you-for-booking.html', values)


def ThankYouForBookingAccomodation(request, room_id):
    user = request.user
    page = PageContents.objects.get(id = 38)
    room = AvailableAccomodation.objects.get(id = room_id)
    booking_details = room.accomodationbookingmodel_set.all()
    partner = PartnersModel.objects.all()
    values = RequestContext(request, {
        'user':user,
        'page': page,
        'room': room,
        'partner' : partner,
        'booking_details':booking_details,
    })
    return render_to_response('thank-you-for-booking.html', values)

@csrf_protect
def AccomodationWhereYouAreGoing(request, trip_id):
    user = request.user
    page = PageContents.objects.get(id = 40)
    trip = TripAvailableDates.objects.get(id = trip_id)
    partner = PartnersModel.objects.all()
    values = RequestContext(request, {
        'user':user,
        'page': page,
        'trip': trip,
        'partner' : partner
    })
    return render_to_response('accomodation-where-you-are-going.html', values)



def AllTripsView(request):
    user = request.user
    partner = PartnersModel.objects.all()
    this_month = timezone.now()
    full_month_name = this_month.strftime("%B")

    #dates = partner.tripavailabledates_set.all().order_by('depature_date')
    dates = TripAvailableDates.objects.all().order_by('depature_date')
    page = PageContents.objects.get(id = 4)

    return render (request, 'all-trips.html', {'user':user, 'dates':dates, 'page':page,'full_month_name':full_month_name})

def AllMonthTripsView(request):
    user = request.user
    partner = PartnersModel.objects.all()
    this_month = timezone.now()
    full_month_name = this_month.strftime("%B")
    #dates = partner.tripavailabledates_set.all().order_by('depature_date')
    dates = TripAvailableDates.objects.all().order_by('depature_date')
    page = PageContents.objects.get(id = 4)

    return render (request, 'all-month-trips.html', {'user':user, 'dates':dates, 'page':page, 'full_month_name':full_month_name})

def OneDayTrips(request):
    user = request.user
    partner = PartnersModel.objects.all()
    this_month = timezone.now()
    full_month_name = this_month.strftime("%B")
    #dates = partner.tripavailabledates_set.all().order_by('depature_date')
    dates = TripAvailableDates.objects.all().order_by('depature_date')
    page = PageContents.objects.get(id = 4)

    return render (request, 'one-day-trips.html', {'user':user, 'dates':dates, 'page':page, 'full_month_name':full_month_name})



def AllTripTags(request):
    page = PageContents.objects.get(id = 44)
    tags = TripIdentificationTag.objects.all()
    user = request.user
    values = RequestContext(request, {
        'page':page, 
        'tags':tags,
        'user':user
        })
    return render_to_response('all-tags.html', values)

#'trip_tag', 'user', 'partner'

def AllPartnerTripsView(request, partner_id):
    user = request.user
    partner = PartnersModel.objects.get(id = partner_id)
    dates = partner.tripavailabledates_set.all().order_by('depature_date')
    page = PageContents.objects.get(id = 4)

    return render (request, 'partner-all-trips.html', {'user':user, 'dates':dates, 'page':page, 'partner':partner})

def AllPartnerFeedsView(request, partner_id):
    user = request.user
    partner = PartnersModel.objects.get(id = partner_id)
    feeds = FeedsModel.objects.all().order_by('-feed_posted_on')
    page = PageContents.objects.get(id = 25)

    return render (request, 'partner-all-feeds.html', {'user':user, 'feeds':feeds, 'page':page, 'partner':partner})


def FeedsView(request):
    user = request.user
    feeds = FeedsModel.objects.all().order_by('?')
    page = PageContents.objects.get(id = 25)
    values = RequestContext(request, {
        'user':user,
        'feeds': feeds,
        'page': page,
    })
    return render_to_response ('all-feeds.html', values)

@csrf_protect
def PartnersView(request):
    page = PageContents.objects.get(id = 26)
    user = request.user
    partner = PartnersModel.objects.all()
    values = RequestContext(request, {
        'user':user,
        'partner':partner,
        'page':page,
    })
    return render(request, 'partners.html', {'user':user, 'partner':partner,'page':page,})

def TourOperatorPartners(request):
    page = PageContents.objects.get(id = 26)
    user = request.user
    partner = PartnersModel.objects.all()
    values = RequestContext(request, {
        'user':user,
        'partner':partner,
        'page':page,
    })
    return render(request, 'tour-operators-partners.html', {'user':user, 'partner':partner,'page':page,})

def AccomodationPartners(request):
    page = PageContents.objects.get(id = 26)
    user = request.user
    partner = PartnersModel.objects.all()
    values = RequestContext(request, {
        'user':user,
        'partner':partner,
        'page':page,
    })
    return render(request, 'accomodation-partners.html', {'user':user, 'partner':partner,'page':page,})


def PartnerLogoFormView(request, partner_id):
    user = request.user
    partner = PartnersModel.objects.get(id = partner_id)
    if partner.partnerlogo:
        logo = partner.partnerlogo
    else:
        None
    if request.method == 'POST':
        form = PartnerLogoForm(request.POST, request.FILES)
        if form.is_valid():
            logo = form.save(commit = False)
            logo.partner = partner
            logo.save()

        #return HttpResponseRedirect('/home')
        return HttpResponseRedirect(reverse('partner-logo-form-view', args=(partner.pk,)))
    else:
        form = PartnerLogoForm()
    return render (request, 'logo-form.html', {'form':form, 'partner': partner, 'user': user, 'logo':logo})

#def PartnerLogoFormView(request, partner_id = None):
#    partner = PartnersModel.onjects.get(id = partner_id)
#    partner = get_object_or_404(PartnersModel, id = partner_id) if partner_id else None
#    image = get_object_or_404(PartnerLogo, pk = image_id) if image_id else None
#    form = PartnerLogoForm()
#    if request.method == "POST":
#        form = FunPicturesForm(request.POST, request.FILES)
#        if form.is_valid():
#            image = form.save(commit = False)
#            image.partner = partner
#            image.save()
#            return HttpResponseRedirect(reverse('modelform_example', args=(image.pk,)))
#    return render(request, 'image_crop/modelform_example.html', {'form': form, 'partner':partner})

def PartnerRewiewVote (request, partner_id):
    user = request.user.id
    person = request.user
    partner = PartnersModel.objects.get(id = partner_id)
    if person.is_authenticated:
        if partner.votes.exists(user):
            pass
#        partner.votes.down(user)
        else:
            partner.votes.up(user)
    else:
        return HttpResponseRedirect('/login')
    ammount = partner.votes.count()
    partner.company_review = ammount
    partner.save()
    return HttpResponseRedirect(reverse('individual-partners-view', args=(partner.id,)))

def IndividualPartnersView(request, partner_id):
    page = PageContents.objects.get(id = 27)
    user = request.user
    partner = PartnersModel.objects.get(id = partner_id)
    feeds = partner.feedsmodel_set.all()
    pictures = partner.partnergallerypicture_set.all()
    dates = partner.tripavailabledates_set.all()
    rooms = partner.availableaccomodation_set.all()[:4]
    if request.method == 'POST':
        form = PartnerGalleryPictureForm(request.POST, request.FILES)
        if form.is_valid():
            picture = form.save(commit = False)
            picture.uploaded_by = request.user
            picture.partner = partner
            picture.save()
            return HttpResponseRedirect(reverse('individual-partners-view', args=(partner.id,)))

    else:
        form = PartnerGalleryPictureForm()

    form2 = FeedsForm()
    return render (request, 'individual-partner.html', {'form': form, 'form2':form2, 'feeds':feeds, 'partner' : partner, 'user':user, 'rooms': rooms, 'pictures':pictures, 'page':page, 'dates':dates})

def PartnersSignupView(request, partner_id = None):
    user = request.user
    partner = get_object_or_404(PartnersModel, pk = partner_id) if partner_id else None
    form = PartnersForm(instance = partner)
    if request.method == 'POST':
        form = PartnersForm(request.POST, request.FILES, instance = partner)
        if form.is_valid():
            partner = form.save(commit = False)
            partner.created_by = user
            partner.originally_registed_as = request.POST['company_name']
            partner.save()
            return HttpResponseRedirect(reverse('individual-partners-view', args=(partner.id,)))
            #return HttpResponseRedirect(reverse('partners-signup-view', args=(partner.id,)))

    else:
        form = PartnersForm()

    return render (request, 'partner-signup.html', {'form': form, 'user': user, 'partner': partner})

def PartnerGalleryPictureView(request):
    user = request.user
    if request.method == 'POST':
        form = PartnerGalleryPictureForm(request.POST, request.FILES)
        if form.is_valid():
            partner = form.save(commit = False)
            partner.created_by = user
            partner.save()

            return HttpResponseRedirect('/partners')

    else:
        form = PartnerGalleryPictureForm()

    return render (request, 'causes-single-copy.html', {'form': form, 'user': user})

def DeletePartnerPic(request, picture_id):
    user = request.user
    picture = PartnerGalleryPicture.objects.get(id = picture_id)
    partner = picture.partner
    partner_id = picture.partner.created_by
    if user.id == partner.created_by.id:
        picture.delete()
    return HttpResponseRedirect(reverse('individual-partners-view', args=(partner.id,)))


@csrf_protect
def TripUpdateFormView(request, trip_id):
    user = request.user
    trip = TripAvailableDates.objects.filter(id = trip_id)
    this_trip = TripAvailableDates.objects.get(id = trip_id)
    page = PageContents.objects.get(id = 42)
    if request.method == 'POST':
        form = TripUpdateForm(request.POST)
        if form.is_valid():
            trip_name_data = request.POST['trip_name']
            trip_price_data = request.POST['trip_price']
            about_trip_data = request.POST['about_trip']
            subject = "A Trip Was Updated"
            from_email = this_trip.user.email
            message = [{
                'Trip Updated On': timezone.now(),
                'Original Trip Name': this_trip.trip_original_name,
                'New Name Created': trip_name_data,
                'Trip Price (edited)': trip_price_data,
                'About Trip (edited)': about_trip_data
            }]
            send_mail(subject,from_email, message, [from_email , 'ivanphilipg@gmail.com'], fail_silently = True)
            trip.update(trip_name = trip_name_data, trip_price = trip_price_data, about_trip = about_trip_data, is_udated = True, trip_updated_on = timezone.now())
        #return HttpResponseRedirect('/home')
        return HttpResponseRedirect(reverse('all-partners-trips-view', args=(this_trip.partner_concerned.id,)))
    else:
        form = TripUpdateForm()
    return render(request, 'trip-update.html', {'form':form, 'user':user, 'this_trip':this_trip, 'trip':trip, 'page':page})

@csrf_protect
def PartnerProfileUpdateForm(request, partner_id):
    user = request.user
    partner = PartnersModel.objects.filter(id = partner_id)
    this_partner = PartnersModel.objects.get(id = partner_id)
    if request.method == 'POST':
        form = PartnerUpdateForm(request.POST)
        if form.is_valid():
            company_name_data = request.POST['company_name']
            company_established_on_data = request.POST['company_established_on']
            company_location_data = request.POST['company_location']
            about_company_data = request.POST['about_company']
            company_website_data = request.POST['company_website']
            subject = "Company Profile Was Updated"
            from_email = this_partner.created_by.email
            message = [{
                'Profile Updated On': timezone.now(),
                'Original Company Name': this_partner.originally_registed_as,
                'New Name Created': company_name_data,
                'Established on (edited)': company_established_on_data,
                'Company Location (edited)':company_location_data,
                'Company Website (edited)': company_website_data,
                'About Company (edited)': about_company_data
            }]
            send_mail(subject,from_email, message, [from_email , 'ivanphilipg@gmail.com'], fail_silently = True)
            partner.update(company_name = company_name_data, company_established_on = company_established_on_data, company_location = company_location_data, company_website = company_website_data, about_company = about_company_data, is_edited = True, edited_on = timezone.now())
        #return HttpResponseRedirect('/home')
        return HttpResponseRedirect(reverse('individual-partners-view', args=(this_partner.id,)))
    else:
        form = PartnerUpdateForm()
    return render(request, 'partner-update.html', {'form':form, 'user':user, 'this_partner':this_partner, 'partner':partner})


@csrf_protect
def AccomodationTypeUpdateForm(request, room_id):
    user = request.user
    room = AvailableAccomodation.objects.filter(id = room_id)
    this_room = AvailableAccomodation.objects.get(id = room_id)
    page = PageContents.objects.get(id = 42)
    if request.method == 'POST':
        form = AccomodationUpdateForm(request.POST)
        if form.is_valid():
            price_data = form.cleaned_data['price']
            available_space_data = form.cleaned_data['available_space']
            noice_level_data = form.cleaned_data['noice_level']
            airport_transport_data = form.cleaned_data['airport_transport']
            available_services_data = form.cleaned_data['available_services']
            subject = "Accomodation Type Was Updated"
            from_email = this_room.user.email
            for available_services_data in available_services_data:
                added_services = available_services_data
            message = [{
                'Updated On': timezone.now(),
                'Original Price Was': this_room.original_price,
                'New Price': price_data,
                'Available Space (edited)': available_space_data,
                'Noice Level (edited)': noice_level_data,
                'Aiport Transport (edited)': airport_transport_data,
                'Available Services (edited)': added_services
            }]

            send_mail(subject,from_email, message, [from_email , 'ivanphilipg@gmail.com'], fail_silently = True)
            #room.update(available_space = available_sapace_data, price_USD = price_data, noise_level = noice_level_data, airport_transport = airport_transport_data, is_updated = True, room_updated_on = timezone.now())
            room.update(price_USD = price_data, available_space = available_space_data, noise_level = noice_level_data, airport_transport = airport_transport_data, is_updated = True, room_updated_on = timezone.now())
            services = Service.objects.all()
            for service in services:
                this_room.services.add(available_services_data)
        return HttpResponseRedirect(reverse('individual-partners-view', args=(this_room.owner_company.id,)))
    else:
        form = AccomodationUpdateForm()

    return render(request, 'room-update.html', {'form':form, 'user':user, 'this_room':this_room, 'room':room, 'page':page})

def UserProfileUpdateFormView(request, user_id):
    user = request.user
    user_updating = User.objects.filter(id = user_id)
    this_user_updating = User.objects.get(id = user_id)
    page = PageContents.objects.get(id = 42)
    if request.method == 'POST':
        form = UserUpdateForm(request.POST)
        if form.is_valid:
            email_data = request.POST['email']
            username_data = request.POST['username']
            first_name_data = request.POST['first_name']
            last_name_data = request.POST['last_name']

            subject = "User Profile Updated"
            from_email = this_user_updating.email
            message = [{
                'Updated On': timezone.now(),
                'New Email': email_data,
                'New Username': username_data,
                'First Name (edited)': first_name_data,
                'Last Name (edited)': last_name_data,
            }]

            send_mail(subject,from_email, message, [from_email , 'ivanphilipg@gmail.com'], fail_silently = True)
            user_updating.update(email = email_data, username = username_data, first_name = first_name_data, last_name = last_name_data)
            return HttpResponseRedirect(reverse('user-profile', args=(this_user_updating.id,)))
    else:
        form = UserUpdateForm()
    return render (request, 'user-update.html', {'form':form, 'page':page, 'user':user, 'this_user_updating':this_user_updating})

def AboutTanzania(request):
    user = request.user
    page = PageContents.objects.get(id = 29)
    best_sell = TeamModel.objects.get(id = 2)
    values = RequestContext(request, {
        'user':user,
        'page':page,
        'best_sell':best_sell
    })
    return render_to_response('page-contents-1.html', values)

def SafariPacklist(request):
    user = request.user
    page = PageContents.objects.get(id = 30)
    best_sell = TeamModel.objects.get(id = 2)
    values = RequestContext(request, {
        'user':user,
        'page':page,
        'best_sell':best_sell
    })
    return render_to_response('page-contents-1.html', values)

def AnimalsMigration(request):
    user = request.user
    page = PageContents.objects.get(id = 31)
    best_sell = TeamModel.objects.get(id = 2)
    values = RequestContext(request, {
        'user':user,
        'page':page,
        'best_sell':best_sell
    })
    return render_to_response('page-contents-1.html', values)

def kilimanjaroPacklist(request):
    user = request.user
    page = PageContents.objects.get(id = 32)
    best_sell = TeamModel.objects.get(id = 2)
    values = RequestContext(request, {
        'user':user,
        'page':page,
        'best_sell':best_sell
    })
    return render_to_response('page-contents-1.html', values)


def kilimanjaroTips(request):
    user = request.user
    page = PageContents.objects.get(id = 33)
    best_sell = TeamModel.objects.get(id = 2)
    values = RequestContext(request, {
        'user':user,
        'page':page,
        'best_sell':best_sell
    })
    return render_to_response('page-contents-1.html', values)

def WhenToClimbKilimanjaro(request):
    user = request.user
    page = PageContents.objects.get(id = 34)
    best_sell = TeamModel.objects.get(id = 2)
    values = RequestContext(request, {
        'user':user,
        'page':page,
        'best_sell':best_sell
    })
    return render_to_response('page-contents-1.html', values)

def FAQView(request):
    user = request.user
    page = PageContents.objects.get(id = 35)
    faqs = FAQS.objects.all()
    values = RequestContext(request, {
        'user':user,
        'page':page,
        'faqs': faqs
    })
    return render_to_response('hybrid-page.html', values)


def TermsAndConditions(request):
    user = request.user
    page = PageContents.objects.get(id = 36)
    paragraph = page.paragraphs_set.all()
    best_sell = TeamModel.objects.get(id = 2)
    values = RequestContext(request, {
        'user':user,
        'page':page,
        'best_sell':best_sell,
        'paragraph':paragraph
    })
    return render_to_response('hybrid-page.html', values)


def CreateATrip(request, partner_id):
    user = request.user
    page = PageContents.objects.get(id = 37)
    partner = PartnersModel.objects.get(id = partner_id)
    if request.method == 'POST':
        form = PartnerTripAvailableDatesForm(request.POST, request.FILES,)
        if form.is_valid():
            trip = form.save(commit = False)
            trip.user = partner.created_by
            trip.partner_concerned = partner
            trip.trip_original_name = form.cleaned_data['trip_name']
            trip.trip_original_price = form.cleaned_data['trip_price']
            trip.save()
            return HttpResponseRedirect(reverse('individual-partners-view', args=(partner.id,)))
    else:
        form = PartnerTripAvailableDatesForm()

    return render(request, 'register-a-trip.html', {'form':form, 'user': user, 'partner': partner, 'page':page})


@csrf_protect
def TripDiscountingView(request, trip_id):
    user = request.user
    page = PageContents.objects.get(id = 46)
    the_trip = TripAvailableDates.objects.filter(id = trip_id) 
    trip = TripAvailableDates.objects.get(id = trip_id)
    partner = trip.partner_concerned
    trip_owner = partner.created_by
    if request.method == 'POST':
        form = TripDiscountForm(request.POST)
        if form.is_valid():
            discount = form.save(commit = False)
            discount.product = trip
            discount.created_by = partner
            discount.save()
            the_trip.update(is_discounted = True)

            return HttpResponseRedirect(reverse('individual-partners-view', args=(partner.id,)))
    else:
        form = TripDiscountForm()
    return render(request, 'trip_discount.html', {'form':form, 'trip_owner':trip_owner, 'page':page, 'user':user, 'trip':trip,})

@csrf_protect
def TripDiscountUpdateView(request, discount_id):
    discount = TripDiscount.objects.filter(id = discount_id)
    the_discount = TripDiscount.objects.get(id = discount_id)
    trip = the_discount.product
    partner = the_discount.created_by
    page = PageContents.objects.get(id = 42)
    user = request.user
    trip_owner = partner.created_by
#    trip_partber = trip.partner_concerned
    if request.method == 'POST':
        form = TripDiscountUpdateForm(request.POST)
        if form.is_valid():
            ammount_in_percentage_data = request.POST['ammount_in_percentage']

            discount.update(ammount_in_percentage = ammount_in_percentage_data)

            return HttpResponseRedirect(reverse('individual-partners-view', args=(partner.id,)))
    else:
        form = TripDiscountUpdateForm()

    return render(request, 'trip-discount-update.html', {'form':form, 'trip_owner':trip_owner, 'the_discount':the_discount, 'trip':trip, 'page':page, 'user':user})

def TripDiscountDelete(request, discount_id):
    user = request.user
    discount = TripDiscount.objects.get(id = discount_id)
    trip = discount.product
    trip_id = trip.id
    the_trip = TripAvailableDates.objects.filter(id = trip_id)
    partner = trip.partner_concerned
    if user.id == partner.created_by.id:
        discount.delete()
        the_trip.update(is_discounted = False)

    return HttpResponseRedirect(reverse('individual-partners-view', args=(partner.id,)))


def DiscountDatePassed(request):
    trips = TripAvailableDates.objects.all()
    discount = TripDiscount.objects.all()
    for discount in discount:
        end_disct = discount.end_discount()
        if end_disct == True:
            discount.delete()
#        if discount.
#    for trips in trips:
#        if trips.




@csrf_protect
def PartnerFeedbackForm(request, partner_id):
    user = request.user.id
    partner = PartnersModel.objects.get(id = partner_id)
    if request.method == 'POST':
        form = FeedsForm(request.POST)
        if form.is_valid():
            feeds = form.save(commit = False)
            feeds.partner = partner
            feeds.feed_posted_on = timezone.now()
            feeds.feed_body = request.POST['feed_body']
            feeds.posted_by = request.POST['posted_by']
            feeds.visit_date = request.POST['visit_date']
            feeds.save()
            if partner.votes.exists(user):
                pass
            else:
                partner.votes.up(user)
            ammount = partner.votes.count()
            partner.company_review = ammount
            partner.save()

    return render (request, 'individual-partner.html', {'form': form})


    user = request.user.id
    person = request.user
    partner = PartnersModel.objects.get(id = partner_id)
    if person.is_authenticated:
        if partner.votes.exists(user):
            pass
#        partner.votes.down(user)
        else:
            partner.votes.up(user)
    else:
        return HttpResponseRedirect('/login')
    ammount = partner.votes.count()
    partner.company_review = ammount

def ContactUsForm(request):
    if request.method == 'POST':
        email = request.POST['email']
        message = request.POST['message']
        subject = "New Email"
        from_email = email
        message = [message]
        send_mail(subject,from_email, message, [from_email , 'safarijointcontact@gmail.com'], fail_silently = True)
    return render(request, 'contact.html')

@csrf_protect
def PartnerBookings(request, partner_id):
    page = PageContents.objects.get(id = 45)
    user = request.user
    partner = PartnersModel.objects.get(id = partner_id)
    trip_bookings = partner.tripbooking_set.all().order_by('-day_of_booking')
    room_bookings = partner.accomodationbookingmodel_set.all().order_by('-reservation_placed_on')
    form = BookingsSearchForm()
    return render(request, 'partner-bookings.html', {'form':form, 'page':page, 'user':user, 'partner':partner, 'trip_bookings': trip_bookings, 'room_bookings': room_bookings})



def TripBookingsSearches(request, partner_id):
    partner = PartnersModel.objects.get(id = partner_id)
    partners_id = partner.id
    if request.method == 'POST':
        serial_number = request.POST.get('serial_number')
        name = request.POST.get('name')
        booking_date = request.POST.get('booking_date')
    else:
        serial_number = ''
        name = ''
        booking_date = ''

    bookings = TripBooking.objects.filter(trip_owner_partner__id__contains = partners_id, receipt_serial__contains = serial_number, full_name__contains = name,day_of_booking__contains = booking_date)

    acc_booking = AccomodationBookingModel.objects.filter(room_owner_partner__id__contains = partners_id, receipt_serial__contains = serial_number, your_name__contains = name, reservation_placed_on__contains = booking_date)


    return render(request, 'search/booking-search-results.html', {'bookings':bookings, 'acc_booking': acc_booking})


@csrf_protect
def AccomodationDiscountingView(request, room_id):
    user = request.user
    page = PageContents.objects.get(id = 46)
    the_room = AvailableAccomodation.objects.filter(id = room_id) 
    room = AvailableAccomodation.objects.get(id = room_id)
    partner = room.owner_company
    room_owner = partner.created_by
    if request.method == 'POST':
        form = AccomodatiomDiscountForm(request.POST)
        if form.is_valid():
            discount = form.save(commit = False)
            discount.product = room
            discount.created_by = partner
            discount.save()
            the_room.update(is_discounted = True)

            return HttpResponseRedirect(reverse('individual-partners-view', args=(partner.id,)))
    else:
        form = AccomodatiomDiscountForm()
    return render(request, 'trip_discount.html', {'form':form, 'page':page, 'room_owner': room_owner, 'user':user, 'room':room,})

def AccomodationDiscountUpdateView(request, discount_id):
    discount = AccomodationDiscount.objects.filter(id = discount_id)
    the_discount = AccomodationDiscount.objects.get(id = discount_id)
    room = the_discount.product
    partner = the_discount.created_by
    room_owner = partner.created_by
    page = PageContents.objects.get(id = 47)
    user = request.user
#    trip_partber = trip.partner_concerned
    if request.method == 'POST':
        form = AccomodationDiscountUpdateForm(request.POST)
        if form.is_valid():
            ammount_in_percentage_data = request.POST['ammount_in_percentage']
            discount.update(ammount_in_percentage = ammount_in_percentage_data)
            return HttpResponseRedirect(reverse('individual-partners-view', args=(partner.id,)))
    else:
        form = AccomodationDiscountUpdateForm()
    return render(request, 'trip-discount-update.html', {'form':form, 'the_discount':the_discount, 'room_owner':room_owner, 'room':room, 'page':page, 'user':user})

def AccomodationDiscountDelete(request, discount_id):
    user = request.user
    discount = AccomodationDiscount.objects.get(id = discount_id)
    room = discount.product
    room_id = room.id
    the_room = AvailableAccomodation.objects.filter(id = room_id)
    partner = room.owner_company
    if user.id == partner.created_by.id:
        discount.delete()
        the_room.update(is_discounted = False)
    return HttpResponseRedirect(reverse('individual-partners-view', args=(partner.id,)))

#class TripItenerarySuggestionForm(SessionWizardView):
#    template_name = 'iteneary-form.html'
#    instance = TripItenerary()

#    def dispatch(self, request, id, *args, **kwargs):
#        self.instance = TripIdentificationTag.objects.get(id=id)
#        return super(TripItenerarySuggestionForm, self).dispatch(request, *args, **kwargs)

    #def get_form_instance( self, step ):
     #   return self.instance

    #def done(self, form_list, **kwargs):
     #   form_data = process_form_data(form_list)

   # def done( self, form_list, id, **kwargs ):
    #    self.instance.save()
        #return HttpResponseRedirect(reverse(thanks))
     #   return HttpResponseRedirect('/home')

#    def done(self, form_list, **kwargs): 
#        form_data = process_form_data(form_list)
        #new = TripItenerary()
        #for form in form_list:
         #   new = construct_instance(form, new, form._meta.fields,   form._meta.exclude)
          #  new.save()
#        HttpResponseRedirect('/home/')

#def process_form_data(form_list):
#    form_data = [form.cleaned_data for form in form_list]
#    heading_one = form_data[0]
#    content_one = form_data[1]
#    heading_two = form_data[2]
#    content_two = form_data[3]
#    heading_three = form_data[4]
#    content_three = form_data[5]
#    heading_four = form_data[6]
#    content_four = form_data[7]
#    heading_five = form_data[8]
#    content_five = form_data[9]
#    heading_six = form_data[10]
#    content_six = form_data[11]
#    heading_seven = form_data[12]
#    content_seven = form_data[13]
#    heading_eight = form_data[14]
#    content_eight = form_data[15]
#    heading_nine = form_data[16]
#    content_nine = form_data[17]
#    heading_ten = form_data[18]
#    content_ten = form_data[19]

    #if form_data.is_valid():
     #   form_data.save()
#    TripItenerary.objects.create(heading_one = heading_one, content_one = content_one, 
#        heading_two = heading_two, content_two = content_two, heading_three = heading_three, 
#        content_three = content_three, heading_four = heading_four, content_four = content_four, 
#        heading_five = heading_five,content_five = content_five , heading_six = heading_six, 
#        content_six = content_six, heading_seven = heading_seven, content_seven = content_seven,
#        heading_eight = heading_eight, content_eight = content_eight, heading_nine = heading_nine,
#        heading_ten = heading_ten, content_ten = content_ten)

#    return form_data
#
#
#def TripItenerarySuggestionForm(request, tag_id):
#    user = request.user
 #   page = PageContents.objects.get(id = 43)
    #partner = user.partnersmodel_set.all()
    #for partner in partner:
     #   return partner

#    tag = TripIdentificationTag.objects.get(id = tag_id)
#    if request.method == 'POST':
#        form = IteneraryForm(request.POST)
#        if form.is_valid():
#            tag = form.save(commit = False)
#            tag.trip_tag = tag
#            tag.user = user
      #      tag.partner = partner
#            tag.save()
#        return HttpResponseRedirect('/home')
#   else:
#        form = IteneraryForm()

#    return render (request, 'iteneary-form.html', {'form':form, 'user':user , 'page':page})
#