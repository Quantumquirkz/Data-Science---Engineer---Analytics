from __future__ import annotations

from projects._portfolio_common import ProjectSpec


SPEC = ProjectSpec(
    number=91,
    slug='scientific_image_segmentation_benchmark',
    title='Scientific Image Segmentation Benchmark',
    description='Compare segmentation methods on microscopy, materials, or astronomy images.',
    theoretical_stack='image processing, segmentation, optimization, evaluation metrics, deep learning',
    domain='astronomy',
    task_kind='segmentation',
    target_name='target_label',
    public_data_note='Compatible with open astronomy archives; default table emulates noisy detector/catalog measurements.',
    random_seed=1820,
)
