#!/usr/bin/env python3
"""Exporta sesiones de Claude Code (.jsonl) a Markdown legible.

Sin dependencias externas (solo biblioteca estándar de Python >= 3.9).

Qué se incluye en cada .md:
  * metadatos de la sesión (fechas, versión de Claude Code, modelo, carpeta);
  * los mensajes del autor, completos;
  * los textos de respuesta de Claude, completos;
  * cada llamada a herramienta resumida en una línea, p. ej. ``[Edit] notebooks/act1.ipynb``;
  * las respuestas del autor a preguntas de Claude y los rechazos de herramientas.

Qué NO se incluye: el razonamiento interno del modelo (bloques «thinking»), las
salidas de las herramientas, el contenido de los ficheros leídos o escritos, las
imágenes ni el contexto que Claude Code inyecta automáticamente (prompt de sistema,
recordatorios, etc.).

Anonimización automática: la ruta raíz del proyecto se sustituye por su nombre
(«Actividad 1») y cualquier otra ruta bajo el directorio personal por «~».

Uso:
    python3 scripts/exportar_sesiones.py                 # exporta según scripts/sesiones.json
    python3 scripts/exportar_sesiones.py --indice        # solo lista los prompts numerados
    python3 scripts/exportar_sesiones.py --privado scripts/privado.json
    python3 scripts/exportar_sesiones.py --claude-ai ~/ruta/conversations.json   # claude.ai

Las conversaciones de claude.ai se leen del conversations.json del export de la cuenta
(Settings → Privacy → Export data) y se escriben en claude-ai/. Se incluyen las listadas
en la clave «claude_ai» de la configuración: [{"uuid", "fichero", "titulo"}].

Configuración (scripts/sesiones.json):
    {
      "raiz_proyecto": "~/ruta/a/Actividad 1",
      "directorio_sesiones": "~/.claude/projects",
      "salida": "claude-code",
      "sesiones": [
        {"id": "<uuid de la sesión>", "fichero": "AAAA-MM-DD_tema.md",
         "titulo": "Título legible"}
      ]
    }

Configuración privada opcional (scripts/privado.json, no se publica):
    {
      "redacciones": [{"patron": "regex", "reemplazo": "[dato redactado]"}]
    }
"""

from __future__ import annotations

import argparse
import glob
import json
import os
import re
import sys
from collections import Counter
from datetime import datetime

MAX_LINEA = 110

RE_REMINDER = re.compile(r"<system-reminder>.*?</system-reminder>", re.S)
RE_CMD_NAME = re.compile(r"<command-name>(.*?)</command-name>", re.S)
RE_CMD_ARGS = re.compile(r"<command-args>(.*?)</command-args>", re.S)
RE_INTERRUPT = re.compile(r"^\[Request interrupted by user[^\]]*\]$")
RE_BASH_IN = re.compile(r"<bash-input>(.*?)</bash-input>", re.S)
RE_PEGADO_INI = re.compile(r"<pasted_content[^>]*>")
RE_PEGADO_FIN = re.compile(r"</pasted_content>")
SALIDA_BASH = "\x00salida-bash"


# ---------------------------------------------------------------- utilidades
def hora_local(ts: str | None) -> datetime | None:
    if not ts:
        return None
    return datetime.fromisoformat(ts.replace("Z", "+00:00")).astimezone()


def recortar(texto: str, n: int = MAX_LINEA) -> str:
    texto = texto.strip()
    primera = texto.splitlines()[0] if texto else ""
    if len(primera) > n:
        return primera[: n - 1] + "…"
    if primera != texto:
        return primera + " …"
    return primera


def codigo_en_linea(s: str) -> str:
    """Envuelve s en código en línea de Markdown aunque contenga acentos graves."""
    if "`" not in s:
        return f"`{s}`"
    return f"`` {s} ``"


def cita(texto: str) -> str:
    return "\n".join(("> " + l) if l.strip() else ">" for l in texto.splitlines())


def texto_resultado(bloque: dict) -> str:
    c = bloque.get("content")
    if isinstance(c, str):
        return c
    if isinstance(c, list):
        return "\n".join(x.get("text", "") for x in c if isinstance(x, dict) and x.get("type") == "text")
    return ""


