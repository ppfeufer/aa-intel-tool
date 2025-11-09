"""
Unit tests for the D-Scan parser module.
"""

# Standard Library
from unittest.mock import MagicMock, patch

# AA Intel Tool
from aa_intel_tool.exceptions import ParserError
from aa_intel_tool.models import Scan, ScanData
from aa_intel_tool.parser.module.dscan import (
    _get_ansiblex_jumpgate_destination,
    _get_deployables_on_grid,
    _get_scan_details,
    _get_ships,
    _get_starbases_on_grid,
    _get_type_info_dict,
    _get_upwell_structures_on_grid,
    _is_on_grid,
    parse,
)
from aa_intel_tool.tests import BaseTestCase


class TestParseDScan(BaseTestCase):
    """
    Testing the D-Scan parser
    """

    def test_raises_error_when_module_is_disabled(self):
        with patch(
            "aa_intel_tool.app_settings.AppSettings.INTELTOOL_ENABLE_MODULE_DSCAN",
            False,
        ):
            with self.assertRaises(ParserError) as context:
                parse(scan_data=[])

            self.assertEqual(
                str(context.exception),
                "A parser error occurred » The D-Scan module is currently disabled.",
            )

    def test_returns_empty_scan_when_no_data_provided(self):
        """
        Testing that an empty scan returns empty parsed data

        :return:
        :rtype:
        """

        with (
            patch(
                "aa_intel_tool.app_settings.AppSettings.INTELTOOL_ENABLE_MODULE_DSCAN",
                True,
            ),
            patch(
                "aa_intel_tool.parser.module.dscan._get_scan_details",
                return_value=(None, {}, {"all": []}),
            ),
            patch(
                "aa_intel_tool.parser.module.dscan.EveType.objects.bulk_get_or_create_esi",
                return_value=MagicMock(values_list=MagicMock(return_value=[])),
            ),
            patch(
                "aa_intel_tool.parser.module.dscan._get_ships",
                return_value={"all": [], "ongrid": [], "offgrid": [], "types": []},
            ),
            patch(
                "aa_intel_tool.parser.module.dscan._get_upwell_structures_on_grid",
                return_value={"all": [], "ongrid": [], "offgrid": [], "types": []},
            ),
            patch(
                "aa_intel_tool.parser.module.dscan._get_deployables_on_grid",
                return_value={"all": [], "ongrid": [], "offgrid": [], "types": []},
            ),
            patch(
                "aa_intel_tool.parser.module.dscan._get_starbases_on_grid",
                return_value={"all": [], "ongrid": [], "offgrid": [], "types": []},
            ),
            patch(
                "aa_intel_tool.parser.module.dscan.safe_scan_to_db"
            ) as mock_safe_scan_to_db,
        ):
            result = parse(scan_data=[])

            expected_parsed = {
                "structures_on_grid": {
                    "section": ScanData.Section.STRUCTURES_ON_GRID,
                    "data": {"all": [], "ongrid": [], "offgrid": [], "types": []},
                },
                "deployables": {
                    "section": ScanData.Section.DEPLOYABLES_ON_GRID,
                    "data": {"all": [], "ongrid": [], "offgrid": [], "types": []},
                },
                "starbases": {
                    "section": ScanData.Section.STARBASES_ON_GRID,
                    "data": {"all": [], "ongrid": [], "offgrid": [], "types": []},
                },
            }

            mock_safe_scan_to_db.assert_called_once_with(
                scan_type=Scan.Type.DSCAN, parsed_data=expected_parsed
            )
            self.assertEqual(result, mock_safe_scan_to_db.return_value)

    def test_parses_scan_data_correctly(self):
        """
        Testing that scan data is parsed correctly

        :return:
        :rtype:
        """

        with (
            patch(
                "aa_intel_tool.app_settings.AppSettings.INTELTOOL_ENABLE_MODULE_DSCAN",
                True,
            ),
            patch(
                "aa_intel_tool.parser.module.dscan._get_scan_details",
                return_value=("Destination", {"all": {1: 2}}, {"all": [1]}),
            ),
            patch(
                "aa_intel_tool.parser.module.dscan.EveType.objects.bulk_get_or_create_esi"
            ) as mock_bulk_get,
            patch(
                "aa_intel_tool.parser.module.dscan._get_ships",
                return_value={
                    "all": ["ship1"],
                    "ongrid": [],
                    "offgrid": [],
                    "types": [],
                },
            ),
            patch(
                "aa_intel_tool.parser.module.dscan._get_upwell_structures_on_grid",
                return_value=[],
            ),
            patch(
                "aa_intel_tool.parser.module.dscan._get_deployables_on_grid",
                return_value=[],
            ),
            patch(
                "aa_intel_tool.parser.module.dscan._get_starbases_on_grid",
                return_value=[],
            ),
            patch(
                "aa_intel_tool.parser.module.dscan.safe_scan_to_db"
            ) as mock_safe_scan_to_db,
        ):
            mock_bulk_get.return_value.values_list.return_value = [
                (1, "Ship", 2, "Group", 1000)
            ]

            result = parse(scan_data=["some data"])

            mock_safe_scan_to_db.assert_called_once_with(
                scan_type=Scan.Type.DSCAN,
                parsed_data={
                    "all": {"section": ScanData.Section.SHIPLIST, "data": ["ship1"]},
                },
            )
            self.assertEqual(result, mock_safe_scan_to_db.return_value)


