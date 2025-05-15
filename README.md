# Implémentation de l'algorithme DES en Python

Ce projet est une implémentation complète de l'algorithme **DES (Data Encryption Standard)** en Python, incluant une **méthode d'attaque par fautes**

---

## Description

Cette implémentation permet de :

- Chiffrer des données avec l'algorithme DES  
- Récupérer une clé de chiffrement DES à partir d'une analyse de fautes  
- Générer des sous-clés pour le processus DES  
- Manipuler des données binaires via plusieurs opérations : permutation, substitution, XOR, etc.

---

## Structure du code

Le projet s'organise autour de plusieurs **classes** et **fonctions** principales :

### Classes principales

- `Message` : Stocke les informations sur un message clair, chiffré, fauté, etc.
- `DES` : Implémente l'algorithme DES avec les blocs, sous-clés, permutations, etc.
- `Key` : Gère les structures de clés (48-bit, 56-bit, 64-bit)

---

### Fonctions principales

| Fonction                  | Description                                                                 |
|---------------------------|-----------------------------------------------------------------------------|
| `hexatobinary()`          | Convertit un nombre hexadécimal en tableau de bits                          |
| `decimaltobinary()`       | Convertit un nombre décimal en tableau de bits                              |
| `TabtoInt()` / `TabtoLong()` | Convertissent un tableau de bits en entier                              |
| `Permutation()`           | Applique une permutation à un tableau de bits                               |
| `splitTab()`              | Divise un tableau en deux parties égales                                    |
| `xor_op()`                | Applique l'opération XOR entre deux tableaux de bits                        |
| `fonctionDES()`           | Implémente le processus de chiffrement complet selon DES                    |
| `rechercheExostive()`     | Effectue une recherche exhaustive pour retrouver la sous-clé K16            |
| `getK56bit()`             | Reconstitue la clé DES de 56 bits à partir de K16                           |
| `getK64bitParite()`       | Reconstitue la clé DES de 64 bits avec bits de parité à partir de 56 bits   |

---

## Analyse de fautes (DFA)

Une partie essentielle du projet repose sur la **cryptanalyse par faute** :

### Principe :

1. Collecte de **paires (clair, chiffré correct)** et **(clair, chiffré fauté)**
2. Analyse des **différences sur le dernier round**
3. Recherche de **valeurs probables pour la sous-clé K16**
4. **Reconstruction** de la clé complète en remontant les étapes du key schedule

---

## Prérequis

Pour faire fonctionner le code, on a défini **les tableaux standards du DES** :

- `ip` : Permutation initiale  
- `ipMoin1` : Permutation initiale inverse  
- `e` : Table d'expansion E  
- `p` : Permutation P  
- `pMoin1` : Permutation P inverse  
- `pc1` : Permutation Choice 1  
- `pc2` : Permutation Choice 2  
- `pc1Moin1` : Inverse de PC1  
- `pc2Moin1` : Inverse de PC2  
- `sbox` : Tableau contenant les 8 S-boxes du DES
