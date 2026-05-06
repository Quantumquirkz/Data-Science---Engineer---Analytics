from __future__ import annotations

from projects._portfolio_common import ProjectSpec


SPEC = ProjectSpec(
    number=56,
    slug='smart_city_noise_map_generator',
    title='Smart City Noise Map Generator',
    description='Build dynamic urban noise maps using open city sound datasets, municipality sensor archives, and spatial interpolation.',
    theoretical_stack='Geostatistics, interpolation, signal smoothing, spatial analytics, environmental modeling',
    domain='environment',
    task_kind='regression',
    target_name='target_value',
    public_data_note='Public meteorological or geospatial data can be swapped in; default demo uses synthetic spatial fields.',
    random_seed=1785,
)
