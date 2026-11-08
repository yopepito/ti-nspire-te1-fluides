# TE1 Phy2a - solveur fluides (revision)
# Entree vide = valeur de l'ancien test.
# Lignes "> " = raisonnement a ecrire sur la copie.
from math import *

G = 9.81
PATM = 101300.0
RHOW = 1000.0

def ask(txt, d):
  s = input(txt + " [" + str(d) + "] ? ")
  if s.strip() == "":
    return d
  try:
    return float(eval(s))
  except:
    print("! valeur invalide, defaut pris")
    return d

def r3(x):
  return "%.4g" % x

def R(*l):
  for x in l:
    print("> " + x)

def pause():
  input("--- [enter] ---")

def titre(t):
  print("")
  print("=" * 26)
  print(t)
  print("=" * 26)

# ---------------------------------------------------------
def ex_pile():
  titre("PILE DE FLUIDES / TUBE U")
  R("Fluides au repos, non",
    "miscibles: loi de",
    "l'hydrostatique",
    "P_b + rho*g*z_b = P_a + rho*g*z_a",
    "dans CHAQUE fluide.",
    "P relative = P - Patm.",
    "Surface libre a l'air:",
    "P = Patm => P_rel = 0.",
    "En descendant, P augmente.")
  pause()
  n = int(ask("nb de couches", 3))
  noms = ["mazout", "eau", "trichlo", "c4", "c5"]
  rhos = [820, 1000, 1500, 1000, 1000]
  hs = [0.9, 0.3, 0.13, 0.1, 0.1]
  p = 0.0
  rl = 0
  for i in range(n):
    print("-- couche " + str(i + 1) + " (" + noms[i] + ")")
    rho = ask(" rho kg/m3", rhos[i])
    h = ask(" epaisseur m", hs[i])
    rl = rho
    a = str(i + 1)
    b = str(i + 2)
    R("Point " + b + " = bas de la couche.",
      "Hydrostatique dans ce",
      "fluide entre " + a + " et " + b + ":",
      "P" + b + " = P" + a + " + rho*g*(H" + a + "-H" + b + ")",
      "On retire Patm des 2 cotes:")
    print("P" + b + "-Patm = P" + a + "-Patm")
    print("   + rho*g*(H" + a + "-H" + b + ")")
    pn = p + rho * G * h
    print("= " + r3(p) + " + " + r3(rho) + "*9.81*" + r3(h))
    print("= " + r3(pn) + " Pa")
    p = pn
    pause()
  print("-- point A dans l'autre")
  print("branche (on REMONTE)")
  rho = ask(" rho branche", rl)
  dz = ask(" A plus haut de m", 0.9)
  pa = p + rho * G * (-dz)
  R("Le fond et la branche",
    "contiennent le MEME fluide",
    "continu => hydrostatique",
    "du fond jusqu'a A.",
    "ATTENTION au signe: on",
    "remonte, donc H4-HA < 0",
    "et la pression BAISSE.")
  print("PA-Patm = P4-Patm")
  print("   + rho*g*(H4-HA)")
  print("H4-HA = -" + r3(dz) + " (<0!)")
  print("= " + r3(p) + " + " + r3(rho) + "*9.81*(-" + r3(dz) + ")")
  print("= " + r3(pa) + " Pa")
  if pa < 0:
    R("P_rel(A) < 0: la pression",
      "dans A est INFERIEURE a",
      "Patm. Si trou: l'air",
      "exterieur pousse plus fort",
      "=> des bulles d'AIR",
      "entrent, le liquide ne",
      "sort pas.")
  else:
    R("P_rel(A) > 0: P dans A",
      "superieure a Patm => le",
      "liquide s'echappe par le",
      "trou.")
  print("P absolue = rel + " + r3(PATM))

