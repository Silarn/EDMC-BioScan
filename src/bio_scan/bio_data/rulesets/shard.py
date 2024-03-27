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
                    'max_temperature': 273.0,
                    'star': ['A', 'F', 'G', 'K', 'MS', 'S'],
                    'distance': 12000.0,
                    'bodies': ['Earthlike body', 'Ammonia world', 'Water world', 'Gas giant with water based life',
                               'Gas giant with ammonia based life', 'Water giant'],
                    'regions': ['exterior']
                }
            ]
        }
    }
}
