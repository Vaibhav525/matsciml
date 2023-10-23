import pytorch_lightning as pl

from matsciml.models import MEGNet
from matsciml.models.base import ScalarRegressionTask
from matsciml.lightning.data_utils import MatSciMLDataModule
from matsciml.datasets.transforms import DistancesTransform, GraphVariablesTransform

# construct a scalar regression task with SchNet encoder
task = ScalarRegressionTask(
    encoder_class=MEGNet,
    encoder_kwargs={
        "edge_feat_dim": 2,
        "node_feat_dim": 128,
        "graph_feat_dim": 9,
        "num_blocks": 4,
        "hiddens": [256, 256, 128],
        "conv_hiddens": [128, 128, 128],
        "s2s_num_layers": 5,
        "s2s_num_iters": 4,
        "output_hiddens": [64, 64],
        "is_classification": False,
        "encoder_only": True,
    },
    output_kwargs={"lazy": False, "input_dim": 640},
    task_keys=["energy_relaxed"],
)
# MPNN expects edge features corresponding to atom-atom distances
dm = MatSciMLDataModule.from_devset(
    "IS2REDataset",
    dset_kwargs={"transforms": [DistancesTransform(), GraphVariablesTransform()]},
    num_workers=0,
)

# run a quick training loop
trainer = pl.Trainer(fast_dev_run=10)
trainer.fit(task, datamodule=dm)