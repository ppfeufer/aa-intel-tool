"""
The models
"""

# Django
from django.db import models, transaction
from django.utils.crypto import get_random_string
from django.utils.translation import gettext_lazy as _


class Scan(models.Model):
    """
    The scans
    """

    class Type(models.TextChoices):
        """
        The choices for Scan.type
        """

        INVALID = "invalid", _("Invalid scan data")
        DSCAN = "dscan", _("D-Scan")
        FLEETCOMP = "fleetcomp", _("Fleet composition")
        CHATLIST = "chatlist", _("Chat list")

    hash = models.CharField(
        primary_key=True,
        editable=False,
        unique=True,
        max_length=30,
        verbose_name=_("Scan hash"),
    )

    created = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
        verbose_name=_("Creation date/time"),
    )

    raw_data = models.TextField(verbose_name=_("Scan raw data"))

    scan_type = models.CharField(
        max_length=9,
        choices=Type.choices,
        default=Type.INVALID,
        verbose_name=_("Scan type"),
    )

    class Meta:  # pylint: disable=too-few-public-methods
        """
        Meta definitions
        """

        default_permissions = ()
        verbose_name = _("Scan")
        verbose_name_plural = _("Scans")

    def __str__(self) -> str:
        return str(self.pk)

    @transaction.atomic()
    def save(self, *args, **kwargs):
        """
        Generates the scan hash on save

        :param args:
        :type args:
        :param kwargs:
        :type kwargs:
        :return:
        :rtype:
        """

        if self._state.adding is True:
            self.hash = Scan.generate_scan_hash()

        super().save(*args, **kwargs)

        if self.hash == "":
            self.hash = Scan.generate_scan_hash()
            self.save()

    @staticmethod
    def generate_scan_hash():
        """
        Get a random string we can use as hash

        :return:
        :rtype:
        """

        scan_hash = get_random_string(length=30)

        while Scan.objects.filter(hash=scan_hash).exists():  # pylint: disable=no-member
            scan_hash = get_random_string(length=30)

        return scan_hash


class ScanData(models.Model):
    """
    Scan section data
    """

    class Section(models.TextChoices):
        """
        The choices for ScanData.section
        """

        INVALID = "invalid", _("Invalid scan data")
        PILOTLIST = "pilotlist", _("Pilot list")
        CORPORATIONLIST = "corporationlist", _("Corporation list")
        ALLIANCELIST = "alliancelist", _("Alliance list")
        SHIPTYPES = "shiptypes", _("Ship types")
        SHIPLIST = "shiplist", _("Ship list")
        SHIPLIST_ON_GRID = "shiplist_on_grid", _("Ship list (on grid)")
        SHIPLIST_OFF_GRID = "shiplist_off_grid", _("Ship list (off grid)")
        STRUCTURES_ON_GRID = "structures_on_grid", _("Structures (on grid)")
        STARBASES_ON_GRID = "starbases_on_grid", _("Starbases (on grid)")
        DEPLOYABLES_ON_GRID = "deployables_on_grid", _("Deployables (on grid)")
        MISCELLANEOUS_ON_GRID = "miscellaneous_on_grid", _("Miscellaneous (on grid)")
        SOLAR_SYSTEM_INFORMATION = "solar_system_information", _("System information")
        FLEETCOMPOSITION = "fleetcomposition", _("Fleet composition")

    scan = models.ForeignKey(
        Scan,
        related_name="scan_data",
        null=True,
        blank=True,
        default=None,
        on_delete=models.CASCADE,
        verbose_name=_("Scan"),
    )

    section = models.CharField(
        max_length=24,
        choices=Section.choices,
        default=Section.INVALID,
        verbose_name=_("Scan section"),
    )

    processed_data = models.JSONField(
        default=dict, verbose_name=_("Processed scan data")
    )

    class Meta:  # pylint: disable=too-few-public-methods
        """
        Meta definitions
        """

        default_permissions = ()
        verbose_name = _("Scan data")
        verbose_name_plural = _("Scan data")

        unique_together = ("scan", "section")