# ------------------------------------------------------- resumen herramientas
def resumir_herramienta(nombre: str, entrada: dict) -> str:
    e = entrada or {}
    if nombre == "Bash":
        detalle = e.get("command", "")
    elif nombre in ("Read", "Write", "Edit", "MultiEdit"):
        detalle = e.get("file_path", "")
    elif nombre == "NotebookEdit":
        detalle = e.get("notebook_path", "")
        if e.get("edit_mode"):
            detalle += f" ({e['edit_mode']})"
    elif nombre in ("Glob", "Grep"):
        detalle = e.get("pattern", "") + (f"  en {e['path']}" if e.get("path") else "")
    elif nombre in ("WebSearch", "ToolSearch"):
        detalle = e.get("query", "")
    elif nombre == "WebFetch":
        detalle = e.get("url", "")
    elif nombre in ("Agent", "Task"):
        detalle = e.get("description", "")
    elif nombre == "Skill":
        detalle = e.get("skill", "")
    elif nombre == "AskUserQuestion":
        qs = e.get("questions") or []
        detalle = " / ".join(q.get("question", "") for q in qs if isinstance(q, dict))
    else:
        detalle = next((v for v in e.values() if isinstance(v, str)), "")
    # anonimizar ANTES de recortar, para no dejar rutas cortadas a medias sin sustituir
    return f"[{nombre}] {recortar(ANONIMIZAR(detalle))}".rstrip()


ANONIMIZAR = lambda s: s  # se reemplaza en main() por la función con las rutas reales


# ------------------------------------------------------------ lectura jsonl
def texto_usuario(contenido) -> tuple[str | None, int]:
    """Devuelve (texto visible del autor, nº de imágenes) o (None, 0) si no es un prompt."""
    if isinstance(contenido, str):
        bloques = [{"type": "text", "text": contenido}]
    elif isinstance(contenido, list):
        bloques = contenido
    else:
        return None, 0
    if any(isinstance(b, dict) and b.get("type") == "tool_result" for b in bloques):
        return None, 0
    partes, imagenes = [], 0
    for b in bloques:
        if not isinstance(b, dict):
            continue
        if b.get("type") == "image":
            imagenes += 1
        elif b.get("type") == "text":
            partes.append(b.get("text", ""))
    texto = RE_REMINDER.sub("", "\n\n".join(partes)).strip()
    if texto.startswith("<local-command") or texto.startswith("Caveat:"):
        return None, 0
    if texto.startswith("<bash-stdout>") or texto.startswith("<bash-stderr>"):
        return SALIDA_BASH, 0
    m = RE_BASH_IN.search(texto)
    if m:  # comando lanzado por el autor con «!»
        return codigo_en_linea("! " + m.group(1).strip()), imagenes
    m = RE_CMD_NAME.search(texto)
    if m:  # comando con barra, p. ej. /model
        args = RE_CMD_ARGS.search(texto)
        texto = codigo_en_linea((m.group(1).strip() + " " + (args.group(1).strip() if args else "")).strip())
        return texto, imagenes
    if not texto and not imagenes:
        return None, 0
    return escapar_etiquetas(texto), imagenes


def escapar_etiquetas(texto: str) -> str:
    """Marca el texto pegado y neutraliza etiquetas HTML que GitHub ocultaría (fuera de `código`)."""
    texto = RE_PEGADO_INI.sub("\n**[Texto pegado por el autor:]**\n", texto)
    texto = RE_PEGADO_FIN.sub("\n**[Fin del texto pegado]**\n", texto)
    trozos = re.split(r"(```.*?```|`[^`\n]*`)", texto, flags=re.S)
    for i in range(0, len(trozos), 2):
        trozos[i] = re.sub(r"<(?=[A-Za-z/!])", "&lt;", trozos[i])
    return "".join(trozos).strip()


