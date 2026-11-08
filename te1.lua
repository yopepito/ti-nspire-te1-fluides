-- TE1 Phy2a - solveur fluides (revision) pour TI-Nspire CX / CX CAS
-- Application Lua (OS 3.0.2+). Entree vide = valeur de l'ancien test.
-- Touches: [enter] valider/continuer, fleches haut/bas defiler,
-- [esc] retour au menu, [del] effacer un caractere.
platform.apilevel = "2.0"

local G = 9.81
local PATM = 101300.0
local RHOW = 1000.0

local NOIR = {0, 0, 0}
local BLEU = {40, 90, 210}
local ROUGE = {220, 0, 0}
local GRIS = {110, 110, 110}
local RAIS = {0, 80, 170}
local ERRC = {200, 0, 0}

-- ---------------------------------------------------------
-- etat de l'application
local paras = {}        -- paragraphes {texte, couleur}
local wrapped = {}      -- lignes coupees {texte, couleur}
local dirty = true
local wrapW = 0
local scroll = 0        -- lignes remontees depuis le bas
local mode = "text"     -- text | input | key | schema
local inbuf = ""
local prompt = ""
local schemaFn = nil
local co = nil
local main

local function inval()
  platform.window:invalidate()
end

local function out(s, col)
  table.insert(paras, {tostring(s), col or NOIR})
  if __log then __log(tostring(s)) end  -- simulateur seulement
  if #paras > 400 then table.remove(paras, 1) end
  dirty = true
  scroll = 0
end

local function R(...)
  local t = {...}
  for i = 1, #t do out("> " .. t[i], RAIS) end
end

local function titre(t)
  out("")
  out("==== " .. t .. " ====", BLEU)
end

-- ---------------------------------------------------------
-- nombres

local function r4(x)
  return string.format("%.4g", x)
end

local function s3(x)
  if x == 0 then return "0" end
  local e = math.floor(math.log10(math.abs(x)))
  if e < -3 or e >= 6 then return string.format("%.2e", x) end
  if e >= 2 then
    local q = 10 ^ (e - 2)
    return string.format("%.0f", math.floor(x / q + 0.5) * q)
  end
  return string.format("%." .. (2 - e) .. "f", x)
end

local function res(nom, v, u)
  out(nom .. " = " .. r4(v) .. " " .. u)
  out("   copie (3 c.s.): " .. s3(v) .. " " .. u, GRIS)
end

local UNITS = {{"lmin", 1 / 60000}, {"kpa", 1e3}, {"hpa", 1e2},
  {"bar", 1e5}, {"atm", 101325}, {"mpa", 1e6}, {"mm", 1e-3},
  {"cm", 1e-2}, {"dm", 1e-1}, {"km", 1e3}, {"ml", 1e-6},
  {"cl", 1e-5}, {"dl", 1e-4}, {"mn", 1e-3}, {"min", 60},
  {"pa", 1}, {"kg", 1}, {"g", 1e-3}, {"l", 1e-3}, {"n", 1},
  {"m", 1}, {"s", 1}}

local function evalnum(s)
  s = s:gsub("\226\136\146", "-")      -- signe moins TI
  s = s:gsub("\225\180\135", "e")      -- touche EE
  local n = tonumber(s)
  if n then return n end
  if math.eval then
    local ok, v = pcall(math.eval, s)
    if ok then
      n = tonumber(v)
      if n then return n end
    end
    ok, v = pcall(math.eval, "approx(" .. s .. ")")
    if ok then return tonumber(v) end
  end
  return nil
end