class TestHelperGetScanDetails(BaseTestCase):
    """
    Testing the _get_scan_details helper function
    """

    def test_returns_correct_details_for_valid_scan_data(self):
        """
        Testing that correct details are returned for valid scan data

        :return:
        :rtype:
        """

        scan_data = [
            "123\tShip Name\tShip Class\t10 km",
            "456\tStructure Name\tStructure Type\t100 km",
        ]

        with patch(
            "aa_intel_tool.parser.module.dscan._is_on_grid",
            side_effect=[True, False],
        ):
            ansiblex_destination, counter, eve_ids = _get_scan_details(
                scan_data=scan_data
            )

            self.assertIsNone(ansiblex_destination)
            self.assertEqual(counter["all"], {123: 1, 456: 1})
            self.assertEqual(counter["ongrid"], {123: 1})
            self.assertEqual(counter["offgrid"], {456: 1})
            self.assertEqual(eve_ids["all"], [123, 456])
            self.assertEqual(eve_ids["ongrid"], [123])
            self.assertEqual(eve_ids["offgrid"], [456])

    def test_handles_empty_scan_data(self):
        """
        Testing that empty scan data is handled correctly

        :return:
        :rtype:
        """

        scan_data = []

        ansiblex_destination, counter, eve_ids = _get_scan_details(scan_data=scan_data)

        self.assertIsNone(ansiblex_destination)
        self.assertEqual(counter.get("all", {}), {})
        self.assertEqual(counter.get("ongrid", {}), {})
        self.assertEqual(counter.get("offgrid", {}), {})
        self.assertEqual(eve_ids.get("all", []), [])
        self.assertEqual(eve_ids.get("ongrid", []), [])
        self.assertEqual(eve_ids.get("offgrid", []), [])

    def test_raises_error_for_invalid_scan_data_format(self):
        """
        Testing that an error is raised for invalid scan data format

        :return:
        :rtype:
        """

        scan_data = ["Invalid Data"]

        with self.assertRaises(AttributeError):
            _get_scan_details(scan_data=scan_data)

    def test_detects_ansiblex_jump_gate_destination(self):
        scan_data = [
            "35841\tC-N4OD » Jita - Der Geile Springen\tAnsiblex Jump Bridge\t2,748 km"
        ]

        ansiblex_destination, counter, eve_ids = _get_scan_details(scan_data=scan_data)

        self.assertEqual(ansiblex_destination, "Jita")
        self.assertEqual(counter["all"], {35841: 1})
        self.assertEqual(counter["ongrid"], {35841: 1})
        self.assertEqual(eve_ids["all"], [35841])
        self.assertEqual(eve_ids["ongrid"], [35841])