def leer_sesion(ruta: str) -> dict:
    """Lee el .jsonl y devuelve metadatos y una lista de turnos."""
    meta = {"inicio": None, "fin": None, "modelos": Counter(), "versiones": set(),
            "carpetas": [], "herramientas": Counter()}
    eventos = []          # (tipo, datos) en orden cronológico
    resultados = {}       # tool_use_id -> bloque tool_result
    vistos = set()
    hijos = Counter()

    with open(ruta, encoding="utf-8", errors="replace") as fh:
        for linea in fh:
            try:
                o = json.loads(linea)
            except json.JSONDecodeError:
                continue
            tipo = o.get("type")
            if tipo not in ("user", "assistant") or o.get("isSidechain"):
                continue
            ts = o.get("timestamp")
            if ts:
                meta["inicio"] = meta["inicio"] or ts
                meta["fin"] = ts
            if o.get("version"):
                meta["versiones"].add(o["version"])
            if o.get("cwd") and o["cwd"] not in meta["carpetas"]:
                meta["carpetas"].append(o["cwd"])
            msg = o.get("message") or {}
            contenido = msg.get("content")

            if tipo == "user":
                if isinstance(contenido, list):
                    for b in contenido:
                        if isinstance(b, dict) and b.get("type") == "tool_result":
                            resultados[b.get("tool_use_id")] = b
                if o.get("isMeta") or o.get("isCompactSummary"):
                    if o.get("isCompactSummary"):
                        eventos.append(("nota", "*[Resumen automático del contexto anterior omitido]*", ts))
                    continue
                texto, imgs = texto_usuario(contenido)
                if texto is None:
                    continue
                if RE_INTERRUPT.match(texto):
                    eventos.append(("nota", "*[El autor interrumpió la respuesta]*", ts))
                    continue
                if texto == SALIDA_BASH:
                    eventos.append(("nota", "*[Salida del comando omitida]*", ts))
                    continue
                if o.get("parentUuid"):
                    hijos[o["parentUuid"]] += 1   # solo prompts: detecta mensajes editados/rebobinados
                eventos.append(("prompt", (texto, imgs), ts))
            else:
                if o.get("isApiErrorMessage"):
                    continue
                if msg.get("model") and not msg["model"].startswith("<"):
                    meta["modelos"][msg["model"]] += 1
                for b in contenido if isinstance(contenido, list) else []:
                    if not isinstance(b, dict):
                        continue
                    clave = (msg.get("id"), json.dumps(b, sort_keys=True, ensure_ascii=False))
                    if clave in vistos:
                        continue
                    vistos.add(clave)
                    if b.get("type") == "text" and b.get("text", "").strip():
                        eventos.append(("texto", b["text"].strip(), ts))
                    elif b.get("type") == "tool_use":
                        meta["herramientas"][b.get("name")] += 1
                        eventos.append(("herramienta", b, ts))

    meta["bifurcaciones"] = sum(1 for n in hijos.values() if n > 1)
    meta["fin_ts"] = meta["fin"]

    # Agrupar en turnos: cada prompt del autor abre un turno.
    turnos, actual = [], None
    for tipo, datos, ts in eventos:
        if tipo == "prompt":
            actual = {"prompt": datos[0], "imagenes": datos[1], "ts": ts, "ts_fin": ts,
                      "items": [], "herramientas": Counter()}
            turnos.append(actual)
            continue
        if actual is None:
            actual = {"prompt": None, "imagenes": 0, "ts": ts, "ts_fin": ts,
                      "items": [], "herramientas": Counter()}
            turnos.append(actual)
        actual["ts_fin"] = ts or actual["ts_fin"]
        if tipo == "herramienta":
            actual["herramientas"][datos.get("name")] += 1
            linea = resumir_herramienta(datos.get("name", "?"), datos.get("input"))
            extra = []
            res = resultados.get(datos.get("id"))
            if res is not None:
                rtexto = texto_resultado(res)
                if "doesn't want to proceed" in rtexto or "was rejected" in rtexto:
                    linea += "  — rechazada por el autor"
                    m = re.search(r"the user said:\s*(.+)", rtexto, re.S)
                    if m:
                        extra.append("comentario del autor: " + m.group(1).strip())
                elif datos.get("name") == "AskUserQuestion":
                    extra.append("respuesta del autor: " + rtexto.strip())
            actual["items"].append(("herramienta", (linea, extra)))
        else:
            actual["items"].append((tipo, datos))
    return {"meta": meta, "turnos": turnos}


