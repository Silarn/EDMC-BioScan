region_map: dict[str, list[int]] = {
    'orion-cygnus': [1, 4, 7, 8, 16, 17, 18, 35],
    'orion-cygnus-1': [4, 7, 8, 16, 17, 18, 35],
    'orion-cygnus-core': [7, 8, 16, 17, 18, 35],
    'sagittarius-carina': [1, 4, 9, 18, 19, 20, 21, 22, 23, 40],
    'sagittarius-carina-core': [9, 18, 19, 20, 21, 22, 23, 40],
    'sagittarius-carina-core-9': [18, 19, 20, 21, 22, 23, 40],
    'scutum-centaurus': [1, 4, 9, 10, 11, 12, 24, 25, 26, 42, 28],
    'scutum-centaurus-core': [9, 10, 11, 12, 24, 25, 26, 42, 28],
    'outer': [1, 2, 5, 6, 13, 14, 27, 29, 31, 41, 37],
    'perseus': [1, 3, 7, 15, 30, 32, 33, 34, 36, 38, 39],
    'perseus-core': [3, 7, 15, 30, 32, 33, 34, 36, 38, 39],
    'exterior': [14, 21, 22, 23, 24, 25, 26, 27, 28, 29, 31, 34, 36,
                 37, 38, 39, 40, 41, 42],
    'anemone-a': [7, 8, 13, 14, 15, 16, 17, 18, 27, 32],
    'amphora': [10, 19, 20, 21, 22],
    'tuber-a': [1, 2, 3, 4, 5, 9, 10, 11],
    'tuber-b': [3, 4, 6, 7, 8, 9, 10, 18, 19],
    'brain-tree': [2, 9, 10, 17, 18, 35],
    'empyrean-straits': [2],
    'center': [1, 2, 3]
}

guardian_nebulae: dict[str, tuple[int, tuple[float, float, float]]] = {
    'Hen 2-333': (750, (-840.65625, -561.15625, 13361.8125)),
    'Gamma Velorum': (750, (1099.21875, -146.6875, -133.59375)),
    'Skaudai AA-A h71': (100, (-5493.09375, -589.28125, 10424.4375)),
    'Blaa Hypai AA-A h68': (100,  (1220.40625, -694.625, 12312.8125)),
    'Eorl Auwsy AA-A h72': (100, (4949.9375, 164, 20640.125)),
    'Prai Hypoo AA-A h60': (100, (-9294.875, -458.40625, 7905.71875)),
    'Eta Carina Nebula': (100, (8579.96875, -138.96875, 2701.375)),
    'NGC 3199': (100, (14574.15625, -259.625, 3511.90625))
}

tuber_zones: dict[str, tuple[int, tuple[float, float, float]]] = {
    'Arcadian Stream': (600, (8897.265, -114.9375, 20520.8)),  # EFGH
    'Galactic Center': (1000, (46, 487, 25916)),  # ABCD
    'Inner Orion Spur': (600, (-3485, 39, 7320)),  # EFGH
    'Inner O-P Conflux': (750, (-13245.7, -85.766, 30306.5)),  # EFGH
    'Inner S-C Arm A': (600, (-1644.44, -39.375, 10697.1)),  # EFGH
    'Inner S-C Arm B': (600, (-6601.435, -78.375, 12551.15)),  # EFGH
    'Inner S-C Arm C': (600, (-9354.53, -38.7345, 17174.1)),  # EFGH
    'Inner S-C Arm D': (250, (-11987.4, 228.1874, 22648.7)),  # ABCD
    'Izanami': (750, (-4595, 420, 37210)),  # EFGH
    'Hawking A': (600, (5792.315, 155.0935, 6313.19)),  # EFGH
    'Hawking B': (600, (9987.79, -114.45325, 8212.201875)),  # EFGH
    'Norma Arm': (1000, (3722.6, 200, 16441)),  # ALL
    'Norma Expanse A': (600, (4250, -92, 12015)),  # EFGH
    'Norma Expanse B': (250, (5573.36, 33.875, 11754.9)),  # ABCD
    'Odin A': (1000, (-7950, 225, 28010)),  # ABCD
    'Odin B': (600, (-5309.345, -114.7345, 18655.5)),  # EFGH
    'Ryker A': (750, (1750, 750, 34100)),  # EFGH
    'Ryker B': (1500, (-1430, 360, 30456)),  # ABCD
    'Trojan Belt': (500, (18615, 55, 31730)),  # ABCD
}
