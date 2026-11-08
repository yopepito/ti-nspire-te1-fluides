# TE1 Phy2a - solveur fluides (revision)
# Entree vide = valeur de l'ancien test / de la serie.
# Unites acceptees a la saisie: 5cm, 6dl, 440mN, 4.7bar,
# 5lmin (L/min), 2min ... sinon valeur en SI.
# Lignes "> " = raisonnement a ecrire sur la copie.
from math import *

G = 9.81
PATM = 101300.0
RHOW = 1000.0
W = 32  # largeur d'ecran pour couper les phrases

# ---------------------------------------------------------
# saisie et affichage

UNITS = [("lmin", 1 / 60000.0), ("kpa", 1e3), ("hpa", 1e2),
         ("bar", 1e5), ("atm", 101325.0), ("mpa", 1e6),
         ("mm", 1e-3), ("cm", 1e-2), ("dm", 1e-1), ("km", 1e3),
         ("ml", 1e-6), ("cl", 1e-5), ("dl", 1e-4),
         ("mn", 1e-3), ("min", 60.0), ("pa", 1.0), ("kg", 1.0),
         ("g", 1e-3), ("l", 1e-3), ("n", 1.0), ("m", 1.0),
         ("s", 1.0)]

def conv(s):
  t = s.strip().lower().replace(" ", "").replace("/", "")
  for u, f in UNITS:
    if t.endswith(u) and len(t) > len(u):
      return float(eval(t[:-len(u)])) * f
  return float(eval(t))

def ask(txt, d):
  s = input(txt + " [" + str(d) + "] ? ")
  if s.strip() == "":
    return d
  try:
    return conv(s)
  except:
    print("! valeur invalide, defaut pris")
    return d

def r3(x):
  return "%.4g" % x

def s3(x):
  # 3 chiffres significatifs, sans notation e si possible
  if x == 0:
    return "0"
  e = int(floor(log10(abs(x))))
  if e < -3 or e >= 6:
    return "%.2e" % x
  if e >= 2:
    q = 10 ** (e - 2)
    return "%.0f" % (round(x / q) * q)
  return ("%." + str(2 - e) + "f") % x

def wrap(txt, pre):
  mots = txt.split(" ")
  ligne = pre
  for m in mots:
    if len(ligne) + len(m) + 1 > W and ligne.strip() != pre.strip():
      print(ligne)
      ligne = "  " + m
    else:
      if ligne == pre:
        ligne = ligne + m
      else:
        ligne = ligne + " " + m
  if ligne.strip() != "":
    print(ligne)

def R(*l):
  # raisonnement: chaque argument = une phrase / un paragraphe
  for x in l:
    wrap(x, "> ")

def res(nom, v, u):
  print(nom + " = " + r3(v) + " " + u)
  print("  (copie, 3 c.s.: " + s3(v) + " " + u + ")")

def pause():
  input("--- [enter] ---")

def titre(t):
  print("")
  print("=" * 26)
  print(t)
  print("=" * 26)

# ---------------------------------------------------------
# schemas: ti_draw sur la calculatrice, texte sur PC

try:
  import ti_draw as D
  from ti_system import get_key
  HAS_DRAW = True
except:
  HAS_DRAW = False

def attendre_touche():
  k = ""
  while k == "":
    k = get_key()

def col(r, g, b):
  D.set_color(r, g, b)

def txt(x, y, s):
  D.draw_text(x, y, s)

BLEU = (40, 90, 210)
NOIR = (0, 0, 0)
ROUGE = (220, 0, 0)

def c(t):
  col(t[0], t[1], t[2])

def schema(nom):
  print("")
  print("SCHEMA A DESSINER: " + nom)
  if HAS_DRAW:
    try:
      D.clear()
      c(NOIR)
      SCHEMAS_DRAW[nom]()
      c(NOIR)
      txt(150, 210, "[touche] continuer")
      attendre_touche()
      D.clear()
      return
    except:
      pass
  print(SCHEMAS_TXT[nom])
  pause()

def d_pile():
  col(120, 170, 235); D.fill_rect(60, 40, 120, 60)
  c(BLEU); D.fill_rect(60, 100, 120, 30)
  col(160, 160, 160); D.fill_rect(60, 130, 120, 25)
  D.fill_rect(60, 155, 180, 12); D.fill_rect(228, 50, 12, 117)
  D.fill_circle(234, 45, 12)
  c(NOIR)
  D.draw_rect(60, 40, 120, 115)
  txt(70, 70, "mazout"); txt(70, 120, "eau"); txt(70, 148, "trichlo")
  c(ROUGE)
  txt(185, 45, "1 (Patm)"); txt(185, 103, "2")
  txt(185, 133, "3"); txt(150, 182, "4 fond"); txt(250, 50, "A")
  c(NOIR)
  D.draw_line(30, 40, 30, 100); txt(8, 75, "h1")
  D.draw_line(30, 100, 30, 130); txt(8, 120, "h2")
  D.draw_line(30, 130, 30, 155); txt(8, 148, "h3")
  D.draw_line(300, 45, 300, 160); txt(280, 110, "dz")
  txt(4, 18, "On descend: +rho*g*h ; on remonte: -")

def d_capil():
  c(BLEU); D.fill_rect(30, 150, 260, 40)
  c(NOIR); D.draw_rect(30, 150, 260, 40)
  D.draw_line(150, 20, 150, 175); D.draw_line(166, 20, 166, 175)
  col(160, 160, 160); D.fill_rect(151, 40, 15, 40)
  c(BLEU); D.fill_rect(151, 130, 15, 45)
  c(ROUGE)
  txt(172, 38, "1 air (Patm)"); txt(172, 52, "2 sous menisque Hg")
  txt(172, 86, "3 / 4 menisque bas Hg"); txt(172, 112, "5 air")
  txt(172, 132, "6 sous menisque eau")
  col(255, 255, 255); txt(180, 172, "7 niveau du bac")
  c(NOIR)
  D.draw_line(140, 40, 140, 80); txt(110, 64, "L")
  txt(4, 18, "Laplace a chaque menisque, rho*g*h dedans")

def d_jurin():
  c(BLEU); D.fill_rect(30, 140, 260, 50); D.fill_rect(151, 70, 15, 70)
  c(NOIR); D.draw_rect(30, 140, 260, 50)
  D.draw_line(150, 30, 150, 160); D.draw_line(166, 30, 166, 160)
  D.draw_arc(151, 64, 15, 12, 180, 180)
  D.draw_line(190, 70, 190, 140); txt(195, 110, "h")
  D.draw_line(166, 70, 185, 50); txt(186, 48, "theta")
  txt(30, 60, "R = r/cos(theta)")
  txt(4, 18, "Jurin: rho*g*h = 2*sigma*cos(th)/r")

def d_laplace():
  c(BLEU); D.draw_circle(100, 110, 50)
  c(NOIR)
  txt(80, 110, "P int"); txt(20, 40, "P ext")
  D.draw_line(100, 110, 150, 110); txt(118, 106, "R")
  D.draw_circle(230, 110, 40); D.draw_circle(230, 110, 36)
  txt(195, 170, "savon: 2 faces")
  txt(4, 18, "P cote concave > P cote convexe")
  txt(4, 200, "goutte: 2s/R   bulle savon: 4s/R")

