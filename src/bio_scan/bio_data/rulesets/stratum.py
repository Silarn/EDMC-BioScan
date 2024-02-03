from typing import Mapping

catalog: dict[str, dict[str, Mapping]] = {
    '$Codex_Ent_Stratum_04_Name;': {
        '$Codex_Ent_Stratum_04_Name;': {
            'name': 'Stratum Aranaemus',
            'value': 2448900,
            'rulesets': []
        }
    },
    '$Codex_Ent_Stratum_Genus_Name;': {
        '$Codex_Ent_Stratum_01_Name;': {
            'name': 'Stratum Excutitus',
            'value': 2448900,
            'rulesets': [
                {
                    'atmosphere': ['CarbonDioxide'],
                    'min_gravity': 0.04,
                    'max_gravity': 0.48,
                    'min_temperature': 165.0,
                    'max_temperature': 190.0,
                    'min_pressure': 0.0035,
                    'body_type': ['Rocky body'],
                    'volcanism': 'None',
                    'regions': ['orion-cygnus']
                },
                {
                    'atmosphere': ['SulphurDioxide'],
                    'min_gravity': 0.27,
                    'max_gravity': 0.4,
                    'min_temperature': 165.0,
                    'max_temperature': 190.0,
                    'body_type': ['Rocky body'],
                    'regions': ['orion-cygnus']
                }
            ],
        },
        '$Codex_Ent_Stratum_02_Name;': {
            'name': 'Stratum Paleas',
            'value': 1362000,
            'rulesets': [
                {
                    'atmosphere': ['Ammonia'],
                    'min_gravity': 0.04,
                    'max_gravity': 0.35,
                    'min_temperature': 165.0,
                    'max_temperature': 177.0,
                    'max_pressure': 0.0135,
                    'body_type': ['Rocky body']
                },
                {
                    'atmosphere': ['CarbonDioxide'],
                    'min_gravity': 0.04,
                    'max_gravity': 0.585,
                    'min_temperature': 165.0,
                    'max_temperature': 395.0,
                    'body_type': ['Rocky body'],
                    'volcanism': 'None'
                },
                {
                    'atmosphere': ['CarbonDioxideRich'],
                    'min_gravity': 0.43,
                    'max_gravity': 0.585,
                    'min_temperature': 185.0,
                    'max_temperature': 260.0,
                    'min_pressure': 0.015,
                    'body_type': ['Rocky body'],
                    'volcanism': 'None'
                },
                {
                    'atmosphere': ['Water'],
                    'min_gravity': 0.04,
                    'max_gravity': 0.056,
                    'body_type': ['Rocky body'],
                    'volcanism': 'None'
                },
                {
                    'atmosphere': ['Water'],
                    'min_gravity': 0.04,
                    'max_gravity': 0.056,
                    'min_pressure': 0.065,
                    'body_type': ['Rocky body'],
                    'volcanism': ['water']
                },
                {
                    'atmosphere': ['Oxygen'],
                    'min_gravity': 0.4,
                    'max_gravity': 0.6,
                    'min_temperature': 165.0,
                    'max_temperature': 250.0,
                    'min_pressure': 0.045,
                    'body_type': ['Rocky body']
                }
            ],
        },
        '$Codex_Ent_Stratum_03_Name;': {
            'name': 'Stratum Laminamus',
            'value': 2788300,
            'rulesets': [
                {
                    'atmosphere': ['Ammonia'],
                    'min_gravity': 0.04,
                    'max_gravity': 0.34,
                    'min_temperature': 165.0,
                    'max_temperature': 177.0,
                    'max_pressure': 0.0135,
                    'body_type': ['Rocky body'],
                    'regions': ['orion-cygnus']
                }
            ],
        },
        '$Codex_Ent_Stratum_04_Name;': {
            'name': 'Stratum Araneamus',
            'value': 2448900,
            'rulesets': [
                {
                    'atmosphere': ['SulphurDioxide'],
                    'min_gravity': 0.26,
                    'max_gravity': 0.55,
                    'min_temperature': 165.0,
                    'max_temperature': 373.0,
                    'body_type': ['Rocky body']
                }
            ],
        },
        '$Codex_Ent_Stratum_05_Name;': {
            'name': 'Stratum Limaxus',
            'value': 1362000,
            'rulesets': [
                {
                    'atmosphere': ['CarbonDioxide'],
                    'min_gravity': 0.045,
                    'max_gravity': 0.4,
                    'min_temperature': 165.0,
                    'max_temperature': 190.0,
                    'min_pressure': 0.05,
                    'body_type': ['Rocky body'],
                    'volcanism': 'None',
                    'regions': ['scutum-centaurus-core']
                },
                {
                    'atmosphere': ['SulphurDioxide'],
                    'min_gravity': 0.27,
                    'max_gravity': 0.4,
                    'min_temperature': 165.0,
                    'max_temperature': 190.0,
                    'body_type': ['Rocky body'],
                    'regions': ['scutum-centaurus-core']
                }
            ],
        },
        '$Codex_Ent_Stratum_06_Name;': {
            'name': 'Stratum Cucumisis',
            'value': 16202800,
            'rulesets': [
                {
                    'atmosphere': ['CarbonDioxide'],
                    'min_gravity': 0.04,
                    'max_gravity': 0.6,
                    'min_temperature': 191.0,
                    'max_temperature': 371.0,
                    'body_type': ['Rocky body'],
                    'volcanism': 'None',
                    'regions': ['sagittarius-carina']
                },
                {
                    'atmosphere': ['CarbonDioxideRich'],
                    'min_gravity': 0.44,
                    'max_gravity': 0.56,
                    'min_temperature': 215.0,
                    'max_temperature': 245.0,
                    'min_pressure': 0.01,
                    'body_type': ['Rocky body'],
                    'volcanism': 'None',
                    'regions': ['sagittarius-carina']
                },
                {
                    'atmosphere': ['Oxygen'],
                    'min_gravity': 0.4,
                    'max_gravity': 0.6,
                    'min_temperature': 200.0,
                    'max_temperature': 250.0,
                    'min_pressure': 0.01,
                    'body_type': ['Rocky body'],
                    'regions': ['sagittarius-carina']
                },
                {
                    'atmosphere': ['SulphurDioxide'],
                    'min_gravity': 0.26,
                    'max_gravity': 0.55,
                    'min_temperature': 191.0,
                    'max_temperature': 373.0,
                    'body_type': ['Rocky body'],
                    'regions': ['sagittarius-carina']
                }
            ],
        },
        '$Codex_Ent_Stratum_07_Name;': {
            'name': 'Stratum Tectonicas',
            'value': 19010800,
            'rulesets': [
                {
                    'atmosphere': ['Ammonia'],
                    'min_gravity': 0.045,
                    'max_gravity': 0.38,
                    'min_temperature': 165.0,
                    'max_temperature': 177.0,
                    'body_type': ['High metal content body']
                },
                {
                    'atmosphere': ['Argon', 'ArgonRich'],
                    'min_gravity': 0.485,
                    'max_gravity': 0.54,
                    'min_temperature': 167.0,
                    'max_temperature': 199.0,
                    'body_type': ['High metal content body'],
                    'volcanism': 'None'
                },
                {
                    'atmosphere': ['CarbonDioxide'],
                    'min_gravity': 0.045,
                    'max_gravity': 0.61,
                    'min_temperature': 165.0,
                    'max_temperature': 430.0,
                    'body_type': ['High metal content body']
                },
                {
                    'atmosphere': ['CarbonDioxideRich'],
                    'min_gravity': 0.035,
                    'max_gravity': 0.61,
                    'min_temperature': 165.0,
                    'max_temperature': 260.0,
                    'body_type': ['High metal content body']
                },
                {
                    'atmosphere': ['Oxygen'],
                    'min_gravity': 0.4,
                    'max_gravity': 0.52,
                    'min_temperature': 165.0,
                    'max_temperature': 246.0,
                    'body_type': ['High metal content body']
                },
                {
                    'atmosphere': ['SulphurDioxide'],
                    'min_gravity': 0.29,
                    'max_gravity': 0.62,
                    'min_temperature': 165.0,
                    'max_temperature': 450.0,
                    'body_type': ['High metal content body']
                },
                {
                    'atmosphere': ['Water'],
                    'min_gravity': 0.045,
                    'max_gravity': 0.063,
                    'body_type': ['High metal content body'],
                    'volcanism': 'None'
                },
            ],
        },
        '$Codex_Ent_Stratum_08_Name;': {
            'name': 'Stratum Frigus',
            'value': 2637500,
            'rulesets': [
                {
                    'atmosphere': ['CarbonDioxide'],
                    'min_gravity': 0.043,
                    'max_gravity': 0.54,
                    'min_temperature': 191.0,
                    'max_temperature': 365.0,
                    'min_pressure': 0.001,
                    'body_type': ['Rocky body'],
                    'volcanism': 'None',
                    'regions': ['perseus-core']
                },
                {
                    'atmosphere': ['CarbonDioxideRich'],
                    'min_gravity': 0.45,
                    'max_gravity': 0.55,
                    'min_temperature': 200.0,
                    'max_temperature': 250.0,
                    'min_pressure': 0.01,
                    'body_type': ['Rocky body'],
                    'volcanism': 'None',
                    'regions': ['perseus-core']
                },
                {
                    'atmosphere': ['SulphurDioxide'],
                    'min_gravity': 0.29,
                    'max_gravity': 0.52,
                    'min_temperature': 191.0,
                    'max_temperature': 369.0,
                    'body_type': ['Rocky body'],
                    'regions': ['perseus-core']
                }
            ],
        },
    },
}
