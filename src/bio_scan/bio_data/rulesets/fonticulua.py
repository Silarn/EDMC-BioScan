from typing import Mapping

catalog: dict[str, dict[str, Mapping]] = {
    '$Codex_Ent_Fonticulus_Genus_Name;': {
        '$Codex_Ent_Fonticulus_01_Name;': {
            'name': 'Fonticulua Segmentatus',
            'value': 19010800,
            'rulesets': [
                {
                    'atmosphere': ['Neon', 'NeonRich'],
                    'body_type': ['Icy body'],
                    'min_gravity': 0.25,
                    'max_gravity': 0.276,
                    'min_temperature': 50.0,
                    'max_temperature': 75.0,
                    'max_pressure': 0.006,
                    'volcanism': 'None'
                }
            ],
        },
        '$Codex_Ent_Fonticulus_02_Name;': {
            'name': 'Fonticulua Campestris',
            'value': 1000000,
            'rulesets': [
                {
                    'atmosphere': ['Argon'],
                    'body_type': ['Icy body', 'Rocky ice body'],
                    'min_gravity': 0.027,
                    'max_gravity': 0.276,
                    'min_temperature': 50.0,
                    'max_temperature': 150.0
                }
            ],
        },
        '$Codex_Ent_Fonticulus_03_Name;': {
            'name': 'Fonticulua Upupam',
            'value': 5727600,
            'rulesets': [
                {
                    'atmosphere': ['ArgonRich'],
                    'body_type': ['Icy body', 'Rocky ice body'],
                    'min_gravity': 0.209,
                    'max_gravity': 0.276,
                    'min_temperature': 61.0,
                    'max_temperature': 125.0,
                    'min_pressure': 0.019
                }
            ],
        },
        '$Codex_Ent_Fonticulus_04_Name;': {
            'name': 'Fonticulua Lapida',
            'value': 3111000,
            'rulesets': [
                {
                    'atmosphere': ['Nitrogen'],
                    'min_gravity': 0.19,
                    'max_gravity': 0.276,
                    'min_temperature': 50.0,
                    'max_temperature': 81.0,
                    'body_type': ['Icy body', 'Rocky ice body']
                }
            ],
        },
        '$Codex_Ent_Fonticulus_05_Name;': {
            'name': 'Fonticulua Fluctus',
            'value': 20000000,
            'rulesets': [
                {
                    'atmosphere': ['Oxygen'],
                    'body_type': ['Icy body'],
                    'min_gravity': 0.235,
                    'max_gravity': 0.276,
                    'min_temperature': 143.0,
                    'max_temperature': 200.0,
                    'min_pressure': 0.012
                }
            ],
        },
        '$Codex_Ent_Fonticulus_06_Name;': {
            'name': 'Fonticulua Digitos',
            'value': 1804100,
            'rulesets': [
                {
                    'atmosphere': ['Methane'],
                    'body_type': ['Icy body', 'Rocky ice body'],
                    'min_gravity': 0.025,
                    'max_gravity': 0.07,
                    'min_temperature': 83.0,
                    'max_temperature': 109.0,
                    'min_pressure': 0.03
                }
            ],
        },
    },
}