def d_lances():
  col(120, 120, 120); D.fill_rect(262, 30, 30, 160)
  c(BLEU)
  D.draw_line(150, 180, 210, 120); D.draw_line(210, 120, 262, 32)
  D.fill_rect(60, 178, 95, 6)
  D.fill_rect(5, 110, 40, 75)
  c(NOIR)
  D.draw_circle(60, 172, 10)
  D.draw_line(300, 30, 300, 185); txt(304, 110, "H")
  c(ROUGE)
  txt(200, 25, "1 sommet v=0"); txt(212, 128, "2 buse")
  txt(100, 198, "3 sol"); txt(55, 160, "4")
  txt(8, 105, "6 Patm"); txt(30, 198, "5")
  c(NOIR)
  txt(4, 18, "Numeroter du sommet vers la citerne")

def d_couronne():
  c(NOIR)
  D.draw_line(80, 30, 80, 70); D.draw_rect(70, 70, 20, 20)
  txt(40, 110, "air: P_air = m*g")
  D.draw_line(220, 30, 220, 95)
  c(BLEU); D.fill_rect(170, 85, 100, 70)
  col(230, 180, 0); D.fill_rect(210, 100, 20, 20)
  D.fill_rect(70, 70, 20, 20)
  c(NOIR)
  D.draw_line(240, 130, 240, 100); txt(244, 115, "F_A")
  D.draw_line(205, 120, 205, 150); txt(160, 150, "m*g")
  txt(160, 175, "eau: P_eau = P_air - F_A")
  txt(4, 18, "F_A = rho_f*V*g, V = volume total")

def d_ecoul():
  c(BLEU); D.fill_rect(40, 90, 240, 30)
  c(NOIR)
  D.draw_rect(40, 90, 240, 30)
  D.draw_line(40, 60, 280, 60); txt(150, 55, "L")
  D.draw_line(20, 90, 20, 120); txt(4, 108, "2r")
  D.draw_line(60, 105, 100, 105); D.draw_line(100, 105, 92, 100)
  txt(60, 140, "Q, v = Q/(pi*r^2)")
  c(ROUGE); txt(30, 85, "P1"); txt(270, 85, "P2")
  c(NOIR)
  txt(4, 18, "Re -> laminaire ? -> R -> dP = R*Q")

def d_serpentin():
  c(BLEU)
  ys = [30, 60, 90, 120, 150, 180]
  D.set_pen("thick", "solid")
  for i in range(6):
    x0 = 40 if (i == 0 or i == 5) else 90
    D.fill_rect(x0, ys[i] - 3, 240 - x0, 6)
  for i in range(5):
    if i % 2 == 0:
      D.draw_arc(225, ys[i], 30, 30, 270, 180)
    else:
      D.draw_arc(75, ys[i], 30, 30, 90, 180)
  D.set_pen("thin", "solid")
  D.fill_rect(37, 30, 6, 150)
  c(NOIR)
  D.fill_circle(40, 105, 12)
  col(255, 255, 255); D.fill_circle(40, 105, 9)
  c(NOIR); D.draw_circle(40, 105, 12)
  D.draw_line(34, 111, 40, 97); D.draw_line(40, 97, 46, 111)
  txt(55, 109, "pompe")
  c(ROUGE)
  txt(25, 50, "1"); txt(150, 25, "2")
  txt(262, 108, "3"); txt(150, 198, "4"); txt(25, 172, "0")
  c(NOIR)
  txt(4, 14, "a: haut/bas  b: rangs  2R: coudes")

def d_bern():
  c(BLEU); D.fill_rect(30, 140, 100, 30)
  D.fill_rect(130, 80, 150, 16)
  D.draw_line(130, 140, 130, 80); D.draw_line(130, 170, 130, 96)
  c(NOIR)
  D.draw_line(10, 195, 300, 195); txt(4, 205, "z = 0")
  D.draw_line(20, 155, 20, 195); txt(4, 180, "z1")
  D.draw_line(295, 88, 295, 195); txt(280, 150, "z2")
  c(ROUGE); txt(60, 135, "1 (P1, v1, S1)"); txt(170, 75, "2 (P2, v2, S2)")
  c(NOIR)
  txt(4, 18, "P + rho*g*z + rho*v^2/2 = cste")

def d_divers():
  c(BLEU); D.fill_rect(40, 120, 230, 40)
  D.fill_rect(40, 80, 30, 40); D.fill_rect(190, 70, 80, 50)
  c(NOIR)
  D.draw_rect(40, 70, 30, 10); D.draw_rect(190, 60, 80, 10)
  D.draw_line(55, 40, 55, 70); txt(60, 45, "F1, S1")
  D.draw_line(230, 30, 230, 60); txt(236, 40, "F2, S2")
  txt(4, 18, "Pascal: F1/S1 = F2/S2 (meme z)")

SCHEMAS_DRAW = {"pile": d_pile, "capil": d_capil, "jurin": d_jurin,
                "laplace": d_laplace, "lances": d_lances,
                "couronne": d_couronne, "ecoul": d_ecoul,
                "serpentin": d_serpentin, "bern": d_bern,
                "divers": d_divers}

SCHEMAS_TXT = {
"pile":
"""     air  1 (Patm, P_rel=0)
   +--------+      ( A )
   | mazout |  h1    |
   +--------+ 2      |
   |  eau   |  h2    | dz
   +--------+ 3      |
   |trichlo |  h3    |
   +--------+ 4 -----+
Noter rho et h de chaque
couche, et dz (fond -> A).""",
"capil":
"""      | |  1 air (Patm)
      |#|  2 sous menisque Hg
      |#|  colonne Hg = L
      |#|  3 / 4 menisque bas Hg
      | |  5 air
      |~|  6 sous menisque eau
 ~~~~~|~|~~~~~ niveau bac
      |~|  7 (Patm)
Dessiner le sens de courbure
de chaque menisque.""",
"jurin":
"""      |(|  menisque, angle theta
      |~|   ^
      |~|   | h
 ~~~~~|~|~~~v~~~~ niveau bac
R = r/cos(theta)""",
"laplace":
"""   ( P_int )   goutte: 1 interface
    \\  R  /    dP = 2*sigma/R
   P_ext       bulle de savon:
               2 interfaces, 4*sigma/R""",
"lances":
"""          1 (sommet, v=0)
         /|      immeuble H
        / |
   2 buse |  (lance a 1 m)
   |      |
 4 pompe---3-- tuyau au sol
 |
 5 conduite
 |
[6 surface citerne, v=0]
Numeroter en remontant le
courant, depuis le sommet.""",
"couronne":
"""  dynamometre    dynamometre
      |              |
     [C]        ~~~~[C]~~~~
   air: P_air   eau: P_eau
Forces: poids m*g vers le bas,
F_A vers le haut, tension.""",
"ecoul":
"""  P1 ==================> P2
      <------- L -------->
  diametre 2r, debit Q""",
"serpentin":
"""   +==========2=======+
   1                  )
   |   (=============+
  (P)   +============) 3
   |   (=============+
   0    +============)
   +==========4=======+
2r = diam. tuyau, R = rayon
des coudes, a = long. haut/bas,
b = long. des rangs. Fleches
dans le sens de la pompe.""",
"bern":
"""  1 (P1,v1,z1)
  ====\\
       \\=========== 2 (P2,v2,z2)
 ---------------------- z = 0""",
"divers":
"""   F1           F2
   |            |
  [S1]~~~~~~~~[ S2 ]
Presse: meme pression
sous les deux pistons."""
}