# ---------------------------------------------------------
def ex_capil():
  titre("CAPILLARITE")
  print("1 Jurin (hauteur)")
  print("2 Laplace (bulle/goutte)")
  print("3 tube Hg + air + eau")
  c = int(ask("choix", 3))
  if c == 1:
    s = ask("sigma N/m", 0.0728)
    th = ask("theta deg", 0)
    rho = ask("rho", 1000)
    r = ask("r tube m", 1e-4)
    R("Menisque = calotte de",
      "rayon R = r/cos(theta).",
      "Laplace: saut de pression",
      "2*sigma/R a l'interface.",
      "Hydrostatique: ce saut est",
      "compense par rho*g*h.",
      "rho*g*h = 2*sigma*cos(th)/r")
    h = 2 * s * cos(radians(th)) / (rho * G * r)
    print("Jurin: h = 2*sigma*cos(th)")
    print("          /(rho*g*r)")
    print("= 2*" + r3(s) + "*cos(" + r3(th) + ")")
    print("  /(" + r3(rho) + "*9.81*" + r3(r) + ")")
    print("h = " + r3(h) + " m")
    R("th<90 (mouillant, eau/",
      "verre): h>0, monte.",
      "th>90 (Hg/verre): h<0,",
      "le liquide descend.")
  elif c == 2:
    s = ask("sigma N/m", 0.0728)
    R_ = ask("rayon R m", 1e-3)
    k = ask("1 goutte/bulle, 2 savon", 1)
    f = 2 if k == 1 else 4
    R("Loi de Laplace: a travers",
      "une interface courbe, la",
      "pression est plus grande",
      "du cote CONCAVE.",
      "1 interface: 2*sigma/R.",
      "Bulle de savon: 2",
      "interfaces => 4*sigma/R.")
    dp = f * s / R_
    print("dP = " + str(f) + "*sigma/R")
    print("= " + str(f) + "*" + r3(s) + "/" + r3(R_))
    print("dP = " + r3(dp) + " Pa")
  else:
    r = ask("r tube m", 1e-4)
    sh = ask("sigma Hg N/m", 0.44)
    ah = ask("angle Hg (r/cos a) deg", 50)
    rhh = ask("rho Hg", 13546)
    L = ask("long. colonne Hg m", 0.1)
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
    R("Methode: on suit le tube",
      "de haut en bas, et on",
      "additionne les sauts:",
      "- interface courbe:",
      "  Laplace +-2*sigma/R",
      "  (+ si on entre du cote",
      "  concave)",
      "- dans un fluide:",
      "  hydrostatique rho*g*h.",
      "Rayon menisque R=r/cos(a)")
    print("R_Hg = r/cos(a) = " + r3(Rh) + " m")
    pause()
    R("1) Hg non mouillant:",
      "menisque BOMBE vers l'air.",
      "Le cote concave est dans",
      "le Hg => P2 > P1.")
    print("P2-P1 = +2*s_Hg/R_Hg")
    print(" = 2*" + r3(sh) + "/" + r3(Rh))
    print(" = " + r3(d1) + " Pa")
    pause()
    R("2) On descend de L dans",
      "le Hg: hydrostatique.")
    print("P3-P2 = rho_Hg*g*L")
    print(" = " + r3(rhh) + "*9.81*" + r3(L))
    print(" = " + r3(d2) + " Pa")
    pause()
    R("3) Menisque inferieur du",
      "Hg, bombe vers l'air du",
      "dessous. On SORT du cote",
      "concave => P baisse.",
      "Meme R => meme valeur.")
    print("P4-P3 = -2*s_Hg/R_Hg")
    print(" = " + r3(d3) + " Pa")
    pause()
    R("4) Colonne d'air:",
      "rho_air negligeable.")
    print("P5-P4 = 0 Pa")
    pause()
    R("5) Eau mouillante: menisque",
      "CREUX, concave vers l'air.",
      "On passe de l'air (concave)",
      "a l'eau => P baisse.")
    print("P6-P5 = -2*s_eau/R_eau")
    print(" = -2*" + r3(sw) + "/" + r3(Rw))
    print(" = " + r3(d5) + " Pa")
    pause()
    R("6) Point 7 sous le niveau",
      "du bac, h = hauteur de 6",
      "au-dessus de 7:",
      "P7-P6 = rho_e*g*h",
      "7) P1 et P7 sont tous deux",
      "a Patm => P7-P1 = 0 = somme",
      "des 6 sauts.",
      "8) On isole h:")
    s = d1 + d2 + d3 + d4 + d5
    h = -s / (rw * G)
    print("0 = d1+d2+d3+d4+d5")
    print("    + rho_e*g*h")
    print("h = -(d1+...+d5)/(rho_e*g)")
    print("somme d1..d5 = " + r3(s) + " Pa")
    print("h = " + r3(-s) + "/(" + r3(rw) + "*9.81)")
    print("h = " + r3(h) + " m")
    if h < 0:
      R("h<0: le menisque d'eau est",
        "SOUS le niveau du bac de",
        r3(-h) + " m: le Hg pese et",
        "comprime l'air, qui",
        "repousse l'eau vers le bas.")

