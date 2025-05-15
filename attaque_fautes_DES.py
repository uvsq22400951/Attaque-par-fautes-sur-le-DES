class Message:
    """Structure utilisée dans la recherche de K16"""
    def __init__(self):
        self.chiffrer_hexa = 0
        self.chiffrer_binaire = [0] * 64
        self.chiffrer_binaire_permuter = [0] * 64
        self.left_chiffrer = [0] * 32
        self.right_chiffrer = [0] * 32
        self.right_chiffrer_exp = [0] * 48
        self.sbox6_bits = [0] * 6
        self.sbox6_bits_xorer = [0] * 6
        self.sbox4_bits = [0] * 4

class Key:
    """Structure utilisée dans les recherche des 16 sous clefs"""
    def __init__(self):
        self.key48bit = [0] * 48
        self.key56bit = [0] * 56
        self.key64bitb = [0] * 64
        self.key8bit = [0] * 8

class DES:
    """Structure utilisée dans le DES"""
    def __init__(self):
        self.claire_binaire = [0] * 64
        self.key64_bit = [0] * 64
        self.claire_binaire_ip = [0] * 64
        self.right32_bit = [0] * 32
        self.left32_bit = [0] * 32
        self.right32_bit_plus1 = [0] * 32
        self.left32_bit_plus1 = [0] * 32
        self.right48_bit = [0] * 48
        self.sub_key = [[0] * 48 for _ in range(16)]
        self.chiffrer_binaire = [0] * 64

# Tables de permutation
# Initial permutation
ip = [
    58, 50, 42, 34, 26, 18, 10, 2,
    60, 52, 44, 36, 28, 20, 12, 4,
    62, 54, 46, 38, 30, 22, 14, 6,
    64, 56, 48, 40, 32, 24, 16, 8,
    57, 49, 41, 33, 25, 17, 9, 1,
    59, 51, 43, 35, 27, 19, 11, 3,
    61, 53, 45, 37, 29, 21, 13, 5,
    63, 55, 47, 39, 31, 23, 15, 7
]

# L'inverse de l'initial permutation
ipmoins1 = [
    40, 8, 48, 16, 56, 24, 64, 32,
    39, 7, 47, 15, 55, 23, 63, 31,
    38, 6, 46, 14, 54, 22, 62, 30,
    37, 5, 45, 13, 53, 21, 61, 29,
    36, 4, 44, 12, 52, 20, 60, 28,
    35, 3, 43, 11, 51, 19, 59, 27,
    34, 2, 42, 10, 50, 18, 58, 26,
    33, 1, 41, 9, 49, 17, 57, 25
]

# Expansion
e = [
    32, 1, 2, 3, 4, 5,
    4, 5, 6, 7, 8, 9,
    8, 9, 10, 11, 12, 13,
    12, 13, 14, 15, 16, 17,
    16, 17, 18, 19, 20, 21,
    20, 21, 22, 23, 24, 25,
    24, 25, 26, 27, 28, 29,
    28, 29, 30, 31, 32, 1
]

# Permutation dans la fonction interne f
p = [
    16, 7, 20, 21, 29, 12, 28, 17,
    1, 15, 23, 26, 5, 18, 31, 10,
    2, 8, 24, 14, 32, 27, 3, 9,
    19, 13, 30, 6, 22, 11, 4, 25
]

# Permutation inverse dans la fonction interne f
pmoins1 = [
    9, 17, 23, 31,
    13, 28, 2, 18,
    24, 16, 30, 6,
    26, 20, 10, 1,
    8, 14, 25, 3,
    4, 29, 11, 19,
    32, 12, 22, 7,
    5, 27, 15, 21
]

# Les 8 S-box contenu dans la fonction f
sbox = [
    [
        [14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7],
        [0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8],
        [4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0],
        [15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13]
    ],
    [
        [15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10],
        [3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5],
        [0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15],
        [13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9]
    ],
    [
        [10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8],
        [13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1],
        [13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7],
        [1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12]
    ],
    [
        [7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15],
        [13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9],
        [10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4],
        [3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14]
    ],
    [
        [2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9],
        [14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6],
        [4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14],
        [11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3]
    ],
    [
        [12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11],
        [10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8],
        [9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6],
        [4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13]
    ],
    [
        [4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1],
        [13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6],
        [1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2],
        [6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12]
    ],
    [
        [13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7],
        [1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2],
        [7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8],
        [2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11]
    ]
]