# ---------------------------------------------------------
def ex_pile():
  titre("PILE DE FLUIDES / TUBE U")
  schema("pile")
  R("Les liquides sont immobiles et ne se melangent pas: ils forment des couches horizontales, du plus leger en haut au plus lourd en bas. Comme rien ne bouge, c'est un probleme d'hydrostatique.",
    "Dans UN meme fluide continu, la loi de l'hydrostatique relie deux points: P_b + rho*g*z_b = P_a + rho*g*z_a. Elle n'est valable qu'a l'interieur d'un seul fluide, c'est pourquoi on avance interface par interface en changeant de rho a chaque couche.",
    "On demande des pressions RELATIVES: P - Patm. A la surface libre, le liquide touche l'air, donc P = Patm et la pression relative y vaut 0. C'est notre point de depart.",
    "Plus on descend, plus il y a de liquide au-dessus qui pese: la pression augmente de rho*g*h quand on descend de h.")
  pause()
  n = int(ask("nb de couches", 3))
  noms = ["mazout", "eau", "trichlo", "c4", "c5"]
  rhos = [820, 1000, 1500, 1000, 1000]
  hs = [0.9, 0.3, 0.13, 0.1, 0.1]
  p = 0.0
  rl = 0
  res_l = []
  for i in range(n):
    print("-- couche " + str(i + 1) + " (" + noms[i] + ")")
    rho = ask(" rho kg/m3", rhos[i])
    h = ask(" epaisseur", hs[i])
    rl = rho
    a = str(i + 1)
    b = str(i + 2)
    R("Le point " + b + " est a l'interface sous la couche de " + noms[i] + ". Entre " + a + " et " + b + " on ne traverse que ce fluide, donc l'hydrostatique s'applique avec rho = " + r3(rho) + ": P" + b + " = P" + a + " + rho*g*(H" + a + " - H" + b + "), ou H" + a + " - H" + b + " = " + r3(h) + " m est l'epaisseur de la couche.",
      "En retirant Patm de chaque cote, on obtient la pression relative en " + b + ": elle vaut celle en " + a + " plus le poids par unite de surface de la couche traversee.")
    print("P" + b + "-Patm = P" + a + "-Patm + rho*g*h")
    pn = p + rho * G * h
    print("= " + r3(p) + " + " + r3(rho) + "*9.81*" + r3(h))
    res("P" + b + "-Patm", pn, "Pa")
    res_l.append(("P" + b, pn))
    p = pn
    pause()
  print("-- point A dans l'autre branche")
  rho = ask(" rho branche", rl)
  dz = ask(" A plus haut que le fond de", 0.9)
  pa = p + rho * G * (-dz)
  R("Le fond du conteneur communique avec le tube qui monte vers A, et ce tube est rempli du MEME liquide sans interruption. On peut donc appliquer l'hydrostatique directement du fond (point 4) jusqu'a A, avec le rho de ce liquide.",
    "Le piege est le signe: en allant du fond vers A on REMONTE, donc H4 - HA = -" + r3(dz) + " m est negatif. Il y a moins de liquide au-dessus de A, la pression y est donc plus faible qu'au fond.")
  print("PA-Patm = P4-Patm + rho*g*(H4-HA)")
  print("= " + r3(p) + " + " + r3(rho) + "*9.81*(-" + r3(dz) + ")")
  res("PA-Patm", pa, "Pa")
  if pa < 0:
    R("La pression relative en A est negative: la pression absolue dans le petit reservoir est un peu plus faible que la pression atmospherique qui l'entoure.",
      "Si un trou apparait, le fluide va du cote de la pression la plus haute vers celui de la plus basse: c'est l'air exterieur qui entre sous forme de bulles, et le liquide ne s'echappe pas.")
  else:
    R("La pression relative en A est positive: le liquide pousse plus fort que l'air exterieur. Par un trou, le liquide s'echapperait vers l'exterieur.")
  print("P absolue = P relative + " + r3(PATM) + " Pa")
  print("-- resume")
  for nm, v in res_l:
    print(nm + "-Patm = " + s3(v) + " Pa")
  print("PA-Patm = " + s3(pa) + " Pa")

