from django import forms
from django.forms import extras
import re
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.forms import UserCreationForm
from time import time
from safari_joint.models import *
from django_countries.widgets import CountrySelectWidget
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.forms import PasswordResetForm
from image_cropping.widgets import ImageCropWidget
from datetime import date


class UserRegistrationForm(UserCreationForm):
    email = forms.CharField(widget = forms.EmailInput(attrs={'placeholder': 'email Address'}), required=True,)
    username = forms.CharField(widget = forms.TextInput(attrs={'placeholder': 'username'}), required=True,)
    first_name = forms.CharField(widget = forms.TextInput(attrs={'placeholder': 'First Name'}), required=True,)
    last_name = forms.CharField(widget = forms.TextInput(attrs={'placeholder': 'Last Name'}), required=True,)
    password1 = forms.CharField(widget = forms.PasswordInput(attrs={'placeholder': 'Password'}), required=True,)
    password2 = forms.CharField(widget = forms.PasswordInput(attrs={'placeholder': 'Comfirm Password'}), required=True,)

    class Meta:
        model = User
        fields = ('email', 'username', 'first_name', 'last_name', 'password1', 'password2')

    def save(self, commit = True):
        user = super(UserRegistrationForm, self).save(commit = False)
        user.email = self.cleaned_data['email']
        user.username = self.cleaned_data['username']
        user.first_name = self.cleaned_data['first_name']
        user.password1 = self.cleaned_data['password1']
        user.last_name = self.cleaned_data['last_name']
        user.password2 = self.cleaned_data['password2']

        if commit:
            user.save()

        return user

    def clean_username(self):
        cleaned_data = super(UserRegistrationForm, self).clean()
        username = self.cleaned_data['username']
        if not re.search(r'^\w+$', username):
            raise forms.ValidationError('username can only contain alphanumeric characters and underscores')
        try:
            User.objects.get(username=username)
        except ObjectDoesNotExist:
            return username
        raise forms.ValidationError('username is already taken')

    def clean_email(self):
        cleaned_data = super(UserRegistrationForm, self).clean()
        email = self.cleaned_data['email']
        try:
            User.objects.get(email=email)
        except ObjectDoesNotExist:
            return email
        raise forms.ValidationError('The Email you Entered Has been Used Already')


    def clean(self):
        cleaned_data = super(UserRegistrationForm, self).clean()
        first_password = cleaned_data.get("password1")
        second_password = cleaned_data.get("password2")
        username = cleaned_data.get("username")

        if first_password and second_password:
            # Only do something if both fields are valid so far.
            if first_password != second_password:
                raise forms.ValidationError(
                    "The Two Passwords Entered Didn't Match, Try Again"
                )

            return cleaned_data




class TripBookingForm(forms.ModelForm):
    comfirm_email = forms.EmailField(required=True, help_text = "Please enter same email as above to comfirm")
    additional_note = forms.CharField(widget=forms.Textarea, required=False)
    class Meta:
        model = TripBooking
        fields = ('trip_booked', 'full_name', 'email_address', 'comfirm_email', 'phone_number', 'your_country', 'additional_note')
        exclude = ['trip_booked']
        widgets = {'country': CountrySelectWidget()}

    def clean(self):
        cleaned_data = super(TripBookingForm, self).clean()
        first_email = cleaned_data.get("email_address")
        email_comfirmation = cleaned_data.get("comfirm_email")

        if first_email and email_comfirmation:
            # Only do something if both fields are valid so far.
            if first_email != email_comfirmation:
                raise forms.ValidationError(
                    "The Two Emails Entered Didn't Match, Try Again"
                )

            return cleaned_data

class FeedsForm(forms.ModelForm):
    feed_body = forms.CharField(widget=forms.Textarea, required=True)
    visit_date = forms.DateField(help_text = "When Did you visit or use the services of this company?")
    class Meta:
        model = FeedsModel
        fields = ('visit_date', 'feed_body' , 'posted_by')
        exclude = ['feed_posted_on', 'partner']

#    def clean_visit_date(self):

