from django.db import models
from django.utils.translation import gettext_lazy as _



class Industry(models.Model):
    name = models.CharField(_("Industry Name"), max_length=100, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Industry")
        verbose_name_plural = _("Industries")


class Sector(models.Model):
    name = models.CharField(_("Sector Name"), max_length=100, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Sector")
        verbose_name_plural = _("Sectors")


class Country(models.Model):
    istat_code = models.CharField(_("ISTAT Code"), max_length=10)
    name_it = models.CharField(_("Name (IT)"), max_length=100)
    name_en = models.CharField(_("Name (EN)"), max_length=100)
    at_code = models.CharField(_("AT Code"), max_length=10)
    unsd_code = models.CharField(_("UNSD Code"), max_length=10)
    iso_alpha2_code = models.CharField(_("ISO Alpha-2 Code"), max_length=2)
    iso_alpha3_code = models.CharField(_("ISO Alpha-3 Code"), max_length=3)
    created_at = models.DateTimeField(_("Created At"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Updated At"), auto_now=True)

    class Meta:
        verbose_name = _('country')
        verbose_name_plural = _('countries')

    def __str__(self):
        return self.name_en


class MunicipalityProvince(models.Model):
    municipality = models.CharField(_("Municipality"), max_length=100)
    province = models.CharField(_("Province"), max_length=100)
    region = models.CharField(_("Region"), max_length=100)
    postal_code = models.CharField(_("Postal Code"), max_length=10)
    tax_code = models.CharField(_("Tax Code"), max_length=11)
    postal_code_from = models.CharField(_("Postal Code From"), max_length=5)
    postal_code_to = models.CharField(_("Postal Code To"), max_length=5)
    created_at = models.DateTimeField(_("Created At"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Updated At"), auto_now=True)

    class Meta:
        verbose_name = _('municipality and province')
        verbose_name_plural = _('municipalities and provinces')

    def __str__(self):
        return f"{self.municipality}, {self.province}, {self.region}"


class Company(models.Model):
    name = models.CharField(_("Company Name"), max_length=255, default='Company default')
    description = models.TextField(_("Description"), blank=True, null=True)
    MACRO_SWITCH_CHOICES = [
        ('public', _('Public')),
        ('private', _('Private')),
    ]

    macro_switch = models.CharField(
        _("Macro Switch"),
        max_length=10,
        choices=MACRO_SWITCH_CHOICES,
        default='public',
        help_text=_("Specify whether the company is public or private.")
    )
    industry = models.ForeignKey(
        Industry,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_("Industry")
    )
    sector = models.ForeignKey(
        Sector,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_("Sector")
    )
    STATUS_CHOICES = [
        ('Attiva', _('Attiva')),
        ('Sospesa', _('Sospesa')),
    ]
    status = models.CharField(
        _("Status"),
        max_length=10,
        choices=STATUS_CHOICES,
        default='Attiva',
        help_text=_("Specify whether the company is Attiva or Sospesa.")
    )
    email = models.EmailField(_("Email"), blank=True, null=True)
    phone_mobile = models.CharField(_("Phone"), max_length=20, blank=True, null=True)
    phone_number = models.CharField(_("Phone Number"), max_length=20, blank=True, null=True)
    number_employees = models.IntegerField(_("Number of employees"), blank=True, null=True)
    address = models.TextField(_("Address"), blank=True, null=True)
    website = models.URLField(_("Website"), blank=True, null=True)
    date_created = models.DateTimeField(_("Date Created"), auto_now_add=True)
    date_updated = models.DateTimeField(_("Date Updated"), auto_now=True)

    def __str__(self):
        return self.name or ''

    class Meta:
        verbose_name = _("Company")
        verbose_name_plural = _("Companies")


class FileType(models.Model):
    type_file = models.CharField(_("Type"), max_length=50, unique=True)  # Traduci "Type"
    description = models.TextField(_("Description"), blank=True)  # Traduci "Description"

    def __str__(self):
        return self.tipo

    class Meta:
        verbose_name = _("File Type")
        verbose_name_plural = _("File Types")


class CompanyFile(models.Model):

    def company_file_upload_to(instance, filename):
        return f'files_aziende/{instance.company.id}/{filename}'

    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name='files',
        verbose_name=_("Company")
    )
    tipo_file = models.ForeignKey(
        FileType,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='company_files',
        verbose_name=_("File Type")
    )
    file = models.FileField(_("File"), upload_to=company_file_upload_to)
    description = models.CharField(_("Description"), max_length=255, blank=True)
    timestamp = models.DateTimeField(_("Timestamp"), auto_now_add=True)

    def __str__(self):
        return self.description or self.file.name

    class Meta:
        verbose_name = _("Company File")
        verbose_name_plural = _("Company Files")


class Office(models.Model):
    company = models.ForeignKey(
        Company,
        null=True,
        on_delete=models.CASCADE,
        related_name='offices',
        verbose_name=_("Company")
    )
    identifier = models.CharField(_("Identifier"), max_length=255, blank=True, null=True)
    is_legal = models.BooleanField(_("Is Legal"))
    is_operative = models.BooleanField(_("Is Operative"))
    address = models.CharField(_("Address"), max_length=255, blank=True, null=True)
    civic_number = models.CharField(_("Civic Number"), max_length=10, blank=True, null=True)
    phone = models.CharField(_("Phone"), max_length=20, blank=True, null=True)
    mobile = models.CharField(_("Mobile"), max_length=20, null=True, blank=True)
    email = models.EmailField(_("Email"), blank=True, null=True)
    fax = models.CharField(_("Fax"), max_length=20, null=True, blank=True)
    country = models.ForeignKey(Country, on_delete=models.CASCADE, verbose_name=_("Country"), default=1)
    municipality_province = models.ForeignKey(MunicipalityProvince, on_delete=models.CASCADE,
                                              verbose_name=_("Municipality Province"), default=7292)
    postal_code = models.CharField(_("Postal Code"), max_length=5, blank=True, null=True)
    created_at = models.DateTimeField(_("Created At"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Updated At"), auto_now=True)

    class Meta:
        verbose_name = _('office')
        verbose_name_plural = _('offices')

    def __str__(self):
        return self.address


class Role(models.Model):
    description = models.CharField(_("Description"), max_length=255)
    created_at = models.DateTimeField(_("Created At"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Updated At"), auto_now=True)

    class Meta:
        verbose_name = _('role')
        verbose_name_plural = _('roles')

    def __str__(self):
        return self.description


class CompanyRepresentative(models.Model):
    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        null=True,
        verbose_name=_("Company")
    )
    full_name = models.CharField(_("Full Name"), max_length=254, default='Company Representative default')
    address = models.CharField(_("Address"), max_length=255)
    civic_number = models.CharField(_("Civic Number"), max_length=10)
    phone_mobile = models.CharField(_("phone_mobile"), max_length=20, default='340123456789')
    phone_number = models.CharField(_("phone_number"), max_length=20, default='011123456789')
    email = models.EmailField(_("Email"), null=True, blank=True)
    fax = models.CharField(_("Fax"), max_length=20, null=True, blank=True)
    whatsapp = models.BooleanField(_("WhatsApp"), default=False)
    facebook = models.URLField(_("Facebook"), null=True, blank=True)
    instagram = models.URLField(_("Instagram"), null=True, blank=True)
    tiktok = models.URLField(_("TikTok"), null=True, blank=True)
    role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True, verbose_name=_("Role"))
    date_of_birth = models.DateField(_("Date of Birth"))
    newsletter_subscription = models.BooleanField(_("Newsletter Subscription"), default=False)
    country = models.ForeignKey(Country, on_delete=models.CASCADE, verbose_name=_("Country"), default=1)
    municipality_province = models.ForeignKey(MunicipalityProvince, on_delete=models.CASCADE,
                                              verbose_name=_("Municipality Province"), default=7292)
    postal_code = models.CharField(_("Postal Code"), max_length=5, blank=True, null=True)
    STATUS_CHOICES = [
        ('Attiva', _('Attiva')),
        ('Sospesa', _('Sospesa')),
    ]
    status = models.CharField(
        _("Status"),
        max_length=10,
        choices=STATUS_CHOICES,
        default='Attiva',
        help_text=_("Specify whether the company is Attiva or Sospesa.")
    )
    created_at = models.DateTimeField(_("Created At"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Updated At"), auto_now=True)

    class Meta:
        verbose_name = _('company representative')
        verbose_name_plural = _('company representatives')

    def __str__(self):
        return f"{self.full_name}"


class RoleHistory(models.Model):
    company_representative = models.ForeignKey(CompanyRepresentative, on_delete=models.CASCADE,
                                               verbose_name=_("Company Representative"))
    role = models.ForeignKey(Role, on_delete=models.CASCADE, verbose_name=_("Role"))
    date_from = models.DateField(_("Date From"))
    date_to = models.DateField(_("Date To"), null=True, blank=True)  # If null, the role is current
    created_at = models.DateTimeField(_("Created At"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Updated At"), auto_now=True)

    class Meta:
        verbose_name = _('role history')
        verbose_name_plural = _('role histories')

    def __str__(self):
        return f"{self.company_representative} - {self.role} - From: {self.date_from} To: {('Current' if self.date_to is None else self.date_to)}"


class ActivityType(models.Model):
    description = models.CharField(_("Description"), max_length=255)

    class Meta:
        verbose_name = _("Activity Type")
        verbose_name_plural = _("Activity Types")

    def __str__(self):
        return self.description


class Activity(models.Model):
    description = models.TextField(_("Description"))
    date = models.DateTimeField(_("Date"))
    alert = models.BooleanField(_("Alert"), default=False)
    visible_to_all = models.BooleanField(_("Visible to All"), default=False)
    # activity_user = models.ForeignKey(
    #     settings.AUTH_USER_MODEL,
    #     on_delete=models.CASCADE,
    #     verbose_name=_("Activity User")
    # )
    activity_type = models.ForeignKey(
        ActivityType,
        on_delete=models.CASCADE,
        verbose_name=_("Activity Type")
    )
    # Assuming you want to link this to CompanyRepresentative as well
    company_representative = models.ForeignKey(
        CompanyRepresentative,
        on_delete=models.CASCADE,
        verbose_name=_("Company Representative")
    )

    class Meta:
        verbose_name = _("Activity")
        verbose_name_plural = _("Activities")

    def __str__(self):
        return "{} - {}".format(self.description, self.date)