# ---------------------------------------------------------
def ex_capil():
  titre("CAPILLARITE")
  print("1 Jurin (hauteur)")
  print("2 Laplace (bulle/goutte)")
  print("3 tube Hg + air + eau")
  c_ = int(ask("choix", 3))
  if c_ == 1:
    schema("jurin")
    s = ask("sigma N/m", 0.0728)
    th = ask("theta deg", 0)
    rho = ask("rho", 1000)
    r = ask("r tube", 1e-4)
    R("Dans un tube tres fin, la surface du liquide n'est pas plate: elle forme un menisque, une calotte de sphere dont le rayon vaut R = r/cos(theta), ou theta est l'angle de contact avec le verre.",
      "D'apres Laplace, une surface courbe cree une difference de pression 2*sigma/R entre ses deux cotes. Pour l'eau, la pression juste sous le menisque est plus faible que Patm, ce qui aspire le liquide vers le haut.",
      "Le liquide monte jusqu'a ce que le poids de la colonne compense cette difference: rho*g*h = 2*sigma/R. En remplacant R, on obtient la loi de Jurin: h = 2*sigma*cos(theta)/(rho*g*r).")
    h = 2 * s * cos(radians(th)) / (rho * G * r)
    print("= 2*" + r3(s) + "*cos(" + r3(th) + ")/(" + r3(rho) + "*9.81*" + r3(r) + ")")
    res("h", h, "m")
    R("Interpretation: si theta < 90 deg (liquide mouillant, comme l'eau sur le verre), cos(theta) > 0 et le liquide monte. Si theta > 90 deg (mercure sur le verre), cos(theta) < 0 et le liquide descend sous le niveau du bac.",
      "Plus le tube est fin (r petit), plus l'effet est grand: h est inversement proportionnel a r.")
  elif c_ == 2:
    schema("laplace")
    s = ask("sigma N/m", 0.0728)
    Rr = ask("rayon R", 1e-3)
    k = ask("1 goutte/bulle, 2 savon", 1)
    f = 2 if k == 1 else 4
    R("La tension superficielle agit comme une membrane tendue: une surface courbe pousse vers son centre de courbure. A l'equilibre, la pression du cote CONCAVE (l'interieur de la courbure) est donc plus grande que celle du cote convexe.",
      "Pour une seule interface (goutte, bulle de gaz dans un liquide), la loi de Laplace donne dP = 2*sigma/R. Une bulle de savon est un film qui a DEUX interfaces avec l'air, une dedans et une dehors: les deux sauts s'additionnent et dP = 4*sigma/R.")
    dp = f * s / Rr
    print("dP = " + str(f) + "*" + r3(s) + "/" + r3(Rr))
    res("dP", dp, "Pa")
    R("Plus la bulle est petite, plus la surpression est grande, puisque dP est inversement proportionnel a R.")
  else:
    schema("capil")
    r = ask("r tube", 1e-4)
    sh = ask("sigma Hg N/m", 0.44)
    ah = ask("angle Hg (R=r/cos a) deg", 50)
    rhh = ask("rho Hg", 13546)
    L = ask("long. colonne Hg", 0.1)
    sw = ask("sigma eau N/m", 0.0728)
    aw = ask("angle eau deg", 0)
    rw = ask("rho eau", 1000)
    Rh = r / cos(radians(ah))
    Rw = r / cos(radians(aw))
    d1 = 2 * sh / Rh
    d2 = rhh * G * L
    d3 = -d1
    d4 = 0.0
    d5 = -2 * sw / Rw
    R("Methode: on suit le tube de haut en bas, du point 1 au point 7, en notant la variation de pression a chaque etape. Il n'y a que deux types d'etapes.",
      "Quand on traverse un menisque, la pression saute de 2*sigma/R (Laplace): elle augmente si on entre du cote concave, elle diminue si on en sort. Quand on descend dans un fluide, elle augmente de rho*g*h (hydrostatique).",
      "Le rayon de chaque menisque vaut R = r/cos(angle): c'est la donnee 'rayon membrane' de l'enonce.")
    print("R_Hg = r/cos(a) = " + r3(Rh) + " m")
    pause()
    R("1) Le mercure ne mouille pas le verre: son menisque superieur est BOMBE vers le haut, comme une goutte. L'interieur de la courbure (cote concave) est dans le mercure.",
      "En passant de 1 (air) a 2 (mercure), on entre du cote concave: la pression augmente de 2*sigma_Hg/R_Hg.")
    print("P2-P1 = +2*s_Hg/R_Hg = 2*" + r3(sh) + "/" + r3(Rh))
    res("P2-P1", d1, "Pa")
    pause()
    R("2) De 2 a 3, on descend dans la colonne de mercure, de longueur L. C'est de l'hydrostatique pure dans un seul fluide: la pression augmente de rho_Hg*g*L.")
    print("P3-P2 = rho_Hg*g*L = " + r3(rhh) + "*9.81*" + r3(L))
    res("P3-P2", d2, "Pa")
    pause()
    R("3) Le menisque inferieur du mercure est bombe vers le bas, vers l'air situe en dessous. On passe du mercure (cote concave) a l'air (cote convexe): la pression diminue.",
      "Le rayon est le meme qu'en haut, donc le saut a la meme valeur, avec le signe oppose.")
    res("P4-P3", d3, "Pa")
    pause()
    R("4) De 4 a 5 on traverse la colonne d'air. L'air est environ 800 fois plus leger que l'eau, donc rho_air*g*h est negligeable: la pression ne change pas.")
    res("P5-P4", d4, "Pa")
    pause()
    R("5) L'eau mouille le verre (angle 0): son menisque est CREUX, en forme de cuvette, et l'interieur de la courbure est du cote de l'air.",
      "En passant de l'air (5) a l'eau (6), on sort du cote concave: la pression diminue de 2*sigma_eau/R_eau.")
    print("P6-P5 = -2*s_eau/R_eau = -2*" + r3(sw) + "/" + r3(Rw))
    res("P6-P5", d5, "Pa")
    pause()
    R("6) Entre le menisque d'eau (6) et le point 7 au niveau de la surface du bac, on est dans l'eau: P7 - P6 = rho_e*g*h, ou h est la hauteur de 6 au-dessus de 7. C'est la seule inconnue.",
      "7) Le point 1 est a l'air libre et le point 7 est au niveau de la surface libre du bac: les deux sont a la pression atmospherique. Donc P7 - P1 = 0, et cette difference est aussi la somme des six variations calculees.",
      "8) On ecrit cette somme egale a zero et on isole h. C'est une equation a une seule inconnue, construite uniquement avec les resultats precedents.")
    s = d1 + d2 + d3 + d4 + d5
    h = -s / (rw * G)
    print("0 = d1+d2+d3+d4+d5 + rho_e*g*h")
    print("h = -(d1+...+d5)/(rho_e*g)")
    print("somme d1..d5 = " + r3(s) + " Pa")
    print("h = " + r3(-s) + "/(" + r3(rw) + "*9.81)")
    res("h", h, "m")
    if h < 0:
      R("h est negatif: le menisque d'eau se trouve " + r3(-h) + " m SOUS le niveau du bac. Les deux sauts du mercure s'annulent, mais son poids (rho_Hg*g*L) comprime l'air enferme, qui repousse l'eau vers le bas bien plus que la capillarite ne la fait monter.")
    else:
      R("h est positif: l'eau monte de " + r3(h) + " m au-dessus du niveau du bac.")