local function conv(s)
  local t = s:lower():gsub(" ", ""):gsub("/", "")
  for i = 1, #UNITS do
    local u, f = UNITS[i][1], UNITS[i][2]
    if #t > #u and t:sub(-#u) == u then
      local n = evalnum(t:sub(1, -#u - 1))
      if n then return n * f end
    end
  end
  return evalnum(t)
end

-- ---------------------------------------------------------
-- entrees / pauses (coroutines)

local function fmtd(d)
  if type(d) == "number" then return string.format("%.6g", d) end
  return tostring(d)
end

local function ask(txt, d)
  prompt = txt .. " [" .. fmtd(d) .. "] ? "
  mode = "input"
  inbuf = ""
  local s = coroutine.yield()
  out(prompt .. s, GRIS)
  prompt = ""
  if s == "" then return d end
  local v = conv(s)
  if v == nil then
    out("! valeur invalide, defaut pris", ERRC)
    return d
  end
  return v
end

local function pause()
  mode = "key"
  prompt = "[enter] pour continuer"
  coroutine.yield()
  prompt = ""
end

local SCH = {}
local function schema(nom)
  out("SCHEMA A DESSINER: " .. nom, BLEU)
  schemaFn = SCH[nom]
  mode = "schema"
  coroutine.yield()
  schemaFn = nil
end

-- ---------------------------------------------------------
-- dessin

local function col(gc, c) gc:setColorRGB(c[1], c[2], c[3]) end
local function txt(gc, x, y, s) gc:drawString(s, x, y, "baseline") end
local function circle(gc, x, y, r) gc:drawArc(x - r, y - r, 2 * r, 2 * r, 0, 360) end
local function fcircle(gc, x, y, r) gc:fillArc(x - r, y - r, 2 * r, 2 * r, 0, 360) end

SCH.pile = function(gc)
  gc:setColorRGB(120, 170, 235); gc:fillRect(60, 40, 120, 60)
  col(gc, BLEU); gc:fillRect(60, 100, 120, 30)
  gc:setColorRGB(160, 160, 160); gc:fillRect(60, 130, 120, 25)
  gc:fillRect(60, 155, 180, 12); gc:fillRect(228, 50, 12, 117)
  fcircle(gc, 234, 45, 12)
  col(gc, NOIR)
  gc:drawRect(60, 40, 120, 115)
  txt(gc, 70, 70, "mazout"); txt(gc, 70, 120, "eau"); txt(gc, 70, 148, "trichlo")
  col(gc, ROUGE)
  txt(gc, 185, 45, "1 (Patm)"); txt(gc, 185, 103, "2")
  txt(gc, 185, 133, "3"); txt(gc, 150, 182, "4 fond"); txt(gc, 250, 50, "A")
  col(gc, NOIR)
  gc:drawLine(30, 40, 30, 100); txt(gc, 8, 75, "h1")
  gc:drawLine(30, 100, 30, 130); txt(gc, 8, 120, "h2")
  gc:drawLine(30, 130, 30, 155); txt(gc, 8, 148, "h3")
  gc:drawLine(300, 45, 300, 160); txt(gc, 280, 110, "dz")
  txt(gc, 4, 18, "On descend: +rho*g*h ; on remonte: -")
end

SCH.capil = function(gc)
  col(gc, BLEU); gc:fillRect(30, 150, 260, 40)
  col(gc, NOIR); gc:drawRect(30, 150, 260, 40)
  gc:drawLine(150, 20, 150, 175); gc:drawLine(166, 20, 166, 175)
  gc:setColorRGB(160, 160, 160); gc:fillRect(151, 40, 15, 40)
  col(gc, BLEU); gc:fillRect(151, 130, 15, 45)
  col(gc, ROUGE)
  txt(gc, 172, 38, "1 air (Patm)"); txt(gc, 172, 52, "2 sous menisque Hg")
  txt(gc, 172, 86, "3 / 4 menisque bas Hg"); txt(gc, 172, 112, "5 air")
  txt(gc, 172, 132, "6 sous menisque eau")
  gc:setColorRGB(255, 255, 255); txt(gc, 180, 172, "7 niveau du bac")
  col(gc, NOIR)
  gc:drawLine(140, 40, 140, 80); txt(gc, 110, 64, "L")
  txt(gc, 4, 18, "Laplace a chaque menisque, rho*g*h dedans")
end

SCH.jurin = function(gc)
  col(gc, BLEU); gc:fillRect(30, 140, 260, 50); gc:fillRect(151, 70, 15, 70)
  col(gc, NOIR); gc:drawRect(30, 140, 260, 50)
  gc:drawLine(150, 30, 150, 160); gc:drawLine(166, 30, 166, 160)
  gc:drawArc(151, 64, 15, 12, 180, 180)
  gc:drawLine(190, 70, 190, 140); txt(gc, 195, 110, "h")
  gc:drawLine(166, 70, 185, 50); txt(gc, 186, 48, "theta")
  txt(gc, 30, 60, "R = r/cos(theta)")
  txt(gc, 4, 18, "Jurin: rho*g*h = 2*sigma*cos(th)/r")
end

SCH.laplace = function(gc)
  col(gc, BLEU); circle(gc, 100, 110, 50)
  col(gc, NOIR)
  txt(gc, 80, 110, "P int"); txt(gc, 20, 40, "P ext")
  gc:drawLine(100, 110, 150, 110); txt(gc, 118, 106, "R")
  circle(gc, 230, 110, 40); circle(gc, 230, 110, 36)
  txt(gc, 195, 170, "savon: 2 faces")
  txt(gc, 4, 18, "P cote concave > P cote convexe")
  txt(gc, 4, 200, "goutte: 2s/R   bulle savon: 4s/R")
end

SCH.lances = function(gc)
  gc:setColorRGB(120, 120, 120); gc:fillRect(262, 30, 30, 160)
  col(gc, BLEU)
  gc:drawLine(150, 180, 210, 120); gc:drawLine(210, 120, 262, 32)
  gc:fillRect(60, 178, 95, 6)
  gc:fillRect(5, 110, 40, 75)
  col(gc, NOIR)
  circle(gc, 60, 172, 10)
  gc:drawLine(300, 30, 300, 185); txt(gc, 304, 110, "H")
  col(gc, ROUGE)
  txt(gc, 200, 25, "1 sommet v=0"); txt(gc, 212, 128, "2 buse")
  txt(gc, 100, 198, "3 sol"); txt(gc, 55, 160, "4")
  txt(gc, 8, 105, "6 Patm"); txt(gc, 30, 198, "5")
  col(gc, NOIR)
  txt(gc, 4, 18, "Numeroter du sommet vers la citerne")
end

SCH.couronne = function(gc)
  col(gc, NOIR)
  gc:drawLine(80, 30, 80, 70)
  txt(gc, 40, 110, "air: P_air = m*g")
  gc:drawLine(220, 30, 220, 95)
  col(gc, BLEU); gc:fillRect(170, 85, 100, 70)
  gc:setColorRGB(230, 180, 0); gc:fillRect(210, 100, 20, 20)
  gc:fillRect(70, 70, 20, 20)
  col(gc, NOIR)
  gc:drawLine(240, 130, 240, 100); txt(gc, 244, 115, "F_A")
  gc:drawLine(205, 120, 205, 150); txt(gc, 160, 150, "m*g")
  txt(gc, 160, 175, "eau: P_eau = P_air - F_A")
  txt(gc, 4, 18, "F_A = rho_f*V*g, V = volume total")
end

SCH.ecoul = function(gc)
  col(gc, BLEU); gc:fillRect(40, 90, 240, 30)
  col(gc, NOIR)
  gc:drawRect(40, 90, 240, 30)
  gc:drawLine(40, 60, 280, 60); txt(gc, 150, 55, "L")
  gc:drawLine(20, 90, 20, 120); txt(gc, 4, 108, "2r")
  gc:drawLine(60, 105, 100, 105); gc:drawLine(100, 105, 92, 100)
  txt(gc, 60, 140, "Q, v = Q/(pi*r^2)")
  col(gc, ROUGE); txt(gc, 30, 85, "P1"); txt(gc, 270, 85, "P2")
  col(gc, NOIR)
  txt(gc, 4, 18, "Re -> laminaire ? -> R -> dP = R*Q")
end

SCH.serpentin = function(gc)
  col(gc, BLEU)
  local ys = {30, 60, 90, 120, 150, 180}
  for i = 1, 6 do
    local x0 = 90
    if i == 1 or i == 6 then x0 = 40 end
    gc:fillRect(x0, ys[i] - 3, 240 - x0, 6)
  end
  gc:setPen("thick", "smooth")
  for i = 1, 5 do
    if i % 2 == 1 then
      gc:drawArc(225, ys[i], 30, 30, 270, 180)
    else
      gc:drawArc(75, ys[i], 30, 30, 90, 180)
    end
  end
  gc:setPen("thin", "smooth")
  gc:fillRect(37, 30, 6, 150)
  col(gc, NOIR)
  fcircle(gc, 40, 105, 12)
  gc:setColorRGB(255, 255, 255); fcircle(gc, 40, 105, 9)
  col(gc, NOIR); circle(gc, 40, 105, 12)
  gc:drawLine(34, 111, 40, 97); gc:drawLine(40, 97, 46, 111)
  txt(gc, 55, 109, "pompe")
  col(gc, ROUGE)
  txt(gc, 25, 50, "1"); txt(gc, 150, 25, "2")
  txt(gc, 262, 108, "3"); txt(gc, 150, 198, "4"); txt(gc, 25, 172, "0")
  col(gc, NOIR)
  txt(gc, 4, 14, "a: haut/bas  b: rangs  2R: coudes")
end

SCH.bern = function(gc)
  col(gc, BLEU); gc:fillRect(30, 140, 100, 30)
  gc:fillRect(130, 80, 150, 16)
  gc:drawLine(130, 140, 130, 80); gc:drawLine(130, 170, 130, 96)
  col(gc, NOIR)
  gc:drawLine(10, 195, 300, 195); txt(gc, 4, 205, "z = 0")
  gc:drawLine(20, 155, 20, 195); txt(gc, 4, 180, "z1")
  gc:drawLine(295, 88, 295, 195); txt(gc, 280, 150, "z2")
  col(gc, ROUGE); txt(gc, 60, 135, "1 (P1, v1, S1)"); txt(gc, 170, 75, "2 (P2, v2, S2)")
  col(gc, NOIR)
  txt(gc, 4, 18, "P + rho*g*z + rho*v^2/2 = cste")
end

SCH.divers = function(gc)
  col(gc, BLEU); gc:fillRect(40, 120, 230, 40)
  gc:fillRect(40, 80, 30, 40); gc:fillRect(190, 70, 80, 50)
  col(gc, NOIR)
  gc:drawRect(40, 70, 30, 10); gc:drawRect(190, 60, 80, 10)
  gc:drawLine(55, 40, 55, 70); txt(gc, 60, 45, "F1, S1")
  gc:drawLine(230, 30, 230, 60); txt(gc, 236, 40, "F2, S2")
  txt(gc, 4, 18, "Pascal: F1/S1 = F2/S2 (meme z)")
end

-- ---------------------------------------------------------
-- exercices

local function ex_pile()
  titre("PILE DE FLUIDES / TUBE U")
  schema("pile")
  R("Les liquides sont immobiles et ne se melangent pas: ils forment des couches horizontales, du plus leger en haut au plus lourd en bas. Comme rien ne bouge, c'est un probleme d'hydrostatique.",
    "Dans UN meme fluide continu, la loi de l'hydrostatique relie deux points: P_b + rho*g*z_b = P_a + rho*g*z_a. Elle n'est valable qu'a l'interieur d'un seul fluide, c'est pourquoi on avance interface par interface en changeant de rho a chaque couche.",
    "On demande des pressions RELATIVES: P - Patm. A la surface libre, le liquide touche l'air, donc P = Patm et la pression relative y vaut 0. C'est notre point de depart.",
    "Plus on descend, plus il y a de liquide au-dessus qui pese: la pression augmente de rho*g*h quand on descend de h.")
  pause()
  local n = math.floor(ask("nb de couches", 3))
  local noms = {"mazout", "eau", "trichlo", "c4", "c5"}
  local rhos = {820, 1000, 1500, 1000, 1000}
  local hs = {0.9, 0.3, 0.13, 0.1, 0.1}
  local p, rl = 0.0, 0
  local resl = {}
  for i = 1, n do
    out("-- couche " .. i .. " (" .. noms[i] .. ")")
    local rho = ask(" rho kg/m3", rhos[i])
    local h = ask(" epaisseur", hs[i])
    rl = rho
    local a, b = tostring(i), tostring(i + 1)
    R("Le point " .. b .. " est a l'interface sous la couche de " .. noms[i] .. ". Entre " .. a .. " et " .. b .. " on ne traverse que ce fluide, donc l'hydrostatique s'applique avec rho = " .. r4(rho) .. ": P" .. b .. " = P" .. a .. " + rho*g*(H" .. a .. " - H" .. b .. "), ou H" .. a .. " - H" .. b .. " = " .. r4(h) .. " m est l'epaisseur de la couche.",
      "En retirant Patm de chaque cote, on obtient la pression relative en " .. b .. ": elle vaut celle en " .. a .. " plus le poids par unite de surface de la couche traversee.")
    out("P" .. b .. "-Patm = P" .. a .. "-Patm + rho*g*h")
    local pn = p + rho * G * h
    out("= " .. r4(p) .. " + " .. r4(rho) .. "*9.81*" .. r4(h))
    res("P" .. b .. "-Patm", pn, "Pa")
    table.insert(resl, {"P" .. b, pn})
    p = pn
    pause()
  end
  out("-- point A dans l'autre branche")
  local rho = ask(" rho branche", rl)
  local dz = ask(" A plus haut que le fond de", 0.9)
  local pa = p + rho * G * (-dz)
  R("Le fond du conteneur communique avec le tube qui monte vers A, et ce tube est rempli du MEME liquide sans interruption. On peut donc appliquer l'hydrostatique directement du fond (point 4) jusqu'a A, avec le rho de ce liquide.",
    "Le piege est le signe: en allant du fond vers A on REMONTE, donc H4 - HA = -" .. r4(dz) .. " m est negatif. Il y a moins de liquide au-dessus de A, la pression y est donc plus faible qu'au fond.")
  out("PA-Patm = P4-Patm + rho*g*(H4-HA)")
  out("= " .. r4(p) .. " + " .. r4(rho) .. "*9.81*(-" .. r4(dz) .. ")")
  res("PA-Patm", pa, "Pa")
  if pa < 0 then
    R("La pression relative en A est negative: la pression absolue dans le petit reservoir est un peu plus faible que la pression atmospherique qui l'entoure.",
      "Si un trou apparait, le fluide va du cote de la pression la plus haute vers celui de la plus basse: c'est l'air exterieur qui entre sous forme de bulles, et le liquide ne s'echappe pas.")
  else
    R("La pression relative en A est positive: le liquide pousse plus fort que l'air exterieur. Par un trou, le liquide s'echapperait vers l'exterieur.")
  end
  out("P absolue = P relative + " .. r4(PATM) .. " Pa")
  out("-- resume")
  for i = 1, #resl do out(resl[i][1] .. "-Patm = " .. s3(resl[i][2]) .. " Pa") end
  out("PA-Patm = " .. s3(pa) .. " Pa")
end

local function ex_capil()
  titre("CAPILLARITE")
  out("1 Jurin (hauteur)")
  out("2 Laplace (bulle/goutte)")
  out("3 tube Hg + air + eau")
  local c = math.floor(ask("choix", 3))
  if c == 1 then
    schema("jurin")
    local s = ask("sigma N/m", 0.0728)
    local th = ask("theta deg", 0)
    local rho = ask("rho", 1000)
    local r = ask("r tube", 1e-4)
    R("Dans un tube tres fin, la surface du liquide n'est pas plate: elle forme un menisque, une calotte de sphere dont le rayon vaut R = r/cos(theta), ou theta est l'angle de contact avec le verre.",
      "D'apres Laplace, une surface courbe cree une difference de pression 2*sigma/R entre ses deux cotes. Pour l'eau, la pression juste sous le menisque est plus faible que Patm, ce qui aspire le liquide vers le haut.",
      "Le liquide monte jusqu'a ce que le poids de la colonne compense cette difference: rho*g*h = 2*sigma/R. En remplacant R, on obtient la loi de Jurin: h = 2*sigma*cos(theta)/(rho*g*r).")
    local h = 2 * s * math.cos(math.rad(th)) / (rho * G * r)
    out("= 2*" .. r4(s) .. "*cos(" .. r4(th) .. ")/(" .. r4(rho) .. "*9.81*" .. r4(r) .. ")")
    res("h", h, "m")
    R("Interpretation: si theta < 90 deg (liquide mouillant, comme l'eau sur le verre), cos(theta) > 0 et le liquide monte. Si theta > 90 deg (mercure sur le verre), cos(theta) < 0 et le liquide descend sous le niveau du bac.",
      "Plus le tube est fin (r petit), plus l'effet est grand: h est inversement proportionnel a r.")
  elseif c == 2 then
    schema("laplace")
    local s = ask("sigma N/m", 0.0728)
    local Rr = ask("rayon R", 1e-3)
    local k = ask("1 goutte/bulle, 2 savon", 1)
    local f = 2
    if k ~= 1 then f = 4 end
    R("La tension superficielle agit comme une membrane tendue: une surface courbe pousse vers son centre de courbure. A l'equilibre, la pression du cote CONCAVE (l'interieur de la courbure) est donc plus grande que celle du cote convexe.",
      "Pour une seule interface (goutte, bulle de gaz dans un liquide), la loi de Laplace donne dP = 2*sigma/R. Une bulle de savon est un film qui a DEUX interfaces avec l'air, une dedans et une dehors: les deux sauts s'additionnent et dP = 4*sigma/R.")
    local dp = f * s / Rr
    out("dP = " .. f .. "*" .. r4(s) .. "/" .. r4(Rr))
    res("dP", dp, "Pa")
    R("Plus la bulle est petite, plus la surpression est grande, puisque dP est inversement proportionnel a R.")
  else
    schema("capil")
    local r = ask("r tube", 1e-4)
    local sh = ask("sigma Hg N/m", 0.44)
    local ah = ask("angle Hg (R=r/cos a) deg", 50)
    local rhh = ask("rho Hg", 13546)
    local L = ask("long. colonne Hg", 0.1)
    local sw = ask("sigma eau N/m", 0.0728)
    local aw = ask("angle eau deg", 0)
    local rw = ask("rho eau", 1000)
    local Rh = r / math.cos(math.rad(ah))
    local Rw = r / math.cos(math.rad(aw))
    local d1 = 2 * sh / Rh
    local d2 = rhh * G * L
    local d3 = -d1
    local d4 = 0.0
    local d5 = -2 * sw / Rw
    R("Methode: on suit le tube de haut en bas, du point 1 au point 7, en notant la variation de pression a chaque etape. Il n'y a que deux types d'etapes.",
      "Quand on traverse un menisque, la pression saute de 2*sigma/R (Laplace): elle augmente si on entre du cote concave, elle diminue si on en sort. Quand on descend dans un fluide, elle augmente de rho*g*h (hydrostatique).",
      "Le rayon de chaque menisque vaut R = r/cos(angle): c'est la donnee 'rayon membrane' de l'enonce.")
    out("R_Hg = r/cos(a) = " .. r4(Rh) .. " m")
    pause()
    R("1) Le mercure ne mouille pas le verre: son menisque superieur est BOMBE vers le haut, comme une goutte. L'interieur de la courbure (cote concave) est dans le mercure.",
      "En passant de 1 (air) a 2 (mercure), on entre du cote concave: la pression augmente de 2*sigma_Hg/R_Hg.")
    out("P2-P1 = +2*s_Hg/R_Hg = 2*" .. r4(sh) .. "/" .. r4(Rh))
    res("P2-P1", d1, "Pa")
    pause()
    R("2) De 2 a 3, on descend dans la colonne de mercure, de longueur L. C'est de l'hydrostatique pure dans un seul fluide: la pression augmente de rho_Hg*g*L.")
    out("P3-P2 = rho_Hg*g*L = " .. r4(rhh) .. "*9.81*" .. r4(L))
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
    out("P6-P5 = -2*s_eau/R_eau = -2*" .. r4(sw) .. "/" .. r4(Rw))
    res("P6-P5", d5, "Pa")
    pause()
    R("6) Entre le menisque d'eau (6) et le point 7 au niveau de la surface du bac, on est dans l'eau: P7 - P6 = rho_e*g*h, ou h est la hauteur de 6 au-dessus de 7. C'est la seule inconnue.",
      "7) Le point 1 est a l'air libre et le point 7 est au niveau de la surface libre du bac: les deux sont a la pression atmospherique. Donc P7 - P1 = 0, et cette difference est aussi la somme des six variations calculees.",
      "8) On ecrit cette somme egale a zero et on isole h. C'est une equation a une seule inconnue, construite uniquement avec les resultats precedents.")
    local s = d1 + d2 + d3 + d4 + d5
    local h = -s / (rw * G)
    out("0 = d1+d2+d3+d4+d5 + rho_e*g*h")
    out("h = -(d1+...+d5)/(rho_e*g)")
    out("somme d1..d5 = " .. r4(s) .. " Pa")
    out("h = " .. r4(-s) .. "/(" .. r4(rw) .. "*9.81)")
    res("h", h, "m")
    if h < 0 then
      R("h est negatif: le menisque d'eau se trouve " .. r4(-h) .. " m SOUS le niveau du bac. Les deux sauts du mercure s'annulent, mais son poids (rho_Hg*g*L) comprime l'air enferme, qui repousse l'eau vers le bas bien plus que la capillarite ne la fait monter.")
    else
      R("h est positif: l'eau monte de " .. r4(h) .. " m au-dessus du niveau du bac.")
    end
  end
end

local function ex_lances()
  titre("BERNOULLI LANCES/POMPE")
  schema("lances")
  local et = ask("nb etages", 10)
  local he = ask("m par etage", 3)
  local zl = ask("hauteur lance", 1)
  local db = ask("d buse", 0.05)
  local n = ask("nb lances", 4)
  local dt = ask("d tuyau", 0.1)
  local pmax = ask("P max tuyau", 4.7e5)
  local H = et * he
  R("Hypotheses: on neglige les frottements (fluide parfait), l'eau est incompressible et le regime est stationnaire. Ce sont exactement les conditions de l'equation de Bernoulli: P + rho*g*z + 1/2*rho*v^2 reste constant le long d'une ligne de courant.",
    "Strategie: on part de ce qu'on connait le mieux, le sommet du jet, et on remonte le courant point par point jusqu'a la citerne: 1 sommet, 2 buse, 3 tuyau au sol, 4 pompe, 5 conduite, 6 surface de la citerne.")
  pause()
  R("1) Pour pousser plus d'eau, il faut plus de pression a la sortie de la buse. Inversement, le debit le plus faible qui fonctionne encore correspond a la pression la plus basse possible a la sortie: la pression atmospherique. On pose donc P2 = Patm.")
  pause()
  local dz = H - zl
  local v2 = math.sqrt(2 * G * dz)
  R("2) On applique Bernoulli entre le sommet du jet (1) et la sortie de la buse (2). Au sommet, l'eau est a l'air libre (P1 = Patm) et sa vitesse verticale est nulle: c'est le minimum pour atteindre la hauteur H. A la buse, P2 = Patm.",
    "Les pressions atmospheriques s'annulent des deux cotes. Il reste rho*g*(z1 - z2) = 1/2*rho*v2^2: toute l'energie cinetique a la sortie se transforme en energie potentielle. On obtient v2 = sqrt(2*g*(z1 - z2)), avec z1 - z2 = H moins la hauteur de la lance.")
  out("z1-z2 = " .. r4(H) .. " - " .. r4(zl) .. " = " .. r4(dz) .. " m")
  out("v2 = sqrt(2*9.81*" .. r4(dz) .. ")")
  res("v2", v2, "m/s")
  pause()
  local sb = math.pi * db ^ 2 / 4
  local q1 = sb * v2
  R("3) Le debit volumique est le volume d'eau qui sort par seconde: section de la buse multipliee par la vitesse. Q = pi*db^2/4 * v2.")
  out("Q = pi*" .. r4(db) .. "^2/4*" .. r4(v2))
  res("Q lance", q1, "m3/s")
  out("  = " .. r4(q1 * 1000) .. " l/s")
  local qp = n * q1
  R("4) Toute l'eau qui sort des " .. r4(n) .. " lances passe d'abord par la pompe. L'eau etant incompressible, rien ne s'accumule en route: Q pompe = n * Q lance.")
  res("Q pompe", qp, "m3/s")
  out("  = " .. r4(qp * 1000) .. " l/s")
  pause()
  local v3 = v2 * (db / dt) ^ 2
  R("5) Dans le tuyau, le debit est le meme qu'a la buse (conservation du debit): pi*db^2/4*v2 = pi*dt^2/4*v3. Le tuyau etant plus large, l'eau y va plus lentement: v3 = v2*(db/dt)^2. Attention a ne pas oublier le carre, car les sections dependent du diametre au carre.")
  out("v3 = " .. r4(v2) .. "*(" .. r4(db) .. "/" .. r4(dt) .. ")^2")
  res("v3", v3, "m/s")
  local p3 = PATM + RHOW * (G * zl + 0.5 * (v2 ^ 2 - v3 ^ 2))
  R("On applique ensuite Bernoulli entre le tuyau au sol (3, z3 = 0) et la buse (2, z2 = hauteur de la lance, P2 = Patm). La pression dans le tuyau doit fournir a la fois l'acceleration de l'eau (v3 -> v2) et la montee jusqu'a la lance:",
    "P3 = Patm + rho*(g*(z2 - z3) + 1/2*(v2^2 - v3^2)).")
  out("= " .. r4(PATM) .. " + 1000*(9.81*" .. r4(zl) .. " + 0.5*(" .. r4(v2) .. "^2 - " .. r4(v3) .. "^2))")
  res("P3", p3, "Pa")
  out("  = " .. r4(p3 / 1e5) .. " bar")
  if p3 < pmax then
    R("P3 reste inferieure a la pression maximale de " .. r4(pmax / 1e5) .. " bar que supportent les tuyaux: il n'y a pas de danger d'eclatement.")
  else
    R("P3 depasse la pression maximale de " .. r4(pmax / 1e5) .. " bar: les tuyaux risquent d'eclater.")
  end
  pause()
  out("-- conduite citerne -> pompe")
  local dc = ask("d conduite", 0.12)
  local hc = ask("haut. eau au-dessus pompe", 4.3)
  local cas = {n, n + 1}
  for i = 1, 2 do
    local nn = cas[i]
    local v5 = nn * v3 * (dt / dc) ^ 2
    local p5 = PATM + RHOW * (G * hc - 0.5 * v5 ^ 2)
    out("-> avec " .. r4(nn) .. " lances:")
    R("La conduite entre la citerne et la pompe transporte l'eau de tous les tuyaux a la fois. Par conservation du debit: v5 = n*v3*(dt/dc)^2.")
    out("v5 = " .. r4(nn) .. "*" .. r4(v3) .. "*(" .. r4(dt) .. "/" .. r4(dc) .. ")^2")
    res("v5", v5, "m/s")
    R("On applique Bernoulli entre la surface de la citerne (6) et la conduite (5). A la surface, P6 = Patm, et v6 est presque nulle parce que la citerne est tres large: le niveau descend tres lentement.",
      "P5 = Patm + rho*(g*(z6 - z5) - 1/2*v5^2). La hauteur d'eau augmente la pression, mais la vitesse dans la conduite la fait baisser.")
    out("= " .. r4(PATM) .. " + 1000*(9.81*" .. r4(hc) .. " - 0.5*" .. r4(v5) .. "^2)")
    res("P5", p5, "Pa")
    if p5 < PATM then
      R("P5 est plus faible que la pression atmospherique: l'air exterieur pousse plus fort sur la paroi que l'eau a l'interieur. Un tuyau souple s'ecraserait, il faut donc une conduite RIGIDE.")
    end
    if p5 <= 0 then
      R("Une pression absolue negative n'a pas de sens physique: cela signifie que la pompe ne peut pas aspirer autant d'eau. En realite, quand P5 s'approche de zero, l'eau se met a bouillir a temperature ambiante a l'entree de la conduite: c'est la CAVITATION, qui abime la pompe.")
    end
    pause()
  end
  local q1b = qp / (n + 1)
  local v2b = q1b / sb
  local hj = v2b ^ 2 / (2 * G) + zl
  R("Hauteur maximale du jet avec n+1 lances. Si la pompe fournit toujours le meme debit, il est partage entre plus de lances: chaque lance recoit Q pompe/(n+1), donc l'eau sort moins vite (v = Q/S).",
    "Bernoulli entre la buse et le sommet du jet donne alors H = v^2/(2g) + hauteur de la lance: le jet monte moins haut.")
  res("Q lance", q1b, "m3/s")
  res("v buse", v2b, "m/s")
  res("H max", hj, "m")
end

local function ex_couronne()
  titre("ARCHIMEDE 2 MATERIAUX")
  schema("couronne")
  local fa = ask("poids air N", 5.3955)
  local fe = ask("poids eau N", 4.6131)
  local r1 = ask("rho 1 (or)", 19320)
  local r2 = ask("rho 2 (diamant)", 3510)
  local rf = ask("rho fluide", 1000)
  local m = fa / G
  R("Idee: on ne peut pas separer l'or et les diamants, mais les deux pesees donnent deux informations, la masse totale et le volume total. Avec deux materiaux de masses volumiques differentes, ces deux informations suffisent pour trouver les deux masses.",
    "1) Dans l'air, la poussee de l'air est negligeable car l'air est tres leger. Le dynamometre mesure donc directement le poids de la couronne: P_air = m*g, d'ou la masse totale.")
  out("m = P_air/g = " .. r4(fa) .. "/9.81")
  res("m", m, "kg")
  local pa = fa - fe
  R("2) Dans l'eau, la couronne parait plus legere parce que l'eau la pousse vers le haut: c'est la poussee d'Archimede. Le dynamometre mesure P_eau = P_air - F_A, donc F_A = P_air - P_eau.")
  out("F_A = " .. r4(fa) .. " - " .. r4(fe))
  res("F_A", pa, "N")
  local v = pa / (rf * G)
  R("3) La poussee d'Archimede est egale au poids de l'eau deplacee: F_A = rho_eau*V*g. Comme la couronne est entierement immergee, le volume d'eau deplace est exactement le volume de la couronne. On prend bien la masse volumique du FLUIDE, pas celle de l'objet.")
  out("V = F_A/(rho_f*g) = " .. r4(pa) .. "/(" .. r4(rf) .. "*9.81)")
  res("V", v, "m3")
  pause()
  R("4) On a deux inconnues, m1 (or) et m2 (diamants), et deux equations: la masse totale, m1 + m2 = m, et le volume total, m1/rho1 + m2/rho2 = V, puisque le volume de chaque materiau vaut sa masse divisee par sa masse volumique.",
    "On remplace m1 = m - m2 dans l'equation du volume, puis on met m2 en facteur pour l'isoler.")
  local m2 = (v - m / r1) / (1 / r2 - 1 / r1)
  out("m2 = (V - m/rho1)/(1/rho2 - 1/rho1)")
  out("= (" .. r4(v) .. " - " .. r4(m) .. "/" .. r4(r1) .. ")/(1/" .. r4(r2) .. " - 1/" .. r4(r1) .. ")")
  res("m2 (diamants)", m2, "kg")
  res("m1 (or)", m - m2, "kg")
  R("Verification: m1 et m2 doivent etre positives et leur somme egale a m. Une masse negative signalerait une erreur de saisie, par exemple deux pesees inversees.")
end

local function ex_ecoul()
  titre("ECOULEMENT VISQUEUX")
  schema("ecoul")
  local rho = ask("rho", 900)
  local eta = ask("eta Pa.s", 0.1)
  local d = ask("diametre", 0.02)
  local L = ask("longueur", 10)
  out("Q connu (1), debit massique (2), v (3)")
  local k = ask("choix", 1)
  local r = d / 2
  local S = math.pi * r ^ 2
  local Q
  if k == 1 then
    Q = ask("Q m3/s", 1e-4)
  elseif k == 2 then
    local mq = ask("debit massique kg/s", 0.09)
    Q = mq / rho
    R("Le debit massique (kg/s) et le debit volumique (m3/s) sont lies par la masse volumique: Q = m_point/rho.")
  else
    Q = ask("v m/s", 0.3) * S
  end
  local v = Q / S
  R("La vitesse moyenne dans le tuyau vaut v = Q/S, avec S = pi*r^2. Attention: r est le RAYON, donc la moitie du diametre.")
  out("S = " .. r4(S) .. " m2, v = " .. r4(v) .. " m/s")
  local Re = rho * v * d / eta
  R("Avant de choisir une formule de perte de charge, il faut savoir si l'ecoulement est laminaire ou turbulent. Le nombre de Reynolds compare l'inertie du fluide a sa viscosite: Re = rho*v*D/eta, ou de facon equivalente Re = 2*rho*Q/(pi*r*eta).")
  out("Re = " .. r4(rho) .. "*" .. r4(v) .. "*" .. r4(d) .. "/" .. r4(eta))
  res("Re", Re, "")
  if Re < 2000 then
    R("Re < 2000: la viscosite domine, l'ecoulement est LAMINAIRE. Le fluide glisse en couches regulieres.")
  elseif Re < 4000 then
    R("2000 < Re < 4000: zone de TRANSITION. Le regime est instable, le signaler sur la copie.")
  else
    R("Re > 4000: l'inertie domine, l'ecoulement est TURBULENT, avec des tourbillons.")
  end
  pause()
  local Rh
  if Re < 2000 then
    Rh = 8 * eta * L / (math.pi * r ^ 4)
    R("En regime laminaire, on utilise la loi de Poiseuille. La resistance hydraulique d'un tuyau droit vaut R = 8*eta*L/(pi*r^4). Elle augmente avec la longueur et la viscosite, et diminue tres vite quand le rayon augmente (r a la puissance 4).")
    out("= 8*" .. r4(eta) .. "*" .. r4(L) .. "/(pi*" .. r4(r) .. "^4)")
  else
    Rh = 0.3164 * rho * Q / (Re ^ 0.25 * math.pi ^ 2 * r ^ 5) * L
    R("En regime turbulent, Poiseuille n'est plus valable. On utilise la correlation de Blasius: R = 0.3164*rho*Q*L/(Re^0.25*pi^2*r^5).")
  end
  res("R", Rh, "Pa.s/m3")
  local dp = Rh * Q
  R("La perte de charge suit une loi analogue a la loi d'Ohm (U = R*I): dP = R*Q. C'est la difference de pression necessaire pour pousser le debit Q a travers le tuyau malgre les frottements.",
    "Si le tuyau debouche a l'air libre, la pression a la sortie vaut Patm, donc la pression a l'entree vaut Patm + dP. La puissance a fournir pour maintenir l'ecoulement vaut P = Q*dP.")
  res("dP", dp, "Pa")
  res("P entree (sortie a l'air)", PATM + dp, "Pa")
  res("Puissance", Q * dp, "W")
end

local function ex_serpentin()
  titre("SERPENTIN (E05 ex.4)")
  schema("serpentin")
  local Q = ask("debit", 5 / 60000)
  local eta = ask("eta Pa.s", 0.2)
  local rho = ask("rho", 900)
  local p0 = ask("P0", PATM)
  local a = ask("a", 5)
  local b = ask("b", 3)
  local r = ask("r tuyau", 0.008)
  local Rc = ask("R coude", 0.1)
  local vert = ask("1 paroi verticale, 0 sol", 1)
  local l1, l2 = 0.131, 1.847
  local g = G
  if vert ~= 1 then g = 0.0 end
  out("Q = " .. r4(Q) .. " m3/s")
  R("Le circuit est ferme: l'huile tourne en boucle, poussee par la pompe. Le debit est le meme partout, car le regime est stationnaire et l'huile incompressible. Le vase d'expansion en 0 fixe la pression de reference: P0 = Patm.",
    "1) Pour savoir quelle formule de perte de charge utiliser, on determine le regime avec le nombre de Reynolds: Re = 2*rho*Q/(pi*r*eta).")
  local Re = 2 * rho * Q / (math.pi * r * eta)
  out("Re = 2*" .. r4(rho) .. "*" .. r4(Q) .. "/(pi*" .. r4(r) .. "*" .. r4(eta) .. ")")
  res("Re", Re, "")
  if Re < 2000 then
    R("Re est bien plus petit que 2000: l'huile tres visqueuse s'ecoule en regime LAMINAIRE. On peut donc utiliser Poiseuille pour les troncons droits.")
  else
    R("Re > 2000: l'ecoulement n'est plus laminaire et la suite, basee sur Poiseuille, n'est plus valable.")
  end
  pause()
  local Rl = 8 * eta / (math.pi * r ^ 4)
  local function Rs(alpha)
    return (l1 + l2 * (2 * r / Rc) ^ 3.5) * rho * Q / (2 * math.pi ^ 3 * r ^ 4) * alpha
  end
  R("2) Le fluide perd de l'energie de deux facons. Dans les troncons DROITS, ce sont les pertes regulieres dues a la viscosite (Poiseuille): R(L) = 8*eta*L/(pi*r^4), proportionnelle a la longueur.",
    "Dans les COUDES, le changement de direction cree des pertes singulieres supplementaires: R*(alpha) = (l1 + l2*(2r/R)^(7/2)) * rho*Q/(2*pi^3*r^4) * alpha, avec alpha l'angle total en radians, l1 = 0.131 et l2 = 1.847.")
  out("8*eta/(pi*r^4) = " .. r4(Rl) .. " Pa.s/m4")
  local Ltot = 8 * Rc + 2 * a + 4 * b
  R("On compte tous les troncons droits en les cochant sur le dessin: le cote de la pompe mesure 8R (la hauteur du circuit moins les deux coins), le haut et le bas mesurent a chacun, et les quatre rangs du milieu mesurent b chacun. Ltot = 8R + 2a + 4b.",
    "On additionne aussi tous les angles: 2 coins d'un quart de tour (2 * pi/2 = pi) et 5 demi-tours (5 * pi), soit 6*pi radians au total.")
  out("Ltot = 8*" .. r4(Rc) .. " + 2*" .. r4(a) .. " + 4*" .. r4(b) .. " = " .. r4(Ltot) .. " m")
  local Rtot = Rl * Ltot + Rs(6 * math.pi)
  res("R*(6pi)", Rs(6 * math.pi), "Pa.s/m3")
  res("R total", Rtot, "Pa.s/m3")
  pause()
  local Pp = Rtot * Q ^ 2
  R("On applique Bernoulli generalise sur un tour complet, de 0 jusqu'a 0 dans le sens de la pompe: (B_arrivee - B_depart)*Q = -R_total*Q^2 + P_pompe. Comme on revient au meme point, B_arrivee = B_depart et le membre de gauche est nul.",
    "Donc P_pompe = R_total*Q^2: en regime stationnaire, la pompe fournit exactement l'energie perdue par frottement sur un tour.")
  out("P_pompe = " .. r4(Rtot) .. "*" .. r4(Q) .. "^2")
  res("P_pompe", Pp, "W")
  pause()
  R("3) Pour la pression en chaque point, on applique Bernoulli generalise entre deux points successifs, toujours dans le sens de la pompe: (B_j - B_i)*Q = -[R(L) + R*(alpha)]*Q^2, plus P_pompe si la pompe se trouve sur le troncon.",
    "La section est la meme partout, donc la vitesse aussi: les termes 1/2*rho*v^2 s'annulent. Il reste P_j = P_i + rho*g*(z_i - z_j) - [R(L) + R*(alpha)]*Q, plus P_pompe/Q sur le troncon de la pompe.")
  if g == 0 then
    R("Circuit horizontal (chauffage au sol): tous les points sont a la meme altitude. On refait exactement les memes calculs en posant g = 0, seules les pertes et la pompe comptent.")
  end
  local segs = {
    {"0->1", 8 * Rc, 0.0, -8 * Rc, true,
     "on traverse la pompe, qui ajoute P_pompe/Q. On monte de 8R, avec un troncon droit de 8R et aucun coude"},
    {"1->2", a - b / 2, math.pi / 2, -Rc, false,
     "un coin d'un quart de tour (pi/2), un troncon droit de a - b/2, et on monte encore de R jusqu'au tuyau du haut"},
    {"2->3", 5 * b / 2, 5 * math.pi / 2, 5 * Rc, false,
     "les troncons droits b/2 + b + b = 5b/2 et les coudes pi + pi + pi/2 = 5pi/2. On descend de 5R"},
    {"3->4", 5 * b / 2, 5 * math.pi / 2, 5 * Rc, false,
     "meme chemin que le precedent: 5b/2 de droit, 5pi/2 de coudes, et on descend encore de 5R"}}
  local P = p0
  local resu = {}
  for i = 1, 4 do
    local nom, L, al, dzz, pompe, desc = segs[i][1], segs[i][2], segs[i][3], segs[i][4], segs[i][5], segs[i][6]
    pause()
    out("-- " .. nom)
    R("Troncon " .. nom .. ": " .. desc .. ".")
    local perte = (Rl * L + Rs(al)) * Q
    local Pn = P + rho * g * dzz - perte
    if pompe then Pn = Pn + Pp / Q end
    out("rho*g*(zi-zj) = " .. r4(rho * g * dzz) .. " Pa")
    out("pertes [R(L)+R*]*Q = " .. r4(perte) .. " Pa")
    if pompe then out("pompe P/Q = " .. r4(Pp / Q) .. " Pa") end
    local pn = "P" .. nom:sub(-1)
    res(pn, Pn, "Pa")
    table.insert(resu, {pn, Pn})
    P = Pn
  end
  R("Coherence: la pression baisse tout au long du circuit a cause des frottements, et c'est la pompe, juste apres le point 0, qui la remonte.")
  out("-- resume")
  out("Re = " .. s3(Re) .. ", P_pompe = " .. s3(Pp) .. " W")
  for i = 1, #resu do out(resu[i][1] .. " = " .. s3(resu[i][2] / 1000) .. " kPa") end
end

local function ex_bern()
  titre("BERNOULLI 2 POINTS")
  schema("bern")
  R("Bernoulli exprime la conservation de l'energie par unite de volume le long d'une ligne de courant, pour un fluide parfait (sans frottement), incompressible et en regime stationnaire: P1 + rho*g*z1 + 1/2*rho*v1^2 = P2 + rho*g*z2 + 1/2*rho*v2^2.",
    "Les trois termes sont la pression, l'energie potentielle et l'energie cinetique. Si l'un augmente, les autres doivent baisser.",
    "Rappels utiles: a une surface libre P = Patm; dans un grand reservoir la vitesse est presque nulle; dans un tuyau le debit se conserve, S1*v1 = S2*v2.")
  out("Inconnue: 1 P2, 2 v2, 3 z2")
  local k = ask("choix", 1)
  local rho = ask("rho", 1000)
  local p1 = ask("P1", PATM)
  local z1 = ask("z1", 0)
  local v1 = ask("v1 m/s", 0)
  local B1 = p1 + rho * G * z1 + 0.5 * rho * v1 ^ 2
  out("B1 = P1 + rho*g*z1 + 1/2*rho*v1^2")
  res("B1", B1, "Pa")
  if k == 1 then
    local z2 = ask("z2", 0)
    out("v2: donnee(1) ou par diametres d1,d2 (2)")
    local kk = ask("choix", 1)
    local v2
    if kk == 2 then
      local d1 = ask("d1", 0.1)
      local d2 = ask("d2", 0.05)
      v2 = v1 * (d1 / d2) ^ 2
      R("Le debit se conserve: S1*v1 = S2*v2, donc v2 = v1*(d1/d2)^2. Un retrecissement accelere le fluide.")
      res("v2", v2, "m/s")
    else
      v2 = ask("v2 m/s", 0)
    end
    local p2 = B1 - rho * G * z2 - 0.5 * rho * v2 ^ 2
    R("On isole P2: P2 = B1 - rho*g*z2 - 1/2*rho*v2^2. Si le fluide accelere ou monte, sa pression diminue.")
    res("P2", p2, "Pa")
    out("  = " .. r4(p2 / 1e5) .. " bar")
  elseif k == 2 then
    local p2 = ask("P2", PATM)
    local z2 = ask("z2", 0)
    local x = 2 * (B1 - p2 - rho * G * z2) / rho
    R("On isole v2: v2 = sqrt(2*(B1 - P2 - rho*g*z2)/rho). La vitesse vient de l'energie qui n'est ni sous forme de pression ni sous forme d'altitude.")
    if x < 0 then
      out("impossible (negatif sous la racine): verifier les donnees", ERRC)
    else
      res("v2", math.sqrt(x), "m/s")
    end
  else
    local p2 = ask("P2", PATM)
    local v2 = ask("v2 m/s", 0)
    local z2 = (B1 - p2 - 0.5 * rho * v2 ^ 2) / (rho * G)
    R("On isole z2: z2 = (B1 - P2 - 1/2*rho*v2^2)/(rho*g).")
    res("z2", z2, "m")
  end
end

local function ex_divers()
  titre("FORMULES RAPIDES")
  out("1 P=rho*g*h  2 F=P*S")
  out("3 presse F2=F1*S2/S1")
  out("4 Archimede FA=rho*V*g")
  out("5 F=2*sigma*L (film)")
  local k = ask("choix", 1)
  if k == 1 then
    local rho = ask("rho", 1000)
    local h = ask("h", 1)
    R("Hydrostatique: en descendant de h dans un fluide immobile de masse volumique rho, la pression augmente du poids de la colonne de fluide par unite de surface, soit rho*g*h.")
    res("dP", rho * G * h, "Pa")
  elseif k == 2 then
    local p = ask("P", 1e5)
    local d = ask("diametre", 0.1)
    local S = math.pi * d ^ 2 / 4
    R("La pression est une force repartie sur une surface: F = P*S. La surface d'un disque vaut pi*d^2/4. Convertir d en metres avant de calculer, sinon l'erreur est elevee au carre.")
    res("S", S, "m2")
    res("F", p * S, "N")
  elseif k == 3 then
    schema("divers")
    local f1 = ask("F1 N", 100)
    local d1 = ask("d1", 0.02)
    local d2 = ask("d2", 0.2)
    R("Principe de Pascal: un liquide transmet la pression dans toutes les directions. Si les deux pistons sont a la meme hauteur, la pression est la meme sous chacun: F1/S1 = F2/S2.",
      "Le rapport des forces est donc le rapport des surfaces, soit le carre du rapport des diametres: F2 = F1*(d2/d1)^2. Une petite force sur le petit piston souleve une grande charge.")
    res("F2", f1 * (d2 / d1) ^ 2, "N")
  elseif k == 4 then
    local rho = ask("rho fluide", 1000)
    local V = ask("V immerge m3", 1e-3)
    R("Poussee d'Archimede: le fluide pousse l'objet vers le haut avec une force egale au poids du fluide deplace, F_A = rho_fluide*V_immerge*g. On utilise le rho du FLUIDE et seulement la partie immergee du volume.")
    res("F_A", rho * V * G, "N")
  else
    local s = ask("sigma N/m", 0.0728)
    local L = ask("L", 0.05)
    R("Un film de savon a deux faces, et chacune tire sur la tige avec une force sigma*L. La force totale vaut donc F = 2*sigma*L.")
    res("F", 2 * s * L, "N")
  end
end

local VF = {
 {"Un fluide peut etre soit solide soit liquide.", "F",
  "Un fluide est un milieu qui s'ecoule: liquide, gaz ou plasma. Un solide garde sa forme et ne s'ecoule pas, ce n'est donc pas un fluide."},
 {"Les plasmas sont des fluides.", "V",
  "Un plasma est un gaz ionise. Comme un gaz, il n'a pas de forme propre et s'ecoule: c'est un fluide."},
 {"La viscosite est une caracteristique des fluides.", "V",
  "La viscosite mesure la resistance d'un fluide a l'ecoulement, c'est-a-dire les frottements internes entre ses couches. C'est une propriete propre a chaque fluide (eau, huile, miel...)."},
 {"L'ecoulement d'un fluide est un processus de relaxation.", "V",
  "Un fluide ne peut pas supporter durablement une contrainte de cisaillement: il se deforme et s'ecoule jusqu'a ce que la contrainte disparaisse. C'est ce retour progressif vers l'equilibre qu'on appelle relaxation."},
 {"Pour les fluides incompressibles, une seconde viscosite doit etre prise en compte pour les mouvements de compression ou de dilatation.", "F",
  "La seconde viscosite (viscosite de volume) n'intervient que si le volume du fluide change. Un fluide incompressible ne se comprime ni ne se dilate, donc ce terme ne joue aucun role."},
 {"Les frottements visqueux dans un fluide s'opposent aux gradients de vitesse d'ecoulement.", "V",
  "Quand deux couches voisines vont a des vitesses differentes, la viscosite freine la plus rapide et entraine la plus lente. Elle tend donc a egaliser les vitesses, c'est-a-dire a reduire le gradient de vitesse."},
 {"En hydrostatique, la pression depend de la viscosite du fluide.", "F",
  "En hydrostatique, le fluide est immobile: il n'y a aucun gradient de vitesse, donc aucun frottement visqueux. La pression ne depend que de rho, g et de la profondeur (P = P0 + rho*g*h)."},
 {"La poussee d'Archimede est une force verticale ascendante egale en norme au poids du fluide deplace.", "V",
  "C'est l'enonce meme du principe d'Archimede: F_A = rho_fluide*V_immerge*g, dirigee vers le haut."},
 {"La courbure de la surface de separation entre les deux milieux fluides indique une difference de temperature de part et d'autre.", "F",
  "La courbure d'une interface indique une difference de PRESSION, pas de temperature: c'est la loi de Laplace, dP = 2*sigma/R, avec la pression la plus grande du cote concave."},
 {"La loi de l'hydrostatique ne peut pas etre retrouvee a partir de l'equation de Bernoulli.", "F",
  "Si on pose v = 0 dans Bernoulli (fluide au repos), il reste P + rho*g*z = constante, ce qui est exactement la loi de l'hydrostatique. Elle en est donc un cas particulier."},
}

local function askText(txt)
  prompt = txt
  mode = "input"
  inbuf = ""
  local s = coroutine.yield()
  out(prompt .. s, GRIS)
  prompt = ""
  return s
end

local function ex_vf()
  titre("VRAI OU FAUX (TE1 2025)")
  R("Pour chaque affirmation, tape v ou f (ou juste [enter] pour voir directement la reponse). Le programme donne la bonne reponse, l'explication, puis ton score.")
  local score, rep = 0, 0
  for i = 1, #VF do
    local phrase, sol, expl = VF[i][1], VF[i][2], VF[i][3]
    out("")
    out(i .. ". " .. phrase)
    local a = askText("v / f ? "):lower()
    local nom = "FAUX"
    if sol == "V" then nom = "VRAI" end
    if a == "v" or a == "f" then
      rep = rep + 1
      if a:upper() == sol then
        score = score + 1
        out("Juste: " .. nom, {0, 140, 0})
      else
        out("Faux, la reponse est " .. nom, ERRC)
      end
    else
      out("Reponse: " .. nom)
    end
    R(expl)
    pause()
  end
  if rep > 0 then out("Score: " .. score .. " / " .. rep) end
  local l = ""
  for i = 1, #VF do l = l .. i .. VF[i][2] .. " " end
  out("-- resume des reponses")
  out(l)
end

-- ---------------------------------------------------------
-- menu

local EX = {ex_pile, ex_capil, ex_lances, ex_couronne, ex_ecoul,
            ex_serpentin, ex_bern, ex_divers, ex_vf}

main = function()
  while true do
    titre("TE1 FLUIDES - MENU")
    out("1 Pile fluides / tube U")
    out("2 Capillarite")
    out("3 Lances incendie/pompe")
    out("4 Archimede couronne")
    out("5 Reynolds / Poiseuille")
    out("6 Serpentin (E05 ex.4)")
    out("7 Bernoulli 2 points")
    out("8 Formules rapides")
    out("9 Vrai ou faux")
    out("[esc] revient ici a tout moment", GRIS)
    local ch = math.floor(ask("choix", 0))
    if EX[ch] then
      EX[ch]()
      pause()
    end
  end
end

local function resume(v)
  if not co then return end
  local ok, err = coroutine.resume(co, v)
  if not ok then
    out("ERREUR: " .. tostring(err), ERRC)
    co = nil
    mode = "key"
    prompt = "[enter] retour au menu"
  end
  inval()
end

local function start()
  co = coroutine.create(main)
  mode = "text"
  resume()
end

-- ---------------------------------------------------------
-- evenements Nspire

local FONT = 9
local function wrapAll(gc, w)
  wrapped = {}
  for i = 1, #paras do
    local t, c = paras[i][1], paras[i][2]
    if t == "" then
      table.insert(wrapped, {"", c})
    else
      local line = ""
      for word in t:gmatch("%S+") do
        local test = word
        if line ~= "" then test = line .. " " .. word end
        if gc:getStringWidth(test) > w and line ~= "" then
          table.insert(wrapped, {line, c})
          line = "  " .. word
        else
          line = test
        end
      end
      table.insert(wrapped, {line, c})
    end
  end
  dirty = false
  wrapW = w
end

function on.paint(gc)
  local W = platform.window:width()
  local H = platform.window:height()
  gc:setFont("sansserif", "r", FONT)
  if mode == "schema" and schemaFn then
    gc:setColorRGB(255, 255, 255); gc:fillRect(0, 0, W, H)
    gc:setColorRGB(0, 0, 0)
    local ok, err = pcall(schemaFn, gc)
    gc:setColorRGB(0, 0, 0)
    gc:setFont("sansserif", "r", FONT)
    if not ok then gc:drawString("schema: " .. tostring(err), 4, 30, "top") end
    gc:drawString("[enter] continuer", W - 95, H - 14, "top")
    return
  end
  if dirty or wrapW ~= W - 8 then wrapAll(gc, W - 8) end
  local lh = gc:getStringHeight("Ag")
  local barH = lh + 6
  local nl = math.floor((H - barH) / lh)
  local last = #wrapped - scroll
  local first = math.max(1, last - nl + 1)
  local y = 2
  for i = first, last do
    local l = wrapped[i]
    gc:setColorRGB(l[2][1], l[2][2], l[2][3])
    gc:drawString(l[1], 4, y, "top")
    y = y + lh
  end
  -- barre de saisie
  gc:setColorRGB(225, 230, 240); gc:fillRect(0, H - barH, W, barH)
  gc:setColorRGB(0, 0, 0)
  local s = prompt
  if mode == "input" then s = prompt .. inbuf .. "_" end
  while gc:getStringWidth(s) > W - 8 and #s > 1 do s = s:sub(2) end
  gc:drawString(s, 4, H - barH + 3, "top")
  if scroll > 0 then
    gc:setColorRGB(200, 0, 0)
    gc:drawString("^" .. scroll, W - 30, 2, "top")
  end
end

function on.charIn(ch)
  if mode == "input" then
    inbuf = inbuf .. ch
    inval()
  elseif mode == "schema" then
    mode = "text"
    resume()
  end
end

function on.backspaceKey()
  if mode == "input" and #inbuf > 0 then
    inbuf = inbuf:sub(1, -2)
    inval()
  end
end

function on.enterKey()
  if mode == "input" then
    local s = inbuf
    inbuf = ""
    mode = "text"
    resume(s)
  elseif mode == "key" or mode == "schema" then
    mode = "text"
    if co then resume() else start() end
  end
end

function on.escapeKey()
  scroll = 0
  start()
end

function on.arrowUp()
  if mode ~= "schema" and scroll < #wrapped - 3 then
    scroll = scroll + 3
    inval()
  end
end

function on.arrowDown()
  if scroll > 0 then
    scroll = math.max(0, scroll - 3)
    inval()
  end
end

function on.resize()
  dirty = true
end

function on.construction()
  start()
end
