create conda environment
```
conda create -n blenderproc python=3.7
conda activate blenderproc
```
github
```
git clone https://github.com/SeungBack/BlenderProc --resursive
cd bop_toolkit
pip install -r requirements.txt
export PYTHONPATH="${PYTHONPATH}:${BOP_TOOLKIT_PATH}"
```
download textures
```
python scripts/download_cc_textures.py
```
render
```
python run.py \
aumask/ir.yaml \
/home/seung/Workspace/datasets/OPE/BOP \
lm \
/home/seung/Workspace/datasets/OPE/BOP/bop_toolkit \
resources/cctextures \
aumask/output \
1,2,3

python run.py
0 {config file}
1 {BOP path}
2 {dataset}
3 {BOP toolkit path}
4 {texture path}
5 {output path}
6 {object_ids}

```




generate mask
```
cd bop_toolkit 
python scripts/cal_gt_masks.py
```
