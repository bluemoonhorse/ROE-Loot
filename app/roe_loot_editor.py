#!/usr/bin/env python3
"""Offline ROE loot editor launcher and local save service (Python standard library)."""
from __future__ import annotations

import json
import os
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
