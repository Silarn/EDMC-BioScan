from typing import Mapping

catalog: dict[str, dict[str, Mapping]] = {
    '$Codex_Ent_Stratum_Genus_Name;': {
        '$Codex_Ent_Stratum_01_Name;': {
            'name': 'Stratum Excutitus',
            'value': 2448900,
            'rulesets': [
                {
                    'atmosphere': ['CarbonDioxide', 'CarbonDioxideRich', 'SulphurDioxide'],
                    'min_gravity': 0.04,
                    'max_gravity': 0.48,
                    'max_temperature': 190.0,
                    'min_temperature': 165.0,
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
                    'atmosphere': ['CarbonDioxideRich', 'Water', 'WaterRich', 'Oxygen'],
                    'min_gravity': 0.04,
                    'max_gravity': 0.585,
                    'min_temperature': 165.0,
                    'body_type': ['Rocky body']
                },
                {
                    'atmosphere': ['CarbonDioxide'],
                    'min_gravity': 0.04,
                    'max_gravity': 0.585,
                    'min_temperature': 165.0,
                    'max_temperature': 381.0,
                    'body_type': ['Rocky body']
                },
                {
                    'atmosphere': ['Ammonia'],
                    'min_gravity': 0.04,
                    'max_gravity': 0.585,
                    'min_temperature': 165.0,
                    'max_temperature': 177.0,
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
                    'max_gravity': 0.34,
                    'max_temperature': 177.0,
                    'min_temperature': 165.0,
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
                    'max_temperature': 375.0,
                    'min_temperature': 165.0,
                    'body_type': ['Rocky body']
                }
            ],
        },
        '$Codex_Ent_Stratum_05_Name;': {
            'name': 'Stratum Limaxus',
            'value': 1362000,
            'rulesets': [
                {
                    'atmosphere': ['CarbonDioxide', 'CarbonDioxideRich', 'SulphurDioxide'],
                    'min_gravity': 0.04,
                    'max_gravity': 0.48,
                    'max_temperature': 190.0,
                    'min_temperature': 165.0,
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
                    'atmosphere': ['CarbonDioxide', 'CarbonDioxideRich', 'SulphurDioxide'],
                    'min_gravity': 0.04,
                    'max_gravity': 0.6,
                    'min_temperature': 190.0,
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
                    'atmosphere': ['Oxygen', 'Water', 'WaterRich'],
                    'min_gravity': 0.045,
                    'max_gravity': 0.607,
                    'min_temperature': 165.0,
                    'body_type': ['High metal content body']
                },
                {
                    'atmosphere': ['CarbonDioxide', 'CarbonDioxideRich'],
                    'min_gravity': 0.045,
                    'max_gravity': 0.607,
                    'max_temperature': 421.0,
                    'min_temperature': 165.0,
                    'body_type': ['High metal content body']
                },
                {
                    'atmosphere': ['SulphurDioxide'],
                    'min_gravity': 0.045,
                    'max_gravity': 0.607,
                    'max_temperature': 450.0,
                    'min_temperature': 165.0,
                    'body_type': ['High metal content body']
                },
                {
                    'atmosphere': ['Ammonia'],
                    'min_gravity': 0.045,
                    'max_gravity': 0.607,
                    'max_temperature': 176.0,
                    'min_temperature': 165.0,
                    'body_type': ['High metal content body']
                }
            ],
        },
        '$Codex_Ent_Stratum_08_Name;': {
            'name': 'Stratum Frigus',
            'value': 2637500,
            'rulesets': [
                {
                    'atmosphere': ['CarbonDioxide', 'CarbonDioxideRich', 'SulphurDioxide'],
                    'min_gravity': 0.04,
                    'max_gravity': 0.55,
                    'min_temperature': 190.0,
                    'body_type': ['Rocky body'],
                    'regions': ['perseus-core']
                }
            ],
        },
    },
}
