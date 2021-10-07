""" List of subclassed of django.db.models.Model for authenticationa and
	authoraization apps.

	The file will include declaration of model which will be used when 
	performing database quiries on views and other parts of the code.

	Generated by: python3 manage.py startapp
	Last modified by: Wendirad Demelash
"""
from django.db import models
from django.utils.translation import gettext_lazy as _

from ausers.validators import PhoneNumberValidator


class Address(models.Model):
    """An abstract class that represent composite attributes of
    it's subclasses.

    Attributes:
            email: an email field, used to store email address of subclass instances
            phone_number: character field, that store formated phone numbers
    """

    email = models.EmailField(_("email address"), unique=True)
    phone_number = models.CharField(
        _("phone number"),
        max_length=13,
        validators=(PhoneNumberValidator,),
        help_text=_(
            "Formated phone number used as an alternative address for subclasses."
        ),
    )

    class Meta:
        abstract = True
