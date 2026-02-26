"""
Unit tests for the fleetcomp parser module.
"""

# Standard Library
from unittest.mock import MagicMock, patch

# AA Intel Tool
from aa_intel_tool.exceptions import ParserError
from aa_intel_tool.models import Scan, ScanData
from aa_intel_tool.parser.module.fleetcomp import (
    get_fleet_composition,
    handle_fleet_composition_and_participation,
    parse,
    parse_line,
    update_ships,
)
from aa_intel_tool.tests import BaseTestCase


class TestGetFleetComposition(BaseTestCase):
    """
    Test cases for the get_fleet_composition function.
    """

    def test_returns_correct_fleet_composition_with_valid_data(self):
        pilots = {
            "Pilot 1": {"ship": "Ship Class 1"},
            "Pilot 2": {"ship": "Ship Class 2"},
        }
        ships = {
            "class": {"Ship Class 1": {"count": 1}, "Ship Class 2": {"count": 1}},
            "type": {"Group 1": {"count": 0}, "Group 2": {"count": 0}},
        }
        ship_class_ids = [1, 2]
        ship_class_details = [
            type(
                "SC",
                (),
                {
                    "id": 1,
                    "name": "Ship Class 1",
                    "eve_group__id": 10,
                    "eve_group__name": "Group 1",
                    "mass": 1000,
                },
            )(),
            type(
                "SC",
                (),
                {
                    "id": 2,
                    "name": "Ship Class 2",
                    "eve_group__id": 20,
                    "eve_group__name": "Group 2",
                    "mass": 2000,
                },
            )(),
        ]
        pilot_details = [
            type(
                "P",
                (),
                {
                    "character_name": "Pilot 1",
                    "character_id": 101,
                    "portrait_url_32": "url1",
                },
            )(),
            type(
                "P",
                (),
                {
                    "character_name": "Pilot 2",
                    "character_id": 102,
                    "portrait_url_32": "url2",
                },
            )(),
        ]

        fetch_qs = MagicMock()
        fetch_filter_qs = MagicMock()
        fetch_filter_qs.values_list.return_value = ship_class_ids
        fetch_qs.filter.return_value = fetch_filter_qs

        bulk_qs = MagicMock()
        bulk_qs.values_list.return_value = ship_class_details

        with (
            patch(
                "aa_intel_tool.parser.module.fleetcomp.EveEntity.objects.fetch_by_names_esi",
                return_value=fetch_qs,
            ) as mock_fetch,
            patch(
                "aa_intel_tool.parser.module.fleetcomp.EveType.objects.bulk_get_or_create_esi",
                return_value=bulk_qs,
            ) as mock_bulk_get,
            patch(
                "aa_intel_tool.parser.module.fleetcomp._get_character_info",
                return_value=pilot_details,
            ) as mock_get_character_info,
        ):
            result = get_fleet_composition(pilots=pilots, ships=ships)
            mock_fetch.assert_called_once_with(names=ships["class"], update=True)
            mock_bulk_get.assert_called_once_with(
                ids=set(ship_class_ids), include_children=True
            )
            mock_get_character_info.assert_called_once_with(
                scan_data=["Pilot 1", "Pilot 2"]
            )
            self.assertEqual(len(result["classes"]), 2)
            self.assertEqual(len(result["types"]), 2)
            self.assertEqual(len(result["pilots"]), 2)

    def test_handles_empty_pilots_and_ships_gracefully(self):
        pilots = {}
        ships = {"class": {}, "type": {}}

        fetch_qs = MagicMock()
        fetch_filter_qs = MagicMock()
        fetch_filter_qs.values_list.return_value = []
        fetch_qs.filter.return_value = fetch_filter_qs

        bulk_qs = MagicMock()
        bulk_qs.values_list.return_value = []

        with (
            patch(
                "aa_intel_tool.parser.module.fleetcomp.EveEntity.objects.fetch_by_names_esi",
                return_value=fetch_qs,
            ) as mock_fetch,
            patch(
                "aa_intel_tool.parser.module.fleetcomp.EveType.objects.bulk_get_or_create_esi",
                return_value=bulk_qs,
            ) as mock_bulk_get,
            patch(
                "aa_intel_tool.parser.module.fleetcomp._get_character_info",
                return_value=[],
            ) as mock_get_character_info,
        ):
            result = get_fleet_composition(pilots=pilots, ships=ships)
            mock_fetch.assert_called_once_with(names=ships["class"], update=True)
            mock_bulk_get.assert_called_once_with(ids=set(), include_children=True)
            mock_get_character_info.assert_called_once_with(scan_data=[])
            self.assertEqual(result["classes"], [])
            self.assertEqual(result["types"], [])
            self.assertEqual(result["pilots"], [])

    def test_raises_error_when_ship_class_not_found(self):
        pilots = {
            "Pilot 1": {"ship": "Unknown Ship Class"},
        }
        ships = {
            "class": {"Unknown Ship Class": {"count": 1}},
            "type": {},
        }

        fetch_qs = MagicMock()
        fetch_filter_qs = MagicMock()
        fetch_filter_qs.values_list.return_value = []
        fetch_qs.filter.return_value = fetch_filter_qs

        bulk_qs = MagicMock()
        bulk_qs.values_list.return_value = []

        missing_pilot = type(
            "P",
            (),
            {
                "character_name": "Pilot 1",
                "character_id": 101,
                "portrait_url_32": "url1",
            },
        )()

        with (
            patch(
                "aa_intel_tool.parser.module.fleetcomp.EveEntity.objects.fetch_by_names_esi",
                return_value=fetch_qs,
            ),
            patch(
                "aa_intel_tool.parser.module.fleetcomp.EveType.objects.bulk_get_or_create_esi",
                return_value=bulk_qs,
            ),
            patch(
                "aa_intel_tool.parser.module.fleetcomp._get_character_info",
                return_value=[missing_pilot],
            ),
        ):
            with self.assertRaises(StopIteration):
                get_fleet_composition(pilots=pilots, ships=ships)