class PartnersForm(forms.ModelForm):
    about_company = forms.CharField(widget=forms.Textarea, required=True)
    company_established_on = forms.DateField(widget = extras.SelectDateWidget(years=range(1969,2016)))
    class Meta:
        model = PartnersModel
        fields = ('created_by', 'company_name', 'company_location', 'company_established_on', 'company_nature', 'company_review', 'image', 'cropping', 'about_company', 'company_website')
        exclude = ['created_by', 'company_review']

    def clean_company_name(self):
        cleaned_data = super(PartnersForm, self).clean()
        company_name = self.cleaned_data['company_name']
#        if not re.search(r'^\w+$', company_name):
#            raise forms.ValidationError('Company name can only contain alphanumeric characters and underscores')
        try:
            PartnersModel.objects.get(company_name = company_name)
        except ObjectDoesNotExist:
            return company_name
        raise forms.ValidationError('A company with this name alredy exist in our system.')


class PartnerGalleryPictureForm(forms.ModelForm):
    class Meta:
        model = PartnerGalleryPicture
        fields = ('uploaded_by', 'partner' , 'picture')
        exclude = ['uploaded_by', 'partner']


class PassworResetForm(PasswordResetForm):
    error_messages = {
        'unknown': ("That email address doesn't have an associated "
                     "user account. Are you sure you've registered?"),
        'unusable': ("The user account associated with this email "
                      "address cannot reset the password."),
        }
    def clean_email(self):
        """
        Validates that an active user exists with the given email address.
        """
        UserModel = get_user_model()
        email = self.cleaned_data["email"]
        self.users_cache = UserModel._default_manager.filter(email__iexact=email)
        if not User.objects.filter(email__iexact = email, is_active = True).exists():
            raise forms.ValidationError("That email address doesn't is associated with any user account in our system. Are you sure you've registered?")
        if not any(user.is_active for user in self.users_cache):
            # none of the filtered users are active
            raise forms.ValidationError("That email address doesn't is associated with any user account in our system. Are you sure you've registered?")
        if any((user.password == UNUSABLE_PASSWORD)
            for user in self.users_cache):
            raise forms.ValidationError("The user account associated with this email address cannot reset the password.")
        return email

    def save(self, domain_override=None,
             subject_template_name='registration/password_reset_subject.txt',
             email_template_name='registration/password_reset_email.html',
             use_https=False, token_generator=default_token_generator,
             from_email=None, request=None):

        from django.core.mail import send_mail

        for user in self.users_cache:
            if not domain_override:
                current_site = get_current_site(request)
                site_name = current_site.name
                domain = current_site.domain
            else:
                site_name = domain = domain_override
            c = {
                'email': user.email,
                'domain': domain,
                'site_name': site_name,
                'uid': int_to_base36(user.pk),
                'user': user,
                'token': token_generator.make_token(user),
                'protocol': use_https and 'https' or 'http',
                }
            subject = loader.render_to_string(subject_template_name, c)
            subject = ''.join(subject.splitlines())
            email = loader.render_to_string(email_template_name, c)
            send_mail(subject, email, from_email, [user.email])



class PartnerTripAvailableDatesForm(forms.ModelForm):
    depature_date = forms.DateField(help_text = 'mm/dd/yyyy')
    returning_date = forms.DateField(help_text = 'mm/dd/yyyy')
    about_trip = forms.CharField(widget=forms.Textarea, required=False)
    trip_price = forms.IntegerField(widget = forms.NumberInput(attrs = {'placeholder': "Trip Price in US Dollars before Tax"}))

    class Meta:
        model = TripAvailableDates
        fields = ('trip_name' , 'trip_serial', 'partner_concerned', 'depature_date', 'returning_date', 'trip_location', 'trip_price', 'trip_tag', 'about_trip' ,  'user', 'trip_picture')
        exclude = ['trip_serial', 'partner_concerned', 'user', 'created_on']

    def clean(self):
        cleaned_data = super(PartnerTripAvailableDatesForm, self).clean()
        clean_depature = self.cleaned_data.get('depature_date')
        depature_date_date = self.cleaned_data['depature_date'] 
        clean_return = self.cleaned_data.get('returning_date')
        returning_date_date = self.cleaned_data['returning_date']
        #if clean_depature and clean_return:
        if clean_return < clean_depature:
            raise forms.ValidationError(
                    ('**Sorry Returning date provided can not be smaller than the depature date')
                )
        return cleaned_data
        #return depature_date_date and returning_date_date
        #return self.cleaned_data['depature_date'] and self.cleaned_data['returning_date']

