from typing import Mapping

catalog: dict[str, dict[str, Mapping]] = {
    '$Codex_Ent_Tube_Name;': {
        '$Codex_Ent_Tube_Name;': {
            'name': 'Roseum Sinuous Tubers',
            'value': 1514500,
            'rulesets': [
                {
                    'body_type': ['High metal content body'],
                    'min_temperature': 200.0,
                    'max_temperature': 500.0,
                    'volcanism': ['rocky magma'],
                    'tuber': ['Galactic Center', 'Odin A', 'Ryker B']
                }
            ],
        },
        '$Codex_Ent_TubeABCD_01_Name;': {
            'name': 'Prasinum Sinuous Tubers',
            'value': 1514500,
            'rulesets': [
                {
                    'body_type': ['Metal rich body', 'High metal content body', 'Rocky body'],
                    'min_temperature': 200.0,
                    'max_temperature': 500.0,
                    'volcanism': 'Any',
                    'tuber': ['Inner S-C Arm B 1']
                },
                {
                    'body_type': ['Metal rich body', 'High metal content body'],
                    'min_temperature': 200.0,
                    'max_temperature': 500.0,
                    'volcanism': ['major rocky magma', 'major silicate vapour'],
                    'tuber': ['Inner S-C Arm D', 'Norma Expanse B', 'Odin B']
                },
                {
                    'body_type': ['Metal rich body', 'High metal content body'],
                    'min_temperature': 200.0,
                    'max_temperature': 500.0,
                    'volcanism': ['major rocky magma', 'major silicate vapour'],
                    'regions': ['empyrean-straits']
                }
            ],
        },
        '$Codex_Ent_TubeABCD_02_Name;': {  # High % sulphur requirement?
            'name': 'Albidum Sinuous Tubers',
            'value': 1514500,
            'rulesets': [
                {
                    'body_type': ['Rocky body'],
                    'min_temperature': 200.0,
                    'max_temperature': 500.0,
                    'max_orbital_period': 86400,
                    'volcanism': ['major silicate vapour', 'major metallic magma'],
                    'tuber': ['Inner S-C Arm B 2', 'Inner S-C Arm D', 'Trojan Belt']
                }
            ],
        },
        '$Codex_Ent_TubeABCD_03_Name;': {
            'name': 'Caeruleum Sinuous Tubers',
            'value': 1514500,
            'rulesets': [
                {
                    'body_type': ['Rocky body'],
                    'min_temperature': 200.0,
                    'max_temperature': 500.0,
                    'max_orbital_period': 86400,
                    'volcanism': ['major silicate vapour'],
                    'tuber': ['Galactic Center', 'Inner S-C Arm D', 'Norma Arm A']
                },
                {
                    'body_type': ['Rocky body'],
                    'min_temperature': 200.0,
                    'max_temperature': 500.0,
                    'volcanism': ['major silicate vapour'],
                    'regions': ['empyrean-straits']
                }
            ],
        },
        '$Codex_Ent_TubeEFGH_01_Name;': {
            'name': 'Lindigoticum Sinuous Tubers',
            'value': 1514500,
            'rulesets': [
                {
                    'body_type': ['Rocky body'],
                    'min_temperature': 200.0,
                    'max_temperature': 500.0,
                    'max_orbital_period': 86400,
                    'volcanism': ['major silicate vapour'],
                    'tuber': ['Inner S-C Arm A', 'Inner S-C Arm C', 'Hawking B', 'Norma Expanse A', 'Odin B']
                }
            ],
        },
        '$Codex_Ent_TubeEFGH_02_Name;': {
            'name': 'Violaceum Sinuous Tubers',
            'value': 1514500,
            'rulesets': [
                {
                    'body_type': ['Metal rich body', 'High metal content body'],
                    'min_temperature': 200.0,
                    'max_temperature': 500.0,
                    'volcanism': ['major rocky magma', 'major silicate vapour'],
                    'tuber': ['Arcadian Stream', 'Empyrean Straits', 'Norma Arm B']
                }
            ],
        },
        '$Codex_Ent_TubeEFGH_03_Name;': {
            'name': 'Viride Sinuous Tubers',
            'value': 1514500,
            'rulesets': [
                {
                    'body_type': ['High metal content body'],
                    'min_temperature': 200.0,
                    'max_temperature': 500.0,
                    'volcanism': ['major rocky magma', 'major silicate vapour'],
                    'tuber': ['Inner O-P Conflux', 'Izanami', 'Ryker A']
                },
                {
                    'body_type': ['Rocky body'],
                    'min_temperature': 200.0,
                    'max_temperature': 500.0,
                    'max_orbital_period': 86400,
                    'volcanism': ['major rocky magma', 'major silicate vapour'],
                    'tuber': ['Inner O-P Conflux', 'Izanami', 'Ryker A']
                }
            ],
        },
        '$Codex_Ent_TubeEFGH_Name;': {
            'name': 'Blatteum Sinuous Tubers',
            'value': 1514500,
            'rulesets': [
                {
                    'body_type': ['Metal rich body', 'High metal content body'],
                    'min_temperature': 200.0,
                    'max_temperature': 500.0,
                    'volcanism': ['=metallic magma volcanism', '=rocky magma volcanism', 'major silicate vapour'],
                    'tuber': ['Arcadian Stream', 'Inner Orion Spur', 'Inner S-C Arm B 2', 'Hawking A']
                }
            ],
        },
    },
}
