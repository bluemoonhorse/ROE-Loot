# Loot JSON format and source scripts

## Are the scripts relevant?

Yes, as research and format references, but they do different jobs:

- `export_loot_tables_2022.py` reads the four extracted XML tables (`control`, `items`, `vehicle_control`, `vehicles`) and emits a JSON **research wrapper**. Each table is nested under metadata such as `path`, `sha256`, `object`, `map_id`, and `rows`; it also adds pool summaries, missing-pool information, and representation-conflict diagnostics. It reads XML, not `items.csv` as its input.
- `generate_loot_plan_2022.py` imports that exporter and produces H1/H2 **sample loot plans** (`input_points`, `entities`, quotas, and policy flags). Its output is a simulation result, not an editable table or a server-ready config.

The supplied files do not document the server's actual JSON loader contract. In particular, neither script proves that its output can be loaded directly by a production server.

## JSON handled by the desktop editor

The editor can import:

1. Its own project JSON, which contains four editable table arrays and the English/Russian translation map.
2. A clean four-table JSON object with top-level `control`, `items`, `vehicle_control`, and `vehicles` arrays.
3. The `export_loot_tables_2022.py` wrapper, where each of those tables contains a `rows` array.

It intentionally rejects H1/H2 placement plans as loot tables. They contain generated placements, not the four source tables.

**Export loot JSON** writes a compact table bundle:

```json
{
  "map_id": 16010,
  "control": [],
  "items": [],
  "vehicle_control": [],
  "vehicles": []
}
```

Each array contains the editable source rows. `source_line` analysis metadata is omitted. The `strItemName`, `strExtraItemName*`, and `strExtra2ItemName*` values are written in English when a catalog translation exists. **Export project** additionally preserves the editor's English/Russian translations for continued editing.

The compact output is a clear four-table JSON handoff, but the developer still needs to confirm that these top-level arrays and field names match the server loader. The app does not claim an undocumented production schema is verified.

## Items and experimental IDs

The item picker is built from IDs and names found in `items.csv`/the supplied JSON, plus the requested ID ranges and clearly marked user hypotheses. Existing IDs are grouped by item family and sorted numerically. `iCount` is shown as selection weight and `iStackCount` as stack quantity; the two extra-item areas allow per-option weight, number of packs, and units per pack.

IDs absent from the supplied CSV appear as experimental placeholders. AUG and SCAR-H do not have names or IDs in the supplied CSV, so no internal ID is assigned to either. The level-1 helmet (`200101`) and level-1 armor (`201001`) names are marked as inferred and should be checked with the developer. Experimental catalog entries are available for selection but are not automatically inserted into active loot groups.

The current user hypotheses include P90 at `103004`, one MG4 somewhere in `10602–10604`, 5.7×28 mm ammunition at `30005`, and possible .45-caliber ammunition in `30007` or `30008`; all remain unverified. `20001` and `20002` are possible Glock-17/USP-45 slots, but which ID is which is unknown. `30009` is tentatively named an RPG-7 round. The usual English term is **rocket-propelled grenade** or **RPG-7 round/projectile**, not “reactive grenade”; the Chinese source field remains ambiguous, so confirm this mapping before a server release. `70001` is labeled **Bandage** without inferring a pack size from its numeric ID.