class TestHelperGetAnsiblexJumpgateDestination(BaseTestCase):
    """
    Testing the _get_ansiblex_jumpgate_destination helper function
    """

    def test_returns_correct_destination_for_valid_ansiblex_name(self):
        """
        Testing that correct destination is returned for valid Ansiblex jumpgate name

        :return:
        :rtype:
        """

        ansiblex_name = "C-N4OD » Jita - Der Geile Springen"

        result = _get_ansiblex_jumpgate_destination(ansiblex_name)

        self.assertEqual(result, "Jita")

    def test_handles_invalid_ansiblex_name_format(self):
        """
        Testing that invalid Ansiblex name format is handled

        :return:
        :rtype:
        """

        ansiblex_name = "Invalid Name Format"

        with self.assertRaises(IndexError):
            _get_ansiblex_jumpgate_destination(ansiblex_name)


class TestHelperGetStarbasesOnGrid(BaseTestCase):
    """
    Testing the _get_starbases_on_grid helper function
    """

    def test_returns_starbases_on_grid_with_valid_data(self):
        """
        Testing that starbases on grid are returned with valid data

        :return:
        :rtype:
        """

        eve_types = [
            (1, "Starbase Alpha", 100, "Starbase Group", 0),
            (2, "Starbase Beta", 101, "Starbase Group", 0),
        ]
        counter = {"ongrid": {1: 2, 2: 1}}

        eve_types_qs = MagicMock()
        eve_types_qs.filter.return_value = eve_types

        with patch(
            "aa_intel_tool.parser.module.dscan._get_type_info_dict"
        ) as mock_type_info:
            mock_type_info.side_effect = lambda eve_type: {
                "id": eve_type[0],
                "name": eve_type[1],
                "type_id": eve_type[2],
                "type_name": eve_type[3],
                "image": f"url/{eve_type[0]}",
            }

            result = _get_starbases_on_grid(eve_types=eve_types_qs, counter=counter)

            self.assertEqual(len(result), 2)
            self.assertEqual(result[0]["name"], "Starbase Alpha")
            self.assertEqual(result[0]["count"], 2)
            self.assertEqual(result[1]["name"], "Starbase Beta")
            self.assertEqual(result[1]["count"], 1)

    def test_returns_empty_list_when_no_starbases_on_grid(self):
        """
        Testing that an empty list is returned when no starbases are on grid

        :return:
        :rtype:
        """

        eve_types = [
            (1, "Starbase Alpha", 100, "Starbase Group", 0),
            (2, "Starbase Beta", 101, "Starbase Group", 0),
        ]
        counter = {"ongrid": {}}

        eve_types_qs = MagicMock()
        eve_types_qs.filter.return_value = eve_types

        result = _get_starbases_on_grid(eve_types=eve_types_qs, counter=counter)

        self.assertEqual(result, [])

    def test_ignores_starbases_not_on_grid(self):
        """
        Testing that starbases not on grid are ignored

        :return:
        :rtype:
        """

        eve_types = [
            (1, "Starbase Alpha", 100, "Starbase Group", 0),
            (2, "Starbase Beta", 101, "Starbase Group", 0),
        ]
        counter = {"ongrid": {1: 2}}

        eve_types_qs = MagicMock()
        eve_types_qs.filter.return_value = eve_types

        with patch(
            "aa_intel_tool.parser.module.dscan._get_type_info_dict"
        ) as mock_type_info:
            mock_type_info.side_effect = lambda eve_type: {
                "id": eve_type[0],
                "name": eve_type[1],
                "type_id": eve_type[2],
                "type_name": eve_type[3],
                "image": f"url/{eve_type[0]}",
            }

            result = _get_starbases_on_grid(eve_types=eve_types_qs, counter=counter)

            self.assertEqual(len(result), 1)
            self.assertEqual(result[0]["name"], "Starbase Alpha")
            self.assertEqual(result[0]["count"], 2)


