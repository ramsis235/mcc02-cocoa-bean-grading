# MCC-02 cocoa bean grading: code

[![Dataset DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.23212578.svg)](https://doi.org/10.5281/zenodo.23212578)

Training and evaluation code for the article

> Siswanto R, Reddy C KK, Santoso H, Adli HK. *Backbone decoupling improves field generalisation of two-stage cocoa bean quality grading.* Manuscript in preparation; citation details will be added on publication.

The framework grades whole cocoa beans into four classes (Fermented, Unfermented, Broken, Moldy) in two stages: a RetinaNet detector with anchors optimised by differential evolution, followed by a Swin-Tiny classifier with multi-scale (EMDMFM) and self-attention (SAFM) fusion, with optional XGBoost and isotonic-calibration stages. Twenty configurations in three ablation chains are trained on MCC-02 and evaluated on laboratory test crops and on smartphone images from working post-harvest facilities.

## Data

The MCC-02 dataset, field images, prediction records and anchor configuration are on Zenodo: https://doi.org/10.5281/zenodo.23212578 (CC BY 4.0).

Download the files, then arrange them into the layout the notebooks expect:

```bash
python prepare_data.py --zenodo <download folder> --out <dataset folder>
```

## Notebooks

Run in this order. The notebooks were developed on Google Colab with a GPU (NVIDIA L4) and the dataset on Google Drive; set `BASE_DIR` (or `BASE_DRIVE_DIR`) in each notebook to your dataset folder.

| Notebook | Content |
|---|---|
| `01_chain_A_ablation.ipynb` | Chain A (A1-A8): ground-truth crops, differential-evolution anchors, detector and classifier training, XGBoost and isotonic calibration, laboratory evaluation |
| `02_chain_X_ablation.ipynb` | Chain X (X1-X6): decoupled detector and classifier encoders |
| `03_chain_Y_ablation.ipynb` | Chain Y (Y1-Y6): one encoder shared by both heads |
| `04_cnn_glcm_baselines.ipynb` | Ten CNN + GLCM baseline classifiers on the same crops |
| `05_field_evaluation_and_analyses.ipynb` | Shared-encoder diagnostic, laboratory per-sample predictions and paired tests, field evaluation of all twenty configurations, anchor analysis, per-class AP, efficiency, Grad-CAM, learning curves and 5-fold cross-validation |
| `06_inter_rater_agreement.ipynb` | Sampling for the inter-rater re-annotation and Fleiss' kappa |

Notes:

- Notebook 01 writes the ground-truth classifier crops to the Colab VM. Notebooks 02, 03 and 05 look for a copy at `<dataset folder>/cropped_splits_gt_based_backup/<split>/<Class>/`; copy the crop folder there after running notebook 01.
- `prepare_data.py` places the released anchor configuration where chains A, X and Y load it, so all chains use the anchors reported in the article.
- In shared-encoder configurations the detector is trained first and the classification head is then trained on the same encoder, so the detector and classifier checkpoints store different encoder states. Notebook 05 evaluates these configurations with one encoder state for both heads, as deployed, and also with each head on its own snapshot for diagnosis.
- Notebook 04 uses TensorFlow/Keras; the other notebooks use PyTorch.

## Requirements

Python 3.10 or later. See `requirements.txt`; on Google Colab only `torchmetrics` and `faster-coco-eval` need to be installed.

## Citation

If you use this code or the dataset, please cite the article and the dataset (see `CITATION.cff`):

```
Siswanto R, Reddy C KK, Santoso H, Adli HK (2026) MCC-02: A whole-bean image dataset for four-class
cocoa bean quality grading, with a field evaluation set (v1.0) [Data set]. Zenodo.
https://doi.org/10.5281/zenodo.23212578
```

## Licence

Code: MIT (see `LICENSE`). Dataset: CC BY 4.0 (see the Zenodo record).

## Contact

Hasyiya Karimah Adli, Universiti Malaysia Kelantan (hasyiya@umk.edu.my)
