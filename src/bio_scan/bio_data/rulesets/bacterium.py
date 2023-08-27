from typing import Mapping

catalog: dict[str, dict[str, Mapping]] = {
    '$Codex_Ent_Bacterial_Genus_Name;': {
        '$Codex_Ent_Bacterial_01_Name;': {
            'name': 'Bacterium Aurasus',
            'value': 1000000,
            'rulesets': [
                {
                    'atmosphere': ['CarbonDioxide'],
                    'body_type': ['Rocky body', 'High metal content body'],
                    'min_gravity': 0.039,
                    'max_gravity': 0.608,
                    'min_temperature': 145.0,
                    'max_temperature': 400.0,
                }
            ],
        },
        '$Codex_Ent_Bacterial_02_Name;': {
            'name': 'Bacterium Nebulus',
            'value': 5289900,
            'rulesets': [
                {
                    'atmosphere': ['Helium'],
                    'body_type': ['Icy body'],
                    'min_gravity': 0.4,
                    'max_gravity': 0.55,
                    'min_temperature': 20.0,
                    'max_temperature': 21.0,
                    'min_pressure': 0.067
                }
            ],
        },
        '$Codex_Ent_Bacterial_03_Name;': {
            'name': 'Bacterium Scopulum',
            'value': 4934500,
            'rulesets': [
                {
                    'atmosphere': ['Argon'],
                    'body_type': ['Icy body', 'Rocky ice body'],
                    'min_gravity': 0.15,
                    'max_gravity': 0.26,
                    'min_temperature': 56,
                    'max_temperature': 150,
                    'volcanism': ['carbon dioxide', 'methane']
                },
                {
                    'atmosphere': ['Helium'],
                    'body_type': ['Icy body'],
                    'min_gravity': 0.48,
                    'max_gravity': 0.51,
                    'min_temperature': 20,
                    'max_temperature': 21,
                    'min_pressure': 0.075,
                    'volcanism': ['methane']
                },
                {
                    'atmosphere': ['Methane'],
                    'body_type': ['Icy body'],
                    'min_gravity': 0.025,
                    'max_gravity': 0.047,
                    'min_temperature': 84,
                    'max_temperature': 110,
                    'min_pressure': 0.03,
                    'volcanism': ['methane']
                },
                {
                    'atmosphere': ['Neon'],
                    'body_type': ['Icy body', 'Rocky ice body'],
                    'min_gravity': 0.025,
                    'max_gravity': 0.61,
                    'min_temperature': 20,
                    'max_temperature': 65,
                    'max_pressure': 0.008,
                    'volcanism': ['carbon dioxide', 'methane']
                },
                {
                    'atmosphere': ['NeonRich'],
                    'body_type': ['Icy body', 'Rocky ice body'],
                    'min_gravity': 0.025,
                    'max_gravity': 0.61,
                    'min_temperature': 20,
                    'max_temperature': 65,
                    'min_pressure': 0.005,
                    'volcanism': ['carbon dioxide', 'methane']
                },
                {
                    'atmosphere': ['Nitrogen'],
                    'body_type': ['Icy body', 'Rocky ice body'],
                    'min_gravity': 0.2,
                    'max_gravity': 0.3,
                    'min_temperature': 60,
                    'max_temperature': 70,
                    'volcanism': ['carbon dioxide', 'methane']
                },
                {
                    'atmosphere': ['Oxygen'],
                    'body_type': ['Icy body'],
                    'min_gravity': 0.27,
                    'max_gravity': 0.32,
                    'min_temperature': 150,
                    'max_temperature': 220,
                    'min_pressure': 0.01,
                    'volcanism': ['carbon dioxide', 'methane']
                }
            ],
        },
        '$Codex_Ent_Bacterial_04_Name;': {
            'name': 'Bacterium Acies',
            'value': 1000000,
            'rulesets': [
                {
                    'atmosphere': ['Neon'],
                    'body_type': ['Icy body', 'Rocky ice body'],
                    'min_gravity': 0.26,
                    'max_gravity': 0.61,
                    'min_temperature': 20.0,
                    'max_temperature': 61.0,
                    'max_pressure': 0.01
                }
            ],
        },
        '$Codex_Ent_Bacterial_05_Name;': {
            'name': 'Bacterium Vesicula',
            'value': 1000000,
            'rulesets': [
                {
                    'atmosphere': ['Argon'],
                    'min_gravity': 0.027,
                    'max_gravity': 0.51,
                    'min_temperature': 50.0,
                    'max_temperature': 243.0
                }
            ],
        },
        '$Codex_Ent_Bacterial_06_Name;': {
            'name': 'Bacterium Alcyoneum',
            'value': 1658500,
            'rulesets': [
                {
                    'atmosphere': ['Ammonia'],
                    'body_type': ['Rocky body', 'Rocky ice body', 'High metal content body'],
                    'min_gravity': 0.04,
                    'max_gravity': 0.376,
                    'min_temperature': 152.0,
                    'max_temperature': 177.0,
                    'max_pressure': 0.0135
                }
            ],
        },
        '$Codex_Ent_Bacterial_07_Name;': {
            'name': 'Bacterium Tela',
            'value': 1949000,
            'rulesets': [
                {
                    'atmosphere': ['Argon'],
                    'body_type': ['Icy body', 'Rocky ice body'],
                    'min_gravity': 0.045,
                    'max_gravity': 0.28,
                    'min_temperature': 50.0,
                    'max_temperature': 150.0,
                    'volcanism': 'Any'
                },
                {
                    'atmosphere': ['ArgonRich'],
                    'min_gravity': 0.24,
                    'max_gravity': 0.45,
                    'min_temperature': 50.0,
                    'max_temperature': 150.0,
                    'max_pressure': 0.05,
                    'volcanism': 'Any'
                },
                {
                    'atmosphere': ['Ammonia'],
                    'min_gravity': 0.025,
                    'max_gravity': 0.23,
                    'min_temperature': 165.0,
                    'max_temperature': 177.0,
                    'min_pressure': 0.0025,
                    'max_pressure': 0.02,
                    'volcanism': 'Any'
                },
                {
                    'atmosphere': ['CarbonDioxide'],
                    'min_gravity': 0.45,
                    'max_gravity': 0.61,
                    'min_temperature': 300.0,
                    'max_temperature': 500.0,
                    'min_pressure': 0.006,
                    'volcanism': 'None'
                },
                {
                    'atmosphere': ['CarbonDioxide', 'CarbonDioxideRich'],
                    'min_gravity': 0.26,
                    'max_gravity': 0.57,
                    'min_temperature': 167.0,
                    'max_temperature': 300.0,
                    'min_pressure': 0.006,
                    'volcanism': 'Any'
                },
                {
                    'atmosphere': ['Helium'],
                    'body_type': ['Icy body'],
                    'min_gravity': 0.025,
                    'max_gravity': 0.61,
                    'min_temperature': 20.0,
                    'max_temperature': 21.0,
                    'min_pressure': 0.067,
                    'volcanism': 'Any'
                },
                {
                    'atmosphere': ['Methane'],
                    'body_type': ['Icy body', 'Rocky body', 'High metal content body'],
                    'min_gravity': 0.026,
                    'max_gravity': 0.126,
                    'min_temperature': 80.0,
                    'max_temperature': 109.0,
                    'min_pressure': 0.012,
                    'volcanism': 'Any'
                },
                {
                    'atmosphere': ['Neon'],
                    'body_type': ['Icy body', 'Rocky ice body'],
                    'min_gravity': 0.27,
                    'max_gravity': 0.61,
                    'min_temperature': 20.0,
                    'max_temperature': 95.0,
                    'max_pressure': 0.008,
                    'volcanism': 'Any'
                },
                {
                    'atmosphere': ['NeonRich'],
                    'body_type': ['Icy body', 'Rocky ice body'],
                    'min_gravity': 0.27,
                    'max_gravity': 0.61,
                    'min_temperature': 20.0,
                    'max_temperature': 95.0,
                    'min_pressure': 0.003,
                    'volcanism': 'Any'
                },
                {
                    'atmosphere': ['Nitrogen'],
                    'min_gravity': 0.21,
                    'max_gravity': 0.35,
                    'min_temperature': 55.0,
                    'max_temperature': 80.0,
                    'volcanism': 'Any'
                },
                {
                    'atmosphere': ['Oxygen'],
                    'min_gravity': 0.23,
                    'max_gravity': 0.5,
                    'min_temperature': 150.0,
                    'max_temperature': 240.0,
                    'min_pressure': 0.01,
                    'volcanism': 'Any'
                },
                {
                    'atmosphere': ['SulphurDioxide'],
                    'min_gravity': 0.18,
                    'max_gravity': 0.61,
                    'min_temperature': 148.0,
                    'max_temperature': 500.0,
                    'volcanism': 'Any'
                },
                {
                    'atmosphere': ['SulphurDioxide'],
                    'min_gravity': 0.18,
                    'max_gravity': 0.61,
                    'min_temperature': 300.0,
                    'max_temperature': 500.0,
                    'volcanism': 'None'
                },
                {
                    'atmosphere': ['Water'],
                    'body_type': ['Rocky body', 'High metal content body'],
                    'min_gravity': 0.04,
                    'max_gravity': 0.063,
                    'volcanism': 'None'
                },
                {
                    'atmosphere': ['WaterRich'],
                    'body_type': ['Icy body', 'Rocky ice body'],
                    'min_gravity': 0.32,
                    'max_gravity': 0.44,
                    'min_temperature': 240.0,
                    'max_temperature': 330.0,
                    'min_pressure': 0.01,
                    'volcanism': 'Any'
                }
            ],
        },
        '$Codex_Ent_Bacterial_08_Name;': {
            'name': 'Bacterium Informem',
            'value': 8418000,
            'rulesets': [
                {
                    'atmosphere': ['Nitrogen'],
                    'min_gravity': 0.05,
                    'max_gravity': 0.6,
                    'min_temperature': 43.0,
                    'max_temperature': 150.0,
                    'volcanism': 'None'
                }
            ],
        },
        '$Codex_Ent_Bacterial_09_Name;': {
            'name': 'Bacterium Volu',
            'value': 7774700,
            'rulesets': [
                {
                    'atmosphere': ['Oxygen'],
                    'min_gravity': 0.239,
                    'max_gravity': 0.61,
                    'min_temperature': 143.5,
                    'max_temperature': 246.0,
                    'min_pressure': 0.013,
                    'volcanism': 'None'
                },
                {
                    'atmosphere': ['Oxygen'],
                    'min_gravity': 0.239,
                    'max_gravity': 0.61,
                    'min_temperature': 143.5,
                    'max_temperature': 246.0,
                    'min_pressure': 0.013,
                    'volcanism': ['water']
                }
            ],
        },
        '$Codex_Ent_Bacterial_10_Name;': {
            'name': 'Bacterium Bullaris',
            'value': 1152500,
            'rulesets': [
                {
                    'atmosphere': ['Methane'],
                    'min_gravity': 0.0245,
                    'max_gravity': 0.35,
                    'min_temperature': 68.0,
                    'max_temperature': 109.0
                },
                {
                    'atmosphere': ['MethaneRich'],
                    'min_gravity': 0.44,
                    'max_gravity': 0.6,
                    'min_temperature': 74.0,
                    'max_temperature': 141.0,
                    'min_pressure': 0.01,
                    'max_pressure': 0.05,
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
                    'atmosphere': ['Argon'],
                    'min_gravity': 0.045,
                    'max_gravity': 0.45,
                    'min_temperature': 50.0,
                    'body_type': ['Icy body'],
                    'volcanism': ['nitrogen', 'ammonia']
                },
                {
                    'atmosphere': ['ArgonRich'],
                    'min_gravity': 0.22,
                    'max_gravity': 0.30,
                    'min_temperature': 80.0,
                    'max_temperature': 90.0,
                    'min_pressure': 0.01,
                    'body_type': ['Icy body'],
                    'volcanism': ['nitrogen', 'ammonia']
                },
                {
                    'atmosphere': ['Helium'],
                    'min_gravity': 0.49,
                    'max_gravity': 0.51,
                    'min_temperature': 20.0,
                    'max_temperature': 21.0,
                    'min_pressure': 0.07,
                    'body_type': ['Icy body'],
                    'volcanism': ['nitrogen', 'ammonia']
                },
                {
                    'atmosphere': ['Methane'],
                    'min_gravity': 0.027,
                    'max_gravity': 0.0455,
                    'min_temperature': 84.0,
                    'max_temperature': 108.0,
                    'min_pressure': 0.035,
                    'body_type': ['Icy body'],
                    'volcanism': ['nitrogen', 'ammonia']
                },
                {
                    'atmosphere': ['Neon'],
                    'min_gravity': 0.31,
                    'max_gravity': 0.57,
                    'min_temperature': 20.0,
                    'max_temperature': 61.0,
                    'max_pressure': 0.0065,
                    'body_type': ['Icy body'],
                    'volcanism': ['nitrogen', 'ammonia']
                },
                {
                    'atmosphere': ['NeonRich'],
                    'min_gravity': 0.27,
                    'max_gravity': 0.61,
                    'min_temperature': 20.0,
                    'max_temperature': 93.0,
                    'min_pressure': 0.0027,
                    'body_type': ['Icy body'],
                    'volcanism': ['nitrogen', 'ammonia']
                },
                {
                    'atmosphere': ['WaterRich'],
                    'min_gravity': 0.38,
                    'max_gravity': 0.45,
                    'min_temperature': 190.0,
                    'max_temperature': 310.0,
                    'min_pressure': 0.07,
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
                    'atmosphere': ['SulphurDioxide'],
                    'min_gravity': 0.042,
                    'max_gravity': 0.605,
                    'min_temperature': 132.0,
                    'max_temperature': 500.0,
                    'body_type': ['Rocky body', 'Rocky ice body', 'High metal content body']
                },
                {
                    'atmosphere': ['Water'],
                    'min_gravity': 0.04,
                    'max_gravity': 0.064,
                    'body_type': ['Rocky body', 'High metal content body'],
                    'volcanism': 'None'
                },
                {
                    'atmosphere': ['Water'],
                    'min_gravity': 0.04,
                    'max_gravity': 0.064,
                    'body_type': ['Rocky body', 'High metal content body'],
                    'volcanism': ['water']
                },
                {
                    'atmosphere': ['WaterRich'],
                    'min_gravity': 0.4,
                    'max_gravity': 0.5,
                    'min_temperature': 240.0,
                    'max_temperature': 320.0,
                    'body_type': ['Rocky ice body'],
                    'volcanism': 'None'
                }
            ],
        },
        '$Codex_Ent_Bacterial_13_Name;': {
            'name': 'Bacterium Verrata',
            'value': 3897000,
            'rulesets': [
                {
                    'atmosphere': ['Ammonia'],
                    'body_type': ['Rocky body', 'Rocky ice body', 'Icy body'],
                    'min_gravity': 0.03,
                    'max_gravity': 0.09,
                    'min_temperature': 160.0,
                    'max_temperature': 180.0,
                    'max_pressure': 0.0135,
                    'volcanism': ['water']
                },
                {
                    'atmosphere': ['Argon'],
                    'body_type': ['Rocky ice body', 'Icy body'],
                    'min_gravity': 0.17,
                    'max_gravity': 0.33,
                    'min_temperature': 60.0,
                    'max_temperature': 150.0,
                    'volcanism': ['water']
                },
                {
                    'atmosphere': ['ArgonRich'],
                    'body_type': ['Icy body'],
                    'min_gravity': 0.04,
                    'max_gravity': 0.08,
                    'min_temperature': 80.0,
                    'max_temperature': 90.0,
                    'max_pressure': 0.01,
                    'volcanism': ['water']
                },
                {
                    'atmosphere': ['CarbonDioxide', 'CarbonDioxideRich'],
                    'body_type': ['Rocky ice body', 'Icy body'],
                    'min_gravity': 0.25,
                    'max_gravity': 0.32,
                    'min_temperature': 167.0,
                    'max_temperature': 240.0,
                    'volcanism': ['water']
                },
                {
                    'atmosphere': ['Helium'],
                    'body_type': ['Icy body'],
                    'min_gravity': 0.49,
                    'max_gravity': 0.53,
                    'min_temperature': 20.0,
                    'max_temperature': 21.0,
                    'min_pressure': 0.065,
                    'volcanism': ['water']
                },
                {
                    'atmosphere': ['Neon'],
                    'body_type': ['Rocky ice body', 'Icy body'],
                    'min_gravity': 0.29,
                    'max_gravity': 0.61,
                    'min_temperature': 20.0,
                    'max_temperature': 51.0,
                    'max_pressure': 0.075,
                    'volcanism': ['water']
                },
                {
                    'atmosphere': ['NeonRich'],
                    'body_type': ['Rocky ice body', 'Icy body'],
                    'min_gravity': 0.43,
                    'max_gravity': 0.61,
                    'min_temperature': 20.0,
                    'max_temperature': 65.0,
                    'min_pressure': 0.005,
                    'volcanism': ['water']
                },
                {
                    'atmosphere': ['Nitrogen'],
                    'body_type': ['Icy body'],
                    'min_gravity': 0.21,
                    'max_gravity': 0.24,
                    'min_temperature': 60.0,
                    'max_temperature': 80.0,
                    'volcanism': ['water']
                },
                {
                    'atmosphere': ['Oxygen'],
                    'body_type': ['Rocky ice body', 'Icy body'],
                    'min_gravity': 0.24,
                    'max_gravity': 0.35,
                    'min_temperature': 154.0,
                    'max_temperature': 220.0,
                    'min_pressure': 0.01,
                    'volcanism': ['water']
                },
                {
                    'atmosphere': ['Water'],
                    'body_type': ['Rocky body'],
                    'min_gravity': 0.04,
                    'max_gravity': 0.054,
                    'volcanism': ['water']
                }
            ]
        }
    }
}
