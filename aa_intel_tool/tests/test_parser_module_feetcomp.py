# Standard Library
from unittest.mock import MagicMock, patch

# AA Intel Tool
from aa_intel_tool.exceptions import ParserError
from aa_intel_tool.parser.module.fleetcomp import get_fleet_composition, parse
from aa_intel_tool.tests import BaseTestCase


class TestParse(BaseTestCase):
    def test_raises_error_when_fleetcomp_module_is_disabled(self):
        """
        Test that ParserError is raised when the fleet composition module is disabled.

        :return:
        :rtype:
        """

        with patch(
            "aa_intel_tool.app_settings.AppSettings.INTELTOOL_ENABLE_MODULE_FLEETCOMP",
            False,
        ):
            with self.assertRaises(ParserError):
                parse(scan_data=[])

    def test_returns_empty_data_for_empty_scan(self):
        """
        Test that an empty scan returns empty parsed data.

        :return:
        :rtype:
        """

        with patch(
            "aa_intel_tool.app_settings.AppSettings.INTELTOOL_ENABLE_MODULE_FLEETCOMP",
            True,
        ):
            with patch(
                "aa_intel_tool.parser.module.fleetcomp.safe_scan_to_db"
            ) as mock_safe_scan:
                mock_safe_scan.return_value = {}

                result = parse(scan_data=[])

                self.assertEqual(result, {})

    def test_parses_valid_scan_data_correctly(self):
        """
        Test that valid scan data is parsed correctly.

        :return:
        :rtype:
        """

        scan_data = [
            "Rounon Dax\tJita\tOmen\tCruiser\tFleet Commander (Boss)\t5 - 5 - 5",
            "Arodem Artemis\tPerimeter\tLeopard\tShuttle\tSquad Member\t0 - 0 - 5\tWing 1 / Squad 1",
        ]
        with patch(
            "aa_intel_tool.app_settings.AppSettings.INTELTOOL_ENABLE_MODULE_FLEETCOMP",
            True,
        ):
            with patch(
                "aa_intel_tool.parser.module.fleetcomp.EveEntity.objects.fetch_by_names_esi"
            ) as mock_fetch:
                mock_qs = MagicMock()
                mock_qs.filter.return_value = mock_qs
                mock_qs.__iter__.return_value = iter([])
                mock_fetch.return_value = mock_qs
                with patch(
                    "aa_intel_tool.parser.module.fleetcomp.safe_scan_to_db"
                ) as mock_safe_scan:
                    mock_safe_scan.return_value = {"parsed": "data"}
                    result = parse(scan_data=scan_data)
                    self.assertEqual(result, {"parsed": "data"})

    def tst_handles_duplicate_pilot_entries_in_scan(self):
        scan_data = [
            "Arodem Artemis\tPerimeter\tLeopard\tShuttle\tSquad Member\t0 - 0 - 5\tWing 1 / Squad 1",
            "Arodem Artemis\tPerimeter\tLeopard\tShuttle\tSquad Member\t0 - 0 - 5\tWing 1 / Squad 1",
        ]
        with patch(
            "aa_intel_tool.app_settings.AppSettings.INTELTOOL_ENABLE_MODULE_FLEETCOMP",
            True,
        ):
            with patch(
                "aa_intel_tool.parser.module.fleetcomp.safe_scan_to_db"
            ) as mock_safe_scan:
                mock_safe_scan.return_value = {"parsed": "data"}
                result = parse(scan_data=scan_data)
                self.assertEqual(result, {"parsed": "data"})


