from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
#from vote.managers import VotableManager
from django.core.urlresolvers import reverse
import datetime
from time import time
import os
from django.conf import settings
from phonenumber_field.modelfields import PhoneNumberField
from django_countries.fields import CountryField
from django.utils.crypto import get_random_string
from datetime import date
from random import *
import random
from vote.managers import VotableManager
#from  image_cropping.fields import ImageCropField, ImageRatioField
from image_cropping import ImageRatioField
from django.core.exceptions import ValidationError


from django.shortcuts import get_object_or_404



def gallery_images(instance, filename):
    return "gallery_pictures/uploaded_by_%s_on_%s_file_called_%s" %(instance.user.username, str(time()).replace('.', '_'), filename)

def page_images(instance, filename):
    return "page_pictures/%s_%s" %(str(time()).replace('.', '_'), filename)

def partner_logo(instance, filename):
    return "partner_pictures/%s_%s" %(str(time()).replace('.', '_'), filename)

def cropped_images(isinstance, filename):
    return "media/cropped_images/%s_%s" %(str(time()).replace('.', '_'), filename)




class PartnersModel(models.Model):
    FIRST_TYPE = 'Tour Operator'
    SECOND_TYPE = 'Accomodation'
    NATURE =(
        (FIRST_TYPE,'Tour Operator'),
        (SECOND_TYPE,'Accomodation'),
        )
    Arusha_Region = 'Arusha Region'
    Dar_es_Salaam_Region = 'Dar es Salaam Region'
    Dodoma_Region = 'Dodoma Region'
    Geita_Region = 'Geita Region'
    Iringa_Region = 'Iringa Region'
    Kagera_Region = 'Kagera Region'
    Katavi_Region = 'Katavi Region'
    Kigoma_Region = 'Kigoma Region'
    Kilimanjaro_Region = 'Kilimanjaro Region'
    Lindi_Region = 'Lindi Region'
    Manyara_Region = 'Manyara Region'
    Mara_Region = 'Mara Region'
    Mbeya_Region = 'Mbeya Region'
    Morogoro_Region = 'Morogoro Region'
    Mtwara_Region = 'Mtwara Region'
    Mwanza_Region = 'Mwanza Region'
    Njombe_Region = 'Njombe Region'
    Pwani_Region = 'Pwani Region'
    Rukwa_Region = 'Rukwa Region'
    Ruvuma_Region = 'Ruvuma Region'
    Shinyanga_Region = 'Shinyanga Region'
    Simiyu_Region = 'Simiyu Region'
    Singida_Region = 'Singida Region'
    Tabora_Region = 'Tabora Region'
    Tanga_Region = 'Tanga Region'
    Zanzibar = 'Zanzibar'

    locations = (
            (Arusha_Region , 'Arusha Region') , (Dar_es_Salaam_Region , 'Dar es Salaam Region'),(Dodoma_Region , 'Dodoma Region'),
            (Geita_Region , 'Geita Region'), (Iringa_Region , 'Iringa Region'), (Kagera_Region , 'Kagera Region'),
            (Katavi_Region , 'Katavi Region'), (Kigoma_Region , 'Kigoma Region'), (Kilimanjaro_Region , 'Kilimanjaro Region'),
            (Lindi_Region , 'Lindi Region'), (Manyara_Region , 'Manyara Region'), (Mara_Region , 'Mara Region') ,
            (Mbeya_Region , 'Mbeya Region'), (Morogoro_Region , 'Morogoro Region') , (Mtwara_Region , 'Mtwara Region') ,
            (Mwanza_Region , 'Mwanza Region'),  (Njombe_Region , 'Njombe Region'), (Pwani_Region , 'Pwani Region') ,
            (Rukwa_Region , 'Rukwa Region'), (Ruvuma_Region,  'Ruvuma Region'),(Shinyanga_Region , 'Shinyanga Region') ,
            (Simiyu_Region , 'Simiyu Region') , (Singida_Region , 'Singida Region'),(Tabora_Region , 'Tabora Region'),
            (Tanga_Region , 'Tanga Region'),(Zanzibar , 'Zanzibar')
    )

    created_by = models.ForeignKey(User)
    company_name = models.CharField(max_length = 100)
    company_established_on = models.DateField()
    company_nature = models.CharField(max_length = 50, choices = NATURE, default = 'FIRST_TYPE')
    company_location = models.CharField(max_length = 50, choices = locations, default = 'Zanzibar')
    company_review = models.IntegerField(default = 0)
    image = models.ImageField(null = True, blank=True, upload_to = 'partner_logo')
    cropping = ImageRatioField('image', '300x300', allow_fullsize = True)
    about_company = models.CharField(max_length = 10000)
    company_website = models.URLField()
    votes = VotableManager()
    is_active = models.BooleanField(default = False)
    is_edited = models.BooleanField(default = False)
    edited_on = models.DateTimeField(null = True, blank = True)
    originally_registed_as = models.CharField(max_length = 100, null = True, blank = True)

    def get_absolute_url(self):
        return reverse('safari_joint.views.IndividualPartnersView', args=[str(self.id)])

    def company_is(self):
        return self.company_nature

    def is_accomodation(self):
        nature = self.company_nature
        if nature == 'Accomodation':
            return True
        else:
            return False


    def __unicode__(self):
        return self.company_name

