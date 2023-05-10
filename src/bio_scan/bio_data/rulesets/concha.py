from typing import Mapping

catalog: dict[str, dict[str, Mapping]] = {
    '$Codex_Ent_Conchas_Genus_Name;': {
        '$Codex_Ent_Conchas_01_Name;': {
            'name': 'Concha Renibus',
            'value': 4572400,
            'rulesets': [
                {
                    'atmosphere': ['CarbonDioxide', 'CarbonDioxideRich'],
                    'max_gravity': 0.275,
                    'max_temperature': 195.0,
                    'min_temperature': 180.0,
                    'body_type': ['Rocky body', 'High metal content body']
                },
                {
                    'atmosphere': ['Water', 'WaterRich'],
                    'max_gravity': 0.275,
                    'max_temperature': 394.0,
                    'min_temperature': 452.0,
                    'body_type': ['Rocky body', 'High metal content body']
                },
                {
                    'atmosphere': ['Methane', 'MethaneRich'],
                    'max_gravity': 0.275,
                    'max_temperature': 90.0,
                    'min_temperature': 80.0,
                    'body_type': ['Rocky body', 'High metal content body']
                },
                {
                    'atmosphere': ['Ammonia'],
                    'max_gravity': 0.275,
                    'max_temperature': 177.0,
                    'min_temperature': 176.0,
                    'body_type': ['Rocky body', 'High metal content body']
                }
            ],
        },
        '$Codex_Ent_Conchas_02_Name;': {
            'name': 'Concha Aureolas',
            'value': 7774700,
            'rulesets': [
                {
                    'atmosphere': ['Ammonia'],
                    'max_gravity': 0.275,
                    'max_temperature': 177.0,
                    'min_temperature': 152.0,
                    'body_type': ['Rocky body', 'High metal content body']
                }
            ],
        },
        '$Codex_Ent_Conchas_03_Name;': {
            'name': 'Concha Labiata',
            'value': 2352400,
            'rulesets': [
                {
                    'atmosphere': ['CarbonDioxide', 'CarbonDioxideRich'],
                    'max_gravity': 0.275,
                    'max_temperature': 196.0,
                    'min_temperature': 150.0,
                    'body_type': ['Rocky body', 'High metal content body']
                }
            ],
        },
        '$Codex_Ent_Conchas_04_Name;': {
            'name': 'Concha Biconcavis',
            'value': 16777215,
            'rulesets': [
                {
                    'atmosphere': ['Nitrogen'],
                    'max_gravity': 0.275,
                    'max_temperature': 42.0,
                    'min_temperature': 51.0,
                    'body_type': ['Rocky body', 'High metal content body']
                }
            ],
        },
    },
}
