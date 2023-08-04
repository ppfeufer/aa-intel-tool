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
        FLEETCOMP = "fleetcomp", _("Fleet Composition")
        CHATLIST = "chatlist", _("Chat List")

    hash = models.CharField(
        primary_key=True,
        editable=False,
        unique=True,
        max_length=30,
        verbose_name=_("The hash of the scan."),
    )

    created = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
        verbose_name=_("Date and time the scan was created."),
    )

    raw_data = models.TextField(verbose_name=_("The original scan data."))
    processed_data = models.JSONField(
        default=dict, verbose_name=_("The processed scan data.")
    )

    scan_type = models.CharField(
        max_length=9,
        choices=Type.choices,
        default=Type.INVALID,
        verbose_name=_("The scan type."),
    )

    class Meta:  # pylint: disable=too-few-public-methods
        """
        Meta definitions
        """

        default_permissions = ()
        verbose_name = _("scan")
        verbose_name_plural = _("scans")

    def __str__(self) -> str:
        return str(self.pk)

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