# ---------------------------------------------------------
def ex_lances():
  titre("BERNOULLI LANCES/POMPE")
  et = ask("nb etages", 10)
  he = ask("m par etage", 3)
  zl = ask("hauteur lance m", 1)
  db = ask("d buse m", 0.05)
  n = ask("nb lances", 4)
  dt = ask("d tuyau m", 0.1)
  pmax = ask("P max tuyau bar", 4.7)
  H = et * he
  R("Hyp.: fluide parfait,",
    "incompressible, regime",
    "stationnaire => Bernoulli",
    "P + rho*g*z + 1/2*rho*v^2",
    "= cst le long du courant.",
    "Faire un schema et numeroter",
    "1 sommet jet, 2 buse,",
    "3 tuyau au sol, 4 pompe,",
    "5 conduite, 6 citerne.")
  pause()
  R("1) Plus P en sortie de buse",
    "est faible, plus le debit",
    "est faible. Debit MINIMAL",
    "=> P2 = Patm (jet a l'air).")
  pause()
  dz = H - zl
  v2 = sqrt(2 * G * dz)
  R("2) Bernoulli entre 1 et 2.",
    "En 1 (sommet): P1 = Patm,",
    "v1 = 0 (minimum pour",
    "atteindre H). P2 = Patm.",
    "Patm+rho*g*z1 = Patm",
    "   +rho*g*z2 + 1/2rho*v2^2",
    "=> v2 = sqrt(2g(z1-z2))",
    "z1-z2 = H - h lance")
  print("z1-z2 = " + r3(H) + "-" + r3(zl) + " = " + r3(dz) + " m")
  print("v2 = sqrt(2*9.81*" + r3(dz) + ")")
  print("v2 = " + r3(v2) + " m/s")
  pause()
  sb = pi * db ** 2 / 4
  q1 = sb * v2
  R("3) Debit = section * vitesse.")
  print("Q = pi*db^2/4 * v2")
  print(" = pi*" + r3(db) + "^2/4*" + r3(v2))
  print(" = " + r3(q1) + " m3/s")
  print(" = " + r3(q1 * 1000) + " l/s")
  qp = n * q1
  R("4) La pompe alimente les",
    "n lances: conservation du",
    "debit (incompressible).")
  print("Q pompe = n*Q lance")
  print(" = " + r3(n) + "*" + r3(q1))
  print(" = " + r3(qp) + " m3/s")
  print(" = " + r3(qp * 1000) + " l/s")
  pause()
  v3 = v2 * (db / dt) ** 2
  R("5) Conservation du debit",
    "dans un tuyau (liquide",
    "incompressible):",
    "pi*db^2/4*v2 = pi*dt^2/4*v3",
    "=> v3 = v2*(db/dt)^2")
  print("v3 = " + r3(v2) + "*(" + r3(db) + "/" + r3(dt) + ")^2")
  print("v3 = " + r3(v3) + " m/s")
  p3 = PATM + RHOW * (G * zl + 0.5 * (v2 ** 2 - v3 ** 2))
  R("Puis Bernoulli entre 3",
    "(sol, z3=0) et 2 (buse,",
    "z2 = h lance, P2 = Patm):",
    "P3 = Patm + rho*(g*(z2-z3)",
    "     + 1/2*(v2^2 - v3^2))")
  print("= " + r3(PATM) + "+1000*(9.81*" + r3(zl))
  print("  +0.5*(" + r3(v2) + "^2-" + r3(v3) + "^2))")
  print("P3 = " + r3(p3) + " Pa")
  print("   = " + r3(p3 / 1e5) + " bar")
  if p3 / 1e5 < pmax:
    R("P3 < " + r3(pmax) + " bar => pas de",
      "danger d'eclatement.")
  else:
    R("P3 > " + r3(pmax) + " bar => DANGER",
      "d'eclatement.")
  pause()
  print("-- conduite citerne->pompe")
  dc = ask("d conduite m", 0.12)
  hc = ask("haut. eau / pompe m", 4.3)
  for nn in [n, n + 1]:
    v5 = nn * v3 * (dt / dc) ** 2
    p5 = PATM + RHOW * (G * hc - 0.5 * v5 ** 2)
    print("-> avec " + r3(nn) + " lances:")
    R("Debit conserve: la conduite",
      "porte le debit des " + r3(nn),
      "tuyaux: v5 = n*v3*(dt/dc)^2")
    print("v5 = " + r3(nn) + "*" + r3(v3) + "*(" + r3(dt) + "/" + r3(dc) + ")^2")
    print("v5 = " + r3(v5) + " m/s")
    R("Bernoulli entre 6 (surface",
      "citerne: P6=Patm, v6=0,",
      "grande section) et 5:",
      "P5 = Patm + rho*(g*(z6-z5)",
      "     - 1/2*v5^2)")
    print("= " + r3(PATM) + "+1000*(9.81*" + r3(hc))
    print("  -0.5*" + r3(v5) + "^2)")
    print("P5 = " + r3(p5) + " Pa")
    if p5 < PATM:
      R("P5 < Patm: la pression",
        "exterieure ecraserait un",
        "tuyau souple => paroi",
        "RIGIDE obligatoire.")
    if p5 <= 0:
      R("P absolue < 0: impossible!",
        "Bien avant, quand P5 -> 0,",
        "l'eau se met a bouillir:",
        "CAVITATION.")
    pause()
  q1b = qp / (n + 1)
  v2b = q1b / sb
  hj = v2b ** 2 / (2 * G) + zl
  R("Hauteur max avec n+1 lances",
    "(hyp.: meme debit pompe):",
    "Q lance = Q pompe/(n+1),",
    "v = Q/S, puis Bernoulli",
    "buse -> sommet:",
    "H = v^2/(2g) + h lance")
  print("Q lance = " + r3(q1b) + " m3/s")
  print("v = " + r3(v2b) + " m/s")
  print("H = " + r3(hj) + " m")