class AvailableAccomodationForm(forms.ModelForm):
    price_USD = forms.IntegerField(widget = forms.NumberInput(attrs = {'placeholder': "Room Price in US Dollars before Tax"}))
    available_space = forms.IntegerField(widget = forms.NumberInput(attrs={'placeholder': 'Available Number of Rooms for the choice above'}))
    class Meta:
        model = AvailableAccomodation
        fields = ('owner_company', 'accomodation_type', 'available_space', 'airport_transport', 'services', 'noise_level', 'price_USD', 'room_picture')
        exclude = ['owner_company']
        help_texts = {
            'services': "Hold Ctrl key in Windows or Command key in Mac and select multiple choices",
            'airport_transport': "Do you offer transport from the Airport?"
                      }
        placeholders = {'available_space': 'Available Rooms'}

class AccomodationBookingForm(forms.ModelForm):
    arrival_date = forms.DateField(help_text = 'mm/dd/yyyy')
    depature_date = forms.DateField(help_text = 'mm/dd/yyyy')
    comfirm_email_address = forms.EmailField()
    class Meta:
        model = AccomodationBookingModel
        fields = ('room_booked', 'arrival_date', 'depature_date', 'your_name', 'email_address', 'comfirm_email_address', 'phone_number', 'country')
        exclude = ['room_booked']
        widgets = {'country': CountrySelectWidget()}

    def clean(self):
        cleaned_data = super(AccomodationBookingForm, self).clean()
        first_email = cleaned_data.get("email_address")
        email_comfirmation = cleaned_data.get("comfirm_email_address")
        if first_email and email_comfirmation:
            # Only do something if both fields are valid so far.
            if first_email != email_comfirmation:
                raise forms.ValidationError(
                    "The Two Emails Entered Didn't Match, Try Again"
                )
            return cleaned_data

    def clean_arrival_date(self):
        cleaned_data = super(AccomodationBookingForm, self).clean()
        clean_arrival_date = cleaned_data.get("arrival_date")
        today_date = date.today()
        if clean_arrival_date and today_date:
            if clean_arrival_date < today_date:
                raise forms.ValidationError(
                    "Sorry You can not make reservation on the arrival date you provided because that day has passed, Please Try Again"
                )
        return clean_arrival_date


    def clean_depature_date(self):
        cleaned_data = super(AccomodationBookingForm, self).clean()
        clean_arrival_date = cleaned_data.get("arrival_date")
        clean_depature_date = cleaned_data.get("depature_date")
        if clean_depature_date and clean_arrival_date:
            if clean_depature_date < clean_arrival_date:
                raise forms.ValidationError(
                    "Sorry You can not leave on the date provided. Depature date can not be before the date of arrival. Please Try Again!"
                )
        return clean_depature_date

class FunPicturesForm(forms.ModelForm):
    class Meta:
        model = FunPictures
        fields = ('image','cropping')
#        widgets = {'cropping': ImageCropWidget()}

class PartnerLogoForm(forms.ModelForm):
    class Meta:
        model = PartnerLogo
        fields = ('partner', 'image', 'cropping')
        exclude = ['partner']
#        widgets = {'cropping': ImageCropWidget()}