class PartnerLogo(models.Model):
    partner = models.OneToOneField(PartnersModel, on_delete = models.CASCADE, blank = True, null = True)
    image = models.ImageField(null = True, blank=True, upload_to = 'partner_logo')
    cropping = ImageRatioField('image', '430x360', allow_fullsize = True)


class Paragraphs(models.Model):
    page = models.ForeignKey('PageContents')
    image = models.ImageField(upload_to = page_images, null = True, blank = True, help_text = "This is a slide picture upload a picture of size 1600*600 or 1900*750 for home page")
    heading = models.CharField(max_length = 500, null = True, blank = True,)
    sub_heading = models.CharField(max_length = 500, null = True, blank = True,)
    content = models.CharField(max_length = 90000, null = True, blank = True,)

    def __unicode__(self):
        return self.page.page_main_heding

class PageContents(models.Model):
    page_main_heding = models.CharField(max_length = 100, default = "This is a page", null = True, blank = True)
    page_head_introduction = models.CharField(max_length = 1000)
    page_main_content = models.CharField(max_length = 1000, null = True, blank = True)
    page_home_picture_one = models.ImageField(upload_to = page_images, null = True, blank = True, help_text = "This is a slide picture upload a picture of size 1600*600 or 1900*750 for home page")
    page_home_picture_two = models.ImageField(upload_to = page_images, null = True, blank = True, help_text = "This is a slide picture upload a picture of size 1600*600 or 1900*750 for home page")
    page_home_picture_three = models.ImageField(upload_to = page_images, null = True, blank = True, help_text = "This is a slide picture upload a picture of size 1600*600 or 1900*750 for home page")
    page_sub_heading_picture = models.ImageField(upload_to = page_images, null = True, blank = True, help_text = "This is an ordinary page picture upload a picture of size 550*480 or 560*209 for home page")
    page_sub_heading_picture_2 = models.ImageField(upload_to = page_images, null = True, blank = True, help_text = "This is an ordinary page picture upload a picture of size 550*480 or 560*209 for home page")
    page_sub_heading_one = models.CharField(max_length = 100, null = True, blank = True)
    sub_heading_content_one = models.CharField(max_length = 1000, null = True, blank = True)
    page_sub_heading_two = models.CharField(max_length = 100, null = True, blank = True)
    sub_heading_content_two = models.CharField(max_length = 1000, null = True, blank = True)

    def __unicode__(self):
        return self.page_main_heding

class TripIteneraryChart(models.Model):
    chart_heading = models.CharField(max_length = 10)
    trip = models.ForeignKey('PageContents', null = True, blank = True)
    chart_day = models.IntegerField()
    chart_start_at = models.CharField(max_length = 100)
    chart_start_attitude_meter = models.IntegerField()
    chart_finish_at = models.CharField(max_length = 100)
    chart_finish_attitude_meter = models.IntegerField()
    chart_minimum_time = models.IntegerField()
    chart_maximum_time = models.IntegerField()
    chart_distance_kilometer = models.IntegerField()

    def start_meter_to_feet_converter(self):
        attitude_in_meter = self.chart_start_attitude_meter

        if attitude_in_meter:
            attitude_in_feets = float(attitude_in_meter * 3.28084)

        return attitude_in_feets

    def finish_meter_to_feet_converter(self):
        attitude_in_meter = self.chart_finish_attitude_meter

        if attitude_in_meter:
            finish_attitude_in_feets = float(attitude_in_meter * 3.28084)

        return finish_attitude_in_feets


    def kilometer_to_miles_converter(self):
        distance_in_kilometers = self.chart_distance_kilometer

        if distance_in_kilometers:
            distance_in_miles = float(distance_in_kilometers * 0.621371)

        return distance_in_miles

    def __unicode__(self):
        return self.chart_heading


