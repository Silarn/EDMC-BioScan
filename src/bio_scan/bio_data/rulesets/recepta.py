from typing import Mapping

catalog: dict[str, dict[str, Mapping]] = {
    '$Codex_Ent_Recepta_Genus_Name;': {
        '$Codex_Ent_Recepta_01_Name;': {
            'name': 'Recepta Umbrux',
            'value': 12934900,
            'rulesets': [
                {
                    'atmosphere': ['CarbonDioxide'],
                    'min_gravity': 0.04,
                    'max_gravity': 0.275,
                    'min_temperature': 151.0,
                    'max_temperature': 200.0,
                    'atmosphere_component': {'SulphurDioxide': 1.05}
                },
                {
                    'atmosphere': ['Oxygen'],
                    'body_type': ['Icy body'],
                    'min_gravity': 0.23,
                    'max_gravity': 0.275,
                    'min_temperature': 154.0,
                    'max_temperature': 175.0,
                    'min_pressure': 0.01,
                    'volcanism': 'None',
                    'atmosphere_component': {'SulphurDioxide': 1.05}
                },
                {
                    'atmosphere': ['Oxygen'],
                    'body_type': ['Icy body'],
                    'min_gravity': 0.23,
                    'max_gravity': 0.275,
                    'min_temperature': 154.0,
                    'max_temperature': 175.0,
                    'min_pressure': 0.01,
                    'volcanism': ['water'],
                    'atmosphere_component': {'SulphurDioxide': 1.05}
                },
                {
                    'atmosphere': ['SulphurDioxide'],
                    'min_gravity': 0.04,
                    'max_gravity': 0.275,
                    'min_temperature': 132.0,
                    'max_temperature': 273.0,
                    'atmosphere_component': {'SulphurDioxide': 1.05}
                }
            ],
        },
        '$Codex_Ent_Recepta_02_Name;': {
            'name': 'Recepta Deltahedronix',
            'value': 16202800,
            'rulesets': [
                {
                    'atmosphere': ['CarbonDioxide'],
                    'body_type': ['Icy body', 'Rocky ice body', "High metal content body"],
                    'min_gravity': 0.04,
                    'max_gravity': 0.275,
                    'min_temperature': 150.0,
                    'max_temperature': 195.0,
                    'volcanism': 'None',
                    'atmosphere_component': {'SulphurDioxide': 1.05}
                },
                {
                    'atmosphere': ['CarbonDioxide'],
                    'body_type': ['Icy body', 'Rocky ice body', "High metal content body"],
                    'min_gravity': 0.04,
                    'max_gravity': 0.275,
                    'min_temperature': 150.0,
                    'max_temperature': 195.0,
                    'volcanism': ['water'],
                    'atmosphere_component': {'SulphurDioxide': 1.05}
                },
                {
                    'atmosphere': ['SulphurDioxide'],
                    'min_gravity': 0.04,
                    'max_gravity': 0.275,
                    'min_temperature': 132.0,
                    'max_temperature': 272.0,
                    'atmosphere_component': {'SulphurDioxide': 1.05}
                }
            ],
        },
        '$Codex_Ent_Recepta_03_Name;': {
            'name': 'Recepta Conditivus',
            'value': 14313700,
            'rulesets': [
                {
                    'atmosphere': ['CarbonDioxide'],
                    'body_type': ['Icy body', 'Rocky ice body'],
                    'min_gravity': 0.04,
                    'max_gravity': 0.275,
                    'min_temperature': 150.0,
                    'max_temperature': 195.0,
                    'volcanism': 'None',
                    'atmosphere_component': {'SulphurDioxide': 1.05}
                },
                {
                    'atmosphere': ['Oxygen'],
                    'body_type': ['Icy body'],
                    'min_gravity': 0.23,
                    'max_gravity': 0.275,
                    'min_temperature': 154.0,
                    'max_temperature': 160.0,
                    'min_pressure': 0.01,
                    'volcanism': 'None',
                    'atmosphere_component': {'SulphurDioxide': 1.05}
                },
                {
                    'atmosphere': ['Oxygen'],
                    'body_type': ['Icy body'],
                    'min_gravity': 0.23,
                    'max_gravity': 0.275,
                    'min_temperature': 154.0,
                    'max_temperature': 160.0,
                    'min_pressure': 0.01,
                    'volcanism': ['water'],
                    'atmosphere_component': {'SulphurDioxide': 1.05}
                },
                {
                    'atmosphere': ['SulphurDioxide'],
                    'min_gravity': 0.04,
                    'max_gravity': 0.275,
                    'min_temperature': 132.0,
                    'max_temperature': 272.0,
                    'atmosphere_component': {'SulphurDioxide': 1.05}
                }
            ],
        },
    },
}