def cortar(sesion: dict, hasta: int) -> None:
    """Publica la sesión solo hasta el prompt nº «hasta» (incluida su respuesta).

    Fin, nº de prompts y recuento de herramientas se recalculan sobre lo publicado."""
    n, conservados = 0, []
    for t in sesion["turnos"]:
        if t["prompt"] is not None:
            n += 1
            if n > hasta:
                break
        conservados.append(t)
    sesion["turnos"] = conservados
    meta = sesion["meta"]
    meta["fin"] = conservados[-1]["ts_fin"] if conservados else meta["inicio"]
    meta["herramientas"] = sum((t["herramientas"] for t in conservados), Counter())


# ----------------------------------------------------------------- render
def anonimizar(texto: str, raiz: str, home: str, usuario: str) -> str:
    nombre_raiz = os.path.basename(raiz.rstrip("/"))
    texto = texto.replace(raiz.rstrip("/") + "/", nombre_raiz + "/").replace(raiz.rstrip("/"), nombre_raiz)
    texto = texto.replace(home.rstrip("/"), "~")
    # directorios temporales de Claude Code: /tmp/claude-<uid>/<carpeta-proyecto>/<id-sesión>/
    texto = re.sub(r"/tmp/claude-\d+/(?:-home-[^/\s`\"']*/)?(?:[0-9a-f]{8}-[0-9a-f-]{27}/)?", "<tmp>/", texto)
    # carpetas de ~/.claude/projects codifican la ruta: -home-<usuario>-...
    texto = re.sub(rf"-home-{re.escape(usuario)}-", "-home-<usuario>-", texto)
    return texto


def render(sesion: dict, cfg_sesion: dict, raiz: str, home: str, usuario: str) -> str:
    meta, turnos = sesion["meta"], sesion["turnos"]
    ini, fin = hora_local(meta["inicio"]), hora_local(meta["fin"])
    mismo_dia = ini and fin and ini.date() == fin.date()

    def hora(ts):
        d = hora_local(ts)
        if not d:
            return ""
        return d.strftime("%H:%M") if mismo_dia else d.strftime("%Y-%m-%d %H:%M")

    herr = ", ".join(f"{k} ×{v}" for k, v in meta["herramientas"].most_common()) or "ninguna"
    n_prompts = sum(1 for t in turnos if t["prompt"] is not None)
    out = [f"# {cfg_sesion.get('titulo', 'Sesión de Claude Code')}", ""]
    out += [
        "| | |", "|---|---|",
        f"| Herramienta | Claude Code {', '.join(sorted(meta['versiones'])) or '?'} |",
        f"| Modelo | {', '.join(meta['modelos']) or '?'} |",
        f"| Inicio | {ini.strftime('%Y-%m-%d %H:%M %Z') if ini else '?'} |",
        f"| Fin | {fin.strftime('%Y-%m-%d %H:%M %Z') if fin else '?'} |",
        f"| Carpeta de trabajo | {', '.join(codigo_en_linea(c) for c in meta['carpetas'])} |",
        f"| Sesión | {codigo_en_linea(cfg_sesion['id'])} |",
        f"| Prompts del autor | {n_prompts} |",
        f"| Llamadas a herramientas | {herr} |",
        "",
        "> Transcripción generada con `scripts/exportar_sesiones.py`. Se reproducen completos los "
        "mensajes del autor y los textos de respuesta de Claude; las llamadas a herramientas se "
        "resumen en una línea y se omiten sus salidas, el contenido de ficheros, las imágenes y el "
        "razonamiento interno del modelo.",
        "",
    ]
    num = 0
    for t in turnos:
        if t["prompt"] is not None:
            num += 1
            out += ["---", "", f"## Prompt {num} · {hora(t['ts'])}", ""]
            texto = t["prompt"]
            if t["imagenes"]:
                texto += ("\n\n" if texto else "") + f"*[{t['imagenes']} imagen(es) adjunta(s) omitida(s)]*"
            out += ["**Autor:**", "", cita(texto), ""]
        en_lista = False
        primera_resp = True
        for tipo, datos in t["items"]:
            if tipo in ("texto", "herramienta") and primera_resp:
                out += ["**Claude:**", ""]
                primera_resp = False
            if tipo == "herramienta":
                if not en_lista:
                    if out[-1] != "":
                        out.append("")
                    en_lista = True
                linea, extra = datos
                out.append(f"- {codigo_en_linea(linea)}")
                for e in extra:
                    out += ["", cita(e), ""]
                continue
            if en_lista:
                out.append("")
                en_lista = False
            if tipo == "texto":
                out += [datos, ""]
            elif tipo == "nota":
                out += [datos, ""]
        if en_lista:
            out.append("")
    md = "\n".join(out).rstrip() + "\n"
    return anonimizar(md, raiz, home, usuario)