# Permutation 1 dans le key schedule
pc1 = [
    57, 49, 41, 33, 25, 17, 9,
    1, 58, 50, 42, 34, 26, 18,
    10, 2, 59, 51, 43, 35, 27,
    19, 11, 3, 60, 52, 44, 36,
    63, 55, 47, 39, 31, 23, 15,
    7, 62, 54, 46, 38, 30, 22,
    14, 6, 61, 53, 45, 37, 29,
    21, 13, 5, 28, 20, 12, 4
]

# Permutation 1 inverse dans le key schedule
pc1moins1 = [
    8, 16, 24, 56, 52, 44, 36, 0,
    7, 15, 23, 55, 51, 43, 35, 0,
    6, 14, 22, 54, 50, 42, 34, 0,
    5, 13, 21, 53, 49, 41, 33, 0,
    4, 12, 20, 28, 48, 40, 32, 0,
    3, 11, 19, 27, 47, 39, 31, 0,
    2, 10, 18, 26, 46, 38, 30, 0,
    1, 9, 17, 25, 45, 37, 29, 0
]

# Permutation 2 dans le key schedule qui fait passer la clef de 56 a 48 bits
pc2 = [
    14, 17, 11, 24, 1, 5,
    3, 28, 15, 6, 21, 10,
    23, 19, 12, 4, 26, 8,
    16, 7, 27, 20, 13, 2,
    41, 52, 31, 37, 47, 55,
    30, 40, 51, 45, 33, 48,
    44, 49, 39, 56, 34, 53,
    46, 42, 50, 36, 29, 32
]

# Permutation 2 inverse dans le key schedule
pc2moins1 = [
    5, 24, 7, 16, 6, 10, 20,
    18, 0, 12, 3, 15, 23, 1,
    9, 19, 2, 0, 14, 22, 11,
    0, 13, 4, 0, 17, 21, 8,
    47, 31, 27, 48, 35, 41, 0,
    46, 28, 0, 39, 32, 25, 44,
    0, 37, 34, 43, 29, 36, 38,
    45, 33, 26, 42, 0, 30, 40
]

# Valeurs constantes
MESSAGE_CLAIRE = 0x5808C76EFB70D5D3
CHIFFRER_JUSTE = 0xCBDEF4300B79D7A0

CHIFFRER_FAUX = [
    0x829EF0315B29DFA0,
    0xCBDEF5100F59C7A0,
    0xCBDBF4308A7917B4,
    0xCBD6F0775B6CD7A0,
    0xDFDEFD312B69C7E0,
    0xCBFFF4340F78C634,
    0x5FDEFD210B6993A0,
    0xCFDFB4340B58D734,
    0xC88AF0341B79D5A4,
    0x8BDEE4384B25D7A1,
    0xCBDEB4302B79E7E0,
    0xCBD9F4E00A78D3A4,
    0xCBCEE6314328D7A0,
    0xDFD6F4214B6D9380,
    0xABCEE6300F38D6E1,
    0x9FDEF4200B719381,
    0x5FDAF5200B7913A4,
    0xCA9EF0761B7AD7A0,
    0xCBDEF4314329DFA1,
    0xDF5EB5000E79C7A0,
    0xCACE70241979D3A0,
    0x8BDCF4700F38C7A9,
    0xC29E70215B69D3A0,
    0x8ADEF4301F3BC7A9,
    0xAFDEE5300F39F6E1,
    0xCBDAF4A00AF9D3A0,
    0xCBCEF4341979D5A0,
    0xCBFEE4384F2DC6A0,
    0xCBDBD4308A7996E0,
    0xCA1EF4205A7DD7A2,
    0xC9CAD4340B79D6E4,
    0xCA9BF4305BFFD7B2
]


# Passer d'un long en hexa en un tableau de bit
def hexatobinary(hexa, nbrHexa):
    tabResult = [0] * (nbrHexa * 4)
    tmp = hexa
    compteur = nbrHexa * 4 - 1
    
    for j in range(nbrHexa):
        entier = tmp & 0xF
        for i in range(4):
            tabResult[compteur] = entier % 2
            entier = entier // 2
            compteur -= 1
        tmp = tmp >> 4
    
    return tabResult

# Transformer un entier en un tableau de bit
def decimaltobinary(decimal, nbrBit):
    tabResult = [0] * nbrBit
    entier = decimal
    
    for i in range(nbrBit - 1, -1, -1):
        tabResult[i] = entier % 2
        entier = entier // 2
    
    return tabResult

# Élevé à la puissance
def puissance(a, b):
    if b == 0:
        return 1
    else:
        return a * puissance(a, b - 1)

# Transformer un tableau de bit en un entier
def TabtoInt(tab, nbrBit):
    nombre = 0
    i = 0
    j = nbrBit - 1
    
    while j >= 0:
        if tab[j] != 0:
            nombre += puissance(2, i)
        i += 1
        j -= 1
    
    return nombre

