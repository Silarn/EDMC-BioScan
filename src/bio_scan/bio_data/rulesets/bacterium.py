from typing import Mapping

catalog: dict[str, dict[str, Mapping]] = {
    '$Codex_Ent_Bacterial_Genus_Name;': {
        '$Codex_Ent_Bacterial_01_Name;': {
            'name': 'Bacterium Aurasus',
            'value': 1000000,
            'rulesets': [
                {
                    'min_gravity': 0.039,
                    'max_gravity': 0.605,
                    'max_temperature': 400.0,
                    'min_temperature': 145.0,
                    'atmosphere': ['CarbonDioxide', 'CarbonDioxideRich'],
                    'body_type': ['Rocky body', 'High metal content body']
                }
            ],
        },
        '$Codex_Ent_Bacterial_02_Name;': {
            'name': 'Bacterium Nebulus',
            'value': 5289900,
            'rulesets': [
                {
                    'min_gravity': 0.4,
                    'max_gravity': 0.55,
                    'max_temperature': 21.0,
                    'min_temperature': 20.0,
                    'atmosphere': ['Helium'],
                    'body_type': ['Icy body']
                }
            ],
        },
        '$Codex_Ent_Bacterial_03_Name;': {
            'name': 'Bacterium Scopulum',
            'value': 4934500,
            'rulesets': [
                {
                    'min_gravity': 0.025,
                    'max_gravity': 0.6,
                    'atmosphere': ['Argon', 'Neon', 'NeonRich', 'Methane', 'Helium'],
                    'body_type': ['Icy body', 'Rocky ice body'],
                    'volcanism': ['carbon dioxide', 'methane']
                }
            ],
        },
        '$Codex_Ent_Bacterial_04_Name;': {
            'name': 'Bacterium Acies',
            'value': 1000000,
            'rulesets': [
                {
                    'min_gravity': 0.265,
                    'max_gravity': 0.731,
                    'max_temperature': 139.0,
                    'min_temperature': 20.0,
                    'atmosphere': ['Neon', 'NeonRich'],
                    'body_type': ['Icy body', 'Rocky ice body']
                }
            ],
        },
        '$Codex_Ent_Bacterial_05_Name;': {
            'name': 'Bacterium Vesicula',
            'value': 1000000,
            'rulesets': [
                {
                    'min_gravity': 0.025,
                    'max_gravity': 0.515,
                    'max_temperature': 234.0,
                    'min_temperature': 50.0,
                    'atmosphere': ['Argon', 'ArgonRich']
                }
            ],
        },
        '$Codex_Ent_Bacterial_06_Name;': {
            'name': 'Bacterium Alcyoneum',
            'value': 1658500,
            'rulesets': [
                {
                    'min_gravity': 0.039,
                    'max_gravity': 0.3715,
                    'max_temperature': 177.0,
                    'min_temperature': 152.0,
                    'atmosphere': ['Ammonia'],
                    'body_type': ['Rocky body', 'Rocky ice body', 'High metal content body']
                }
            ],
        },
        '$Codex_Ent_Bacterial_07_Name;': {
            'name': 'Bacterium Tela',
            'value': 1949000,
            'rulesets': [
                {
                    'min_gravity': 0.025,
                    'max_gravity': 0.61,
                    'min_temperature': 300.0,
                    'atmosphere': ['SulphurDioxide', 'CarbonDioxide', 'Water'],
                    'volcanism': 'None'
                },
                {
                    'min_gravity': 0.025,
                    'max_gravity': 0.61,
                    'atmosphere': 'Any',
                    'volcanism': 'Any'
                }
            ],
        },
        '$Codex_Ent_Bacterial_08_Name;': {
            'name': 'Bacterium Informem',
            'value': 8418000,
            'rulesets': [
                {
                    'min_gravity': 0.125,
                    'max_gravity': 0.6,
                    'max_temperature': 149.0,
                    'min_temperature': 43.0,
                    'atmosphere': ['Nitrogen']
                }
            ],
        },
        '$Codex_Ent_Bacterial_09_Name;': {
            'name': 'Bacterium Volu',
            'value': 7774700,
            'rulesets': [
                {
                    'min_gravity': 0.24,
                    'max_gravity': 0.515,
                    'max_temperature': 245.0,
                    'min_temperature': 145.0,
                    'atmosphere': ['Oxygen'],
                }
            ],
        },
        '$Codex_Ent_Bacterial_10_Name;': {
            'name': 'Bacterium Bullaris',
            'value': 1152500,
            'rulesets': [
                {
                    'min_gravity': 0.025,
                    'max_gravity': 0.6,
                    'max_temperature': 135.0,
                    'min_temperature': 68.0,
                    'atmosphere': ['Methane', 'MethaneRich']
                }
            ],
        },
        '$Codex_Ent_Bacterial_11_Name;': {
            'name': 'Bacterium Omentum',
            'value': 4638900,
            'rulesets': [
                {
                    'min_gravity': 0.025,
                    'max_gravity': 0.6,
                    'atmosphere': ['Argon', 'ArgonRich', 'Neon', 'NeonRich', 'Methane', 'MethaneRich', 'Helium', 'WaterRich'],
                    'body_type': ['Icy body'],
                    'volcanism': ['nitrogen', 'ammonia']
                }
            ],
        },
        '$Codex_Ent_Bacterial_12_Name;': {
            'name': 'Bacterium Cerbrus',
            'value': 1689800,
            'rulesets': [
                {
                    'min_gravity': 0.039,
                    'max_gravity': 0.6,
                    'max_temperature': 499.0,
                    'min_temperature': 132.0,
                    'atmosphere': ['SulphurDioxide'],
                    'body_type': ['Rocky body', 'Rocky ice body', 'High metal content body']
                },
                {
                    'min_gravity': 0.039,
                    'max_gravity': 0.6,
                    'max_temperature': 452.0,
                    'min_temperature': 392.0,
                    'atmosphere': ['Water'],
                    'body_type': ['Rocky body', 'Rocky ice body', 'High metal content body']
                }
            ],
        },
        '$Codex_Ent_Bacterial_13_Name;': {
            'name': 'Bacterium Verrata',
            'value': 3897000,
            'rulesets': [
                {
                    'min_gravity': 0.04,
                    'max_gravity': 0.61,
                    'atmosphere': ['Neon', 'NeonRich', 'Argon', 'ArgonRich', 'Ammonia', 'Helium'],
                    'volcanism': ['water'],
                    'body_type': ['Rocky body', 'Rocky ice body', 'Icy body']
                }
            ]
        }
    }
}