class TripItenerary(models.Model):
    trip_tag = models.ForeignKey('TripIdentificationTag', null = True, blank = True,)
    user = models.ForeignKey(User, null = True, blank = True,)
#    partner = models.ForeignKey('PartnersModel', null = True, blank = True,)
    heading = models.CharField(max_length = 10, null = True, blank = True)
    content = models.CharField(max_length = 1000, null = True, blank = True)
#    heading_two = models.CharField(max_length = 10, null = True, blank = True)
#    content_two = models.CharField(max_length = 1000, null = True, blank = True)
#    heading_three = models.CharField(max_length = 10, null = True, blank = True)
#    content_three = models.CharField(max_length = 1000, null = True, blank = True)
#    heading_four = models.CharField(max_length = 10, null = True, blank = True)
#    content_four = models.CharField(max_length = 1000, null = True, blank = True)
#    heading_five = models.CharField(max_length = 10, null = True, blank = True)
#    content_five = models.CharField(max_length = 1000, null = True, blank = True)
#    heading_six = models.CharField(max_length = 10, null = True, blank = True)
#    content_six = models.CharField(max_length = 1000, null = True, blank = True)
#    heading_seven = models.CharField(max_length = 10, null = True, blank = True)
#    content_seven = models.CharField(max_length = 1000, null = True, blank = True)
#    heading_eight = models.CharField(max_length = 10, null = True, blank = True)
#    content_eight = models.CharField(max_length = 1000, null = True, blank = True)
#    heading_nine = models.CharField(max_length = 10, null = True, blank = True)
#    content_nine = models.CharField(max_length = 1000, null = True, blank = True)
#    heading_ten = models.CharField(max_length = 10, null = True, blank = True)
#    content_ten = models.CharField(max_length = 1000, null = True, blank = True)


    #def __unicode__(self):
     #   return self.trip_tag.heading_one


class TeamModel(models.Model):
    team_heading = models.CharField(max_length = 100)
    team_image_one = models.ImageField(upload_to = page_images, null = True, blank = True, help_text = "This is a slide picture upload a picture of size 250*190 or icon of size 78*78")
    team_heading_one = models.CharField(max_length = 100, null = True, blank = True)
    team_content_one = models.CharField(max_length = 1000, null = True, blank = True)
    team_url_one = models.CharField(max_length = 100, null = True, blank = True)
    team_image_two = models.ImageField(upload_to = page_images, null = True, blank = True, help_text = "This is a slide picture upload a picture of size 250*190 or icon of size 78*78")
    team_heading_two = models.CharField(max_length = 100, null = True, blank = True)
    team_content_two = models.CharField(max_length = 1000, null = True, blank = True)
    team_url_two = models.CharField(max_length = 100, null = True, blank = True)
    team_image_three = models.ImageField(upload_to = page_images, null = True, blank = True, help_text = "This is a slide picture upload a picture of size 250*190 or icon of size 78*78")
    team_heading_three = models.CharField(max_length = 100, null = True, blank = True)
    team_content_three = models.CharField(max_length = 1000, null = True, blank = True)
    team_url_three = models.CharField(max_length = 100, null = True, blank = True)
    team_image_four = models.ImageField(upload_to = page_images, null = True, blank = True, help_text = "This is a slide picture upload a picture of size 250*190 or icon of size 78*78")
    team_heading_four = models.CharField(max_length = 100, null = True, blank = True)
    team_content_four = models.CharField(max_length = 1000, null = True, blank = True)
    team_url_four = models.CharField(max_length = 100, null = True, blank = True)

    def __unicode__(self):
        return self.team_heading

def get_random_chars():
    time = timezone.now()
    serial_chars = get_random_string( length = 2, allowed_chars = 'TZA123456789BCDEFGHIJKLMNOPQRSTUVWXYZ' )
    serial_chars_3 = get_random_string( length = 2, allowed_chars = '789BCDEFGHIJKLMNTZA123456OPQRSTUVWXYZ' )
    seconds =str(time.minute+time.second*time.microsecond)
    ultimate_chars = serial_chars+seconds+serial_chars_3
    return ultimate_chars