# ---------------------------------------------------------
def ex_lances():
  titre("BERNOULLI LANCES/POMPE")
  schema("lances")
  et = ask("nb etages", 10)
  he = ask("m par etage", 3)
  zl = ask("hauteur lance", 1)
  db = ask("d buse", 0.05)
  n = ask("nb lances", 4)
  dt = ask("d tuyau", 0.1)
  pmax = ask("P max tuyau", 4.7e5)
  H = et * he
  R("Hypotheses: on neglige les frottements (fluide parfait), l'eau est incompressible et le regime est stationnaire. Ce sont exactement les conditions de l'equation de Bernoulli: P + rho*g*z + 1/2*rho*v^2 reste constant le long d'une ligne de courant.",
    "Strategie: on part de ce qu'on connait le mieux, le sommet du jet, et on remonte le courant point par point jusqu'a la citerne: 1 sommet, 2 buse, 3 tuyau au sol, 4 pompe, 5 conduite, 6 surface de la citerne.")
  pause()
  R("1) Pour pousser plus d'eau, il faut plus de pression a la sortie de la buse. Inversement, le debit le plus faible qui fonctionne encore correspond a la pression la plus basse possible a la sortie: la pression atmospherique. On pose donc P2 = Patm.")
  pause()
  dz = H - zl
  v2 = sqrt(2 * G * dz)
  R("2) On applique Bernoulli entre le sommet du jet (1) et la sortie de la buse (2). Au sommet, l'eau est a l'air libre (P1 = Patm) et sa vitesse verticale est nulle: c'est le minimum pour atteindre la hauteur H. A la buse, P2 = Patm.",
    "Les pressions atmospheriques s'annulent des deux cotes. Il reste rho*g*(z1 - z2) = 1/2*rho*v2^2: toute l'energie cinetique a la sortie se transforme en energie potentielle. On obtient v2 = sqrt(2*g*(z1 - z2)), avec z1 - z2 = H moins la hauteur de la lance.")
  print("z1-z2 = " + r3(H) + " - " + r3(zl) + " = " + r3(dz) + " m")
  print("v2 = sqrt(2*9.81*" + r3(dz) + ")")
  res("v2", v2, "m/s")
  pause()
  sb = pi * db ** 2 / 4
  q1 = sb * v2
  R("3) Le debit volumique est le volume d'eau qui sort par seconde: section de la buse multipliee par la vitesse. Q = pi*db^2/4 * v2.")
  print("Q = pi*" + r3(db) + "^2/4*" + r3(v2))
  res("Q lance", q1, "m3/s")
  print("  = " + r3(q1 * 1000) + " l/s")
  qp = n * q1
  R("4) Toute l'eau qui sort des " + r3(n) + " lances passe d'abord par la pompe. L'eau etant incompressible, rien ne s'accumule en route: Q pompe = n * Q lance.")
  res("Q pompe", qp, "m3/s")
  print("  = " + r3(qp * 1000) + " l/s")
  pause()
  v3 = v2 * (db / dt) ** 2
  R("5) Dans le tuyau, le debit est le meme qu'a la buse (conservation du debit): pi*db^2/4*v2 = pi*dt^2/4*v3. Le tuyau etant plus large, l'eau y va plus lentement: v3 = v2*(db/dt)^2. Attention a ne pas oublier le carre, car les sections dependent du diametre au carre.")
  print("v3 = " + r3(v2) + "*(" + r3(db) + "/" + r3(dt) + ")^2")
  res("v3", v3, "m/s")
  p3 = PATM + RHOW * (G * zl + 0.5 * (v2 ** 2 - v3 ** 2))
  R("On applique ensuite Bernoulli entre le tuyau au sol (3, z3 = 0) et la buse (2, z2 = hauteur de la lance, P2 = Patm). La pression dans le tuyau doit fournir a la fois l'acceleration de l'eau (v3 -> v2) et la montee jusqu'a la lance:",
    "P3 = Patm + rho*(g*(z2 - z3) + 1/2*(v2^2 - v3^2)).")
  print("= " + r3(PATM) + " + 1000*(9.81*" + r3(zl) + " + 0.5*(" + r3(v2) + "^2 - " + r3(v3) + "^2))")
  res("P3", p3, "Pa")
  print("  = " + r3(p3 / 1e5) + " bar")
  if p3 < pmax:
    R("P3 reste inferieure a la pression maximale de " + r3(pmax / 1e5) + " bar que supportent les tuyaux: il n'y a pas de danger d'eclatement.")
  else:
    R("P3 depasse la pression maximale de " + r3(pmax / 1e5) + " bar: les tuyaux risquent d'eclater.")
  pause()
  print("-- conduite citerne -> pompe")
  dc = ask("d conduite", 0.12)
  hc = ask("haut. eau au-dessus pompe", 4.3)
  for nn in [n, n + 1]:
    v5 = nn * v3 * (dt / dc) ** 2
    p5 = PATM + RHOW * (G * hc - 0.5 * v5 ** 2)
    print("-> avec " + r3(nn) + " lances:")
    R("La conduite entre la citerne et la pompe transporte l'eau de tous les tuyaux a la fois. Par conservation du debit: v5 = n*v3*(dt/dc)^2.")
    print("v5 = " + r3(nn) + "*" + r3(v3) + "*(" + r3(dt) + "/" + r3(dc) + ")^2")
    res("v5", v5, "m/s")
    R("On applique Bernoulli entre la surface de la citerne (6) et la conduite (5). A la surface, P6 = Patm, et v6 est presque nulle parce que la citerne est tres large: le niveau descend tres lentement.",
      "P5 = Patm + rho*(g*(z6 - z5) - 1/2*v5^2). La hauteur d'eau augmente la pression, mais la vitesse dans la conduite la fait baisser.")
    print("= " + r3(PATM) + " + 1000*(9.81*" + r3(hc) + " - 0.5*" + r3(v5) + "^2)")
    res("P5", p5, "Pa")
    if p5 < PATM:
      R("P5 est plus faible que la pression atmospherique: l'air exterieur pousse plus fort sur la paroi que l'eau a l'interieur. Un tuyau souple s'ecraserait, il faut donc une conduite RIGIDE.")
    if p5 <= 0:
      R("Une pression absolue negative n'a pas de sens physique: cela signifie que la pompe ne peut pas aspirer autant d'eau. En realite, quand P5 s'approche de zero, l'eau se met a bouillir a temperature ambiante a l'entree de la conduite: c'est la CAVITATION, qui abime la pompe.")
    pause()
  q1b = qp / (n + 1)
  v2b = q1b / sb
  hj = v2b ** 2 / (2 * G) + zl
  R("Hauteur maximale du jet avec n+1 lances. Si la pompe fournit toujours le meme debit, il est partage entre plus de lances: chaque lance recoit Q pompe/(n+1), donc l'eau sort moins vite (v = Q/S).",
    "Bernoulli entre la buse et le sommet du jet donne alors H = v^2/(2g) + hauteur de la lance: le jet monte moins haut.")
  res("Q lance", q1b, "m3/s")
  res("v buse", v2b, "m/s")
  res("H max", hj, "m")

# ---------------------------------------------------------
def ex_couronne():
  titre("ARCHIMEDE 2 MATERIAUX")
  schema("couronne")
  fa = ask("poids air N", 5.3955)
  fe = ask("poids eau N", 4.6131)
  r1 = ask("rho 1 (or)", 19320)
  r2 = ask("rho 2 (diamant)", 3510)
  rf = ask("rho fluide", 1000)
  m = fa / G
  R("Idee: on ne peut pas separer l'or et les diamants, mais les deux pesees donnent deux informations, la masse totale et le volume total. Avec deux materiaux de masses volumiques differentes, ces deux informations suffisent pour trouver les deux masses.",
    "1) Dans l'air, la poussee de l'air est negligeable car l'air est tres leger. Le dynamometre mesure donc directement le poids de la couronne: P_air = m*g, d'ou la masse totale.")
  print("m = P_air/g = " + r3(fa) + "/9.81")
  res("m", m, "kg")
  pa = fa - fe
  R("2) Dans l'eau, la couronne parait plus legere parce que l'eau la pousse vers le haut: c'est la poussee d'Archimede. Le dynamometre mesure P_eau = P_air - F_A, donc F_A = P_air - P_eau.")
  print("F_A = " + r3(fa) + " - " + r3(fe))
  res("F_A", pa, "N")
  v = pa / (rf * G)
  R("3) La poussee d'Archimede est egale au poids de l'eau deplacee: F_A = rho_eau*V*g. Comme la couronne est entierement immergee, le volume d'eau deplace est exactement le volume de la couronne. On prend bien la masse volumique du FLUIDE, pas celle de l'objet.")
  print("V = F_A/(rho_f*g) = " + r3(pa) + "/(" + r3(rf) + "*9.81)")
  res("V", v, "m3")
  pause()
  R("4) On a deux inconnues, m1 (or) et m2 (diamants), et deux equations: la masse totale, m1 + m2 = m, et le volume total, m1/rho1 + m2/rho2 = V, puisque le volume de chaque materiau vaut sa masse divisee par sa masse volumique.",
    "On remplace m1 = m - m2 dans l'equation du volume, puis on met m2 en facteur pour l'isoler.")
  m2 = (v - m / r1) / (1 / r2 - 1 / r1)
  print("m2 = (V - m/rho1)/(1/rho2 - 1/rho1)")
  print("= (" + r3(v) + " - " + r3(m) + "/" + r3(r1) + ")/(1/" + r3(r2) + " - 1/" + r3(r1) + ")")
  res("m2 (diamants)", m2, "kg")
  res("m1 (or)", m - m2, "kg")
  R("Verification: m1 et m2 doivent etre positives et leur somme egale a m. Une masse negative signalerait une erreur de saisie, par exemple deux pesees inversees.")

