# ourSharedMagnets config

`magnets.config.yaml` is the one config file for the developer and franchise layer. It says:

- which product APIs OSM documents and tests, and where each product's route table and Bruno collections live (the product stays the source of truth);
- that collections run against staging, and production stays off until Matt opens it;
- what mock and demo data may hold: synthetic people only, the under-5 floor, place as an H3 cell, never a real person's details;
- the only fields OSM may ever send to ourEventRings (edge E4, boundary doc 4.4), switched off until OSM has code;
- where the franchise knowledge lives, and that ourAirwaves, not OSM, runs a deployment and holds a client's tier.

Secrets are named, never pasted.

## Check it

```bash
pip install pyyaml
python3 scripts/check-config.py
python3 scripts/check-config.py --brain ../OCR-docs/ocr-docs-brain
python3 -m unittest discover -s scripts/tests
```

The same runs on every pull request that touches `config/` or `scripts/` (`.github/workflows/config-check.yml`).
