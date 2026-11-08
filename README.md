# Solveur TE1 Fluides pour TI-Nspire CX II

Programme Python pour la TI-Nspire CX II qui résout les exercices types du TE1 de Physique 2a (HEIG-VD, mécanique des fluides). Tu choisis un type d'exercice, tu entres les valeurs de l'énoncé, et le programme affiche :

- le **raisonnement** à écrire sur la copie (lignes qui commencent par `> `) : hypothèses, loi utilisée, pièges de signe, conclusion ;
- la **formule littérale** ;
- l'**application numérique** avec les valeurs remplacées ;
- le **résultat** avec son unité.

Il sert à réviser et à vérifier ses réponses après un test. Ce n'est pas un outil à utiliser pendant l'examen : les directives du TE limitent les aides à un formulaire A4 recto/verso.

## Exercices couverts

| Menu | Type d'exercice | Exemple tiré des anciens tests |
|---|---|---|
| 1 | Pile de fluides / tube en U, pression relative | Conteneur mazout/eau/trichloréthylène, point A |
| 2 | Capillarité : Jurin, Laplace, tube Hg + air + eau | Colonne de mercure dans un tube fin |
| 3 | Bernoulli : lances à incendie, pompe, conduite | Jet jusqu'au 10e étage, cavitation |
| 4 | Archimède à deux matériaux | Couronne or + diamants pesée dans l'air puis dans l'eau |
| 5 | Reynolds, Poiseuille, Blasius, perte de charge | Huile dans un tuyau |
| 6 | Bernoulli entre deux points (inconnue P, v ou z) | Cas général |
| 7 | Formules rapides | ρgh, F = P·S, presse hydraulique, film de savon |

Laisser une entrée vide reprend la valeur de l'ancien test. On peut donc vérifier qu'on retrouve le corrigé, puis changer seulement les valeurs qui diffèrent. Les entrées acceptent les expressions (`2*60`, `5e-2`).

## Vérification

Avec les valeurs par défaut, le programme retrouve le corrigé officiel du TE1 2025 :

| Grandeur | Corrigé | Programme |
|---|---|---|
| Pressions relatives de la pile de fluides | 7240 / 10183 / 12096 / −1148 Pa | identique |
| Vitesse en sortie de buse v2 | 23,85 m/s | 23,85 m/s |
| Débit de la pompe | 187 l/s | 187 l/s |
| Pression dans le tuyau P3 | 3,78 bar | 3,78 bar |

Le corrigé donne P5 = 6465 Pa et le programme 6287 Pa. L'écart vient d'une erreur d'arrondi dans le corrigé, qui écrit v5 = 16,556 m/s au lieu de 16,565 m/s.

La partie capillarité (exercice mercure/eau) n'a pas de corrigé officiel. Les signes viennent de la loi de Laplace : vérifie-les avec le cours.

## Installation sur la calculatrice

Il faut une TI-Nspire CX II avec l'OS 5.2 ou plus récent, pour avoir Python.

1. Installe **TI-Nspire Computer Link**, gratuit sur [education.ti.com](https://education.ti.com).
2. Branche la calculatrice en USB et copie `te1.tns` dessus.
3. Sur la calculatrice : `Documents` → `te1` → `Ctrl+R` pour lancer.

## Tester sur PC

Le même fichier tourne avec n'importe quel Python 3 :

```bash
python te1.py
```

## Modifier le programme

Après une modification de `te1.py`, régénère le `.tns` :

```bash
pip install pycryptodome
python py2tns.py te1.py te1.tns
```

`py2tns.py` reprend en Python la partie « Python vers TNS » de [Luna](https://github.com/ndless-nspire/Luna) (Mozilla Public License 1.1). Il ajoute au document le chiffrement des fichiers XML et l'en-tête zip propres au format TI.

Le code de `te1.py` reste compatible avec le Python de la calculatrice : pas de f-strings, uniquement le module `math`, et des lignes courtes pour l'écran.

## Fichiers

| Fichier | Rôle |
|---|---|
| `te1.py` | Le solveur |
| `te1.tns` | Le solveur prêt à copier sur la calculatrice |
| `py2tns.py` | Convertisseur `.py` vers `.tns` |

## Limites

- Je n'ai pas encore lancé le `.tns` sur une vraie calculatrice. Si elle le refuse, ouvre une issue avec le message d'erreur.
- Le programme affiche 4 chiffres significatifs. Les directives du TE en demandent 3 : arrondis sur la copie.
- Les modèles suivent le cours : fluide parfait pour Bernoulli, Poiseuille en laminaire, Blasius en turbulent.