# ---------------------------------------------------------
def ex_ecoul():
  titre("ECOULEMENT VISQUEUX")
  schema("ecoul")
  rho = ask("rho", 900)
  eta = ask("eta Pa.s", 0.1)
  d = ask("diametre", 0.02)
  L = ask("longueur", 10)
  print("Q connu (1), debit massique (2), v (3)")
  k = ask("choix", 1)
  r = d / 2
  S = pi * r ** 2
  if k == 1:
    Q = ask("Q m3/s", 1e-4)
  elif k == 2:
    mq = ask("debit massique kg/s", 0.09)
    Q = mq / rho
    R("Le debit massique (kg/s) et le debit volumique (m3/s) sont lies par la masse volumique: Q = m_point/rho.")
  else:
    Q = ask("v m/s", 0.3) * S
  v = Q / S
  R("La vitesse moyenne dans le tuyau vaut v = Q/S, avec S = pi*r^2. Attention: r est le RAYON, donc la moitie du diametre.")
  print("S = " + r3(S) + " m2, v = " + r3(v) + " m/s")
  Re = rho * v * d / eta
  R("Avant de choisir une formule de perte de charge, il faut savoir si l'ecoulement est laminaire ou turbulent. Le nombre de Reynolds compare l'inertie du fluide a sa viscosite: Re = rho*v*D/eta, ou de facon equivalente Re = 2*rho*Q/(pi*r*eta).")
  print("Re = " + r3(rho) + "*" + r3(v) + "*" + r3(d) + "/" + r3(eta))
  res("Re", Re, "")
  if Re < 2000:
    R("Re < 2000: la viscosite domine, l'ecoulement est LAMINAIRE. Le fluide glisse en couches regulieres.")
  elif Re < 4000:
    R("2000 < Re < 4000: zone de TRANSITION. Le regime est instable, le signaler sur la copie.")
  else:
    R("Re > 4000: l'inertie domine, l'ecoulement est TURBULENT, avec des tourbillons.")
  pause()
  if Re < 2000:
    Rh = 8 * eta * L / (pi * r ** 4)
    R("En regime laminaire, on utilise la loi de Poiseuille. La resistance hydraulique d'un tuyau droit vaut R = 8*eta*L/(pi*r^4). Elle augmente avec la longueur et la viscosite, et diminue tres vite quand le rayon augmente (r a la puissance 4).")
    print("= 8*" + r3(eta) + "*" + r3(L) + "/(pi*" + r3(r) + "^4)")
  else:
    Rh = 0.3164 * rho * Q / (Re ** 0.25 * pi ** 2 * r ** 5) * L
    R("En regime turbulent, Poiseuille n'est plus valable. On utilise la correlation de Blasius: R = 0.3164*rho*Q*L/(Re^0.25*pi^2*r^5).")
  res("R", Rh, "Pa.s/m3")
  dp = Rh * Q
  R("La perte de charge suit une loi analogue a la loi d'Ohm (U = R*I): dP = R*Q. C'est la difference de pression necessaire pour pousser le debit Q a travers le tuyau malgre les frottements.",
    "Si le tuyau debouche a l'air libre, la pression a la sortie vaut Patm, donc la pression a l'entree vaut Patm + dP. La puissance a fournir pour maintenir l'ecoulement vaut P = Q*dP.")
  res("dP", dp, "Pa")
  res("P entree (sortie a l'air)", PATM + dp, "Pa")
  res("Puissance", Q * dp, "W")

