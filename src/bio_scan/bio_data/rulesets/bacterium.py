from typing import Mapping

catalog: dict[str, dict[str, Mapping]] = {
    '$Codex_Ent_Bacterial_Genus_Name;': {
        '$Codex_Ent_Bacterial_01_Name;': {
            'name': 'Bacterium Aurasus',
            'value': 1000000,
            'rulesets': [
                {
                    'min_gravity': 0.039,
                    'max_gravity': 0.608,
                    'max_temperature': 400.0,
                    'min_temperature': 145.0,
                    'atmosphere': ['CarbonDioxide'],
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
                    'min_temperature': 20.0,
                    'max_temperature': 21.0,
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
                    'max_gravity': 0.61,
                    'min_temperature': 20,
                    'max_temperature': 65,
                    'atmosphere': ['Neon', 'NeonRich'],
                    'body_type': ['Icy body', 'Rocky ice body'],
                    'volcanism': ['carbon dioxide', 'methane']
                },
                {
                    'min_gravity': 0.15,
                    'max_gravity': 0.26,
                    'min_temperature': 56,
                    'max_temperature': 150,
                    'atmosphere': ['Argon'],
                    'body_type': ['Icy body', 'Rocky ice body'],
                    'volcanism': ['carbon dioxide', 'methane']
                },
                {
                    'min_gravity': 0.025,
                    'max_gravity': 0.047,
                    'min_temperature': 84,
                    'max_temperature': 110,
                    'atmosphere': ['Methane'],
                    'body_type': ['Icy body'],
                    'volcanism': ['methane']
                },
                {
                    'min_gravity': 0.48,
                    'max_gravity': 0.51,
                    'min_temperature': 20,
                    'max_temperature': 21,
                    'atmosphere': ['Helium'],
                    'body_type': ['Icy body'],
                    'volcanism': ['methane']
                },
                {
                    'min_gravity': 0.27,
                    'max_gravity': 0.32,
                    'min_temperature': 150,
                    'max_temperature': 220,
                    'atmosphere': ['Oxygen'],
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
                    'min_gravity': 0.26,
                    'max_gravity': 0.61,
                    'min_temperature': 20.0,
                    'max_temperature': 61.0,
                    'atmosphere': ['Neon'],
                    'body_type': ['Icy body', 'Rocky ice body']
                }
            ],
        },
        '$Codex_Ent_Bacterial_05_Name;': {
            'name': 'Bacterium Vesicula',
            'value': 1000000,
            'rulesets': [
                {
                    'min_gravity': 0.027,
                    'max_gravity': 0.51,
                    'min_temperature': 50.0,
                    'max_temperature': 243.0,
                    'atmosphere': ['Argon'],
                    'body_type': ['Icy body', 'Rocky ice body']
                }
            ],
        },
        '$Codex_Ent_Bacterial_06_Name;': {
            'name': 'Bacterium Alcyoneum',
            'value': 1658500,
            'rulesets': [
                {
                    'min_gravity': 0.04,
                    'max_gravity': 0.376,
                    'min_temperature': 152.0,
                    'max_temperature': 177.0,
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
                    'min_gravity': 0.45,
                    'max_gravity': 0.61,
                    'min_temperature': 300.0,
                    'max_temperature': 500.0,
                    'atmosphere': ['CarbonDioxide'],
                    'volcanism': 'None'
                },
                {
                    'min_gravity': 0.26,
                    'max_gravity': 0.57,
                    'min_temperature': 167.0,
                    'max_temperature': 300.0,
                    'atmosphere': ['CarbonDioxide', 'CarbonDioxideRich'],
                    'volcanism': 'Any'
                },
                {
                    'min_gravity': 0.18,
                    'max_gravity': 0.61,
                    'min_temperature': 148.0,
                    'max_temperature': 500.0,
                    'atmosphere': ['SulphurDioxide']
                },
                {  # Hot thin sulphur dioxide
                    'min_gravity': 0.53,
                    'max_gravity': 0.57,
                    'min_temperature': 500.0
                },
                {
                    'min_gravity': 0.04,
                    'max_gravity': 0.063,
                    'min_temperature': 395.0,
                    'max_temperature': 451.0,
                    'atmosphere': ['Water'],
                    'volcanism': 'None',
                    'body_type': ['Rocky body', 'High metal content body']
                },
                {
                    'min_gravity': 0.32,
                    'max_gravity': 0.44,
                    'min_temperature': 240.0,
                    'max_temperature': 330.0,
                    'atmosphere': ['WaterRich'],
                    'volcanism': 'Any',
                    'body_type': ['Icy body', 'Rocky ice body']
                },
                {
                    'min_gravity': 0.025,
                    'max_gravity': 0.61,
                    'min_temperature': 20.0,
                    'max_temperature': 21.0,
                    'atmosphere': ['Helium'],
                    'volcanism': 'Any',
                    'body_type': ['Icy body', 'Rocky ice body']
                },
                {
                    'min_gravity': 0.27,
                    'max_gravity': 0.61,
                    'min_temperature': 20.0,
                    'max_temperature': 95.0,
                    'atmosphere': ['Neon', 'NeonRich'],
                    'volcanism': 'Any',
                    'body_type': ['Icy body', 'Rocky ice body']
                },
                {
                    'min_gravity': 0.27,
                    'max_gravity': 0.61,
                    'min_temperature': 20.0,
                    'max_temperature': 95.0,
                    'atmosphere': ['NeonRich'],
                    'volcanism': 'Any',
                    'body_type': ['Icy body', 'Rocky ice body']
                },
                {
                    'min_gravity': 0.025,
                    'max_gravity': 0.23,
                    'min_temperature': 165.0,
                    'max_temperature': 177.0,
                    'atmosphere': ['Ammonia'],
                    'volcanism': 'Any',
                },
                {
                    'min_gravity': 0.045,
                    'max_gravity': 0.28,
                    'min_temperature': 50.0,
                    'max_temperature': 150.0,
                    'atmosphere': ['Argon'],
                    'volcanism': 'Any',
                    'body_type': ['Icy body', 'Rocky ice body']
                },
                {
                    'min_gravity': 0.24,
                    'max_gravity': 0.45,
                    'min_temperature': 50.0,
                    'max_temperature': 150.0,
                    'atmosphere': ['ArgonRich'],
                    'volcanism': 'Any'
                },
                {
                    'min_gravity': 0.21,
                    'max_gravity': 0.35,
                    'min_temperature': 55.0,
                    'max_temperature': 80.0,
                    'atmosphere': ['Nitrogen'],
                    'volcanism': 'Any'
                }
            ],
        },
        '$Codex_Ent_Bacterial_08_Name;': {
            'name': 'Bacterium Informem',
            'value': 8418000,
            'rulesets': [
                {
                    'min_gravity': 0.05,
                    'max_gravity': 0.6,
                    'min_temperature': 43.0,
                    'max_temperature': 150.0,
                    'atmosphere': ['Nitrogen'],
                    'volcanism': 'None'
                }
            ],
        },
        '$Codex_Ent_Bacterial_09_Name;': {
            'name': 'Bacterium Volu',
            'value': 7774700,
            'rulesets': [
                {
                    'min_gravity': 0.239,
                    'max_gravity': 0.61,
                    'min_temperature': 143.5,
                    'max_temperature': 246.0,
                    'atmosphere': ['Oxygen'],
                    'volcanism': 'None'
                },
                {
                    'min_gravity': 0.239,
                    'max_gravity': 0.61,
                    'min_temperature': 143.5,
                    'max_temperature': 246.0,
                    'atmosphere': ['Oxygen'],
                    'volcanism': ['water']
                }
            ],
        },
        '$Codex_Ent_Bacterial_10_Name;': {
            'name': 'Bacterium Bullaris',
            'value': 1152500,
            'rulesets': [
                {
                    'min_gravity': 0.0245,
                    'max_gravity': 0.35,
                    'min_temperature': 68.0,
                    'max_temperature': 109.0,
                    'atmosphere': ['Methane']
                },
                {
                    'min_gravity': 0.44,
                    'max_gravity': 0.6,
                    'min_temperature': 74.0,
                    'max_temperature': 141.0,
                    'atmosphere': ['MethaneRich'],
                    'volcanism': 'None',
                    'body_type': ['Rocky body', 'High metal content body']
                }
            ],
        },
        '$Codex_Ent_Bacterial_11_Name;': {
            'name': 'Bacterium Omentum',
            'value': 4638900,
            'rulesets': [
                {
                    'min_gravity': 0.045,
                    'max_gravity': 0.45,
                    'min_temperature': 50.0,
                    'atmosphere': ['Argon'],
                    'body_type': ['Icy body'],
                    'volcanism': ['nitrogen', 'ammonia']
                },
                {
                    'min_gravity': 0.22,
                    'max_gravity': 0.30,
                    'min_temperature': 80.0,
                    'max_temperature': 90.0,
                    'atmosphere': ['ArgonRich'],
                    'body_type': ['Icy body'],
                    'volcanism': ['nitrogen', 'ammonia']
                },
                {
                    'min_gravity': 0.49,
                    'max_gravity': 0.51,
                    'min_temperature': 20.0,
                    'max_temperature': 21.0,
                    'atmosphere': ['Helium'],
                    'body_type': ['Icy body'],
                    'volcanism': ['nitrogen', 'ammonia']
                },
                {
                    'min_gravity': 0.027,
                    'max_gravity': 0.0455,
                    'min_temperature': 84.0,
                    'max_temperature': 108.0,
                    'atmosphere': ['Methane'],
                    'body_type': ['Icy body'],
                    'volcanism': ['nitrogen', 'ammonia']
                },
                {
                    'min_gravity': 0.31,
                    'max_gravity': 0.57,
                    'min_temperature': 20.0,
                    'max_temperature': 61.0,
                    'atmosphere': ['Neon'],
                    'body_type': ['Icy body'],
                    'volcanism': ['nitrogen', 'ammonia']
                },
                {
                    'min_gravity': 0.27,
                    'max_gravity': 0.61,
                    'min_temperature': 20.0,
                    'max_temperature': 93.0,
                    'atmosphere': ['NeonRich'],
                    'body_type': ['Icy body'],
                    'volcanism': ['nitrogen', 'ammonia']
                },
                {
                    'min_gravity': 0.38,
                    'max_gravity': 0.45,
                    'min_temperature': 190.0,
                    'max_temperature': 310.0,
                    'atmosphere': ['WaterRich'],
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
                    'min_gravity': 0.042,
                    'max_gravity': 0.605,
                    'min_temperature': 132.0,
                    'max_temperature': 500.0,
                    'atmosphere': ['SulphurDioxide'],
                    'body_type': ['Rocky body', 'Rocky ice body', 'High metal content body']
                },
                {
                    'min_gravity': 0.04,
                    'max_gravity': 0.064,
                    'min_temperature': 392.0,
                    'max_temperature': 452.0,
                    'atmosphere': ['Water'],
                    'volcanism': 'None',
                    'body_type': ['Rocky body', 'High metal content body']
                },
                {
                    'min_gravity': 0.04,
                    'max_gravity': 0.064,
                    'min_temperature': 392.0,
                    'max_temperature': 452.0,
                    'atmosphere': ['Water'],
                    'volcanism': ['water'],
                    'body_type': ['Rocky body', 'High metal content body']
                },
                {
                    'min_gravity': 0.4,
                    'max_gravity': 0.5,
                    'min_temperature': 240.0,
                    'max_temperature': 320.0,
                    'atmosphere': ['WaterRich'],
                    'volcanism': 'None',
                    'body_type': ['Rocky ice body']
                }
            ],
        },
        '$Codex_Ent_Bacterial_13_Name;': {
            'name': 'Bacterium Verrata',
            'value': 3897000,
            'rulesets': [
                {
                    'min_gravity': 0.03,
                    'max_gravity': 0.09,
                    'min_temperature': 160.0,
                    'max_temperature': 180.0,
                    'atmosphere': ['Ammonia'],
                    'volcanism': ['water'],
                    'body_type': ['Rocky body', 'Rocky ice body', 'Icy body']
                },
                {
                    'min_gravity': 0.17,
                    'max_gravity': 0.33,
                    'min_temperature': 60.0,
                    'max_temperature': 150.0,
                    'atmosphere': ['Argon'],
                    'volcanism': ['water'],
                    'body_type': ['Rocky ice body', 'Icy body']
                },
                {
                    'min_gravity': 0.04,
                    'max_gravity': 0.08,
                    'min_temperature': 80.0,
                    'max_temperature': 90.0,
                    'atmosphere': ['ArgonRich'],
                    'volcanism': ['water'],
                    'body_type': ['Icy body']
                },
                {
                    'min_gravity': 0.25,
                    'max_gravity': 0.32,
                    'min_temperature': 167.0,
                    'max_temperature': 240.0,
                    'atmosphere': ['CarbonDioxide', 'CarbonDioxideRich'],
                    'volcanism': ['water'],
                    'body_type': ['Rocky ice body', 'Icy body']
                },
                {
                    'min_gravity': 0.49,
                    'max_gravity': 0.53,
                    'min_temperature': 20.0,
                    'max_temperature': 21.0,
                    'atmosphere': ['Helium'],
                    'volcanism': ['water'],
                    'body_type': ['Icy body']
                },
                {
                    'min_gravity': 0.29,
                    'max_gravity': 0.61,
                    'min_temperature': 20.0,
                    'max_temperature': 51.0,
                    'atmosphere': ['Neon'],
                    'volcanism': ['water'],
                    'body_type': ['Rocky ice body', 'Icy body']
                },
                {
                    'min_gravity': 0.43,
                    'max_gravity': 0.61,
                    'min_temperature': 20.0,
                    'max_temperature': 65.0,
                    'atmosphere': ['NeonRich'],
                    'volcanism': ['water'],
                    'body_type': ['Rocky ice body', 'Icy body']
                },
                {
                    'min_gravity': 0.21,
                    'max_gravity': 0.24,
                    'min_temperature': 60.0,
                    'max_temperature': 80.0,
                    'atmosphere': ['Nitrogen'],
                    'volcanism': ['water'],
                    'body_type': ['Icy body']
                },
                {
                    'min_gravity': 0.24,
                    'max_gravity': 0.35,
                    'min_temperature': 154.0,
                    'max_temperature': 220.0,
                    'atmosphere': ['Oxygen'],
                    'volcanism': ['water'],
                    'body_type': ['Rocky ice body', 'Icy body']
                },
                {
                    'min_gravity': 0.04,
                    'max_gravity': 0.054,
                    'min_temperature': 400.0,
                    'max_temperature': 450.0,
                    'atmosphere': ['Water'],
                    'volcanism': ['water'],
                    'body_type': ['Rocky body']
                }
            ]
        }
    }
}