def get_locations():
        locations = (
                ('Arusha Region' , 'Arusha Region') , ('Dar es Salaam Region' , 'Dar es Salaam Region'),('Dodoma Region' , 'Dodoma Region'),
                ('Geita Region ', 'Geita Region'), ('Iringa Region' , 'Iringa Region'), ('Kagera Region' , 'Kagera Region'),
                ('Katavi Region' , 'Katavi Region'), ('Kigoma Region' , 'Kigoma Region'), ('Kilimanjaro Region' , 'Kilimanjaro Region'),
                ('Lindi Region' , 'Lindi Region'), ('Manyara Region' , 'Manyara Region'), ('Mara Region' , 'Mara Region') ,
                ('Mbeya Region' , 'Mbeya Region'), ('Morogoro Region' , 'Morogoro Region') , ('Mtwara Region' , 'Mtwara Region') ,
                ('Mwanza Region' , 'Mwanza Region'),  ('Njombe Region' , 'Njombe Region'), ('Pwani Region' , 'Pwani Region') ,
                ('Rukwa Region' , 'Rukwa Region'), ('Ruvuma Region',  'Ruvuma Region'),('Shinyanga Region' , 'Shinyanga Region') ,
                ('Simiyu Region', 'Simiyu Region') , ('Singida Region' , 'Singida Region'),('Tabora Region' , 'Tabora Region'),
                ('Tanga Region', 'Tanga Region'),('Zanzibar' , 'Zanzibar')
        )
        return locations

def room_types():
    TYPE =(
            ('Single', 'Single') , ('Double', 'Double'), ('Triple', 'Triple'),
            ('Quad', 'Quad'), ('Queen', 'Queen'), ('King', 'King'),('Twin', 'Twin'),
            ('Double-double', 'Double-double'), ('Studio', 'Studio'),
            ('Mini-Suite', 'Mini-Suite'),('Suite', 'Suite'),
            ('Connecting rooms', 'Connecting rooms'), ('Adjoining rooms', 'Adjoining rooms'),
            ('Adjacent rooms', 'Adjacent rooms')
            )

    return TYPE

def noice_lovel():
    LEVEL = (
            ('Loud', 'Loud'),
            ('Quite', 'Quite'),
            ('Sound Proof', 'Sound Proof')
    )

    return LEVEL

class TripSearchForm(forms.Form):
#    trip_name = forms.CharField()
    trip_depature_date = forms.DateField(required = True)
    the_trip_tag = forms.ModelChoiceField(queryset= TripIdentificationTag.objects.all(), required = True)
#    trip_location = forms.ChoiceField(choices= get_locations())

class AccomodationSearch(forms.Form):
    destination = forms.ChoiceField(choices= get_locations(), required = True)
    room_type = forms.ChoiceField(choices= room_types())
#    include_airport_transport = forms.BooleanField(required = False)

class PartnerUpdateForm(forms.Form):
    company_name = forms.CharField(max_length = 100, required = True)
    company_established_on = forms.DateField(required = True)

    #company_established_on = forms.DateField(required = True) forms.DateField(widget=forms.TextInput(attrs={'type': 'date'}), required = True)
    company_location = forms.ChoiceField(choices= get_locations(), required = True)
    company_website = forms.URLField(required = True)
    about_company = forms.CharField(widget=forms.Textarea, required = True)

    def clean_company_name(self):
        cleaned_data = super(PartnerUpdateForm, self).clean()
        company_name = self.cleaned_data['company_name']
#        if not re.search(r'^\w+$', company_name):
#            raise forms.ValidationError('Company name can only contain alphanumeric characters and underscores')
        try:
            PartnersModel.objects.get(company_name = company_name)
        except ObjectDoesNotExist:
            return company_name
        raise forms.ValidationError('A company with this name alredy exist in our system.')

class TripUpdateForm(forms.Form):
    trip_name = forms.CharField(max_length = 100, required = True)
    trip_price = forms.IntegerField(required = True)
    about_trip = forms.CharField(widget=forms.Textarea, required = True)

class AccomodationUpdateForm(forms.Form):
    price = forms.IntegerField()
    available_space = forms.IntegerField()
    available_services = forms.ModelMultipleChoiceField(queryset= Service.objects.all())
    noice_level = forms.ChoiceField(choices = noice_lovel())
    airport_transport = forms.BooleanField(required = False)