# ---------------------------------------------------------
def ex_serpentin():
  titre("SERPENTIN (E05 ex.4)")
  schema("serpentin")
  ql = ask("debit", 5 / 60000.0)
  eta = ask("eta Pa.s", 0.2)
  rho = ask("rho", 900)
  p0 = ask("P0", PATM)
  a = ask("a", 5)
  b = ask("b", 3)
  r = ask("r tuyau", 0.008)
  Rc = ask("R coude", 0.1)
  vert = ask("1 paroi verticale, 0 sol", 1)
  l1 = 0.131
  l2 = 1.847
  g = G if vert == 1 else 0.0
  Q = ql
  print("Q = " + r3(Q) + " m3/s")
  R("Le circuit est ferme: l'huile tourne en boucle, poussee par la pompe. Le debit est le meme partout, car le regime est stationnaire et l'huile incompressible. Le vase d'expansion en 0 fixe la pression de reference: P0 = Patm.",
    "1) Pour savoir quelle formule de perte de charge utiliser, on determine le regime avec le nombre de Reynolds: Re = 2*rho*Q/(pi*r*eta).")
  Re = 2 * rho * Q / (pi * r * eta)
  print("Re = 2*" + r3(rho) + "*" + r3(Q) + "/(pi*" + r3(r) + "*" + r3(eta) + ")")
  res("Re", Re, "")
  if Re < 2000:
    R("Re est bien plus petit que 2000: l'huile tres visqueuse s'ecoule en regime LAMINAIRE. On peut donc utiliser Poiseuille pour les troncons droits.")
  else:
    R("Re > 2000: l'ecoulement n'est plus laminaire et la suite, basee sur Poiseuille, n'est plus valable.")
  pause()
  Rl = 8 * eta / (pi * r ** 4)
  def Rs(alpha):
    return (l1 + l2 * (2 * r / Rc) ** 3.5) * rho * Q / (2 * pi ** 3 * r ** 4) * alpha
  R("2) Le fluide perd de l'energie de deux facons. Dans les troncons DROITS, ce sont les pertes regulieres dues a la viscosite (Poiseuille): R(L) = 8*eta*L/(pi*r^4), proportionnelle a la longueur.",
    "Dans les COUDES, le changement de direction cree des pertes singulieres supplementaires: R*(alpha) = (l1 + l2*(2r/R)^(7/2)) * rho*Q/(2*pi^3*r^4) * alpha, avec alpha l'angle total en radians, l1 = 0.131 et l2 = 1.847.")
  print("8*eta/(pi*r^4) = " + r3(Rl) + " Pa.s/m4")
  Ltot = 8 * Rc + 2 * a + 4 * b
  R("On compte tous les troncons droits en les cochant sur le dessin: le cote de la pompe mesure 8R (la hauteur du circuit moins les deux coins), le haut et le bas mesurent a chacun, et les quatre rangs du milieu mesurent b chacun. Ltot = 8R + 2a + 4b.",
    "On additionne aussi tous les angles: 2 coins d'un quart de tour (2 * pi/2 = pi) et 5 demi-tours (5 * pi), soit 6*pi radians au total.")
  print("Ltot = 8*" + r3(Rc) + " + 2*" + r3(a) + " + 4*" + r3(b) + " = " + r3(Ltot) + " m")
  Rtot = Rl * Ltot + Rs(6 * pi)
  res("R*(6pi)", Rs(6 * pi), "Pa.s/m3")
  res("R total", Rtot, "Pa.s/m3")
  pause()
  Pp = Rtot * Q ** 2
  R("On applique Bernoulli generalise sur un tour complet, de 0 jusqu'a 0 dans le sens de la pompe: (B_arrivee - B_depart)*Q = -R_total*Q^2 + P_pompe. Comme on revient au meme point, B_arrivee = B_depart et le membre de gauche est nul.",
    "Donc P_pompe = R_total*Q^2: en regime stationnaire, la pompe fournit exactement l'energie perdue par frottement sur un tour.")
  print("P_pompe = " + r3(Rtot) + "*" + r3(Q) + "^2")
  res("P_pompe", Pp, "W")
  pause()
  R("3) Pour la pression en chaque point, on applique Bernoulli generalise entre deux points successifs, toujours dans le sens de la pompe: (B_j - B_i)*Q = -[R(L) + R*(alpha)]*Q^2, plus P_pompe si la pompe se trouve sur le troncon.",
    "La section est la meme partout, donc la vitesse aussi: les termes 1/2*rho*v^2 s'annulent. Il reste P_j = P_i + rho*g*(z_i - z_j) - [R(L) + R*(alpha)]*Q, plus P_pompe/Q sur le troncon de la pompe.")
  if g == 0:
    R("Circuit horizontal (chauffage au sol): tous les points sont a la meme altitude. On refait exactement les memes calculs en posant g = 0, seules les pertes et la pompe comptent.")
  segs = [("0->1", 8 * Rc, 0.0, -8 * Rc, True,
           "on traverse la pompe, qui ajoute P_pompe/Q. On monte de 8R, avec un troncon droit de 8R et aucun coude"),
          ("1->2", a - b / 2, pi / 2, -Rc, False,
           "un coin d'un quart de tour (pi/2), un troncon droit de a - b/2, et on monte encore de R jusqu'au tuyau du haut"),
          ("2->3", 5 * b / 2, 5 * pi / 2, 5 * Rc, False,
           "les troncons droits b/2 + b + b = 5b/2 et les coudes pi + pi + pi/2 = 5pi/2. On descend de 5R"),
          ("3->4", 5 * b / 2, 5 * pi / 2, 5 * Rc, False,
           "meme chemin que le precedent: 5b/2 de droit, 5pi/2 de coudes, et on descend encore de 5R")]
  P = p0
  resu = []
  for nom, L, al, dzz, pompe, desc in segs:
    pause()
    print("-- " + nom)
    R("Troncon " + nom + ": " + desc + ".")
    perte = (Rl * L + Rs(al)) * Q
    Pn = P + rho * g * dzz - perte
    if pompe:
      Pn = Pn + Pp / Q
    print("rho*g*(zi-zj) = " + r3(rho * g * dzz) + " Pa")
    print("pertes [R(L)+R*]*Q = " + r3(perte) + " Pa")
    if pompe:
      print("pompe P/Q = " + r3(Pp / Q) + " Pa")
    res("P" + nom[-1], Pn, "Pa")
    resu.append(("P" + nom[-1], Pn))
    P = Pn
  R("Coherence: la pression baisse tout au long du circuit a cause des frottements, et c'est la pompe, juste apres le point 0, qui la remonte.")
  print("-- resume")
  print("Re = " + s3(Re) + ", P_pompe = " + s3(Pp) + " W")
  for nm, v in resu:
    print(nm + " = " + s3(v / 1000) + " kPa")

# ---------------------------------------------------------
def ex_bern():
  titre("BERNOULLI 2 POINTS")
  schema("bern")
  R("Bernoulli exprime la conservation de l'energie par unite de volume le long d'une ligne de courant, pour un fluide parfait (sans frottement), incompressible et en regime stationnaire: P1 + rho*g*z1 + 1/2*rho*v1^2 = P2 + rho*g*z2 + 1/2*rho*v2^2.",
    "Les trois termes sont la pression, l'energie potentielle et l'energie cinetique. Si l'un augmente, les autres doivent baisser.",
    "Rappels utiles: a une surface libre P = Patm; dans un grand reservoir la vitesse est presque nulle; dans un tuyau le debit se conserve, S1*v1 = S2*v2.")
  print("Inconnue: 1 P2, 2 v2, 3 z2")
  k = ask("choix", 1)
  rho = ask("rho", 1000)
  p1 = ask("P1", PATM)
  z1 = ask("z1", 0)
  v1 = ask("v1 m/s", 0)
  B1 = p1 + rho * G * z1 + 0.5 * rho * v1 ** 2
  print("B1 = P1 + rho*g*z1 + 1/2*rho*v1^2")
  res("B1", B1, "Pa")
  if k == 1:
    z2 = ask("z2", 0)
    print("v2: donnee(1) ou par diametres d1,d2 (2)")
    kk = ask("choix", 1)
    if kk == 2:
      d1 = ask("d1", 0.1)
      d2 = ask("d2", 0.05)
      v2 = v1 * (d1 / d2) ** 2
      R("Le debit se conserve: S1*v1 = S2*v2, donc v2 = v1*(d1/d2)^2. Un retrecissement accelere le fluide.")
      res("v2", v2, "m/s")
    else:
      v2 = ask("v2 m/s", 0)
    p2 = B1 - rho * G * z2 - 0.5 * rho * v2 ** 2
    R("On isole P2: P2 = B1 - rho*g*z2 - 1/2*rho*v2^2. Si le fluide accelere ou monte, sa pression diminue.")
    res("P2", p2, "Pa")
    print("  = " + r3(p2 / 1e5) + " bar")
  elif k == 2:
    p2 = ask("P2", PATM)
    z2 = ask("z2", 0)
    x = 2 * (B1 - p2 - rho * G * z2) / rho
    R("On isole v2: v2 = sqrt(2*(B1 - P2 - rho*g*z2)/rho). La vitesse vient de l'energie qui n'est ni sous forme de pression ni sous forme d'altitude.")
    if x < 0:
      print("impossible (negatif sous la racine): verifier les donnees")
    else:
      res("v2", sqrt(x), "m/s")
  else:
    p2 = ask("P2", PATM)
    v2 = ask("v2 m/s", 0)
    z2 = (B1 - p2 - 0.5 * rho * v2 ** 2) / (rho * G)
    R("On isole z2: z2 = (B1 - P2 - 1/2*rho*v2^2)/(rho*g).")
    res("z2", z2, "m")