# ---------------------------------------------------------
def ex_couronne():
  titre("ARCHIMEDE 2 MATERIAUX")
  fa = ask("poids air N", 5.3955)
  fe = ask("poids eau N", 4.6131)
  r1 = ask("rho 1 (or)", 19320)
  r2 = ask("rho 2 (diamant)", 3510)
  rf = ask("rho fluide", 1000)
  m = fa / G
  R("1) Dans l'air (poussee de",
    "l'air negligee), le",
    "dynamometre mesure le poids:",
    "P_air = m*g")
  print("m = P_air/g")
  print(" = " + r3(fa) + "/9.81 = " + r3(m) + " kg")
  pa = fa - fe
  R("2) Dans l'eau, la poussee",
    "d'Archimede allege l'objet:",
    "P_eau = P_air - F_A")
  print("F_A = P_air - P_eau")
  print(" = " + r3(fa) + "-" + r3(fe) + " = " + r3(pa) + " N")
  v = pa / (rf * G)
  R("3) F_A = poids du fluide",
    "deplace = rho_f*V*g, avec",
    "V = volume total de l'objet.")
  print("V = F_A/(rho_f*g)")
  print(" = " + r3(pa) + "/(" + r3(rf) + "*9.81)")
  print("V = " + r3(v) + " m3")
  pause()
  R("4) Deux inconnues m1, m2:",
    "masse: m1 + m2 = m",
    "volume: m1/rho1 + m2/rho2 = V",
    "On remplace m1 = m - m2:")
  m2 = (v - m / r1) / (1 / r2 - 1 / r1)
  print("m2 = (V - m/rho1)")
  print("    /(1/rho2 - 1/rho1)")
  print(" = (" + r3(v) + "-" + r3(m) + "/" + r3(r1) + ")")
  print("   /(1/" + r3(r2) + "-1/" + r3(r1) + ")")
  print("m2 = " + r3(m2) + " kg")
  print("m1 = m - m2 = " + r3(m - m2) + " kg")