class TestGetFleetComposition(BaseTestCase):
    """
    Testing the get_fleet_composition function
    """

    def test_returns_correct_fleet_composition_for_valid_data(self):
        """
        Test that the fleet composition is returned correctly for valid data.

        :return:
        :rtype:
        """

        pilots = {
            "Pilot1": {"ship": "Omen"},
            "Pilot2": {"ship": "Zealot"},
        }
        ships = {
            "class": {"Omen": {"count": 1}, "Zealot": {"count": 1}},
            "type": {"Cruiser": {"count": 1}, "Heavy Assault Cruiser": {"count": 1}},
        }

        ship1 = MagicMock()
        ship1.id = 1
        ship1.name = "Omen"
        ship1.eve_group__id = 10
        ship1.eve_group__name = "Cruiser"
        ship1.mass = 1000

        ship2 = MagicMock()
        ship2.id = 2
        ship2.name = "Zealot"
        ship2.eve_group__id = 20
        ship2.eve_group__name = "Heavy Assault Cruiser"
        ship2.mass = 500

        with (
            patch(
                "aa_intel_tool.parser.module.fleetcomp.EveEntity.objects.fetch_by_names_esi"
            ) as mock_fetch,
            patch(
                "aa_intel_tool.parser.module.fleetcomp.EveType.objects.bulk_get_or_create_esi"
            ) as mock_bulk,
            patch(
                "aa_intel_tool.parser.module.fleetcomp._get_character_info"
            ) as mock_get_character_info,
        ):
            mock_fetch.return_value.filter.return_value.values_list.return_value = [
                1,
                2,
            ]
            mock_bulk.return_value.values_list.return_value = [ship1, ship2]
            mock_get_character_info.return_value = [
                MagicMock(
                    character_name="Pilot1",
                    character_id=1001,
                    portrait_url_32="portrait1.png",
                ),
                MagicMock(
                    character_name="Pilot2",
                    character_id=1002,
                    portrait_url_32="portrait2.png",
                ),
            ]

            result = get_fleet_composition(pilots=pilots, ships=ships)

            self.assertEqual(len(result["classes"]), 2)
            self.assertEqual(len(result["types"]), 2)
            self.assertEqual(len(result["pilots"]), 2)

    def test_handles_empty_pilots_and_ships(self):
        """
        Test that empty pilots and ships return empty fleet composition.
        :return:
        :rtype:
        """

        pilots = {}
        ships = {"class": {}, "type": {}}

        with (
            patch(
                "aa_intel_tool.parser.module.fleetcomp.EveEntity.objects.fetch_by_names_esi"
            ) as mock_fetch,
            patch(
                "aa_intel_tool.parser.module.fleetcomp.EveType.objects.bulk_get_or_create_esi"
            ) as mock_bulk,
            patch(
                "aa_intel_tool.parser.module.fleetcomp._get_character_info"
            ) as mock_get_character_info,
        ):
            mock_fetch.return_value.filter.return_value.values_list.return_value = []
            mock_bulk.return_value.values_list.return_value = []
            mock_get_character_info.return_value = []

            result = get_fleet_composition(pilots=pilots, ships=ships)

            self.assertEqual(result["classes"], [])
            self.assertEqual(result["types"], [])
            self.assertEqual(result["pilots"], [])

    def test_raises_error_for_missing_ship_class_in_pilots(self):
        """
        Test that an error is raised when a ship class in pilots is missing.

        :return:
        :rtype:
        """

        pilots = {"Pilot1": {"ship": "Unknown"}}
        ships = {"class": {}, "type": {}}
        mock_ship_class_details = []

        with (
            patch(
                "aa_intel_tool.parser.module.fleetcomp.EveEntity.objects.fetch_by_names_esi"
            ) as mock_fetch,
            patch(
                "aa_intel_tool.parser.module.fleetcomp.EveType.objects.bulk_get_or_create_esi"
            ) as mock_bulk,
            patch(
                "aa_intel_tool.parser.module.fleetcomp._get_character_info"
            ) as mock_get_character_info,
        ):
            mock_fetch.return_value.filter.return_value.values_list.return_value = []
            mock_bulk.return_value.values_list.return_value = mock_ship_class_details
            mock_get_character_info.return_value = [
                MagicMock(
                    character_name="Pilot1",
                    character_id=1001,
                    portrait_url_32="portrait1.png",
                )
            ]

            with self.assertRaises(StopIteration):
                get_fleet_composition(pilots=pilots, ships=ships)
