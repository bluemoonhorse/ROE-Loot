#!/usr/bin/env python3
"""Offline ROE loot editor launcher and local save service (Python standard library)."""
from __future__ import annotations

import json
import os
import re
import shutil
import socket
import threading
import webbrowser
from datetime import datetime
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse

HERE = Path(__file__).resolve().parent
APP_NAME = "ROE Loot Table Studio Python"
TABLES = ("control", "items", "vehicle_control", "vehicles")


def read_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def app_data_dir() -> Path:
    base = Path(os.environ.get("LOCALAPPDATA", Path.home() / "AppData" / "Local"))
    return base / APP_NAME


def initial_project():
    project = read_json(HERE / "seed.json")
    catalog = read_json(HERE / "item-catalog.json")
    translation = project.setdefault("translation", {})
    names = translation.setdefault("items", {})
    # Keep supplied hand-written names, and fill the rest from the bilingual catalog.
    for item in catalog:
        item_id = str(item["id"])
        old = names.get(item_id, {})
        names[item_id] = {
            "en": old.get("en") or item.get("name_en", ""),
            "ru": old.get("ru") or item.get("name_ru", ""),
        }
    return project


def html_document():
    page = (HERE / "roe-loot-admin.html").read_text(encoding="utf-8")
    catalog = read_json(HERE / "item-catalog.json")
    catalog.sort(key=lambda x: (int(x.get("category_order", 999)), int(x.get("id", 0))))
    js_catalog = json.dumps(catalog, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
    # Let the editor's existing picker offer the complete bilingual catalog, not only
    # items already present in the currently selected group.
    page = page.replace(
        "const names={};for(const [id,v] of Object.entries(tr.items))names[id]={en:v[0],ru:v[1]};",
        "const fullCatalog=" + js_catalog + ";\nconst names={};for(const [id,v] of Object.entries(tr.items))names[id]={en:v[0],ru:v[1]};",
        1,
    )
    old_catalog_fn = "function catalog(){let map=new Map();for(let r of rows(keys[section][1])){let key=`${r.iItemID}|${r.strItemName}`;if(!map.has(key))map.set(key,r)}return [...map.values()].sort((a,b)=>itemName(a).localeCompare(itemName(b)))}"
    new_catalog_fn = "function catalog(){let map=new Map();for(const c of fullCatalog){let id=String(c.id),name=names[id]?.en||c.name_en||('Item '+id);map.set(id+'|'+name,{iItemID:id,strItemName:name,_category:c.category,_categoryOrder:Number(c.category_order)||999})}for(let r of rows(keys[section][1])){let id=String(r.iItemID),name=names[id]?.en||r.strItemName||('Item '+id);if(!map.has(id+'|'+name))map.set(id+'|'+name,r)}return [...map.values()].sort((a,b)=>(a._categoryOrder||999)-(b._categoryOrder||999)||String(a.iItemID).localeCompare(String(b.iItemID),undefined,{numeric:true}))}"
    if old_catalog_fn not in page:
        raise RuntimeError("Could not locate the item catalog picker in the bundled GUI.")
    page = page.replace(old_catalog_fn, new_catalog_fn, 1)
    # Projects in the seed use translation.items; browser exports use a flat translation map.
    page = page.replace("if(p.translation)Object.assign(names,p.translation);", "if(p.translation)Object.assign(names,p.translation.items||p.translation);", 1)
    page = page.replace("if(obj.translation)Object.assign(names,obj.translation);", "if(obj.translation)Object.assign(names,obj.translation.items||obj.translation);", 1)
    # The portable server JSON uses English item labels while project translations retain both languages.
    old_bundle = "function projectBundle(){let clean=k=>rows(k).map(r=>Object.fromEntries(Object.entries(r).filter(([key])=>!key.startsWith('_'))));return {format:'roe-loot-editor-v1',model,translation:clone(names),tables:{control:clean('control'),items:clean('items'),vehicle_control:clean('vehicle_control'),vehicles:clean('vehicles')},source_notes:{original_server_algorithm_verified:false,description:'Editable copy of supplied ROE 2022 research tables. H1/H2 are research interpretations, not verified native behavior.'}}}"
    new_bundle = "function projectBundle(){let clean=k=>rows(k).map(r=>{let o=Object.fromEntries(Object.entries(r).filter(([key])=>!key.startsWith('_')));if(k==='items'||k==='vehicles'){let id=String(o.iItemID||'');if(names[id]?.en)o.strItemName=names[id].en;for(let prefix of ['Extra','Extra2'])for(let n=1;n<=9;n++){let extra=String(o[`i${prefix}ItemID${n}`]||'');if(extra&&names[extra]?.en)o[`str${prefix}ItemName${n}`]=names[extra].en}}return o});return {format:'roe-loot-editor-v1',model,translation:clone(names),tables:{control:clean('control'),items:clean('items'),vehicle_control:clean('vehicle_control'),vehicles:clean('vehicles')},source_notes:{original_server_algorithm_verified:false,description:'Editable copy of supplied ROE 2022 research tables. H1/H2 are research interpretations, not verified native behavior.'}}}"
    if old_bundle not in page:
        raise RuntimeError("Could not locate the project export function in the bundled GUI.")
    page = page.replace(old_bundle, new_bundle, 1)

    # Editable group names should become the visible labels once changed, while
    # untouched imported names continue to use the bilingual display catalog.
    old_locale = "function localeName(row,kind=section){let id=String(row.iID), dict=kind==='vehicles'?tr.vehicleGroups:tr.groups;let v=dict[id];return v?v[language==='ru'?1:0]:(row.strName||`Group ${id}`)}"
    new_locale = "function localeName(row,kind=section){let id=String(row.iID),table=kind==='vehicles'?'vehicle_control':'control',original=(initial[table]||[]).find(x=>String(x.iID)===id);if(!original||String(row.strName||'')!==String(original.strName||''))return row.strName||`Group ${id}`;let dict=kind==='vehicles'?tr.vehicleGroups:tr.groups,v=dict[id];return v?v[language==='ru'?1:0]:(row.strName||`Group ${id}`)}"
    if old_locale not in page:
        raise RuntimeError("Could not locate the group-name display function.")
    page = page.replace(old_locale, new_locale, 1)
    page = page.replace("${language==='ru'?'Исходное имя':'Source name'}", "${language==='ru'?'Название группы':'Group name'}", 1)
    page = page.replace("Control-table fields. The source name stays separate from its translated display label.", "Edit the group name and spawn settings. The group name is exported in strName.", 1)
    page = page.replace("Поля таблицы управления лутом. Исходное китайское имя сохраняется отдельно от перевода.", "Изменяйте название группы и параметры появления. Название экспортируется в strName.", 1)

    # Replace raw numeric extra-ID fields with catalog selectors and add/remove
    # controls for each supported extra-item slot.
    new_extra_editor = r'''function extraEditor(r,prefix,count){let slots=Array.from({length:count},(_,i)=>i+1).filter(n=>{let id=`i${prefix}ItemID${n}`,weight=`i${prefix}ItemWeight${n}`,packs=`i${prefix}ItemCount${n}`,stack=`i${prefix}ItemStackCount${n}`;return Boolean(r[id]||r[weight]||r[packs]||r[stack]||(r[`_editing_${prefix}`]||[]).includes(n))}),items=catalog().filter(x=>x._category!=='Vehicles');let slotHtml=slots.map(n=>{let idField=`i${prefix}ItemID${n}`,nameField=`str${prefix}ItemName${n}`,weightField=`i${prefix}ItemWeight${n}`,countField=`i${prefix}ItemCount${n}`,stackField=`i${prefix}ItemStackCount${n}`,selectedId=String(r[idField]||'');let options=items.map(x=>{let id=String(x.iItemID),label=`${itemName(x)} · #${id}`;return `<option value="${esc(id)}" ${id===selectedId?'selected':''}>${esc(label)}</option>`}).join('');if(selectedId&&!items.some(x=>String(x.iItemID)===selectedId))options=`<option value="${esc(selectedId)}" selected>Unknown item · #${esc(selectedId)}</option>`+options;return `<div class="extra-slot"><label class="label">${prefix==='Extra'?(language==='ru'?'Доп. предмет':'Loot extra'):(language==='ru'?'Модификация':'Attachment')} ${n}</label><select class="select" data-extra-id="${idField}" data-row="${esc(r.iID)}"><option value="">${language==='ru'?'Выберите предмет':'Select catalog item'}</option>${options}</select><div class="extra-fields"><input class="input" type="number" min="0" max="100" title="${language==='ru'?'Вес шанса %':'Chance weight %'}" placeholder="${language==='ru'?'Вес %':'Weight %'}" data-rowfield="${weightField}" data-row="${esc(r.iID)}" value="${esc(r[weightField]??'100')}"><input class="input" type="number" min="1" title="${language==='ru'?'Число выпадений':'Roll count'}" placeholder="${language==='ru'?'Выпадений':'Rolls'}" data-rowfield="${countField}" data-row="${esc(r.iID)}" value="${esc(r[countField]??'1')}"><input class="input" type="number" min="1" title="${language==='ru'?'Размер стопки':'Stack size'}" placeholder="${language==='ru'?'Стопка':'Stack'}" data-rowfield="${stackField}" data-row="${esc(r.iID)}" value="${esc(r[stackField]??'1')}"><button class="btn danger" data-action="remove-extra" data-row="${esc(r.iID)}" data-prefix="${prefix}" data-slot="${n}">${language==='ru'?'Удалить':'Remove'}</button></div></div>`}).join('');return `<div class="extra-grid">${slotHtml||`<div class="empty-extra">${language==='ru'?'Дополнительных предметов пока нет':'No extra items added yet'}</div>`}</div><button class="btn" data-action="add-extra" data-row="${esc(r.iID)}" data-prefix="${prefix}">＋ ${language==='ru'?'Добавить предмет':'Add item'}</button>`}'''
    page, substitutions = re.subn(r"function extraEditor\(r,prefix,count\)\{.*?\}(?=\s*function rowHTML)", new_extra_editor + "\n", page, count=1, flags=re.S)
    if substitutions != 1:
        raise RuntimeError("Could not replace the extra-item editor.")
    page = page.replace("<button class=\"icon-btn\" data-action=\"delete-item\" data-row=\"${esc(r.iID)}\" title=\"Remove\">×</button>", "<button class=\"btn danger\" data-action=\"delete-item\" data-row=\"${esc(r.iID)}\" title=\"Remove\">${language==='ru'?'Удалить':'Remove'}</button>", 1)
    page = page.replace("</style>", ".extra-slot{min-width:240px;border:1px solid var(--line);background:#12191e;border-radius:9px;padding:9px}.extra-slot>.select{width:100%;margin:5px 0}.extra-fields{display:grid;grid-template-columns:repeat(4,minmax(65px,1fr));gap:5px}.extra-fields .btn{padding:5px 7px}.empty-extra{color:var(--muted);font-size:12px;padding:8px}.extra-grid{grid-template-columns:repeat(auto-fill,minmax(240px,1fr))}\n</style>", 1)

    rowfield_listener = "m.querySelectorAll('[data-rowfield]').forEach(i=>i.onchange=()=>{let r=contents().find(x=>String(x.iID)===i.dataset.row);if(!r)return;r[i.dataset.rowfield]=i.value;setDirty();render()});"
    extra_select_listener = "m.querySelectorAll('[data-extra-id]').forEach(i=>i.onchange=()=>{let r=contents().find(x=>String(x.iID)===i.dataset.row);if(!r)return;let id=String(i.value||''),field=i.dataset.extraId;r[field]=id;r[field.replace(/^i/,'str').replace('ID','Name')]=id?(names[id]?.en||catalog().find(x=>String(x.iItemID)===id)?.strItemName||`Item ${id}`):'';setDirty();render()});"
    if rowfield_listener not in page:
        raise RuntimeError("Could not locate the row field editor bindings.")
    page = page.replace(rowfield_listener, rowfield_listener + extra_select_listener, 1)
    add_item_listener = "m.querySelector('[data-action=\"add-item\"]')?.addEventListener('click',addItem);"
    extra_button_listeners = "m.querySelectorAll('[data-action=\"add-extra\"]').forEach(b=>b.onclick=()=>{let r=contents().find(x=>String(x.iID)===b.dataset.row),prefix=b.dataset.prefix,count=prefix==='Extra'?7:4;if(!r)return;let n=Array.from({length:count},(_,i)=>i+1).find(i=>!r[`i${prefix}ItemID${i}`]&&!(r[`_editing_${prefix}`]||[]).includes(i));if(!n){alert(language==='ru'?'Достигнут предел слотов':'No more extra-item slots are available');return}r[`_${'editing_'+prefix}`]=[...(r[`_editing_${prefix}`]||[]),n];r[`i${prefix}ItemWeight${n}`]='100';r[`i${prefix}ItemCount${n}`]='1';r[`i${prefix}ItemStackCount${n}`]='1';setDirty();render()});m.querySelectorAll('[data-action=\"remove-extra\"]').forEach(b=>b.onclick=()=>{let r=contents().find(x=>String(x.iID)===b.dataset.row),prefix=b.dataset.prefix,n=Number(b.dataset.slot);if(!r)return;for(let key of [`i${prefix}ItemID${n}`,`str${prefix}ItemName${n}`,`i${prefix}ItemWeight${n}`,`i${prefix}ItemCount${n}`,`i${prefix}ItemStackCount${n}`])delete r[key];r[`_editing_${prefix}`]=(r[`_editing_${prefix}`]||[]).filter(i=>i!==n);setDirty();render()});"
    if add_item_listener not in page:
        raise RuntimeError("Could not locate the add-item button binding.")
    page = page.replace(add_item_listener, add_item_listener + extra_button_listeners, 1)
    return page.encode("utf-8")


class Handler(BaseHTTPRequestHandler):
    server_version = "ROELootLocal/1.0"

    def log_message(self, _format, *args):
        # Keep the console quiet while the GUI is in use.
        pass

    def _send(self, status: int, body: bytes, content_type: str):
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        path = urlparse(self.path).path
        if path == "/" or path == "/index.html":
            self._send(200, html_document(), "text/html; charset=utf-8")
            return
        if path == "/api/project":
            target = app_data_dir() / "loot-project.json"
            project = read_json(target) if target.exists() else initial_project()
            self._send(200, json.dumps(project, ensure_ascii=False).encode("utf-8"), "application/json; charset=utf-8")
            return
        if path == "/favicon.ico":
            self._send(204, b"", "image/x-icon")
            return
        self._send(404, b"Not found", "text/plain; charset=utf-8")

    def do_PUT(self):
        if urlparse(self.path).path != "/api/project":
            self._send(404, b'{"error":"Not found"}', "application/json; charset=utf-8")
            return
        try:
            length = int(self.headers.get("Content-Length", "0"))
            if length <= 0 or length > 32 * 1024 * 1024:
                raise ValueError("Project size is empty or exceeds 32 MB.")
            project = json.loads(self.rfile.read(length).decode("utf-8"))
            tables = project.get("tables", {})
            if not isinstance(project, dict) or not isinstance(tables, dict) or not all(isinstance(tables.get(t), list) for t in TABLES):
                raise ValueError("Project must contain the four loot and vehicle table arrays.")
            target_dir = app_data_dir()
            target_dir.mkdir(parents=True, exist_ok=True)
            target = target_dir / "loot-project.json"
            backup_name = ""
            if target.exists():
                backup_dir = target_dir / "backups"
                backup_dir.mkdir(exist_ok=True)
                stamp = datetime.now().strftime("%Y%m%d-%H%M%S-%f")
                backup = backup_dir / f"loot-project-{stamp}.json"
                shutil.copy2(target, backup)
                backup_name = backup.name
                old = sorted(backup_dir.glob("loot-project-*.json"), key=lambda p: p.name, reverse=True)
                for obsolete in old[20:]:
                    obsolete.unlink(missing_ok=True)
            temp = target.with_suffix(".json.tmp")
            temp.write_text(json.dumps(project, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
            temp.replace(target)
            body = {"saved": str(target), "backup": backup_name or "first save"}
            self._send(200, json.dumps(body).encode("utf-8"), "application/json; charset=utf-8")
        except Exception as exc:
            body = json.dumps({"error": str(exc)}).encode("utf-8")
            self._send(400, body, "application/json; charset=utf-8")


def main():
    # Bind only to loopback; no internet access or third-party packages are used.
    server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
    server.daemon_threads = True
    host, port = server.server_address
    url = f"http://{host}:{port}/"
    print("ROE Loot Table Studio is running locally.")
    print("This app does not connect to the internet. Close this window to stop it.")
    print(url)
    threading.Timer(0.8, lambda: webbrowser.open(url)).start()
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
