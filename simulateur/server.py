# Serveur local du simulateur.
# - En-tetes COOP/COEP: activent SharedArrayBuffer (input() bloquant en Python).
# - POST /tns: ouvre un .tns comme la calculatrice (dechiffre Problem1.xml)
#   et renvoie le script Lua ou Python qu'il contient, en JSON.
# Usage: python server.py   puis ouvrir http://localhost:8765/simulateur/
import http.server, json, os, struct, sys, zlib

PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 8765
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
sys.path.insert(0, ROOT)


def lire_tns(b):
    """Retourne (infos, langage, nom, code) a partir des octets d'un .tns."""
    import py2tns
    infos = []
    magic = b[:10].decode("latin-1")
    infos.append("en-tete: %s  %s" % (magic, "OK" if magic.startswith("*TIMLP") else "INVALIDE"))
    e = b.rfind(b"TIPD")
    if e < 0:
        raise ValueError("fin de repertoire TIPD introuvable")
    n, size, off = struct.unpack("<HII", b[e + 10:e + 20])
    p = off
    fichiers = {}
    for _ in range(n):
        f = struct.unpack("<IHHHHIIIIHHHHHII", b[p:p + 46])
        name = b[p + 46:p + 46 + f[9]].decode("latin-1")
        lo = f[15]
        hdr = 10 if lo == 0 else 4
        lf = struct.unpack("<HHHIIIIHH", b[lo + hdr:lo + hdr + 26])
        start = lo + hdr + 26 + lf[7] + lf[8]
        data = b[start:start + lf[5]]
        if lf[2] == 8:
            plain = zlib.decompressobj(-15).decompress(data)
        else:
            plain = data
        ok = (zlib.crc32(plain) & 0xFFFFFFFF) == lf[4] and len(plain) == lf[6]
        meth = {13: "TI chiffre", 8: "deflate", 0: "brut"}.get(lf[2], str(lf[2]))
        infos.append("%s  %s  %d o  CRC %s" % (name, meth, lf[6], "OK" if ok else "FAUX"))
        if lf[2] == 13 and name == "Problem1.xml":
            # dechiffrement TI: en-tete de 40 octets puis deflate chiffre
            plain = zlib.decompressobj(-15).decompress(py2tns.doccrypt(plain[40:]))
            infos.append("  -> dechiffre: %d o, debut %r" % (len(plain), plain[:14]))
        fichiers[name] = plain
        p += 46 + f[9] + f[10] + f[11]
    prob = fichiers.get("Problem1.xml", b"")
    if b"TI.ScriptApp" in prob or b"<sc:script" in prob or b"TI.S\xac\x84" in prob:
        i = prob.find(b"<![CDATA[") + 9
        j = prob.rfind(b"]]>")
        code = prob[i:j].replace(b"]]]]><![CDATA[>", b"]]>").decode("utf-8")
        infos.append("Problem1.xml contient un script Lua")
        return infos, "lua", "Problem1.xml", code
    for name, data in fichiers.items():
        if name.endswith(".py"):
            if b"PythonEditor" in prob:
                infos.append("Problem1.xml reference un script Python (CX II seulement)")
            return infos, "python", name, data.decode("utf-8")
    infos.append("ATTENTION: aucun script trouve")
    return infos, None, None, None


class H(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header("Cross-Origin-Opener-Policy", "same-origin")
        self.send_header("Cross-Origin-Embedder-Policy", "credentialless")
        self.send_header("Cache-Control", "no-store")
        super().end_headers()

    def translate_path(self, path):
        # /v/<n'importe quoi>/fichier -> /fichier (contourne les caches)
        if path.startswith("/v/"):
            path = "/" + path.split("/", 3)[3] if path.count("/") >= 3 else "/"
        return super().translate_path(path)

    def do_POST(self):
        if not self.path.startswith("/tns"):
            self.send_error(404)
            return
        n = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(n)
        try:
            infos, lang, name, code = lire_tns(body)
            rep = {"ok": True, "infos": infos, "lang": lang, "name": name, "code": code}
        except Exception as e:
            rep = {"ok": False, "infos": ["Erreur: %s" % e]}
        data = json.dumps(rep).encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def log_message(self, *a):
        pass


print("Simulateur: http://localhost:%d/simulateur/lua.html (CX)" % PORT, flush=True)
print("            http://localhost:%d/simulateur/ (Python, CX II)" % PORT, flush=True)
http.server.ThreadingHTTPServer(("127.0.0.1", PORT), H).serve_forever()