def aplicar_privado(md: str, privado: dict) -> str:
    for r in privado.get("redacciones", []):
        md = re.sub(r["patron"], r.get("reemplazo", "[dato redactado]"), md)
    return md


# ------------------------------------------------- conversaciones claude.ai
RE_SANDBOX = [
    (re.compile(r"/tmp/claude-\d+/-home-claude/[0-9a-f-]{36}/"), "<tmp>/"),
    (re.compile(r"/mnt/user-data/attachments/[0-9a-f-]{36}/"), "<adjuntos>/"),
    (re.compile(r"/mnt/user-data/(uploads|outputs)/"), r"<\1>/"),
    (re.compile(r"/projects/[0-9a-f-]{36}/"), "<proyecto>/"),
]


def anonimizar_sandbox(texto: str) -> str:
    for patron, reemplazo in RE_SANDBOX:
        texto = patron.sub(reemplazo, texto)
    return texto


def resumir_herramienta_web(nombre: str, entrada: dict) -> str:
    e = entrada or {}
    corto = nombre.split("__")[-1]
    if nombre == "Projects":
        detalle = e.get("method", "")
        if e.get("path"):
            detalle += f" {e['path']}"
        if e.get("query"):
            detalle += f" «{e['query']}»"
        return f"[Proyecto] {recortar(anonimizar_sandbox(detalle))}"
    if corto == "memory_read":
        rutas = e.get("path")
        rutas = rutas if isinstance(rutas, list) else [rutas]
        return f"[Memoria] {', '.join(os.path.basename(str(r)) for r in rutas)}"
    if corto == "conversation_search":
        return f"[Buscar en chats] «{e.get('query', '')}»"
    if corto == "recent_chats":
        return f"[Chats recientes] {e.get('n', '')}"
    if nombre == "SendUserFile":
        return f"[Fichero enviado] {recortar(e.get('caption', ''))}"
    # anonimizar las rutas del sandbox ANTES de que resumir_herramienta recorte la línea
    e = {k: anonimizar_sandbox(v) if isinstance(v, str) else v for k, v in e.items()}
    return resumir_herramienta(corto, e)


def leer_conversacion(c: dict) -> dict:
    meta = {"inicio": c.get("created_at"), "fin": None, "herramientas": Counter()}
    msgs = sorted(c.get("chat_messages", []), key=lambda m: m.get("created_at", ""))
    turnos = []
    for m in msgs:
        meta["fin"] = m.get("created_at") or meta["fin"]
        bloques = m.get("content") or []
        if m.get("sender") == "human":
            textos = [b.get("text", "") for b in bloques if b.get("type") == "text"]
            texto = "\n\n".join(t for t in textos if t.strip()) or (m.get("text") or "")
            adjuntos = [a.get("file_name") for a in (m.get("attachments") or []) + (m.get("files") or [])]
            adjuntos = list(dict.fromkeys(a for a in adjuntos if a))
            imagenes = sum(1 for b in bloques if b.get("type") == "image")
            turnos.append({"prompt": escapar_etiquetas(texto.strip()), "ts": m.get("created_at"),
                           "adjuntos": adjuntos, "imagenes": imagenes, "items": []})
            continue
        if not turnos:
            turnos.append({"prompt": None, "ts": m.get("created_at"), "adjuntos": [], "imagenes": 0, "items": []})
        for b in bloques:
            if b.get("type") == "text" and b.get("text", "").strip():
                turnos[-1]["items"].append(("texto", b["text"].strip()))
            elif b.get("type") == "tool_use":
                meta["herramientas"][b.get("name", "?").split("__")[-1]] += 1
                turnos[-1]["items"].append(("herramienta", (resumir_herramienta_web(b.get("name", "?"), b.get("input")), [])))
    return {"meta": meta, "turnos": turnos}