# Transformer un tableau de bit en un hexadecimal
def TabtoLong(tab, nbrBit):
    nombre = 0
    i = 0
    j = nbrBit - 1
    
    while j >= 0:
        if tab[j] != 0:
            nombre += puissance(2, i)
        i += 1
        j -= 1
    
    return nombre

# Gère toutes les permutations y compris l'expansion
def Permutation(aPermuter, tablePermutation, nbrBit):
    resultat = [0] * nbrBit
    
    for i in range(nbrBit):
        if tablePermutation[i] != 0:
            resultat[i] = aPermuter[tablePermutation[i] - 1]
    
    return resultat

# Divise un tableau de bit en 2 tableaux de même longueur
def splitTab(completTab, nbrBit):
    leftTab = [0] * nbrBit
    rightTab = [0] * nbrBit
    
    for i in range(nbrBit):
        leftTab[i] = completTab[i]
        rightTab[i] = completTab[i + nbrBit]
    
    return leftTab, rightTab

# Applique un XOR entre 2 tableaux de bit
def xor_op(premierK, deuxiemeK, nbrBit):
    tabResult = [0] * nbrBit
    
    for i in range(nbrBit):
        tabResult[i] = premierK[i] ^ deuxiemeK[i]
    
    return tabResult

# Trouve la position du bit fauté
def bitFauter(tabJuste, tabFaux):
    tabxor = xor_op(tabJuste, tabFaux, 32)
    
    for j in range(32):
        if tabxor[j] == 1:
            return j
    
    return -1

# La boite de substitution qui transforme 6 bit en 4 bit selon la S-box choisie
def Sboxfonc(entrer, numSbox, sbox):
    row = entrer[0] * 2 + entrer[5]
    column = 0
    i = 0
    j = 4
    
    while j > 0:
        if entrer[j] != 0:
            column += puissance(2, i)
        i += 1
        j -= 1
    
    resultat4bit = sbox[numSbox][row][column]
    return hexatobinary(resultat4bit, 1)

# S'occupe de retrouver le L16 et le L16 fauté
def obtenirR16L16(hexa, e):
    m = Message()
    m.chiffrer_hexa = hexa
    m.chiffrer_binaire = hexatobinary(hexa, 16)
    m.chiffrer_binaire_permuter = Permutation(m.chiffrer_binaire, ip, 64)
    m.left_chiffrer, m.right_chiffrer = splitTab(m.chiffrer_binaire_permuter, 32)
    return m

# On extrait 6 bit à une position bien définie au niveau des S-box
def extraire6Bits(m, position):
    for i in range(6):
        m.sbox6_bits[i] = m.right_chiffrer_exp[6 * position + i]

# Compare deux tableaux de même taille
def egale(tab1, tab2, nbrBit):
    for i in range(nbrBit):
        if tab1[i] != tab2[i]:
            return 0
    return 1

# Cette fonction traite les résultats de la recherche exhaustive pour trouver le bon K16
def k16enHexa(tabK16):
    resultat = 0
    tab = [0] * 8
    tabresult = [0] * 64
    
    for i in range(8):
        max_val = 0
        for j in range(64):
            if tabK16[i][j] > max_val:
                max_val = tabK16[i][j]
                tab[i] = j
        
        print(tab[i])
        tabclef = decimaltobinary(tab[i], 6)
        
        for j in range(6):
            tabresult[i * 6 + j] = tabclef[j]
    
    resultat = TabtoLong(tabresult, 48)
    return resultat

