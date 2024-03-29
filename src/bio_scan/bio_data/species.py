from typing import Mapping
from bio_scan.bio_data.rulesets.aleoida import catalog as aleoida
from bio_scan.bio_data.rulesets.anemone import catalog as anemone
from bio_scan.bio_data.rulesets.bacterium import catalog as bacterium
from bio_scan.bio_data.rulesets.brain_tree import catalog as brain_tree
from bio_scan.bio_data.rulesets.cactoida import catalog as cactoida
from bio_scan.bio_data.rulesets.clypeus import catalog as clypeus
from bio_scan.bio_data.rulesets.concha import catalog as concha
from bio_scan.bio_data.rulesets.electricae import catalog as electricae
from bio_scan.bio_data.rulesets.fonticulua import catalog as fonticulua
from bio_scan.bio_data.rulesets.frutexa import catalog as frutexa
from bio_scan.bio_data.rulesets.fumerola import catalog as fumerola
from bio_scan.bio_data.rulesets.fungoida import catalog as fungoida
from bio_scan.bio_data.rulesets.osseus import catalog as osseus
from bio_scan.bio_data.rulesets.recepta import catalog as recepta
from bio_scan.bio_data.rulesets.shard import catalog as shard
from bio_scan.bio_data.rulesets.stratum import catalog as stratum
from bio_scan.bio_data.rulesets.tubers import catalog as tubers
from bio_scan.bio_data.rulesets.tubus import catalog as tubus
from bio_scan.bio_data.rulesets.tussock import catalog as tussock

_mound_amphora: dict[str, dict[str, Mapping]] = {
    '$Codex_Ent_Cone_Name;': {  # No atmos, near center of nebula
        '$Codex_Ent_Cone_Name;': {
            'name': 'Bark Mound',
            'value': 1471900,
            'rulesets': [
                {
                    'volcanism': 'Any',
                    'nebula': 'large',
                    'regions': ['!center']
                }
            ]
        }
    },
    '$Codex_Ent_Vents_Name;': {
        '$Codex_Ent_Vents_Name;': {
            'name': 'Amphora Plant',
            'value': 1628800,
            'rulesets': [
                {
                    'body_type': ['Metal rich body'],
                    'atmosphere': ['None'],
                    'star': 'A',
                    'min_temperature': 1000.0,
                    'max_temperature': 1750.0,
                    'volcanism': ['metallic', 'rocky', 'silicate'],
                    'bodies': ['Earthlike body', 'Gas giant with water based life', 'Water giant'],
                    'regions': ['amphora']
                }
            ]
        }
    },
}

rules: dict[str, dict[str, Mapping]] = (_mound_amphora | aleoida | anemone | bacterium | brain_tree | cactoida |
                                        clypeus | concha | electricae | fonticulua | frutexa | fumerola | fungoida |
                                        osseus | recepta | shard | stratum | tubers | tubus | tussock)
