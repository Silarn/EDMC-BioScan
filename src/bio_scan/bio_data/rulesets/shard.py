from typing import Mapping

catalog: dict[str, dict[str, Mapping]] = {
    '$Codex_Ent_Ground_Struct_Ice_Name;': {
        '$Codex_Ent_Ground_Struct_Ice_Name;': {
            'name': 'Crystalline Shards',
            'value': 1628800,
            'rulesets': [
                {
                    'atmosphere': ['None', 'Argon', 'ArgonRich', 'CarbonDioxide', 'CarbonDioxideRich',
                                   'Helium', 'Methane', 'Neon', 'NeonRich'],
                    'max_gravity': 2.0,
                    'max_temperature': 266.0,
                    'main_star': ['A', 'B', 'F', 'G', 'K', 'N', 'H'],
                    'distance': 10000.0,
                    'life_plus': True,
                    'regions': ['exterior']
                }
            ]
        }
    }
}