class TripAvailableDates(models.Model):

    Arusha_Region = 'Arusha Region'
    Dar_es_Salaam_Region = 'Dar es Salaam Region'
    Dodoma_Region = 'Dodoma Region'
    Geita_Region = 'Geita Region'
    Iringa_Region = 'Iringa Region'
    Kagera_Region = 'Kagera Region'
    Katavi_Region = 'Katavi Region'
    Kigoma_Region = 'Kigoma Region'
    Kilimanjaro_Region = 'Kilimanjaro Region'
    Lindi_Region = 'Lindi Region'
    Manyara_Region = 'Manyara Region'
    Mara_Region = 'Mara Region'
    Mbeya_Region = 'Mbeya Region'
    Morogoro_Region = 'Morogoro Region'
    Mtwara_Region = 'Mtwara Region'
    Mwanza_Region = 'Mwanza Region'
    Njombe_Region = 'Njombe Region'
    Pwani_Region = 'Pwani Region'
    Rukwa_Region = 'Rukwa Region'
    Ruvuma_Region = 'Ruvuma Region'
    Shinyanga_Region = 'Shinyanga Region'
    Simiyu_Region = 'Simiyu Region'
    Singida_Region = 'Singida Region'
    Tabora_Region = 'Tabora Region'
    Tanga_Region = 'Tanga Region'
    Zanzibar = 'Zanzibar'

    locations = (
            (Arusha_Region , 'Arusha Region') , (Dar_es_Salaam_Region , 'Dar es Salaam Region'),(Dodoma_Region , 'Dodoma Region'),
            (Geita_Region , 'Geita Region'), (Iringa_Region , 'Iringa Region'), (Kagera_Region , 'Kagera Region'),
            (Katavi_Region , 'Katavi Region'), (Kigoma_Region , 'Kigoma Region'), (Kilimanjaro_Region , 'Kilimanjaro Region'),
            (Lindi_Region , 'Lindi Region'), (Manyara_Region , 'Manyara Region'), (Mara_Region , 'Mara Region') ,
            (Mbeya_Region , 'Mbeya Region'), (Morogoro_Region , 'Morogoro Region') , (Mtwara_Region , 'Mtwara Region') ,
            (Mwanza_Region , 'Mwanza Region'),  (Njombe_Region , 'Njombe Region'), (Pwani_Region , 'Pwani Region') ,
            (Rukwa_Region , 'Rukwa Region'), (Ruvuma_Region,  'Ruvuma Region'),(Shinyanga_Region , 'Shinyanga Region') ,
            (Simiyu_Region , 'Simiyu Region') , (Singida_Region , 'Singida Region'),(Tabora_Region , 'Tabora Region'),
            (Tanga_Region , 'Tanga Region'),(Zanzibar , 'Zanzibar')
    )