def render_web(conv: dict, cfg_conv: dict, raiz: str, home: str, usuario: str) -> str:
    meta, turnos = conv["meta"], conv["turnos"]
    ini, fin = hora_local(meta["inicio"]), hora_local(meta["fin"])
    mismo_dia = ini and fin and ini.date() == fin.date()
    herr = ", ".join(f"{k} ×{v}" for k, v in meta["herramientas"].most_common()) or "ninguna"
    out = [f"# {cfg_conv.get('titulo', 'Conversación en claude.ai')}", "",
           "| | |", "|---|---|",
           "| Herramienta | Claude en claude.ai (proyecto de la asignatura) |",
           "| Modelo | no consta en el export |",
           f"| Inicio | {ini.strftime('%Y-%m-%d %H:%M %Z') if ini else '?'} |",
           f"| Fin | {fin.strftime('%Y-%m-%d %H:%M %Z') if fin else '?'} |",
           f"| Conversación | {codigo_en_linea(cfg_conv['uuid'])} |",
           f"| Mensajes del autor | {sum(1 for t in turnos if t['prompt'] is not None)} |",
           f"| Llamadas a herramientas | {herr} |", "",
           "> Transcripción generada con `scripts/exportar_sesiones.py` a partir del export de la "
           "cuenta de claude.ai. Se reproducen completos los mensajes del autor y los textos de "
           "respuesta de Claude; las llamadas a herramientas se resumen en una línea y se omiten sus "
           "resultados, el contenido de los adjuntos y el razonamiento interno del modelo.", ""]
    num = 0
    for t in turnos:
        if t["prompt"] is not None:
            num += 1
            d = hora_local(t["ts"])
            out += ["---", "", f"## Mensaje {num} · {d.strftime('%H:%M' if mismo_dia else '%Y-%m-%d %H:%M') if d else ''}", ""]
            texto = t["prompt"]
            extras = [f"*[Fichero adjunto: {codigo_en_linea(a)}]*" for a in t["adjuntos"]]
            if t["imagenes"]:
                extras.append(f"*[{t['imagenes']} imagen(es) adjunta(s)]*")
            texto = "\n\n".join(x for x in [texto] + extras if x)
            out += ["**Autor:**", "", cita(texto), ""]
        primera, en_lista = True, False
        for tipo, datos in t["items"]:
            if primera:
                out += ["**Claude:**", ""]
                primera = False
            if tipo == "herramienta":
                if not en_lista and out[-1] != "":
                    out.append("")
                en_lista = True
                out.append(f"- {codigo_en_linea(datos[0])}")
                continue
            if en_lista:
                out.append("")
                en_lista = False
            out += [datos, ""]
        if en_lista:
            out.append("")
    md = "\n".join(out).rstrip() + "\n"
    return anonimizar_sandbox(anonimizar(md, raiz, home, usuario))


