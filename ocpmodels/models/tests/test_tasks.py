import pytorch_lightning as pl

from ocpmodels.models.base import ForceRegressionTask
from ocpmodels.models import PLEGNNBackbone
from ocpmodels.datasets.materials_project import MaterialsProjectDataset
from ocpmodels.lightning.data_utils import MatSciMLDataModule

pl.seed_everything(2156161)


def test_regression_devset():
    dset = MaterialsProjectDataset.from_devset()


def test_force_regression():
    devset = MatSciMLDataModule.from_devset("S2EFDataset")
    model_args = {
        "embed_in_dim": 128,
        "embed_hidden_dim": 32,
        "embed_out_dim": 128,
        "embed_depth": 5,
        "embed_feat_dims": [128, 128, 128],
        "embed_message_dims": [128, 128, 128],
        "embed_position_dims": [64, 64],
        "embed_edge_attributes_dim": 0,
        "embed_activation": "relu",
        "embed_residual": True,
        "embed_normalize": True,
        "embed_tanh": True,
        "embed_activate_last": False,
        "embed_k_linears": 1,
        "embed_use_attention": False,
        "embed_attention_norm": "sigmoid",
        "readout": "sum",
        "node_projection_depth": 3,
        "node_projection_hidden_dim": 128,
        "node_projection_activation": "relu",
        "prediction_out_dim": 1,
        "prediction_depth": 3,
        "prediction_hidden_dim": 128,
        "prediction_activation": "relu",
        "encoder_only": True,
    }

    model = PLEGNNBackbone(**model_args)
    task = ForceRegressionTask(model)
    trainer = pl.Trainer(max_steps=5, logger=False, enable_checkpointing=False)
    trainer.fit(task, datamodule=devset)
    # make sure losses are tracked
    for key in ["energy", "force"]:
        assert f"train_{key}" in trainer.logged_metrics
