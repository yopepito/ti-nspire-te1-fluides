# Solveur TE1 Fluides pour TI-Nspire

Programme pour TI-Nspire qui résout les exercices types du TE1 de Physique 2a (HEIG-VD, mécanique des fluides). Tu choisis un exercice, tu entres les valeurs de l'énoncé, et le programme te guide du schéma jusqu'au résultat :

1. **Le schéma à dessiner**, tracé en couleur à l'écran, avec les points numérotés comme dans le corrigé.
2. **Le raisonnement** (lignes qui commencent par `> `), écrit en phrases complètes : hypothèses, choix de la loi et pourquoi elle s'applique, pièges de signe, interprétation du résultat.
3. **La formule littérale**, puis l'**application numérique** avec les valeurs remplacées.
4. **Le résultat** avec 4 chiffres significatifs, plus la version arrondie à 3 chiffres à recopier sur la copie, comme le demandent les directives du TE.

Il sert à réviser et à vérifier ses réponses après un test. Ce n'est pas un outil à utiliser pendant l'examen : les directives du TE limitent les aides à un formulaire A4 recto/verso.

## Quel fichier pour quelle calculatrice ?

Regarde l'étiquette au-dessus de l'écran.

| Étiquette | Fichier | Langage |
|---|---|---|
| **TI-Nspire CX** ou **CX CAS** (sans « II ») | `te1_CX.tns` | Lua (OS 3.2 ou plus récent) |
| **TI-Nspire CX II** ou **CX II CAS** | `te1_CX.tns` ou `te1_CXII.tns` | Lua ou Python (OS 5.2 ou plus récent) |

Python n'existe que sur la CX II. Sur une CX, un document Python s'ouvre sur une page vide. La version Lua marche sur les deux modèles.

## Contenu du menu

| Menu | Exercice | Source des valeurs par défaut |
|---|---|---|
| 1 | Pile de fluides / tube en U, pressions relatives, point A | TE1 2024 et 2025, ex. 1 |
| 2 | Capillarité : Jurin, Laplace, tube mercure + air + eau | TE1 2024, ex. 2 |
| 3 | Bernoulli : lances à incendie, pompe, conduite, cavitation | TE1 2025, ex. 2 (TE1 2024, ex. 3) |
| 4 | Archimède à deux matériaux (couronne or + diamants) | TE1 2024, ex. 4 |
| 5 | Reynolds, Poiseuille, Blasius, perte de charge | Série E05 |
| 6 | Serpentin de chauffage, Bernoulli généralisé avec coudes | Série E05, ex. 4 |
| 7 | Bernoulli entre deux points (inconnue P, v ou z) | Cas général |
| 8 | Formules rapides : ρgh, F = P·S, presse, Archimède, film de savon | Cas général |
| 9 | Vrai ou faux : les 10 affirmations complètes, avec réponse et explication | TE1 2025 |

## Utilisation sur la calculatrice