# ---------------------------------------------------------
def ex_divers():
  titre("FORMULES RAPIDES")
  print("1 P=rho*g*h  2 F=P*S")
  print("3 presse F2=F1*S2/S1")
  print("4 Archimede FA=rho*V*g")
  print("5 F=2*sigma*L (film)")
  k = ask("choix", 1)
  if k == 1:
    rho = ask("rho", 1000)
    h = ask("h", 1)
    R("Hydrostatique: en descendant de h dans un fluide immobile de masse volumique rho, la pression augmente du poids de la colonne de fluide par unite de surface, soit rho*g*h.")
    res("dP", rho * G * h, "Pa")
  elif k == 2:
    p = ask("P", 1e5)
    d = ask("diametre", 0.1)
    S = pi * d ** 2 / 4
    R("La pression est une force repartie sur une surface: F = P*S. La surface d'un disque vaut pi*d^2/4. Convertir d en metres avant de calculer, sinon l'erreur est elevee au carre.")
    res("S", S, "m2")
    res("F", p * S, "N")
  elif k == 3:
    schema("divers")
    f1 = ask("F1 N", 100)
    d1 = ask("d1", 0.02)
    d2 = ask("d2", 0.2)
    R("Principe de Pascal: un liquide transmet la pression dans toutes les directions. Si les deux pistons sont a la meme hauteur, la pression est la meme sous chacun: F1/S1 = F2/S2.",
      "Le rapport des forces est donc le rapport des surfaces, soit le carre du rapport des diametres: F2 = F1*(d2/d1)^2. Une petite force sur le petit piston souleve une grande charge.")
    res("F2", f1 * (d2 / d1) ** 2, "N")
  elif k == 4:
    rho = ask("rho fluide", 1000)
    V = ask("V immerge m3", 1e-3)
    R("Poussee d'Archimede: le fluide pousse l'objet vers le haut avec une force egale au poids du fluide deplace, F_A = rho_fluide*V_immerge*g. On utilise le rho du FLUIDE et seulement la partie immergee du volume.")
    res("F_A", rho * V * G, "N")
  else:
    s = ask("sigma N/m", 0.0728)
    L = ask("L", 0.05)
    R("Un film de savon a deux faces, et chacune tire sur la tige avec une force sigma*L. La force totale vaut donc F = 2*sigma*L.")
    res("F", 2 * s * L, "N")

# ---------------------------------------------------------
VF = [
 ("Un fluide peut etre soit solide soit liquide.", "F",
  "Un fluide est un milieu qui s'ecoule: liquide, gaz ou plasma. Un solide garde sa forme et ne s'ecoule pas, ce n'est donc pas un fluide."),
 ("Les plasmas sont des fluides.", "V",
  "Un plasma est un gaz ionise. Comme un gaz, il n'a pas de forme propre et s'ecoule: c'est un fluide."),
 ("La viscosite est une caracteristique des fluides.", "V",
  "La viscosite mesure la resistance d'un fluide a l'ecoulement, c'est-a-dire les frottements internes entre ses couches. C'est une propriete propre a chaque fluide (eau, huile, miel...)."),
 ("L'ecoulement d'un fluide est un processus de relaxation.", "V",
  "Un fluide ne peut pas supporter durablement une contrainte de cisaillement: il se deforme et s'ecoule jusqu'a ce que la contrainte disparaisse. C'est ce retour progressif vers l'equilibre qu'on appelle relaxation."),
 ("Pour les fluides incompressibles, une seconde viscosite doit etre prise en compte pour les mouvements de compression ou de dilatation.", "F",
  "La seconde viscosite (viscosite de volume) n'intervient que si le volume du fluide change. Un fluide incompressible ne se comprime ni ne se dilate, donc ce terme ne joue aucun role."),
 ("Les frottements visqueux dans un fluide s'opposent aux gradients de vitesse d'ecoulement.", "V",
  "Quand deux couches voisines vont a des vitesses differentes, la viscosite freine la plus rapide et entraine la plus lente. Elle tend donc a egaliser les vitesses, c'est-a-dire a reduire le gradient de vitesse."),
 ("En hydrostatique, la pression depend de la viscosite du fluide.", "F",
  "En hydrostatique, le fluide est immobile: il n'y a aucun gradient de vitesse, donc aucun frottement visqueux. La pression ne depend que de rho, g et de la profondeur (P = P0 + rho*g*h)."),
 ("La poussee d'Archimede est une force verticale ascendante egale en norme au poids du fluide deplace.", "V",
  "C'est l'enonce meme du principe d'Archimede: F_A = rho_fluide*V_immerge*g, dirigee vers le haut."),
 ("La courbure de la surface de separation entre les deux milieux fluides indique une difference de temperature de part et d'autre.", "F",
  "La courbure d'une interface indique une difference de PRESSION, pas de temperature: c'est la loi de Laplace, dP = 2*sigma/R, avec la pression la plus grande du cote concave."),
 ("La loi de l'hydrostatique ne peut pas etre retrouvee a partir de l'equation de Bernoulli.", "F",
  "Si on pose v = 0 dans Bernoulli (fluide au repos), il reste P + rho*g*z = constante, ce qui est exactement la loi de l'hydrostatique. Elle en est donc un cas particulier."),
]

def ex_vf():
  titre("VRAI OU FAUX (TE1 2025)")
  R("Pour chaque affirmation, tape v ou f (ou juste [enter] pour voir directement la reponse). Le programme donne la bonne reponse, l'explication, puis ton score.")
  score = 0
  rep = 0
  for i in range(len(VF)):
    phrase, sol, expl = VF[i]
    print("")
    wrap(str(i + 1) + ". " + phrase, "")
    a = input("v / f ? ").strip().lower()
    nom = "VRAI" if sol == "V" else "FAUX"
    if a in ("v", "f"):
      rep = rep + 1
      if a.upper() == sol:
        score = score + 1
        print("Juste: " + nom)
      else:
        print("Faux, la reponse est " + nom)
    else:
      print("Reponse: " + nom)
    R(expl)
    pause()
  if rep > 0:
    print("Score: " + str(score) + " / " + str(rep))
  print("-- resume des reponses")
  ligne = ""
  for i in range(len(VF)):
    ligne = ligne + str(i + 1) + VF[i][1] + " "
  wrap(ligne, "")

# ---------------------------------------------------------
def main():
  while True:
    titre("TE1 FLUIDES - MENU")
    print("1 Pile fluides / tube U")
    print("2 Capillarite")
    print("3 Lances incendie/pompe")
    print("4 Archimede couronne")
    print("5 Reynolds / Poiseuille")
    print("6 Serpentin (E05 ex.4)")
    print("7 Bernoulli 2 points")
    print("8 Formules rapides")
    print("9 Vrai ou faux")
    print("0 Quitter")
    ch = input("choix ? ").strip()
    if ch == "0":
      break
    f = {"1": ex_pile, "2": ex_capil, "3": ex_lances,
         "4": ex_couronne, "5": ex_ecoul, "6": ex_serpentin,
         "7": ex_bern, "8": ex_divers, "9": ex_vf}.get(ch)
    if f:
      f()
      pause()

main()