#image = models.ImageField(null = True, blank=True, upload_to = 'cropped_images')
#    cropping = ImageRatioField('image', '430x360', allow_fullsize = True)


    trip_name = models.CharField(max_length = 100)
    user = models.ForeignKey(User, null = True, blank = True)
    trip_picture = models.ImageField(null = True, blank=True, upload_to = 'trip_images')
    cropping = ImageRatioField('trip_picture', '430x360', allow_fullsize = True)
    created_on = models.DateTimeField(auto_now_add = True, null = True, blank = True)
    trip_serial = models.CharField(default = get_random_chars, unique=True,  max_length = 20, null = True, blank = True, help_text = 'Do not Edit the value of this Field Unless it Brings Errors!')
    partner_concerned = models.ForeignKey('PartnersModel', null = True, blank = True)
    trip_tag = models.ForeignKey('TripIdentificationTag', null = True, blank = True)
    depature_date = models.DateField(null = True, blank = True)
    returning_date = models.DateField(null = True, blank = True)
    trip_price = models.IntegerField(null = True, blank = True)
    trip_location = models.CharField(max_length = 50, choices = locations, default = 'Zanzibar')
    about_trip = models.CharField(max_length = 3000, null = True, blank = True)
    is_udated = models.BooleanField(default = False)
    trip_updated_on = models.DateTimeField(null = True, blank = True)
    trip_original_name = models.CharField(max_length = 100, null = True, blank = True)
    trip_original_price = models.IntegerField(null = True, blank = True)
    is_discounted = models.BooleanField(default = False)

    def days_sepent(self):
        first_day = self.depature_date
        last_day = self.returning_date
        remaining_seconds = (last_day - first_day).total_seconds()
        remaining_days = remaining_seconds / 86400
        if int(remaining_days) <= 9:
            return int(remaining_days)
        else:
            return int(remaining_days)

    def is_one_day(self):
        first_day = self.depature_date
        last_day = self.returning_date
        difference = last_day - first_day 
        remaining_seconds = difference.total_seconds()
        remaining_days = remaining_seconds / 86400
        remaining_days_integer = int(remaining_days)
        if remaining_days_integer <= 1:
            return True
        else:
            return False

    def is_this_month(self):
        to_get_month = self.depature_date
        month = to_get_month.strftime('%B')
        today = timezone.now()
        this_month = today.strftime('%B')
        if month == this_month:
            return True
        return False

    def is_today(self):
        today = timezone.now()
        today_date = today.strftime('%d')
        depature = self.depature_date
        depature_date = depature.strftime('%d')
        if today_date == depature_date:
            return True
        else:
            return False


    def trip_month(self):
        to_get_month = self.depature_date
        month = to_get_month.strftime('%B')
        return month

    def this_month(self):
        today = timezone.now()
        this_month = today.strftime('%B')
        return this_month

    def is_past_due(self):
        today = date.today()
        depature = self.depature_date
        if depature > today:
            return True
        elif depature < today:
            return False

    def __unicode__(self):
        return str(self.trip_serial +" "+ self.trip_name)

class TripDiscount(models.Model):
    starting_date = models.DateField()
    ending_date = models.DateField()
    ammount_in_percentage = models.FloatField()
    created_on = models.DateTimeField(auto_now_add = True)
    created_by = models.ForeignKey('PartnersModel')
    product = models.OneToOneField('TripAvailableDates')
    
    from django import forms
    def discount_dates(self):
        starting_date_data = self.ending_date
        product_depature = self.product.depature_date
        if starting_date_data <= product_depature:
            raise forms.ValidationError("Hey this offer can not be Valid untill the trip has departed.")


    def ammount_saved(self):
        percentage = self.ammount_in_percentage
        trip_price = self.product.trip_price
        trip_price_val = float(trip_price)
        percentage_val = float(percentage)
        decimal_percentage = float(percentage_val/100)
        ammount_saved = decimal_percentage * trip_price_val
        return int(ammount_saved)

    def ammount_remaining(self):
        today_date = date.today()
        starting_date = self.starting_date
        percentage = self.ammount_in_percentage
        trip_price = self.product.trip_price
        trip_price_val = float(trip_price)
        percentage_val = float(percentage)
        decimal_percentage = float(percentage_val/100)
        ammount_saved = decimal_percentage * trip_price_val
        remaining_ammount = trip_price_val - ammount_saved
        if starting_date >= today_date:
            return int(remaining_ammount)
        #else:
         #   return int(trip_price)

    def begin_discount(self):
        today_date = date.today()
        starting_date = self.starting_date
        #trip_disc_field = self.product.is_discounted
        if starting_date >= today_date:
            #trip_disc_field = True
            return True

    def end_discount(self):
        today_date = date.today()
        ending_date = self.ending_date
        if today_date >= ending_date:
            return True
            self.delete()
            #return True

    def original_price(self):
        product = self.product
        product_price = product.trip_price
        if product_price:
            return product_price

    def get_discount_percentage(self):
        ammount = self.ammount_in_percentage
        if ammount:
            return int(ammount)


class TripIdentificationTag(models.Model):
    tag_created_by = models.ForeignKey(User)
    tag_name = models.CharField(max_length = 200)
    tag_created_on = models.DateTimeField(auto_now_add = True)
    tag_status = models.BooleanField(default = True)

    def __unicode__(self):
        return str(self.tag_name)


def random_booking_chars():
    time = timezone.now()
#    date = date.today()
    serial_chars = get_random_string( length = 4, allowed_chars = 'TZA123456789BCDEFGHIJKLMNOPQRSTUVWXYZ' )
    date_string =str(time.minute+time.second*time.microsecond)
    ultimate_booking_chars = serial_chars+date_string+"WNM"
    return ultimate_booking_chars



