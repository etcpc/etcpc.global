""" List of subclassed of django.db.models.Model for authenticationa and
	authoraization apps.

	The file will include declaration of model which will be used when 
	performing database quiries on views and other parts of the code.

	Generated by: python3 manage.py startapp
	Last modified by: Wendirad Demelash
"""
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin, UserManager
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from ausers.validators import PhoneNumberValidator


class Address(models.Model):
    """
    An abstract class that represent composite attributes of
    it's subclasses.

    Attributes:
            email: an email field, used to store email address of subclass instances
            phone_number: character field, that store formated phone numbers
    """

    email = models.EmailField(_("email address"), unique=True)
    phone_number = models.CharField(
        _("phone number"),
        max_length=13,
        validators=(PhoneNumberValidator(),),
        help_text=_(
            "Formated phone number used as an alternative address for subclasses."
        ),
    )

    class Meta:
        abstract = True


class User(AbstractBaseUser, PermissionsMixin, Address):
    """
    A user base class that implement fully featured User model with
    admin-compliant permissions. Inherite :models:`ausers.Address` to
    include addtional attributes.

    Attributes:
        username: non-optional charcter field, used to authenticate users.

    """

    username_validator = UnicodeUsernameValidator()
    username = models.CharField(
        _("username"),
        max_length=150,
        unique=True,
        help_text=_(
            "Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only."
        ),
        validators=[username_validator],
        error_messages={
            "unique": _("A user with that username already exists."),
        },
    )
    is_staff = models.BooleanField(
        _("staff status"),
        default=False,
        help_text=_("Designates whether the user can log into this admin site."),
    )
    is_active = models.BooleanField(
        _("active"),
        default=True,
        help_text=_(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting account"
        ),
    )
    date_joined = models.DateTimeField(_("date joined"), auto_now_add=True)

    objects = UserManager()

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email"]

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")


class ETCPCUser(User):
    """
    An abstract class, that is subclass of :model:`ausers.User`. It containt
    additional attributes, and serve as base class for all users except system
    administrator.

    Since system administrator has exceptional permissions, all other users
    need to be managed in different models.

    Attributes:
            (title, first_name, last_name, sex, date_of_birth)
    """

    class SexChoice(models.TextChoices):
        MALE = "M", _("Male")
        FEMALE = "F", _("Female")

    class TitleChoice(models.IntegerChoices):
        MR = 0, _("mr")
        MRS = 1, _("mrs")
        MS = 2, _("ms")
        MISS = 3, _("miss")
        DR = 4, _("doctor")
        PROFESSOR = 5, _("professor")

    title = models.IntegerField(choices=TitleChoice.choices)
    first_name = models.CharField(_("first name"), max_length=150)
    last_name = models.CharField(_("last name"), max_length=150)
    sex = models.CharField(_("sex"), max_length=1, choices=SexChoice.choices)
    date_of_birth = models.DateField(_("birth date"))

    class Meta:
        abstract = True


class Director(ETCPCUser):
    """
    Subclass of ETCPCUser that represent ETCPC organization director.
    This user is found in the top of ETCPC users hierarchy.

    Attributes: Does not contain any additional attributes.
    """

    class Meta:
        permissions = (("list_directors", "Can list directors"),)


class Manager(ETCPCUser):
    """
    Representation of ETCPC manager. This user is under always under revision
    of :model:`ausers.Director`, also he/she is second in ETCPC user hierarchy.

    Attributes: Does not contain any additional attributes.
    """

    class Meta:
        permissions = (("list_managers", "Can list managers"),)


class Institution(Address):
    """
    A basic representation of any institution that works with ETCPC.

    Attributes:
            name: Legal name of an institution
            short_name: short name institution, specially for universities
                        ex. Adama Science and Technology University >> ASTU
            logo: Legal institution logo.
    """

    name = models.CharField(_("name"), max_length=150)
    short_name = models.CharField(_("short name"), max_length=7, blank=True, null=True)
    logo = models.ImageField(_("logo"), upload_to="institutions/logo/")

    class Meta:
        permissions = (("list_institutions", "Can list institutions"),)


class GeneralScientificCommittee(ETCPCUser):
    """
    ETCPCUser subclass that defines ETCPC's  Scientifi committee. The model
    represent general scientific committees.

    Attributes: Does not contain any additional attributes.
    """

    class Meta:
        permissions = (
            (
                "list_general_scientific_committees",
                "Can list general scientific committee",
            ),
        )


class LocalScientificCommittee(ETCPCUser):
    """
    Local ETCPC's  Scientifi committee, which is accountable for each institutions.

    Attributes:
        (institution)
    """

    institution = models.ForeignKey(
        Institution, verbose_name=_("institution"), on_delete=models.CASCADE
    )

    class Meta:
        permissions = (
            ("list_local_scientific_committees", "Can list local scientific committee"),
        )