# ---------------------------------------------------------
def ex_ecoul():
  titre("ECOULEMENT VISQUEUX")
  rho = ask("rho", 900)
  eta = ask("eta Pa.s", 0.1)
  d = ask("diametre m", 0.02)
  L = ask("longueur m", 10)
  print("Q connu (1) ou v (2)")
  k = ask("choix", 1)
  r = d / 2
  S = pi * r ** 2
  if k == 1:
    Q = ask("Q m3/s", 1e-4)
    v = Q / S
  else:
    v = ask("v m/s", 0.3)
    Q = v * S
  R("v moyenne = Q/S, S = pi*r^2")
  print("S = " + r3(S) + " m2")
  print("v = " + r3(v) + " m/s, Q = " + r3(Q))
  Re = rho * v * d / eta
  R("Le regime se determine par",
    "le nombre de Reynolds:",
    "Re = rho*v*D/eta",
    "(= 2*rho*Q/(pi*r*eta))")
  print("= " + r3(rho) + "*" + r3(v) + "*" + r3(d) + "/" + r3(eta))
  print("Re = " + r3(Re))
  if Re < 2000:
    R("Re < 2000: LAMINAIRE")
  elif Re < 4000:
    R("2000 < Re < 4000:",
      "TRANSITION (incertain)")
  else:
    R("Re > 4000: TURBULENT")
  pause()
  if Re < 2000:
    Rh = 8 * eta * L / (pi * r ** 4)
    R("Laminaire => loi de",
      "Poiseuille, resistance",
      "hydraulique:",
      "R = 8*eta*L/(pi*r^4)")
    print("= 8*" + r3(eta) + "*" + r3(L) + "/(pi*" + r3(r) + "^4)")
  else:
    Rh = 0.3164 * rho * Q / (Re ** 0.25 * pi ** 2 * r ** 5) * L
    R("Turbulent => Blasius:",
      "R = 0.3164*rho*Q*L",
      "  /(Re^0.25*pi^2*r^5)")
  print("R = " + r3(Rh) + " Pa.s/m3")
  dp = Rh * Q
  R("Perte de charge (analogue",
    "loi d'Ohm): dP = R*Q.",
    "Puissance a fournir:",
    "P = Q*dP")
  print("dP = " + r3(dp) + " Pa")
  print("P = " + r3(Q * dp) + " W")

