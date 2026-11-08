# Serveur local du simulateur.
# Les en-tetes COOP/COEP activent SharedArrayBuffer, necessaire pour que
# input() et get_key() bloquent comme sur la calculatrice.
# Usage: python server.py   puis ouvrir http://localhost:8765/simulateur/
import http.server, os, sys

PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 8765
os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

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

    def log_message(self, *a):
        pass

print("Simulateur: http://localhost:%d/simulateur/" % PORT, flush=True)
http.server.ThreadingHTTPServer(("127.0.0.1", PORT), H).serve_forever()