class TripBooking(models.Model):
    trip_booked = models.ForeignKey('TripAvailableDates', null = True, blank = True)
    trip_owner_partner = models.ForeignKey('PartnersModel', null = True, blank = True)
    receipt_serial = models.CharField(max_length = 30, null = True, blank = True)
    day_of_booking = models.DateTimeField(auto_now_add = True)
    full_name = models.CharField(max_length = 100)
    email_address = models.EmailField()
    phone_number = PhoneNumberField()
    your_country = CountryField()
    additional_note = models.CharField(max_length = 1000, null = True, blank = True)


class FeedsModel(models.Model):
    feed_posted_on = models.DateTimeField(auto_now_add = True)
    feed_body = models.CharField(max_length = 1000, help_text = "shortly as you can!")
    posted_by = models.CharField(max_length = 200)
    partner = models.ForeignKey('PartnersModel', null = True, blank = True)
    visit_date = models.DateField(null = True, blank = True, help_text = "When Did you visit or use the services of this company?")

    def __unicode__(self):
        return self.posted_by + " " + str(self.feed_posted_on)


class Service(models.Model):
    service_name = models.CharField(max_length = 100)
    created_on = models.DateTimeField(auto_now_add = True)
    created_by = models.ForeignKey(User)
    service_status = models.BooleanField(default = True)

    def __unicode__(self):
        return self.service_name



class AvailableAccomodation(models.Model):
    Single = 'Single'
    Double = 'Double'
    Triple = 'Triple'
    Quad = 'Quad'
    Queen = 'Queen'
    King = 'King'
    Twin = 'Twin'
    Double_double = 'Double-double'
    Studio = 'Studio'
    Mini_Suite = 'Mini-Suite'
    Suite = 'Suite'
    Connecting_rooms = 'Connecting rooms'
    Adjoining_rooms = 'Adjoining rooms'
    Adjacent_rooms = 'Adjacent rooms'

    TYPE =(
        (Single, 'Single') , (Double, 'Double'), (Triple, 'Triple'),
        (Quad, 'Quad'), (Queen, 'Queen'), (King, 'King'),(Twin, 'Twin'),
        (Double_double, 'Double-double'), (Studio, 'Studio'),
        (Mini_Suite, 'Mini-Suite'),(Suite, 'Suite'),
        (Connecting_rooms, 'Connecting rooms'), (Adjoining_rooms, 'Adjoining rooms'),
        (Adjacent_rooms, 'Adjacent rooms')
        )

    Loud = 'Loud'
    Quite = 'Quite'
    sound_proof = 'Sound Proof'
    LEVEL = (
            (Loud, 'Loud'),
            (Quite, 'Quite'),
            (sound_proof, 'Sound Proof')
    )
    owner_company = models.ForeignKey(PartnersModel)
    room_serial_number = models.CharField(default = get_random_chars, unique=True,  max_length = 20, null = True, blank = True, help_text = 'Do not Edit the value of this Field Unless it Brings Errors!')
    accomodation_type = models.CharField(max_length = 50, choices = TYPE, default = Single)
    available_space = models.IntegerField()
    created_on = models.DateTimeField(auto_now_add = True)
    price_USD = models.IntegerField(null = True, blank = True)
    room_picture = models.ImageField(null = True, blank=True, upload_to = 'room_images')
    cropping = ImageRatioField('room_picture', '430x360', allow_fullsize = True)
    noise_level = models.CharField(max_length = 50, choices = LEVEL, default = Quite)
    airport_transport = models.BooleanField(default = False)
    services = models.ManyToManyField(Service)
    user = models.ForeignKey(User, null = True, blank = True)
    is_updated = models.BooleanField(default = False)
    original_price = models.IntegerField(null = True, blank = True)
    room_updated_on = models.DateTimeField(null = True, blank = True)
    is_discounted = models.BooleanField(default = False)


    def __unicode__(self):
        return self.accomodation_type

    def availability(self):
        available_space = self.available_space
        related_bookings = self.accomodationbookingmodel_set.all()
        booking_count = related_bookings.count()
        remaining_rooms = int(available_space) - int(booking_count)
        if booking_count >= available_space:
            return False
        elif booking_count < available_space:
            return True

    def booking_count(self):
        available_space = self.available_space
        related_bookings = self.accomodationbookingmodel_set.all()
        booking_count = related_bookings.count()
        return booking_count

    def available_date(self):
        available_space = self.available_space
        related_bookings = self.accomodationbookingmodel_set.all().order_by('depature_date')
        booking_count = related_bookings.count()
        for related_bookings in related_bookings:
            return related_bookings.depature_date

    def available_on(self):
        available_space = self.available_space
        related_bookings = self.accomodationbookingmodel_set.all().order_by('depature_date')
        booking_count = related_bookings.count()
        remaining_rooms = int(available_space) - int(booking_count)
        if booking_count >= available_space:
            available =  False
        else:
            available = True
        for related_bookings in related_bookings:
            if available == False:
                return "Will Be Available From: " + str(related_bookings.depature_date)


