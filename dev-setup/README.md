# Development setup

A single FAIR Data Point, seeded with one catalog and one dataset in basic DCAT-AP.
Useful for trying out `fairclient` against a real FDP.

## Usage

```sh
docker compose up
```

The `fdp-init` service installs `fairclient` from this checkout (the parent directory)
and uploads the test data once the FDP is up.

| Service    | URL                     |
| ---------- | ----------------------- |
| FDP client | <http://localhost:8081> |
| GraphDB    | <http://localhost:7201> |

FDP credentials: `albert.einstein@example.com` / `password`.

To reset, remove the volumes:

```sh
docker compose down -v
```

## Contents

- `fdp/application.yml` — FDP configuration.
- `fdp/data/` — the catalog and dataset uploaded at startup.
- `fdp/upload_data.py` — uploads them via `fairclient`.
- `graphdb/import/fdp/` — GraphDB repository config, preloaded before the FDP starts.

The dataset's `dct:isPartOf` carries a `__CATALOG_UUID__` placeholder that
`upload_data.py` replaces with the URI of the catalog it just created.

