# Port Python de Luna 2.1 (ndless-nspire/Luna, MPL 1.1), partie Python -> TNS.
# Usage: python py2tns.py script.py|script.lua sortie.tns
import sys, os, struct, zlib
from Crypto.Cipher import DES3

DEFAULT_DOC = bytes.fromhex(
    "0FCED8D28106865B4A4AC5CEA916F2D51DA82F6E0022F2F0C1A606774D7EA6C03AF05C74BAAA4460"
    "CD58E670D740F69C17DCF09477BFCADEF70209C962B15DEF22FA5137A0819148E1834DAD08312DD0"
    "D3E32D60AB13C2982BED395B092439922F0C7A4C9574913B0CF460CC7327CB077E7FA91787E2ACA2"
    "3BCCA0C4E38E89F0C0519FC2BECE2845C3D41190A6EC53A0FB5B466B41ADE953BB97DBB1D268E2F6"
    "360F2636759BE91F48ADE92967005819C3C01276"
    "A04A73F3B1D30918D606DD9724533E22A4FB82507B7C12884E7D4180FE72922987E85C5672FF2916"
    "8C425B8B9BA7D2086DD398FF91A99EF393A82E1CB2A96B6ADFF6CE2D1517CE6EC04F9A9C0EDF198D"
    "2DFA699F11D22012E07914044E628F0A2A18725A8B80B33C9BD567594B514DE0C33828C3DCCD3922"
    "128C4055")

TIEN_HEADER = bytes.fromhex(
    "0FCED8D28106865B99DDA23DD9E94BD431BB50B64DB32924706049381C30F899004B9264E458E6BC")

PY_HEADER = (b'TIXC0100-1.0?><prob xmlns="urn:TI.Problem" ver="1.0" pbname="">'
             b'<sym>\x0E\x01<card clay="0" h1="10000" h2="10000" w1="10000" '
             b'w2="10000"><isDummyCard>0\x0E\x03<flag>0\x0E\x04<wdgt xmlns:py="urn:'
             b'TI.PythonEditor" type="TI.PythonEditor" ver="1.0"><py:data><py:name>')
PY_FOOTER = (b'\x0E\x07<py:dirf>-10000000\x0E\x08\x0E\x06<py:mFlags>1024\x0E\x09'
             b'<py:value>10\x0E\x0A\x0E\x05\x0E\x02\x0E\x00')

LUA_HEADER = bytes.fromhex(
    "54495843303130302d312e303f3e3c70726f6220786d6c6e733d2275726e3a54492e50a85f5b1f0a"
    "22207665723d22312e30222070626e616d653d22223e3c73796d3e0e013c6361726420636c61793d"
    "2230222068313d22f10000ff222068323d22f10000ff222077313d22f10000ff222077323d22f100"
    "00ff223e3c697344756d6d79436172643e300e033c666c61673e300e043c7764677420786d6c6e73"
    "3a73633d2275726e3a54492e53ac84f22a4170702220747970653d2254492e53ac84f22a41707022"
    "207665723d22312e30223e3c73633a6d466c6167733e300e063c73633a76616c75653e2d310e073c"
    "73633a7363726970742076657273696f6e3d22353132222069643d2230223e3c215b43444154415b")
LUA_FOOTER = bytes.fromhex("5d5d3e0e080e050e020e00")

K = bytes([0x16, 0xA7, 0xA7, 0x32, 0x68, 0xA7, 0xBA, 0x73,
           0xD9, 0xA8, 0x86, 0xA4, 0x34, 0x45, 0x94, 0x10,
           0x3D, 0x80, 0x8C, 0xB5, 0xDF, 0xB3, 0x80, 0x6B])

def doccrypt(data):
    c = DES3.new(K, DES3.MODE_ECB)
    out = bytearray(data)
    incr = 0
    for off in range(0, len(out), 8):
        iv = bytes(4) + struct.pack("<I", (0x6FE21307 + incr) & 0xFFFFFFFF)
        incr = (incr + 1) % 1024
        ks = c.encrypt(iv)
        for i in range(min(8, len(out) - off)):
            out[off + i] ^= ks[i]
    return bytes(out)

def raw_deflate(data):
    co = zlib.compressobj(zlib.Z_DEFAULT_COMPRESSION, zlib.DEFLATED, -15, 8)
    return co.compress(data) + co.flush()

def build(py_path, out_path, tiversion=0x0500):
    name = os.path.basename(py_path).encode()
    src = open(py_path, "rb").read()
    if src.startswith(b"\xef\xbb\xbf"):
        src = src[3:]
    # la TI attend des fins de ligne LF uniquement
    src = src.replace(b"\r\n", b"\n").replace(b"\r", b"\n")
    # (nom, methode, donnees stockees, crc/taille sur donnees non compressees)
    if py_path.lower().endswith(".lua"):
        # Lua: le script est integre dans Problem1.xml (section CDATA)
        src = src.replace(b"]]>", b"]]]]><![CDATA[>")
        prob = TIEN_HEADER + doccrypt(raw_deflate(LUA_HEADER + src + LUA_FOOTER))
        entries = [
            (b"Document.xml", 0x0D, DEFAULT_DOC, DEFAULT_DOC),
            (b"Problem1.xml", 0x0D, prob, prob),
        ]
    else:
        prob = TIEN_HEADER + doccrypt(raw_deflate(PY_HEADER + name + PY_FOOTER))
        entries = [
            (b"Document.xml", 0x0D, DEFAULT_DOC, DEFAULT_DOC),
            (b"Problem1.xml", 0x0D, prob, prob),
            (name, 8, raw_deflate(src), src),
        ]
    # date DOS que minizip calcule pour une date "vide": jour 0, mois 1, an 1980
    DOSDATE = 0x00200000
    out = bytearray()
    central = bytearray()
    for idx, (fn, method, stored, plain) in enumerate(entries):
        offset = len(out)
        crc = zlib.crc32(plain) & 0xFFFFFFFF
        internal_fa = 1 if method == 8 else 0  # zlib marque le script comme texte
        if idx == 0:
            out += b"*TIMLP" + ("%04X" % tiversion).encode()
        else:
            out += struct.pack("<I", 0x04034B50)
        out += struct.pack("<HHHIIIIHH", 20, 0, method, DOSDATE, crc,
                           len(stored), len(plain), len(fn), 0)
        out += fn + stored
        central += struct.pack("<IHHHHIIIIHHHHHII", 0x02014B50, 0, 20, 0, method,
                               DOSDATE, crc, len(stored), len(plain), len(fn),
                               0, 0, 0, internal_fa, 0, offset) + fn
    cd_off = len(out)
    out += central
    out += struct.pack("<IHHHHIIH", 0x44504954, 0, 0, len(entries), len(entries),
                       len(central), cd_off, 0)
    open(out_path, "wb").write(out)

if __name__ == "__main__":
    build(sys.argv[1], sys.argv[2])
    print("ok ->", sys.argv[2])
