"""Born-red tests for scripts/check-config.py: each injects one fault and
asserts the check catches it. Run: python3 -m unittest discover -s scripts/tests
"""
import copy
import importlib.util
import unittest
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location("check_config", ROOT / "scripts/check-config.py")
cc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(cc)
CFG = yaml.safe_load((ROOT / "config/magnets.config.yaml").read_text())


class Config(unittest.TestCase):
    def assertCaught(self, mutate, words):
        cfg = copy.deepcopy(CFG)
        mutate(cfg)
        errs = cc.check_config(cfg)
        self.assertTrue(any(words in e for e in errs), f"expected {words!r} in {errs}")

    def test_real_config_passes(self):
        self.assertEqual(cc.check_config(copy.deepcopy(CFG)), [])

    def test_production_open(self):
        self.assertCaught(lambda c: c["environments"]["production"].update(enabled=True), "production is closed")

    def test_staging_not_stg(self):
        self.assertCaught(lambda c: c["environments"]["staging"].update(ow_base_url="https://ourwkrp.com"), "https://stg.")

    def test_secret_value(self):
        self.assertCaught(lambda c: c["api_sources"]["ose"].update(auth_secret="a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7"), "secret NAME")

    def test_unknown_source(self):
        self.assertCaught(lambda c: c["api_sources"].update(oer={"route_table": "x"}), "ose, ow and oaw only")

    def test_real_people_in_mocks(self):
        self.assertCaught(lambda c: c["mock_data"].update(people="real"), "synthetic_only")

    def test_floor_off_in_mocks(self):
        self.assertCaught(lambda c: c["mock_data"].update(counts_follow_under_5_floor=False), "under_5_floor")

    def test_coordinates_in_mocks(self):
        self.assertCaught(lambda c: c["mock_data"].update(location="lat_lng"), "place, not person")

    def test_dropping_never_contains(self):
        self.assertCaught(lambda c: c["mock_data"]["never_contains"].remove("ip_address"), "never_contains is missing")

    def test_extra_telemetry_field(self):
        self.assertCaught(lambda c: c["telemetry"]["allowed_fields"].append("operator_email"), "beyond the boundary doc")

    def test_telemetry_on_without_code(self):
        self.assertCaught(lambda c: c["telemetry"].update(enabled=True), "contract_only")

    def test_wrong_edge(self):
        self.assertCaught(lambda c: c["telemetry"].update(edge="E3"), "must be E4")

    def test_osm_deploying(self):
        self.assertCaught(lambda c: c["franchise"].update(deployment_handled_by="osm"), "OA does it")

    def test_copying_corridors(self):
        self.assertCaught(lambda c: c["franchise"].update(corridors_source="config/corridors.yaml"), "not a copy")

    def test_dropping_never_gated(self):
        self.assertCaught(lambda c: c["never_tier_gated"].remove("under_5_floor"), "never_tier_gated is missing")

    def test_wrong_side(self):
        self.assertCaught(lambda c: c["app"].update(side="named"), "anonymous side")


if __name__ == "__main__":
    unittest.main()