class TestHelperGetDeployablesOnGrid(BaseTestCase):
    """
    Testing the _get_deployables_on_grid helper function
    """

    def test_returns_deployables_on_grid_with_valid_data(self):
        """
        Testing that deployables on grid are returned with valid data

        :return:
        :rtype:
        """

        eve_types = [
            (1, "Deployable Alpha", 200, "Deployable Group", 0),
            (2, "Deployable Beta", 201, "Deployable Group", 0),
        ]
        counter = {"ongrid": {1: 3, 2: 1}}

        eve_types_qs = MagicMock()
        eve_types_qs.filter.return_value = eve_types

        with patch(
            "aa_intel_tool.parser.module.dscan._get_type_info_dict"
        ) as mock_type_info:
            mock_type_info.side_effect = lambda eve_type: {
                "id": eve_type[0],
                "name": eve_type[1],
                "type_id": eve_type[2],
                "type_name": eve_type[3],
                "image": f"url/{eve_type[0]}",
            }

            result = _get_deployables_on_grid(eve_types=eve_types_qs, counter=counter)

            self.assertEqual(len(result), 2)
            self.assertEqual(result[0]["name"], "Deployable Alpha")
            self.assertEqual(result[0]["count"], 3)
            self.assertEqual(result[1]["name"], "Deployable Beta")
            self.assertEqual(result[1]["count"], 1)

    def test_returns_empty_list_when_no_deployables_on_grid(self):
        """
        Testing that an empty list is returned when no deployables are on grid

        :return:
        :rtype:
        """

        eve_types = [
            (1, "Deployable Alpha", 200, "Deployable Group", 0),
            (2, "Deployable Beta", 201, "Deployable Group", 0),
        ]
        counter = {"ongrid": {}}

        eve_types_qs = MagicMock()
        eve_types_qs.filter.return_value = eve_types

        result = _get_deployables_on_grid(eve_types=eve_types_qs, counter=counter)

        self.assertEqual(result, [])

    def test_ignores_deployables_not_on_grid(self):
        """
        Testing that deployables not on grid are ignored

        :return:
        :rtype:
        """

        eve_types = [
            (1, "Deployable Alpha", 200, "Deployable Group", 0),
            (2, "Deployable Beta", 201, "Deployable Group", 0),
        ]
        counter = {"ongrid": {1: 2}}

        eve_types_qs = MagicMock()
        eve_types_qs.filter.return_value = eve_types

        with patch(
            "aa_intel_tool.parser.module.dscan._get_type_info_dict"
        ) as mock_type_info:
            mock_type_info.side_effect = lambda eve_type: {
                "id": eve_type[0],
                "name": eve_type[1],
                "type_id": eve_type[2],
                "type_name": eve_type[3],
                "image": f"url/{eve_type[0]}",
            }

            result = _get_deployables_on_grid(eve_types=eve_types_qs, counter=counter)

            self.assertEqual(len(result), 1)
            self.assertEqual(result[0]["name"], "Deployable Alpha")
            self.assertEqual(result[0]["count"], 2)


class TestHelperGetUpwellStructuresOnGrid(BaseTestCase):
    """
    Testing the _get_upwell_structures_on_grid helper function
    """

    def test_returns_upwell_structures_on_grid_with_valid_data(self):
        """
        Testing that upwell structures on grid are returned with valid data

        :return:
        :rtype:
        """

        eve_types = [
            (1, "Structure Alpha", 300, "Structure Group", 0),
            (2, "Structure Beta", 301, "Structure Group", 0),
        ]
        counter = {"ongrid": {1: 2, 2: 1}}
        ansiblex_destination = "System XYZ"

        eve_types_qs = MagicMock()
        eve_types_qs.filter.return_value = eve_types

        with patch(
            "aa_intel_tool.parser.module.dscan._get_type_info_dict"
        ) as mock_type_info:
            mock_type_info.side_effect = lambda eve_type: {
                "id": eve_type[0],
                "name": eve_type[1],
                "type_id": eve_type[2],
                "type_name": eve_type[3],
                "image": f"url/{eve_type[0]}",
            }

            result = _get_upwell_structures_on_grid(
                eve_types=eve_types_qs,
                counter=counter,
                ansiblex_destination=ansiblex_destination,
            )

            self.assertEqual(len(result), 2)
            self.assertEqual(result[0]["name"], "Structure Alpha")
            self.assertEqual(result[1]["name"], "Structure Beta")

    def test_returns_empty_list_when_no_upwell_structures_on_grid(self):
        """
        Testing that an empty list is returned when no upwell structures are on grid

        :return:
        :rtype:
        """

        eve_types = [
            (1, "Structure Alpha", 300, "Structure Group", 0),
            (2, "Structure Beta", 301, "Structure Group", 0),
        ]
        counter = {"ongrid": {}}

        eve_types_qs = MagicMock()
        eve_types_qs.filter.return_value = eve_types

        result = _get_upwell_structures_on_grid(eve_types=eve_types_qs, counter=counter)

        self.assertEqual(result, [])

    def test_handles_ansiblex_jump_gate_with_destination(self):
        """
        Testing that Ansiblex jump gate with destination is handled

        :return:
        :rtype:
        """

        eve_types = [
            (35841, "Ansiblex Jump Gate", 400, "Structure Group", 0),
        ]
        counter = {"ongrid": {35841: 1}}
        ansiblex_destination = "System ABC"

        eve_types_qs = MagicMock()
        eve_types_qs.filter.return_value = eve_types

        with patch(
            "aa_intel_tool.parser.module.dscan._get_type_info_dict"
        ) as mock_type_info:
            mock_type_info.side_effect = lambda eve_type: {
                "id": eve_type[0],
                "name": eve_type[1],
                "type_id": eve_type[2],
                "type_name": eve_type[3],
                "image": f"url/{eve_type[0]}",
            }

            result = _get_upwell_structures_on_grid(
                eve_types=eve_types_qs,
                counter=counter,
                ansiblex_destination=ansiblex_destination,
            )

            self.assertEqual(len(result), 1)
            self.assertEqual(result[0]["name"], "Ansiblex Jump Gate » System ABC")


