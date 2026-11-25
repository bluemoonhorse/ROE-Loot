# ROE item ID catalog

English display names for item IDs found in the supplied `items.csv`/JSON, plus the requested experimental ID ranges. `Source status` distinguishes names/IDs present in the CSV from inferred or placeholder entries. This catalog is for the editor; it does not assert every listed ID is valid in a live server build.

## AUG and SCAR-H

Neither AUG nor SCAR-H appears as a named row in the supplied `items.csv`, and that CSV does not provide their IDs. A [Ring of Elysium community guide](https://steamcommunity.com/sharedfiles/filedetails/?id=1574895499) lists the AUG as an in-game weapon; a [historical ROE weapon wiki page](https://seore.org/raw/%EB%AC%B8%EC%84%9C%3ARing%20of%20Elysium/%EB%AC%B4%EA%B8%B0) describes SCAR-H as tentative/bugged. Neither source ties either weapon to these loot-table IDs. IDs 10207, 10209, and 10210 are therefore kept as unassigned experimental assault-rifle placeholders. Confirm their mappings with the developer before adding them to a server table.

## Catalog


### Sniper rifles

| ID | English name | Source status |
| --- | --- | --- |
| 10101 | R700 sniper rifle | Present in supplied items.csv |
| 10102 | Mosin–Nagant rifle | Present in supplied items.csv |
| 10103 | Unidentified sniper rifle · experimental ID 10103 | Experimental placeholder; absent from supplied items.csv |
| 10104 | G28 marksman rifle | Present in supplied items.csv |
| 10105 | VKS .50 rifle | Present in supplied items.csv |
| 10106 | Unidentified sniper rifle · experimental ID 10106 | Experimental placeholder; absent from supplied items.csv |
| 10107 | MK12 marksman rifle | Present in supplied items.csv |
| 10108 | Unidentified sniper rifle · experimental ID 10108 | Experimental placeholder; absent from supplied items.csv |
| 10109 | Unidentified sniper rifle · experimental ID 10109 | Experimental placeholder; absent from supplied items.csv |
| 10110 | FAL rifle | Present in supplied items.csv |

### Assault rifles

| ID | English name | Source status |
| --- | --- | --- |
| 10201 | M4A1 assault rifle | Present in supplied items.csv |
| 10202 | AK-47 assault rifle | Present in supplied items.csv |
| 10203 | AK-15 assault rifle | Present in supplied items.csv |
| 10204 | LVOA assault rifle | Present in supplied items.csv |
| 10205 | Groza assault rifle | Present in supplied items.csv |
| 10206 | FAMAS assault rifle | Present in supplied items.csv |
| 10207 | Unidentified assault rifle · experimental ID 10207 | Unassigned experimental AR ID; absent from supplied items.csv; do not assume AUG/SCAR-H mapping |
| 10208 | G36 assault rifle | Present in supplied items.csv |
| 10209 | Unidentified assault rifle · experimental ID 10209 | Unassigned experimental AR ID; absent from supplied items.csv; do not assume AUG/SCAR-H mapping |
| 10210 | Unidentified assault rifle · experimental ID 10210 | Unassigned experimental AR ID; absent from supplied items.csv; do not assume AUG/SCAR-H mapping |

### Submachine guns

| ID | English name | Source status |
| --- | --- | --- |
| 10301 | MP5 submachine gun | Present in supplied items.csv |
| 10302 | Unidentified submachine gun · experimental ID 10302 | Experimental placeholder; absent from supplied items.csv |
| 10303 | Vector submachine gun | Present in supplied items.csv |
| 10304 | P90 submachine gun (hypothesis; verify ID) · experimental ID 10304 | P90 candidate per user note; ID not present in supplied CSV, verify |
| 10305 | MPX submachine gun | Present in supplied items.csv |
| 10306 | Scorpion submachine gun | Present in supplied items.csv |
 |  |  |

### Shotguns

| ID | English name | Source status |
| --- | --- | --- |
| 10401 | R870 shotgun | Present in supplied items.csv |
| 10402 | Citori shotgun | Present in supplied items.csv |
| 10403 | Fostech Origin-12 shotgun | Present in supplied items.csv |

### Machine guns and launchers

| ID | English name | Source status |
| --- | --- | --- |
| 10601 | PKM light machine gun | Present in supplied items.csv |
| 10602 | Unidentified machine gun/launcher · possible MG4; ID unconfirmed | Absent from supplied CSV; one of 10602–10604 may be MG4, exact ID unverified |
| 10603 | Unidentified machine gun/launcher · possible MG4; ID unconfirmed | Absent from supplied CSV; one of 10602–10604 may be MG4, exact ID unverified |
| 10604 | Unidentified machine gun/launcher · possible MG4; ID unconfirmed | Absent from supplied CSV; one of 10602–10604 may be MG4, exact ID unverified |
| 10605 | Rocket launcher | Present in supplied items.csv |

### Pistols

| ID | English name | Source status |
| --- | --- | --- |
| 20001 | Unassigned pistol · candidate Glock-17 or USP-45; mapping unknown | Pistol ID present only as a proposed slot; Glock-17 vs USP-45 mapping unknown |
| 20002 | Unassigned pistol · candidate Glock-17 or USP-45; mapping unknown | Pistol ID present only as a proposed slot; Glock-17 vs USP-45 mapping unknown |
| 20003 | Desert Eagle pistol (.50) | Present in supplied items.csv |

### Helmets

| ID | English name | Source status |
| --- | --- | --- |
| 200101 | Level 1 helmet (inferred; verify) | Inferred level-1 gear ID; absent from supplied items.csv; verify |
| 200102 | Level 2 helmet | Present in supplied items.csv |
| 200103 | Level 3 helmet | Present in supplied items.csv |

### Body armor

| ID | English name | Source status |
| --- | --- | --- |
| 201001 | Level 1 body armor (inferred; verify) | Inferred level-1 gear ID; absent from supplied items.csv; verify |
| 201002 | Level 2 body armor | Present in supplied items.csv |
| 201003 | Level 3 body armor | Present in supplied items.csv |

### Ammunition and ordnance

| ID | English name | Source status |
| --- | --- | --- |
| 30001 | 5.56 mm ammunition | Present in supplied items.csv |
| 30002 | 7.62 mm ammunition | Present in supplied items.csv |
| 30003 | 9 mm ammunition | Present in supplied items.csv |
| 30004 | 12-gauge shells | Present in supplied items.csv |
| 30005 | 5.7×28 mm ammunition (hypothesis; verify) | 5.7×28 mm ammunition hypothesis; absent from supplied CSV, verify |
| 30006 | .50-caliber ammunition pack (10 rounds) | Present in supplied items.csv |
| 30007 | .45-caliber ammunition candidate (hypothesis; verify) | .45-caliber ammunition candidate; exact ID/name unknown |
| 30008 | .45-caliber ammunition candidate (hypothesis; verify) | .45-caliber ammunition candidate; exact ID/name unknown |
| 30009 | RPG-7 rocket-propelled grenade round | RPG-7 round hypothesis; CSV source name 火箭筒 is ambiguous, verify |

### Muzzle and barrel attachments

| ID | English name | Source status |
| --- | --- | --- |
| 40101 | Sniper-rifle suppressor | Present in supplied items.csv |
| 40102 | Unidentified muzzle/barrel attachment · experimental ID 40102 | Experimental placeholder; absent from supplied items.csv |
| 40103 | Rifle suppressor | Present in supplied items.csv |
| 40104 | Rifle compensator | Present in supplied items.csv |
| 40105 | SMG suppressor | Present in supplied items.csv |
| 40106 | SMG compensator | Present in supplied items.csv |
| 40107 | Shotgun choke | Present in supplied items.csv |
| 40108 | SMG flash hider | Present in supplied items.csv |
| 40109 | Sniper-rifle flash hider | Present in supplied items.csv |
| 40110 | Rifle flash hider | Present in supplied items.csv |
| 40111 | Sniper-rifle compensator | Present in supplied items.csv |
| 40112 | Extended barrel | Present in supplied items.csv |

### Foregrips

| ID | English name | Source status |
| --- | --- | --- |
| 40201 | Angled foregrip | Present in supplied items.csv |
| 40202 | Vertical foregrip | Present in supplied items.csv |

### Optics

| ID | English name | Source status |
| --- | --- | --- |
| 40301 | Unidentified optic · experimental ID 40301 | Experimental placeholder; absent from supplied items.csv |
| 40302 | 8× scope | Present in supplied items.csv |
| 40303 | 4× scope | Present in supplied items.csv |
| 40304 | 2× scope | Present in supplied items.csv |
| 40305 | Red-dot sight | Present in supplied items.csv |
| 40306 | Holographic sight | Present in supplied items.csv |

### Magazines

| ID | English name | Source status |
| --- | --- | --- |
| 40401 | Sniper-rifle extended magazine | Present in supplied items.csv |
| 40402 | Unidentified magazine · experimental ID 40402 | Experimental placeholder; absent from supplied items.csv |
| 40403 | Rifle extended magazine | Present in supplied items.csv |
| 40404 | Unidentified magazine · experimental ID 40404 | Experimental placeholder; absent from supplied items.csv |
| 40405 | SMG extended magazine | Present in supplied items.csv |

### Stocks

| ID | English name | Source status |
| --- | --- | --- |
| 40501 | Unidentified stock · experimental ID 40501 | Experimental placeholder; absent from supplied items.csv |
| 40502 | Tactical stock (M4/LVOA) | Present in supplied items.csv |

### Grenades

| ID | English name | Source status |
| --- | --- | --- |
| 50001 | Frag grenade | Present in supplied items.csv |
| 50002 | Smoke grenade | Present in supplied items.csv |
| 50003 | Flash grenade | Present in supplied items.csv |

### Healing items

| ID | English name | Source status |
| --- | --- | --- |
| 70001 | Bandage | Present in supplied items.csv |
| 70002 | First-aid kit | Present in supplied items.csv |
| 70003 | Medical kit | Present in supplied items.csv |

### Documents and event items

| ID | English name | Source status |
| --- | --- | --- |
| 90101 | Sheriff note · 01 | Present in supplied items.csv |
| 90102 | Sheriff note · 02 | Present in supplied items.csv |
| 90103 | Sheriff note · 03 | Present in supplied items.csv |
| 90104 | Sheriff note · 04 | Present in supplied items.csv |
| 90105 | Sheriff note · 05 | Present in supplied items.csv |
| 90106 | Sheriff note · 06 | Present in supplied items.csv |
| 90107 | Sheriff note · 07 | Present in supplied items.csv |
| 90108 | Sheriff note · 08 | Present in supplied items.csv |
| 90109 | Sheriff note · 09 | Present in supplied items.csv |
| 90110 | Sheriff note · 10 | Present in supplied items.csv |
| 90111 | Sheriff note · 11 | Present in supplied items.csv |
| 90112 | Sheriff note · 12 | Present in supplied items.csv |
| 90113 | Sheriff note · 13 | Present in supplied items.csv |
| 90114 | Sheriff note · 14 | Present in supplied items.csv |
| 90201 | Newspaper · 01 | Present in supplied items.csv |
| 90202 | Newspaper · 02 | Present in supplied items.csv |
| 90203 | Newspaper · 03 | Present in supplied items.csv |
| 90204 | Newspaper · 04 | Present in supplied items.csv |
| 90205 | Newspaper · 05 | Present in supplied items.csv |
| 90206 | Newspaper · 06 | Present in supplied items.csv |
| 90207 | Newspaper · 07 | Present in supplied items.csv |
| 90208 | Newspaper · 08 | Present in supplied items.csv |
| 90209 | Newspaper · 09 | Present in supplied items.csv |
| 90210 | Newspaper · 10 | Present in supplied items.csv |
| 90211 | Newspaper · 11 | Present in supplied items.csv |
| 90212 | Newspaper · 12 | Present in supplied items.csv |
| 90213 | Newspaper · 13 | Present in supplied items.csv |
| 90214 | Newspaper · 14 | Present in supplied items.csv |
| 90215 | Newspaper · 15 | Present in supplied items.csv |
| 90216 | Newspaper · 16 | Present in supplied items.csv |
| 90217 | Newspaper · 17 | Present in supplied items.csv |
| 90218 | Newspaper · 18 | Present in supplied items.csv |
| 90219 | Newspaper · 19 | Present in supplied items.csv |
| 90220 | Newspaper · 20 | Present in supplied items.csv |
| 90301 | Diary fragment · 01 | Present in supplied items.csv |
| 90302 | Diary fragment · 02 | Present in supplied items.csv |
| 90303 | Diary fragment · 03 | Present in supplied items.csv |
| 90304 | Diary fragment · 04 | Present in supplied items.csv |
| 90305 | Diary fragment · 05 | Present in supplied items.csv |
| 90306 | Diary fragment · 06 | Present in supplied items.csv |
| 90307 | Diary fragment · 07 | Present in supplied items.csv |
| 90308 | Diary fragment · 08 | Present in supplied items.csv |
| 90309 | Diary fragment · 09 | Present in supplied items.csv |
| 90310 | Diary fragment · 10 | Present in supplied items.csv |
| 90311 | Diary fragment · 11 | Present in supplied items.csv |
| 90312 | Diary fragment · 12 | Present in supplied items.csv |
| 90313 | Diary fragment · 13 | Present in supplied items.csv |
| 90314 | Diary fragment · 14 | Present in supplied items.csv |
| 90315 | Diary fragment · 15 | Present in supplied items.csv |
| 90316 | Diary fragment · 16 | Present in supplied items.csv |
| 90317 | Diary fragment · 17 | Present in supplied items.csv |
| 90318 | Diary fragment · 18 | Present in supplied items.csv |
| 90319 | Diary fragment · 19 | Present in supplied items.csv |
| 90320 | Diary fragment · 20 | Present in supplied items.csv |
| 90321 | Diary fragment · 21 | Present in supplied items.csv |
| 90322 | Diary fragment · 22 | Present in supplied items.csv |
| 90323 | Diary fragment · 23 | Present in supplied items.csv |
| 90324 | Diary fragment · 24 | Present in supplied items.csv |
| 90325 | Diary fragment · 25 | Present in supplied items.csv |
| 90401 | Brochure · 01 | Present in supplied items.csv |
| 90402 | Brochure · 02 | Present in supplied items.csv |
| 90403 | Brochure · 03 | Present in supplied items.csv |
| 90404 | Brochure · 04 | Present in supplied items.csv |
| 90405 | Brochure · 05 | Present in supplied items.csv |
| 90901 | Puzzle clue · stage 1 | Present in supplied items.csv |
| 90902 | Puzzle clue · stage 2 | Present in supplied items.csv |
| 90903 | Puzzle clue · stage 3 | Present in supplied items.csv |
| 90904 | Puzzle clue · stage 4 | Present in supplied items.csv |
| 90905 | Puzzle clue · stage 5 | Present in supplied items.csv |
| 90906 | Puzzle clue · stage 6 | Present in supplied items.csv |
| 90907 | Puzzle clue · stage 7 | Present in supplied items.csv |
| 90999 | Puzzle clue · dummy | Present in supplied items.csv |

### Vehicles

| ID | English name | Source status |
| --- | --- | --- |
| 101 | Vehicle | Present in supplied items.csv |
| 102 | Vehicle | Present in supplied items.csv |
| 105 | Vehicle | Present in supplied items.csv |
| 107 | Vehicle | Present in supplied items.csv |
| 109 | Vehicle | Present in supplied items.csv |
| 110 | Vehicle | Present in supplied items.csv |
| 114 | Vehicle | Present in supplied items.csv |
| 115 | Vehicle | Present in supplied items.csv |
| 203 | Boat | Present in supplied items.csv |

## Additional user hypotheses

- `10601` is PKM and `10605` is the launcher in the supplied CSV. `10602–10604` are missing; one may be MG4, but the exact ID is unknown.
- `103004` is listed as a P90 candidate, not a confirmed CSV mapping.
- IDs `20001` and `20002` are left as unnamed Glock-17/USP-45 candidate slots; the mapping between names and IDs is unknown.
- `30005` is a candidate 5.7×28 mm ammunition ID. `30007`/`30008` are possible .45-caliber ammunition slots, with exact names and IDs unresolved.
- `30009` is tentatively labeled an RPG-7 round, not the launcher. The standard wording is **rocket-propelled grenade** or **RPG-7 round/projectile**, not “reactive grenade”; [U.S. Army ODIN](https://odin.t2com.army.mil/WEG/Asset/RPG-7_Russia_Rocket-Propell_Grenade_Launcher) identifies the RPG-7 as the launcher, and the [Small Arms Survey guide](https://www.smallarmssurvey.org/sites/default/files/SAS-HB-06-Weapons-ID-Guide-Full.pdf) describes its ammunition/projectile. The CSV text `火箭筒` is closer to “rocket launcher,” so this item-name interpretation still needs confirmation.
- `40108` is normalized to **SMG flash hider**. `70001` is **Bandage**; no quantity of five is implied by its ID/name.
- IDs `40401`, `40403`, and `40405` are present while `40402` and `40404` are absent. The files do not explain the numbering gaps or support a faster-reload/sidegrade interpretation.


## Input coverage requested

Included ranges: `10101–10110`, `10201–10210`, `20001–20003`, `200101–200103`, `201001–201003`, `30001–30009`, `40101–40112`, `40201–40202`, `40301–40306`, `40401–40405`, `40501–40502`, plus IDs found elsewhere in the supplied loot and vehicle pools.