class UserUpdateForm(forms.Form):
    email = forms.EmailField()
    username = forms.CharField()
    first_name = forms.CharField()
    last_name = forms.CharField()

    def clean_username(self):
        cleaned_data = super(UserUpdateForm, self).clean()
        username = self.cleaned_data['username']
        if not re.search(r'^\w+$', username):
            raise forms.ValidationError('username can only contain alphanumeric characters and underscores')
        try:
            User.objects.get(username=username)
        except ObjectDoesNotExist:
            return username
        raise forms.ValidationError('username is already taken')

    def clean_email(self):
        cleaned_data = super(UserUpdateForm, self).clean()
        email = self.cleaned_data['email']
        try:
            User.objects.get(email=email)
        except ObjectDoesNotExist:
            return email
        raise forms.ValidationError('The Email you Entered Has been Used Already')


class BookingsSearchForm(forms.Form):
    serial_number = forms.CharField(required = False, widget = forms.TextInput(attrs={'placeholder': 'Search By Serial Number'}))
    name = forms.CharField(required = False, widget = forms.TextInput(attrs={'placeholder': 'Search by Clients Name'}))
    booking_date = forms.DateField(required = False, widget = forms.DateInput(attrs={'placeholder': 'Search by Date Booking was made.'}))

class TripDiscountForm(forms.ModelForm):
    class  Meta:
        model = TripDiscount
        fields = ('starting_date', 'ending_date', 'ammount_in_percentage', 'created_by', 'product')
        exclude = ['created_by', 'product']

    def clean(self):
        cleaned_data = super(TripDiscountForm, self).clean()
        ammount_entered = self.cleaned_data['ammount_in_percentage']
        if ammount_entered <= 0:
            raise forms.ValidationError('You can have that ammount as a discount ammount.')

        date_one = self.cleaned_data['starting_date']
        date_two = self.cleaned_data['ending_date']
        if date_two < date_one:
            raise forms.ValidationError('These dates are invalid. you can not have the date to end the discount smaller than the date you start.')

        #date_one = self.cleaned_data['starting_date']
        today_date = date.today()
        if date_one < today_date:
            raise forms.ValidationError('You can only start discount from today or later!')

        return cleaned_data

class TripDiscountUpdateForm(forms.Form):
    ammount_in_percentage = forms.FloatField(required = False, widget = forms.NumberInput(attrs={'placeholder': 'E.g. discount is 10 percent enter 10'}))

    def clean(self):
        cleaned_data = super(TripDiscountUpdateForm, self).clean()
        ammount_entered = self.cleaned_data['ammount_in_percentage']
        if ammount_entered <= 0 or ammount_entered >= 100:
            raise forms.ValidationError('You can have that ammount as a discount ammount.')

        return cleaned_data


class AccomodatiomDiscountForm(forms.ModelForm):
    class  Meta:
        model = AccomodationDiscount
        fields = ('starting_date', 'ending_date', 'ammount_in_percentage', 'created_by', 'product')
        exclude = ['created_by', 'product']

    def clean(self):
        cleaned_data = super(AccomodatiomDiscountForm, self).clean()
        ammount_entered = self.cleaned_data['ammount_in_percentage']
        if ammount_entered <= 0:
            raise forms.ValidationError('You can have that ammount as a discount ammount.')

        date_one = self.cleaned_data['starting_date']
        date_two = self.cleaned_data['ending_date']
        if date_two < date_one:
            raise forms.ValidationError('These dates are invalid. you can not have the date to end the discount smaller than the date you start.')

        #date_one = self.cleaned_data['starting_date']
        today_date = date.today()
        if date_one < today_date:
            raise forms.ValidationError('You can only start discount from today or later!')

        return cleaned_data

class AccomodationDiscountUpdateForm(forms.Form):
    ammount_in_percentage = forms.FloatField(required = False, widget = forms.NumberInput(attrs={'placeholder': 'E.g. discount is 10 percent enter 10'}))

    def clean(self):
        cleaned_data = super(AccomodationDiscountUpdateForm, self).clean()
        ammount_entered = self.cleaned_data['ammount_in_percentage']
        if ammount_entered <= 0 or ammount_entered >= 100:
            raise forms.ValidationError('You can have that ammount as a discount ammount.')
        return cleaned_data