class TestParseLine(BaseTestCase):
    """
    Test cases for the parse_line function.
    """

    def test_parses_line_with_all_fields_correctly(self):
        line = "Pilot Name\tSystem Name\tShip Class\tShip Type\tPosition\tFC\tWing Name"
        result = parse_line(line)
        self.assertEqual(
            result,
            [
                "Pilot Name",
                "System Name",
                "Ship Class",
                "Ship Type",
                "Position",
                "FC",
                "Wing Name",
            ],
        )


class TestUpdateShips(BaseTestCase):
    """
    Test cases for the update_ships function.
    """

    def test_updates_ships_with_new_class_and_type(self):
        ships = {"class": {}, "type": {}}
        line = [
            "Pilot Name",
            "System Name",
            "New Ship Class",
            "New Ship Type",
            "",
            "",
            "",
        ]
        result = update_ships(ships, line)
        self.assertEqual(result["class"], {"New Ship Class": {"count": 1}})
        self.assertEqual(result["type"], {"New Ship Type": {"count": 1}})

    def test_increments_count_for_existing_class_and_type(self):
        ships = {
            "class": {"Existing Ship Class": {"count": 1}},
            "type": {"Existing Ship Type": {"count": 2}},
        }
        line = [
            "Pilot Name",
            "System Name",
            "Existing Ship Class",
            "Existing Ship Type",
            "",
            "",
            "",
        ]
        result = update_ships(ships, line)
        self.assertEqual(result["class"], {"Existing Ship Class": {"count": 2}})
        self.assertEqual(result["type"], {"Existing Ship Type": {"count": 3}})

    def test_handles_empty_ships_dict(self):
        ships = {"class": {}, "type": {}}
        line = ["Pilot Name", "System Name", "", "", "", "", ""]
        result = update_ships(ships, line)
        self.assertEqual(result["class"], {"": {"count": 1}})
        self.assertEqual(result["type"], {"": {"count": 1}})

    def test_handles_empty_line(self):
        ships = {"class": {}, "type": {}}
        line = ["", "", "", "", "", "", ""]
        result = update_ships(ships, line)
        self.assertEqual(result["class"], {"": {"count": 1}})
        self.assertEqual(result["type"], {"": {"count": 1}})


class TestHandleFleetCompositionAndParticipation(BaseTestCase):
    """
    Test cases for the handle_fleet_composition_and_participation function.
    """

    def test_returns_fleet_composition_and_participation_when_chat_scan_enabled(self):
        pilots = {"Pilot 1": {"ship": "Ship Class 1"}}
        ships = {
            "class": {"Ship Class 1": {"count": 1}},
            "type": {"Group 1": {"count": 1}},
        }
        fleet_composition = {"classes": [], "types": [], "pilots": []}
        participation = {"some": "data"}

        with (
            patch(
                "aa_intel_tool.parser.module.fleetcomp.get_fleet_composition",
                return_value=fleet_composition,
            ) as mock_get_fleet_composition,
            patch(
                "aa_intel_tool.parser.module.fleetcomp.parse_pilots",
                return_value=participation,
            ) as mock_parse_pilots,
            patch(
                "aa_intel_tool.parser.module.fleetcomp.AppSettings.INTELTOOL_ENABLE_MODULE_CHATSCAN",
                True,
            ),
        ):
            result = handle_fleet_composition_and_participation(pilots, ships)
            mock_get_fleet_composition.assert_called_once_with(
                pilots=pilots, ships=ships
            )
            mock_parse_pilots.assert_called_once_with(
                scan_data=list(set(pilots)), safe_to_db=False, ignore_limit=True
            )
            self.assertEqual(result, (fleet_composition, participation))

    def test_returns_fleet_composition_and_none_when_chat_scan_disabled(self):
        pilots = {"Pilot 1": {"ship": "Ship Class 1"}}
        ships = {
            "class": {"Ship Class 1": {"count": 1}},
            "type": {"Group 1": {"count": 1}},
        }
        fleet_composition = {"classes": [], "types": [], "pilots": []}

        with (
            patch(
                "aa_intel_tool.parser.module.fleetcomp.get_fleet_composition",
                return_value=fleet_composition,
            ) as mock_get_fleet_composition,
            patch(
                "aa_intel_tool.parser.module.fleetcomp.AppSettings.INTELTOOL_ENABLE_MODULE_CHATSCAN",
                False,
            ),
        ):
            result = handle_fleet_composition_and_participation(pilots, ships)
            mock_get_fleet_composition.assert_called_once_with(
                pilots=pilots, ships=ships
            )
            self.assertEqual(result, (fleet_composition, None))

    def test_handles_empty_pilots_and_ships(self):
        pilots = {}
        ships = {"class": {}, "type": {}}
        fleet_composition = {"classes": [], "types": [], "pilots": []}

        with (
            patch(
                "aa_intel_tool.parser.module.fleetcomp.get_fleet_composition",
                return_value=fleet_composition,
            ) as mock_get_fleet_composition,
            patch(
                "aa_intel_tool.parser.module.fleetcomp.AppSettings.INTELTOOL_ENABLE_MODULE_CHATSCAN",
                False,
            ),
        ):
            result = handle_fleet_composition_and_participation(pilots, ships)
            mock_get_fleet_composition.assert_called_once_with(
                pilots=pilots, ships=ships
            )
            self.assertEqual(result, (fleet_composition, None))


