# Copyright (C) 2022 Intel Corporation
# SPDX-License-Identifier: MIT License

import pytest
import torch
import dgl
from matsciml.models import DimeNetPP
from matsciml.datasets import transforms
from matsciml.datasets.materials_project import MaterialsProjectDataset

torch.random.manual_seed(10)
dgl.random.seed(10)


@pytest.fixture
def test_batch():
    dset = MaterialsProjectDataset.from_devset(
        transforms=[
            transforms.PointCloudToGraphTransform("dgl", cutoff_dist=20.0),
            transforms.DistancesTransform(),
        ]
    )
    data = [dset.__getitem__(index) for index in range(2)]
    batch = dset.collate_fn(data)
    return batch


@torch.no_grad()
def test_dimenet_pp_single(test_batch):
    # use the default settings
    model = DimeNetPP(out_emb_size=256)
    output = model(test_batch)
    assert torch.isfinite(output).all()
    assert output.shape == (2, 256)