def exportar_claude_ai(ruta_json: str, cfg: dict, base: str, raiz: str, home: str, usuario: str,
                       privado: dict, indice: bool) -> int:
    with open(ruta_json, encoding="utf-8") as fh:
        datos = {c["uuid"]: c for c in json.load(fh)}
    salida = os.path.join(base, cfg.get("salida_claude_ai", "claude-ai"))
    os.makedirs(salida, exist_ok=True)
    for s in cfg.get("claude_ai", []):
        c = datos.get(s["uuid"])
        if c is None:
            print(f"ERROR: la conversación {s['uuid']} no está en el export", file=sys.stderr)
            return 1
        conv = leer_conversacion(c)
        if indice:
            print(f"\n=== {s['uuid'][:8]}  {s['fichero']}")
            n = 0
            for t in conv["turnos"]:
                if t["prompt"] is None:
                    continue
                n += 1
                p = anonimizar(t["prompt"], raiz, home, usuario).replace("\n", " ⏎ ")
                print(f"{n:3d}. {hora_local(t['ts']).strftime('%H:%M')}  ({len(t['prompt'])} car.)  {p[:160]}")
            continue
        md = aplicar_privado(render_web(conv, s, raiz, home, usuario), privado)
        destino = os.path.join(salida, s["fichero"])
        with open(destino, "w", encoding="utf-8") as fh:
            fh.write(md)
        print(f"{s['uuid'][:8]} -> {os.path.relpath(destino, base)}  ({len(md) / 1024:.1f} KB)")
    return 0


# ------------------------------------------------------------------- main
def main() -> int:
    base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--config", default=os.path.join(base, "scripts", "sesiones.json"))
    ap.add_argument("--privado", default=os.path.join(base, "scripts", "privado.json"),
                    help="configuración privada (se ignora si no existe)")
    ap.add_argument("--indice", action="store_true", help="solo imprime los prompts numerados")
    ap.add_argument("--solo", help="exportar solo la sesión cuyo id empiece por este prefijo")
    ap.add_argument("--claude-ai", metavar="CONVERSATIONS_JSON",
                    help="exporta en su lugar las conversaciones de claude.ai listadas en "
                         "«claude_ai» de la configuración, a partir del conversations.json del export")
    args = ap.parse_args()

    with open(args.config, encoding="utf-8") as fh:
        cfg = json.load(fh)
    privado = {}
    if os.path.exists(args.privado):
        with open(args.privado, encoding="utf-8") as fh:
            privado = json.load(fh)

    home = os.path.expanduser("~")
    usuario = os.path.basename(home)
    raiz = os.path.expanduser(cfg["raiz_proyecto"])
    dir_ses = os.path.expanduser(cfg.get("directorio_sesiones", "~/.claude/projects"))
    salida = os.path.join(base, cfg.get("salida", "claude-code"))
    os.makedirs(salida, exist_ok=True)
    global ANONIMIZAR
    ANONIMIZAR = lambda s: anonimizar(s, raiz, home, usuario)
    if args.claude_ai:
        return exportar_claude_ai(os.path.expanduser(args.claude_ai), cfg, base, raiz, home,
                                  usuario, privado, args.indice)

    for s in cfg["sesiones"]:
        if args.solo and not s["id"].startswith(args.solo):
            continue
        rutas = glob.glob(os.path.join(dir_ses, "*", s["id"] + ".jsonl"))
        if not rutas:
            print(f"ERROR: no encuentro la sesión {s['id']}", file=sys.stderr)
            return 1
        sesion = leer_sesion(rutas[0])
        hasta = privado.get("hasta_turno", {}).get(s["id"])
        if hasta:
            cortar(sesion, hasta)
        if sesion["meta"]["bifurcaciones"]:
            print(f"  aviso: {s['id'][:8]} tiene {sesion['meta']['bifurcaciones']} bifurcación(es) "
                  "con varios prompts (mensajes editados o rebobinados); se exportan en orden "
                  "cronológico", file=sys.stderr)
        if args.indice:
            print(f"\n=== {s['id'][:8]}  {s.get('fichero', '')}")
            n = 0
            for t in sesion["turnos"]:
                if t["prompt"] is None:
                    continue
                n += 1
                p = anonimizar(t["prompt"], raiz, home, usuario).replace("\n", " ⏎ ")
                print(f"{n:3d}. {hora_local(t['ts']).strftime('%H:%M')}  ({len(t['prompt'])} car.)  {p[:160]}")
            continue
        md = render(sesion, s, raiz, home, usuario)
        md = aplicar_privado(md, privado)
        destino = os.path.join(salida, s["fichero"])
        with open(destino, "w", encoding="utf-8") as fh:
            fh.write(md)
        print(f"{s['id'][:8]} -> {os.path.relpath(destino, base)}  ({len(md) / 1024:.1f} KB)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
