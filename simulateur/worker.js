// Worker: execute le script Python avec Pyodide.
// input() et get_key() bloquent grace a SharedArrayBuffer + Atomics.
importScripts("https://cdn.jsdelivr.net/pyodide/v0.26.4/full/pyodide.js");

let ctrl, data, keyCtrl, keyData;
const dec = new TextDecoder();

function blockingInput(prompt) {
  postMessage({ type: "input", prompt: String(prompt) });
  Atomics.store(ctrl, 0, 0);
  Atomics.wait(ctrl, 0, 0);
  const len = Atomics.load(ctrl, 1);
  const txt = dec.decode(data.slice(0, len));
  Atomics.store(ctrl, 0, 0);
  if (Atomics.load(ctrl, 2) === 1) throw new Error("STOP");
  return txt;
}

function getKey(wait) {
  // non bloquant comme sur la TI, sauf get_key(1)
  for (;;) {
    if (Atomics.load(ctrl, 2) === 1) throw new Error("STOP");
    if (Atomics.load(keyCtrl, 0) === 1) {
      const len = Atomics.load(keyCtrl, 1);
      const k = dec.decode(keyData.slice(0, len));
      Atomics.store(keyCtrl, 0, 0);
      return k;
    }
    Atomics.wait(keyCtrl, 0, 0, 30);
    if (!wait) {
      if (Atomics.load(keyCtrl, 0) === 1) continue;
      return "";
    }
  }
}

const PY_SETUP = `
import sys, types, builtins, json
import tibridge

def _input(p=""):
    s = tibridge.input(str(p))
    print(str(p) + s)
    return s
builtins.input = _input

def _d(*a):
    tibridge.draw(json.dumps(a))

m = types.ModuleType("ti_draw")
m.clear = lambda: _d("clear")
m.clear_rect = lambda x, y, w, h: _d("clear_rect", x, y, w, h)
m.draw_line = lambda x1, y1, x2, y2: _d("line", x1, y1, x2, y2)
m.draw_rect = lambda x, y, w, h: _d("rect", x, y, w, h)
m.fill_rect = lambda x, y, w, h: _d("frect", x, y, w, h)
m.draw_circle = lambda x, y, r: _d("circle", x, y, r)
m.fill_circle = lambda x, y, r: _d("fcircle", x, y, r)
m.draw_arc = lambda x, y, w, h, a0, da: _d("arc", x, y, w, h, a0, da)
m.fill_arc = lambda x, y, w, h, a0, da: _d("farc", x, y, w, h, a0, da)
m.draw_text = lambda x, y, s: _d("text", x, y, str(s))
m.draw_poly = lambda xs, ys: _d("poly", list(xs), list(ys))
m.fill_poly = lambda xs, ys: _d("fpoly", list(xs), list(ys))
def _color(r, g=None, b=None):
    if g is None:
        r, g, b = r
    _d("color", r, g, b)
m.set_color = _color
m.set_pen = lambda *a: _d("pen", *[str(x) for x in a])
m.use_buffer = lambda: None
m.paint_buffer = lambda: None
m.get_screen_dim = lambda: (318, 212)
sys.modules["ti_draw"] = m

s = types.ModuleType("ti_system")
s.get_key = lambda w=0: tibridge.getkey(1 if w else 0)
s.disp_clr = lambda: tibridge.draw(json.dumps(["cls"]))
sys.modules["ti_system"] = s
`;

let pyodide = null;

onmessage = async (e) => {
  const msg = e.data;
  if (msg.type === "init") {
    ctrl = new Int32Array(msg.sab, 0, 4);
    data = new Uint8Array(msg.sab, 16);
    keyCtrl = new Int32Array(msg.keySab, 0, 2);
    keyData = new Uint8Array(msg.keySab, 8);
    pyodide = await loadPyodide();
    pyodide.setStdout({ batched: (s) => postMessage({ type: "out", s }) });
    pyodide.setStderr({ batched: (s) => postMessage({ type: "err", s }) });
    pyodide.registerJsModule("tibridge", {
      input: blockingInput,
      getkey: (w) => getKey(w === 1),
      draw: (j) => postMessage({ type: "draw", cmd: JSON.parse(j) }),
    });
    pyodide.runPython(PY_SETUP);
    postMessage({ type: "ready" });
  } else if (msg.type === "run") {
    try {
      pyodide.globals.set("__src", msg.code);
      pyodide.runPython(
        "__g = {'__name__': '__main__'}\nexec(compile(__src, " +
          JSON.stringify(msg.name) + ", 'exec'), __g)"
      );
      postMessage({ type: "done" });
    } catch (err) {
      const t = String(err.message || err);
      if (t.includes("STOP")) postMessage({ type: "done", stopped: true });
      else postMessage({ type: "error", s: t });
    }
  }
};
