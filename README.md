# Solveur TE1 Fluides pour TI-Nspire CX II

Programme Python pour la TI-Nspire CX II qui résout les exercices types du TE1 de Physique 2a (HEIG-VD, mécanique des fluides). Tu choisis un exercice, tu entres les valeurs de l'énoncé, et le programme te guide du schéma jusqu'au résultat :

1. **Le schéma à dessiner.** Il est tracé à l'écran de la calculatrice (module `ti_draw`) et affiché en texte sur PC. Les points sont numérotés comme dans le corrigé.
2. **Le raisonnement** (lignes qui commencent par `> `), écrit en phrases complètes : hypothèses, choix de la loi et pourquoi elle s'applique, pièges de signe, interprétation du résultat.
3. **La formule littérale**, puis l'**application numérique** avec les valeurs remplacées.
4. **Le résultat** avec 4 chiffres significatifs, plus la version arrondie à 3 chiffres à recopier sur la copie, comme le demandent les directives du TE.

Il sert à réviser et à vérifier ses réponses après un test. Ce n'est pas un outil à utiliser pendant l'examen : les directives du TE limitent les aides à un formulaire A4 recto/verso.

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

## Saisie des valeurs

- Laisser l'entrée vide reprend la valeur de l'ancien test. Tu peux ainsi retrouver le corrigé, puis ne changer que ce qui diffère.
- Les unités usuelles sont converties automatiquement en SI : `5cm`, `8mm`, `6dl`, `175cl`, `440mN`, `4.7bar`, `15kPa`, `1atm`, `5lmin` (L/min), `2min`, `856g`.
- Les expressions sont acceptées : `2*60+15`, `5e-2`.

## Vérification

Avec les valeurs par défaut, le programme retrouve les corrigés officiels :

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

## Installation sur la calculatrice

Il faut une TI-Nspire CX II avec l'OS 5.2 ou plus récent, pour avoir Python.

1. Installe **TI-Nspire Computer Link**, gratuit sur [education.ti.com](https://education.ti.com).
2. Branche la calculatrice en USB et copie `te1.tns` dessus.
3. Sur la calculatrice : `Documents` → `te1` → `Ctrl+R` pour lancer.

Pour revenir au texte après un schéma, appuie sur n'importe quelle touche.

## Simulateur (tester sans la calculatrice)

Le dossier `simulateur/` contient une page qui imite l'écran de la TI-Nspire CX II : une console Python avec `input()`, les dessins `ti_draw` en couleur, `get_key` au clavier, et le chargement d'un `.tns` avec vérification de sa structure.

```bash
python simulateur/server.py
```

Ouvre ensuite http://localhost:8765/simulateur/ et appuie sur **Ctrl+R**. Le bouton « Ouvrir .py / .tns » charge un autre fichier.

Le serveur est nécessaire : il envoie les en-têtes qui permettent à `input()` de bloquer comme sur la calculatrice. Python est chargé depuis le CDN de Pyodide, il faut donc une connexion Internet au premier lancement.

Le simulateur exécute du CPython et non le MicroPython de la TI, et c'est lui qui vérifie le `.tns`, pas l'OS de TI. Il détecte la plupart des problèmes, mais pas tous.

## Tester sur PC sans simulateur

```bash
python te1.py
```

Dans ce cas, les schémas s'affichent en texte.

## Modifier le programme

```bash
pip install pycryptodome
python py2tns.py te1.py te1.tns
```

`py2tns.py` reprend en Python la partie « Python vers TNS » de [Luna](https://github.com/ndless-nspire/Luna) (Mozilla Public License 1.1). Il ajoute au document le chiffrement des fichiers XML et l'en-tête zip propres au format TI.

Le code reste compatible avec le Python de la calculatrice : pas de f-strings, uniquement le module `math` (plus `ti_draw` et `ti_system` s'ils sont disponibles), et les phrases sont coupées automatiquement à la largeur de l'écran.

## Fichiers

| Fichier | Rôle |
|---|---|
| `te1.py` | Le solveur |
| `te1.tns` | Le solveur prêt à copier sur la calculatrice |
| `py2tns.py` | Convertisseur `.py` vers `.tns` |

## Limites

- Je n'ai pas encore lancé le `.tns` sur une vraie calculatrice. Si elle le refuse, ou si un schéma s'affiche mal, ouvre une issue avec le message ou une photo.
- Les modèles suivent le cours : fluide parfait pour Bernoulli, Poiseuille en laminaire, Blasius en turbulent, et les coefficients λ1 = 0,131 et λ2 = 1,847 pour les coudes.