1. Installe **TI-Nspire Computer Link**, gratuit sur [education.ti.com](https://education.ti.com).
2. Branche la calculatrice en USB et copie le bon fichier `.tns` dessus.
3. Ouvre-le depuis `Documents`.
   - **Version Lua (CX)** : l'application démarre directement sur le menu.
   - **Version Python (CX II)** : l'éditeur s'ouvre, appuie sur `Ctrl+R` pour lancer.

Touches de la version Lua :

| Touche | Action |
|---|---|
| chiffres + `enter` | choisir dans le menu, saisir une valeur |
| `enter` seul | prendre la valeur par défaut, passer à l'étape suivante, quitter un schéma |
| `del` | effacer un caractère |
| flèches haut / bas | faire défiler le texte |
| `esc` | revenir au menu |

## Saisie des valeurs

- Laisser l'entrée vide reprend la valeur de l'ancien test. Tu peux ainsi retrouver le corrigé, puis ne changer que ce qui diffère.
- Les unités usuelles sont converties automatiquement en SI : `5cm`, `8mm`, `6dl`, `175cl`, `440mN`, `4.7bar`, `15kPa`, `1atm`, `5lmin` (L/min), `2min`, `856g`.
- Les expressions sont acceptées : `2*60+15`, `5e-2`. Sur la calculatrice, les touches `(-)` et `EE` fonctionnent aussi.

## Vérification

Avec les valeurs par défaut, les deux versions retrouvent les corrigés officiels :

| Exercice | Corrigé | Programme |
|---|---|---|
| Pile de fluides (TE1 2025) | 7240 / 10183 / 12096 / −1148 Pa | identique |
| Lances (TE1 2025) : v2, Q pompe, P3 | 23,85 m/s ; 187 l/s ; 3,78 bar | identique |
| Serpentin vertical (E05-4) : Re, P pompe | 29,8 ; 19,7 W | identique |
| Serpentin vertical : P1 / P2 / P3 / P4 | 322 / 285 / 212 / 138 kPa | identique |
| Serpentin au sol : P1 / P2 / P3 / P4 | 329 / 293 / 215 / 138 kPa | identique |
| Vrai ou faux (TE1 2025) | F V V V F V F V F F | identique |

Pour P5 dans l'exercice des lances, le corrigé donne 6465 Pa et le programme 6287 Pa. L'écart vient d'une erreur d'arrondi dans le corrigé, qui écrit v5 = 16,556 m/s au lieu de 16,565 m/s.

L'exercice mercure/eau (menu 2, choix 3) et la couronne (menu 4) n'ont pas de corrigé officiel. Les signes de Laplace ont été vérifiés à la main, mais confronte-les au cours.

## Simulateur (tester sans la calculatrice)

```bash
python simulateur/server.py
```

| Page | Simule |
|---|---|
| http://localhost:8765/simulateur/lua.html | TI-Nspire CX : application Lua, API graphique et événements de la Nspire |
| http://localhost:8765/simulateur/ | TI-Nspire CX II : console Python, `input()`, `ti_draw`, `get_key` |

Les deux pages ouvrent aussi un `.tns`. Le serveur déchiffre le document comme la calculatrice, affiche sa structure (en-tête, fichiers, sommes de contrôle), puis lance le script qu'il contient.

Les moteurs (Pyodide pour Python, fengari pour Lua) sont chargés depuis un CDN : il faut Internet au premier lancement.

Ce ne sont pas des émulateurs de l'OS de TI. Fengari exécute du Lua 5.3, alors que la Nspire utilise Lua 5.1, et Pyodide exécute CPython, alors que la CX II utilise MicroPython. Les simulateurs détectent la plupart des problèmes, mais pas tous.

## Modifier le programme

```bash
pip install pycryptodome
python py2tns.py te1.lua te1_CX.tns
python py2tns.py te1.py te1_CXII.tns
```

`py2tns.py` reprend en Python le convertisseur [Luna](https://github.com/ndless-nspire/Luna) (Mozilla Public License 1.1), pour Lua et Python. Ses fichiers ont été vérifiés identiques octet par octet à ceux de Luna 2.1 compilé.

## Fichiers

| Fichier | Rôle |
|---|---|
| `te1.lua` | Le solveur en Lua (CX et CX II) |
| `te1.py` | Le solveur en Python (CX II) |
| `te1_CX.tns`, `te1_CXII.tns` | Les versions prêtes à copier sur la calculatrice |
| `py2tns.py` | Convertisseur `.lua` / `.py` vers `.tns` |
| `simulateur/` | Simulateurs dans le navigateur et serveur local |

## Limites

- Je n'ai pas encore lancé la version Lua sur une vraie calculatrice. Si quelque chose s'affiche mal, ouvre une issue avec une photo de l'écran.
- Les modèles suivent le cours : fluide parfait pour Bernoulli, Poiseuille en laminaire, Blasius en turbulent, et les coefficients λ1 = 0,131 et λ2 = 1,847 pour les coudes.