# ---------------------------------------------------------
def ex_bern():
  titre("BERNOULLI 2 POINTS")
  R("Hyp.: fluide parfait,",
    "incompressible, stationnaire.",
    "P1+rho*g*z1+1/2rho*v1^2",
    "= P2+rho*g*z2+1/2rho*v2^2",
    "Surface libre: P = Patm.",
    "Grand reservoir: v ~ 0.",
    "Sections: S1*v1 = S2*v2.")
  print("Inconnue: 1 P2, 2 v2, 3 z2")
  k = ask("choix", 1)
  rho = ask("rho", 1000)
  p1 = ask("P1 Pa", PATM)
  z1 = ask("z1 m", 0)
  v1 = ask("v1 m/s", 0)
  B1 = p1 + rho * G * z1 + 0.5 * rho * v1 ** 2
  print("B1 = " + r3(B1) + " Pa")
  if k == 1:
    z2 = ask("z2 m", 0)
    print("v2: donnee(1) ou par")
    print("sections d1,d2 (2)")
    kk = ask("choix", 1)
    if kk == 2:
      d1 = ask("d1 m", 0.1)
      d2 = ask("d2 m", 0.05)
      v2 = v1 * (d1 / d2) ** 2
      R("Debit conserve:",
        "v2 = v1*(d1/d2)^2")
      print("v2 = " + r3(v2) + " m/s")
    else:
      v2 = ask("v2 m/s", 0)
    p2 = B1 - rho * G * z2 - 0.5 * rho * v2 ** 2
    print("P2 = B1 - rho*g*z2")
    print("   - 1/2*rho*v2^2")
    print("P2 = " + r3(p2) + " Pa")
    print("   = " + r3(p2 / 1e5) + " bar")
  elif k == 2:
    p2 = ask("P2 Pa", PATM)
    z2 = ask("z2 m", 0)
    x = 2 * (B1 - p2 - rho * G * z2) / rho
    print("v2 = sqrt(2(B1-P2-rho*g*z2)")
    print("    /rho)")
    if x < 0:
      print("impossible (negatif)")
    else:
      print("v2 = " + r3(sqrt(x)) + " m/s")
  else:
    p2 = ask("P2 Pa", PATM)
    v2 = ask("v2 m/s", 0)
    z2 = (B1 - p2 - 0.5 * rho * v2 ** 2) / (rho * G)
    print("z2 = (B1-P2-1/2rho*v2^2)")
    print("    /(rho*g)")
    print("z2 = " + r3(z2) + " m")

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
    h = ask("h m", 1)
    R("Hydrostatique: dP = rho*g*h")
    print("P = " + r3(rho * G * h) + " Pa")
  elif k == 2:
    p = ask("P Pa", 1e5)
    d = ask("diametre m", 0.1)
    S = pi * d ** 2 / 4
    R("Pression = force/surface")
    print("S = pi*d^2/4 = " + r3(S))
    print("F = P*S = " + r3(p * S) + " N")
  elif k == 3:
    f1 = ask("F1 N", 100)
    d1 = ask("d1 m", 0.02)
    d2 = ask("d2 m", 0.2)
    f2 = f1 * (d2 / d1) ** 2
    R("Pascal: meme pression sous",
      "les 2 pistons (meme z):",
      "F1/S1 = F2/S2")
    print("F2 = F1*(d2/d1)^2")
    print("F2 = " + r3(f2) + " N")
  elif k == 4:
    rho = ask("rho fluide", 1000)
    V = ask("V immerge m3", 1e-3)
    R("Archimede: poussee = poids",
      "du fluide deplace")
    print("FA = " + r3(rho * V * G) + " N")
  else:
    s = ask("sigma N/m", 0.0728)
    L = ask("L m", 0.05)
    R("Un film a 2 faces => 2*s*L")
    print("F = 2*s*L = " + r3(2 * s * L) + " N")

# ---------------------------------------------------------
def main():
  while True:
    titre("TE1 FLUIDES - MENU")
    print("1 Pile fluides / tube U")
    print("2 Capillarite")
    print("3 Lances incendie/pompe")
    print("4 Archimede couronne")
    print("5 Reynolds / Poiseuille")
    print("6 Bernoulli 2 points")
    print("7 Formules rapides")
    print("0 Quitter")
    c = input("choix ? ").strip()
    if c == "0":
      break
    f = {"1": ex_pile, "2": ex_capil, "3": ex_lances,
         "4": ex_couronne, "5": ex_ecoul, "6": ex_bern,
         "7": ex_divers}.get(c)
    if f:
      f()
      pause()

main()
