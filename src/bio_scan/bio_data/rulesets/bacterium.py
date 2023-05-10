from typing import Mapping

catalog: dict[str, dict[str, Mapping]] = {
    '$Codex_Ent_Bacterial_Genus_Name;': {
        '$Codex_Ent_Bacterial_01_Name;': {
            'name': 'Bacterium Aurasus',
            'value': 1000000,
            'rulesets': [
                {
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
                    'atmosphere': ['Argon', 'ArgonRich', 'Neon', 'NeonRich', 'Methane', 'MethaneRich', 'Nitrogen'],
                    'body_type': ['Icy body'],
                    'volcanism': ['carbon dioxide', 'methane']
                }
            ],
        },
        '$Codex_Ent_Bacterial_04_Name;': {
            'name': 'Bacterium Acies',
            'value': 1000000,
            'rulesets': [
                {
                    'atmosphere': ['Neon', 'NeonRich'],
                    'body_type': ['Icy body', 'Rocky body']
                }
            ],
        },
        '$Codex_Ent_Bacterial_05_Name;': {
            'name': 'Bacterium Vesicula',
            'value': 1000000,
            'rulesets': [
                {
                    'atmosphere': ['Argon', 'ArgonRich'],
                    'body_type': ['Icy body', 'Rocky body', 'Rocky ice body']
                }
            ],
        },
        '$Codex_Ent_Bacterial_06_Name;': {
            'name': 'Bacterium Alcyoneum',
            'value': 1658500,
            'rulesets': [
                {
                    'atmosphere': ['Ammonia'],
                    'body_type': ['Rocky body', 'High metal content body']
                }
            ],
        },
        '$Codex_Ent_Bacterial_07_Name;': {
            'name': 'Bacterium Tela',
            'value': 1949000,
            'rulesets': [
                {
                    'atmosphere': ['Water', 'WaterRich'],
                    'body_type': ['Rocky body', 'High metal content body']
                },
                {
                    'atmosphere': 'Any',
                    'body_type': ['Rocky body', 'High metal content body'],
                    'volcanism': ['helium', 'iron', 'silicate', 'ammonia']
                }
            ],
        },
        '$Codex_Ent_Bacterial_08_Name;': {
            'name': 'Bacterium Informem',
            'value': 8418000,
            'rulesets': [
                {
                    'atmosphere': ['Nitrogen']
                }
            ],
        },
        '$Codex_Ent_Bacterial_09_Name;': {
            'name': 'Bacterium Volu',
            'value': 7774700,
            'rulesets': [
                {
                    'atmosphere': ['Oxygen'],
                    'body_type': ['Rocky body', 'Rocky ice body', 'High metal content body']
                }
            ],
        },
        '$Codex_Ent_Bacterial_10_Name;': {
            'name': 'Bacterium Bullaris',
            'value': 1152500,
            'rulesets': [
                {
                    'atmosphere': ['Methane', 'MethaneRich'],
                    'body_type': ['Icy body', 'Rocky body', 'High metal content body']
                }
            ],
        },
        '$Codex_Ent_Bacterial_11_Name;': {
            'name': 'Bacterium Omentum',
            'value': 4638900,
            'rulesets': [
                {
                    'atmosphere': ['Argon', 'ArgonRich', 'Neon', 'NeonRich', 'Methane', 'MethaneRich'],
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
                    'atmosphere': ['Water', 'WaterRich', 'SulphurDioxide'],
                    'body_type': ['Rocky body', 'Rocky ice body', 'High metal content body']
                }
            ],
        },
        '$Codex_Ent_Bacterial_13_Name;': {
            'name': 'Bacterium Verrata',
            'value': 3897000,
            'atmosphere': 'Any',
            'volcanism': ['water']
        }
    }
}