class AccomodationDiscount(models.Model):
    starting_date = models.DateField()
    ending_date = models.DateField()
    ammount_in_percentage = models.FloatField()
    created_on = models.DateTimeField(auto_now_add = True)
    created_by = models.ForeignKey('PartnersModel')
    product = models.OneToOneField('AvailableAccomodation')
    

    def ammount_saved(self):
        percentage = self.ammount_in_percentage
        price_USD = self.product.price_USD
        trip_price_val = float(price_USD)
        percentage_val = float(percentage)
        decimal_percentage = float(percentage_val/100)
        ammount_saved = decimal_percentage * trip_price_val
        return int(ammount_saved)

    def ammount_remaining(self):
        today_date = date.today()
        starting_date = self.starting_date
        percentage = self.ammount_in_percentage
        price_USD = self.product.price_USD
        trip_price_val = float(price_USD)
        percentage_val = float(percentage)
        decimal_percentage = float(percentage_val/100)
        ammount_saved = decimal_percentage * trip_price_val
        remaining_ammount = trip_price_val - ammount_saved
        if starting_date >= today_date:
            return int(remaining_ammount)
        #else:
         #   return int(trip_price)

    def begin_discount(self):
        today_date = date.today()
        starting_date = self.starting_date
        #trip_disc_field = self.product.is_discounted
        if starting_date == today_date:
            #trip_disc_field = True
            return True

    def end_discount(self):
        today_date = date.today()
        ending_date = self.ending_date
        if today_date == ending_date:
            self.delete()
            #return True

    def original_price(self):
        product = self.product
        product_price = product.price_USD
        if product_price:
            return product_price

    def get_discount_percentage(self):
        ammount = self.ammount_in_percentage
        if ammount:
            return int(ammount)



class AccomodationBookingModel(models.Model):
    room_booked = models.ForeignKey(AvailableAccomodation)
    room_owner_partner = models.ForeignKey('PartnersModel', null = True, blank = True)
    receipt_serial = models.CharField(max_length = 30, null = True, blank = True)
    reservation_placed_on = models.DateTimeField(auto_now_add = True, null = True, blank = True)
    arrival_date = models.DateField(null = True, blank = True)
    depature_date = models.DateField(null = True, blank = True)
    your_name = models.CharField(max_length = 100, null = True, blank = True)
    email_address = models.EmailField(null = True, blank = True)
    phone_number = PhoneNumberField(null = True, blank = True)
    country = CountryField(null = True, blank = True)

    def __unicode__(self):
        return self.your_name

#    def clean(self):
#        room_booked = self.instance.room_booked
#        room_booked_id = room_booked.id

#        any_room = AvailableAccomodation.objects.get(id = room_booked_id)
#        room_status = any_room.availability()
#        today_date = date.today()
#        if room_status == False:
#            raise ValidationError(
#                    "Room Fully Booked"
#                )


class PartnerGalleryPicture(models.Model):
    uploaded_by = models.ForeignKey(User)
    uploaded_on = models.DateTimeField(auto_now_add = True, null = True, blank = True)
    partner = models.ForeignKey(PartnersModel)
    picture = models.ImageField(upload_to = partner_logo)


class FAQS(models.Model):
    head = models.CharField(max_length = 100)
    body = models.CharField(max_length = 1000)

    def __unicode__(self):
        return self.head

class FunPictures(models.Model):
    image = models.ImageField(null = True, blank=True, upload_to = 'cropped_images')
    cropping = ImageRatioField('image', '430x360', allow_fullsize = True)