class TestParse(BaseTestCase):
    """
    Test cases for the parse function.
    """

    def test_raises_error_when_fleetcomp_module_disabled(self):
        with patch(
            "aa_intel_tool.parser.module.fleetcomp.AppSettings.INTELTOOL_ENABLE_MODULE_FLEETCOMP",
            False,
        ):
            with self.assertRaises(ParserError) as context:
                parse(scan_data=[])
            self.assertEqual(
                str(context.exception),
                "A parser error occurred » The fleet composition module is currently disabled.",
            )

    def test_parses_empty_scan_data_correctly(self):
        with (
            patch(
                "aa_intel_tool.parser.module.fleetcomp.AppSettings.INTELTOOL_ENABLE_MODULE_FLEETCOMP",
                True,
            ),
            patch(
                "aa_intel_tool.parser.module.fleetcomp.safe_scan_to_db"
            ) as mock_safe_scan_to_db,
            patch(
                "aa_intel_tool.parser.module.fleetcomp.handle_fleet_composition_and_participation",
                return_value=({"classes": [], "types": [], "pilots": []}, None),
            ),
        ):
            result = parse(scan_data=[])
            mock_safe_scan_to_db.assert_called_once_with(
                scan_type=Scan.Type.FLEETCOMP, parsed_data={}
            )
            self.assertEqual(result, mock_safe_scan_to_db.return_value)

    def test_parses_scan_data_with_valid_entries(self):
        scan_data = [
            "Rounon Dax\tJita\tOmen\tCruiser\tFleet Commander (Boss)\t5 - 5 - 5",
            "Arodem Artemis\tPerimeter\tLeopard\tShuttle\tSquad Member\t0 - 0 - 5\tWing 1 / Squad 1",
        ]
        fleet_composition = {
            "classes": [{"id": 1, "name": "Omen"}],
            "types": [{"id": 10, "name": "Cruiser"}],
            "pilots": [
                {"id": 101, "name": "Rounon Dax"},
                {"id": 102, "name": "Arodem Artemis"},
            ],
        }
        participation = {"pilots": {"section": ScanData.Section.PILOTLIST, "data": []}}
        expected_parsed = {
            "classes": {
                "section": ScanData.Section.SHIPLIST,
                "data": fleet_composition["classes"],
            },
            "shiptypes": {
                "section": ScanData.Section.SHIPTYPES,
                "data": fleet_composition["types"],
            },
            "pilots_flying": {
                "section": ScanData.Section.FLEETCOMPOSITION,
                "data": fleet_composition["pilots"],
            },
        }
        expected_parsed.update(participation)

        with (
            patch(
                "aa_intel_tool.parser.module.fleetcomp.AppSettings.INTELTOOL_ENABLE_MODULE_FLEETCOMP",
                True,
            ),
            patch(
                "aa_intel_tool.parser.module.fleetcomp.handle_fleet_composition_and_participation",
                return_value=(fleet_composition, participation),
            ),
            patch(
                "aa_intel_tool.parser.module.fleetcomp.safe_scan_to_db"
            ) as mock_safe_scan,
        ):
            mock_safe_scan.return_value = {"parsed": "data"}
            result = parse(scan_data=scan_data)
            mock_safe_scan.assert_called_once_with(
                scan_type=Scan.Type.FLEETCOMP, parsed_data=expected_parsed
            )
            self.assertEqual(result, mock_safe_scan.return_value)
