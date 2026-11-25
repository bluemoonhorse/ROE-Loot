# ROE Loot Table Studio — Python launcher

This is a local, offline loot-table editor. Python serves the included browser GUI on the loopback interface (`127.0.0.1`) and opens it in your default browser. The app uses only Python's standard library; it makes no internet requests and needs no pip packages. It does not depend on Tcl/Tk.

## Start

Double-click `Start ROE Loot Editor.cmd`, or run `py -3 roe_loot_editor.py` in this folder. Keep all files in this folder together. Close the command window to stop the local service.

## Editing and translations

- The item picker is populated from the bundled 167-item catalog, sorted by item category and ID. It shows the chosen English or Russian name according to the global language selector.
- The bundled seed has English and Russian translations for the catalog. In the contents table, expand **Translations & drop settings** to edit an item's English and Russian display names. Translation edits are saved in the project JSON.
- Loot JSON export writes English names into `strItemName` and known extra-item name fields. The project save preserves both languages.
- Import JSON, CSV, or XML; edit loot and vehicle groups, spawn settings, weights, and extra-item parameters; export project JSON or XML.
- **Save** persists a project under `%LOCALAPPDATA%\ROE Loot Table Studio Python\loot-project.json` and retains up to 20 rolling backups.

## Included data

`seed.json` is the starting table project. `item-catalog.json` and `roe-item-id-catalog.md` document item IDs and translations, including clearly marked uncertain identifications. Verify uncertain IDs and validate the exported JSON against the server's actual loader before deployment; the supplied scripts do not establish that exact schema.

