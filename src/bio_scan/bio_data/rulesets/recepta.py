from typing import Mapping

catalog: dict[str, dict[str, Mapping]] = {
    '$Codex_Ent_Recepta_Genus_Name;': {
        '$Codex_Ent_Recepta_01_Name;': {
            'name': 'Recepta Umbrux',
            'value': 12934900,
            'rulesets': [
                {
                    'atmosphere': ['SulphurDioxide'],
                    'atmosphere_component': {'SulphurDioxide': 1.05},
                    'max_gravity': 0.275,
                    'min_gravity': 0.043,
                    'min_temperature': 132.0,
                    'max_temperature': 272.0
                },
                {
                    'atmosphere': ['CarbonDioxide'],
                    'atmosphere_component': {'SulphurDioxide': 1.05},
                    'max_gravity': 0.275,
                    'min_gravity': 0.043,
                    'min_temperature': 151.0,
                    'max_temperature': 195.0
                },
                {
                    'atmosphere': ['Oxygen'],
                    'atmosphere_component': {'SulphurDioxide': 1.05},
                    'max_gravity': 0.275,
                    'min_gravity': 0.043,
                    'min_temperature': 151.0,
                    'max_temperature': 175.0
                }
            ],
        },
        '$Codex_Ent_Recepta_02_Name;': {
            'name': 'Recepta Deltahedronix',
            'value': 16202800,
            'rulesets': [
                {
                    'atmosphere': ['SulphurDioxide', 'Oxygen', 'CarbonDioxide'],
                    'atmosphere_component': {'SulphurDioxide': 1.05},
                    'max_gravity': 0.275,
                    'min_gravity': 0.043
                }
            ],
        },
        '$Codex_Ent_Recepta_03_Name;': {
            'name': 'Recepta Conditivus',
            'value': 14313700,
            'rulesets': [
                {
                    'atmosphere': ['SulphurDioxide', 'Oxygen', 'CarbonDioxide'],
                    'atmosphere_component': {'SulphurDioxide': 1.05},
                    'max_gravity': 0.275,
                    'min_gravity': 0.043,
                    'body_type': ['Icy body', 'Rocky ice body']
                }
            ],
        },
    },
}