class TestHelperGetShips(BaseTestCase):
    """
    Testing the _get_ships helper function
    """

    def test_returns_all_ships_with_valid_data(self):
        """
        Testing that all ships are returned with valid data

        :return:
        :rtype:
        """

        eve_types = [
            (1, "Ship Alpha", 100, "Frigate", 500),
            (2, "Ship Beta", 101, "Destroyer", 1000),
        ]
        counter = {"all": {1: 3, 2: 2}, "ongrid": {1: 2}, "offgrid": {2: 1}}

        eve_types_qs = MagicMock()
        eve_types_qs.filter.return_value = eve_types

        with patch(
            "aa_intel_tool.parser.module.dscan._get_type_info_dict"
        ) as mock_type_info:
            mock_type_info.side_effect = lambda eve_type: {
                "id": eve_type[0],
                "name": eve_type[1],
                "type_id": eve_type[2],
                "type_name": eve_type[3],
                "image": f"url/{eve_type[0]}",
            }

            result = _get_ships(eve_types=eve_types_qs, counter=counter)

            self.assertEqual(len(result["all"]), 2)
            self.assertEqual(result["all"][0]["name"], "Ship Alpha")
            self.assertEqual(result["all"][0]["count"], 3)
            self.assertEqual(result["all"][0]["mass"], 1500)
            self.assertEqual(result["all"][1]["name"], "Ship Beta")
            self.assertEqual(result["all"][1]["count"], 2)
            self.assertEqual(result["all"][1]["mass"], 2000)

    def test_returns_empty_lists_when_no_ships(self):
        """
        Testing that empty lists are returned when no ships are present

        :return:
        :rtype:
        """

        eve_types = []
        counter = {"all": {}, "ongrid": {}, "offgrid": {}}

        eve_types_qs = MagicMock()
        eve_types_qs.filter.return_value = eve_types

        result = _get_ships(eve_types=eve_types_qs, counter=counter)

        self.assertEqual(result["all"], [])
        self.assertEqual(result["ongrid"], [])
        self.assertEqual(result["offgrid"], [])
        self.assertEqual(result["types"], [])

    def test_separates_ships_into_correct_categories(self):
        """
        Testing that ships are separated into correct categories

        :return:
        :rtype:
        """

        eve_types = [
            (1, "Ship Alpha", 100, "Frigate", 500),
            (2, "Ship Beta", 101, "Destroyer", 1000),
        ]
        counter = {
            "all": {1: 3, 2: 2},
            "ongrid": {1: 2},
            "offgrid": {2: 1},
        }

        eve_types_qs = MagicMock()
        eve_types_qs.filter.return_value = eve_types

        with patch(
            "aa_intel_tool.parser.module.dscan._get_type_info_dict"
        ) as mock_type_info:
            mock_type_info.side_effect = lambda eve_type: {
                "id": eve_type[0],
                "name": eve_type[1],
                "type_id": eve_type[2],
                "type_name": eve_type[3],
                "image": f"url/{eve_type[0]}",
            }

            result = _get_ships(eve_types=eve_types_qs, counter=counter)

            self.assertEqual(len(result["ongrid"]), 1)
            self.assertEqual(result["ongrid"][0]["name"], "Ship Alpha")
            self.assertEqual(result["ongrid"][0]["count"], 2)
            self.assertEqual(len(result["offgrid"]), 1)
            self.assertEqual(result["offgrid"][0]["name"], "Ship Beta")
            self.assertEqual(result["offgrid"][0]["count"], 1)

    def test_aggregates_ship_types_correctly(self):
        """
        Testing that ship types are aggregated correctly

        :return:
        :rtype:
        """

        eve_types = [
            (1, "Ship Alpha", 100, "Frigate", 500),
            (2, "Ship Beta", 101, "Frigate", 1000),
        ]
        counter = {"all": {1: 3, 2: 2}, "ongrid": {}, "offgrid": {}}

        eve_types_qs = MagicMock()
        eve_types_qs.filter.return_value = eve_types

        with patch(
            "aa_intel_tool.parser.module.dscan._get_type_info_dict"
        ) as mock_type_info:
            mock_type_info.side_effect = lambda eve_type: {
                "id": eve_type[0],
                "name": eve_type[1],
                "type_id": eve_type[2],
                "type_name": eve_type[3],
                "image": f"url/{eve_type[0]}",
            }

            result = _get_ships(eve_types=eve_types_qs, counter=counter)

            self.assertEqual(len(result["types"]), 1)
            self.assertEqual(result["types"][0]["name"], "Frigate")
            self.assertEqual(result["types"][0]["count"], 5)