# Fait la recherche exhaustive pour trouver la clef K15
def rechercheExostive(LechiffrerJuste, LeschiffrerFaux, e, pMoin1, sbox):
    juste = Message()
    faux = Message()
    resultat = [[0 for _ in range(64)] for _ in range(8)]
    
    juste = obtenirR16L16(LechiffrerJuste, e)
    
    for w in range(32):
        faux = obtenirR16L16(LeschiffrerFaux[w], e)
        resultatxorLeft = xor_op(juste.left_chiffrer, faux.left_chiffrer, 32)
        leftPmoin1 = Permutation(resultatxorLeft, pMoin1, 32)
        
        bitfaux = bitFauter(juste.right_chiffrer, faux.right_chiffrer)
        print(f"bit faux : {bitfaux}")
        
        juste.right_chiffrer_exp = Permutation(juste.right_chiffrer, e, 48)
        faux.right_chiffrer_exp = Permutation(faux.right_chiffrer, e, 48)
        
        for i in range(48):
            if e[i] == (bitfaux + 1):
                extraire6Bits(juste, i // 6)
                extraire6Bits(faux, i // 6)
                
                resLeftJuste = [leftPmoin1[4 * (i // 6) + y] for y in range(4)]
                
                for j in range(64):
                    key = decimaltobinary(j, 6)
                    juste.sbox6_bits_xorer = xor_op(juste.sbox6_bits, key, 6)
                    faux.sbox6_bits_xorer = xor_op(faux.sbox6_bits, key, 6)
                    
                    juste.sbox4_bits = Sboxfonc(juste.sbox6_bits_xorer, i // 6, sbox)
                    faux.sbox4_bits = Sboxfonc(faux.sbox6_bits_xorer, i // 6, sbox)
                    
                    resSbox = xor_op(juste.sbox4_bits, faux.sbox4_bits, 4)
                    
                    if egale(resLeftJuste, resSbox, 4):
                        resultat[i // 6][TabtoInt(key, 6)] += 1
    
    aRetourner = k16enHexa(resultat)
    return aRetourner

# Initialise le tableau de bit à 0
def initTab(nbrBit):
    return [0] * nbrBit

# S'occupe de shifter les bit de nbrShift fois vers la gauche
def shiftGauche(tabAshifter, nbrShift, nbrBit):
    resultat = [0] * nbrBit
    
    for i in range(-nbrShift, nbrBit - nbrShift):
        if i < 0:
            resultat[i + nbrBit] = tabAshifter[i + nbrShift]
        else:
            resultat[i] = tabAshifter[i + nbrShift]
    
    return resultat

# On fusionne deux tableaux de même dimension
def fusionTab(leftTab, rightTab, nbrBit):
    resultat = [0] * (2 * nbrBit)
    
    for i in range(nbrBit):
        resultat[i] = leftTab[i]
        resultat[i + nbrBit] = rightTab[i]
    
    return resultat

# Génère les 16 clefs de K0 à K15 dans le DES
def generationSubKey(key64Bit, pc1, pc2):
    v = [1, 1, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 1]
    key56bit = Permutation(key64Bit, pc1, 56)
    Les16SubKey = [[0] * 48 for _ in range(16)]
    
    for i in range(16):
        tabSplit0, tabSplit1 = splitTab(key56bit, 28)
        tabSplitRes0 = shiftGauche(tabSplit0, v[i], 28)
        tabSplitRes1 = shiftGauche(tabSplit1, v[i], 28)
        key56bit = fusionTab(tabSplitRes0, tabSplitRes1, 28)
        Les16SubKey[i] = Permutation(key56bit, pc2, 48)
    
    return Les16SubKey

# Fonction interne F du DES
def f(Ri, Ki, e, p, sbox):
    right48b = Permutation(Ri, e, 48)
    resultatXor = xor_op(right48b, Ki, 48)
    sorti32bit = [0] * 32
    
    for j in range(8):
        entrerSbox = [resultatXor[6 * j + i] for i in range(6)]
        sortiSbox = Sboxfonc(entrerSbox, j, sbox)
        
        for i in range(4):
            sorti32bit[j * 4 + i] = sortiSbox[i]
    
    return Permutation(sorti32bit, p, 32)

# Sert à copier un tableau dans un autre de même dimension
def copieTab(aCopier, nbrBit):
    return aCopier.copy()

# DES : Prend en entrée un message clair et une clef pour donner un message chiffré
def fonctionDES(claire, k64, ip, ipMoin1, e, p, pc1, pc2, sbox):
    d = DES()
    d.claireBinaire = hexatobinary(claire, 16)
    d.key64Bit = hexatobinary(k64, 16)
    d.claireBinaireIp = Permutation(d.claireBinaire, ip, 64)
    d.left32Bit, d.right32Bit = splitTab(d.claireBinaireIp, 32)
    d.subKey = generationSubKey(d.key64Bit, pc1, pc2)
    
    for i in range(16):
        d.left32BitPlus1 = copieTab(d.right32Bit, 32)
        resultatF = f(d.right32Bit, d.subKey[i], e, p, sbox)
        d.right32BitPlus1 = xor_op(d.left32Bit, resultatF, 32)
        d.left32Bit = copieTab(d.left32BitPlus1, 32)
        d.right32Bit = copieTab(d.right32BitPlus1, 32)
    
    resultatConcat = fusionTab(d.right32Bit, d.left32Bit, 32)
    d.chiffrerBinaire = Permutation(resultatConcat, ipMoin1, 64)
    return TabtoLong(d.chiffrerBinaire, 64)

# Sert à obtenir les 56 bits justes de la clef de chiffrement
def getK56bit(claire, chiffrer, k16, pc2Moin1, pc1Moin1, ip, ipMoin1, e, p, pc1, pc2, sbox):
    k = Key()
    k.key48bit = hexatobinary(k16, 12)
    k.key56bit = Permutation(k.key48bit, pc2Moin1, 56)
    k.key64bitb = Permutation(k.key56bit, pc1Moin1, 64)
    
    position8bit = [14, 15, 19, 20, 51, 54, 58, 60]
    i = 0
    
    while i < 256:
        k.key8bit = decimaltobinary(i, 8)
        
        for j in range(8):
            k.key64bitb[position8bit[j] - 1] = k.key8bit[j]
        
        clef = TabtoLong(k.key64bitb, 64)
        
        if chiffrer == fonctionDES(claire, clef, ip, ipMoin1, e, p, pc1, pc2, sbox):
            return clef
        
        i += 1
    
    return 0

# Renvoie la clef de chiffrement complète de 64 bits
def getK64bitParite(claire, chiffrer, k16, pc2Moin1, pc1Moin1, ip, ipMoin1, e, p, pc1, pc2, sbox):
    compteur = 0
    tabClefB = hexatobinary(getK56bit(claire, chiffrer, k16, pc2Moin1, pc1Moin1, ip, ipMoin1, e, p, pc1, pc2, sbox), 16)
    
    for i in range(64):
        print(tabClefB[i], end="")
        if (i + 1) % 8 == 0:
            print(" ", end="")
    print()
    
    for i in range(1, 65):
        if (i % 8) == 0:
            if compteur % 2 == 1:
                tabClefB[i - 1] = 0
            else:
                tabClefB[i - 1] = 1
            compteur = 0
        else:
            compteur += tabClefB[i - 1]
    
    for i in range(64):
        print(tabClefB[i], end="")
        if (i + 1) % 8 == 0:
            print(" ", end="")
    print()
    
    return TabtoLong(tabClefB, 64)

def main():
    claire = 0x5808C76EFB70D5D3
    chiffrer = 0xCBDEF4300B79D7A0

    # tableau contenant 32 messages fautés (à adapter à ton cas réel)
    messages_fautes = [0x829EF0315B29DFA0,
    0xCBDEF5100F59C7A0, 
    0xCBDBF4308A7917B4, 
    0xCBD6F0775B6CD7A0,
    0xDFDEFD312B69C7E0, 
    0xCBFFF4340F78C634, 
    0x5FDEFD210B6993A0, 
    0xCFDFB4340B58D734,
    0xC88AF0341B79D5A4, 
    0x8BDEE4384B25D7A1, 
    0xCBDEB4302B79E7E0, 
    0xCBD9F4E00A78D3A4,
    0xCBCEE6314328D7A0, 
    0xDFD6F4214B6D9380, 
    0xABCEE6300F38D6E1, 
    0x9FDEF4200B719381,
    0x5FDAF5200B7913A4, 
    0xCA9EF0761B7AD7A0, 
    0xCBDEF4314329DFA1, 
    0xDF5EB5000E79C7A0,
    0xCACE70241979D3A0, 
    0x8BDCF4700F38C7A9, 
    0xC29E70215B69D3A0, 
    0x8ADEF4301F3BC7A9,
    0xAFDEE5300F39F6E1, 
    0xCBDAF4A00AF9D3A0, 
    0xCBCEF4341979D5A0, 
    0xCBFEE4384F2DC6A0,
    0xCBDBD4308A7996E0, 
    0xCA1EF4205A7DD7A2, 
    0xC9CAD4340B79D6E4, 
    0xCA9BF4305BFFD7B2]  # <= 32 chiffrés fautés avec 1 bit inversé dans R15

    print("\n Recherche de K16")
    k16 = rechercheExostive(chiffrer, messages_fautes, e, pmoins1, sbox)
    print(f"K16 (48 bits) = {hex(k16)}")

    print("\n Recherche de la cle 56 bits")
    k56 = getK56bit(claire, chiffrer, k16, pc2moins1, pc1moins1, ip, ipmoins1, e, p, pc1, pc2, sbox)
    print(f"Cle 56 bits = {hex(k56)}")

    print("\n Calcul de la cle 64 bits avec bits de parite")
    k64 = getK64bitParite(claire, chiffrer, k16, pc2moins1, pc1moins1, ip, ipmoins1, e, p, pc1, pc2, sbox)
    print(f"Cle globale 64 bits avec parite = {hex(k64)}")

if __name__ == "__main__":
    main()