class TestHelperGetTypeInfoDict(BaseTestCase):
    """
    Testing the _get_type_info_dict helper function
    """

    def test_returns_correct_dict_for_valid_eve_type(self):
        """
        Testing that correct dict is returned for valid eve type

        :return:
        :rtype:
        """
        eve_type = (123, "Test Ship", 456, "Test Group")

        result = _get_type_info_dict(eve_type)

        self.assertEqual(result["id"], 123)
        self.assertEqual(result["name"], "Test Ship")
        self.assertEqual(result["type_id"], 456)
        self.assertEqual(result["type_name"], "Test Group")
        self.assertIn(str(123), result["image"])

    def test_handles_empty_eve_type_tuple(self):
        """
        Testing that empty eve type tuple is handled

        :return:
        :rtype:
        """

        eve_type = ()

        with self.assertRaises(IndexError):
            _get_type_info_dict(eve_type)

    def test_handles_partial_eve_type_tuple(self):
        """
        Testing that partial eve type tuple is handled

        :return:
        :rtype:
        """

        eve_type = (123, "Test Ship")

        with self.assertRaises(IndexError):
            _get_type_info_dict(eve_type)

    def test_handles_non_integer_id_in_eve_type(self):
        """
        Testing that non-integer ID in eve type is handled

        :return:
        :rtype:
        """

        eve_type = ("abc", "Test Ship", 456, "Test Group")

        with self.assertRaises(ValueError):
            _get_type_info_dict(eve_type)


class TestHelperIsOnGrid(BaseTestCase):
    """
    Testing the _is_on_grid helper function
    """

    def test_returns_true_for_distance_within_grid_size(self):
        """
        Testing that true is returned for distance within grid size

        :return:
        :rtype:
        """

        with patch(
            "aa_intel_tool.app_settings.AppSettings.INTELTOOL_DSCAN_GRID_SIZE", 150
        ):
            self.assertTrue(_is_on_grid("100 km"))

    def test_returns_false_for_distance_exceeding_grid_size(self):
        """
        Testing that false is returned for distance exceeding grid size

        :return:
        :rtype:
        """

        with patch(
            "aa_intel_tool.app_settings.AppSettings.INTELTOOL_DSCAN_GRID_SIZE", 150
        ):
            self.assertFalse(_is_on_grid("200 km"))

    def test_returns_false_for_invalid_distance_format(self):
        """
        Testing that false is returned for invalid distance format

        :return:
        :rtype:
        """

        self.assertFalse(_is_on_grid("invalid distance"))

    def test_returns_false_for_empty_distance_string(self):
        """
        Testing that false is returned for empty distance string

        :return:
        :rtype:
        """

        self.assertFalse(_is_on_grid(""))
