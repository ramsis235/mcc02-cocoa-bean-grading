"""Arrange the MCC-02 Zenodo release into the folder layout expected by the notebooks.

Download the files from https://doi.org/10.5281/zenodo.23212578 into one folder, then run

    python prepare_data.py --zenodo <download folder> --out <dataset folder>

and set BASE_DIR in the notebooks to <dataset folder>. The resulting layout is

    <dataset folder>/
        annotations_coco.json            file_name = images/<Class>/<file>
        images/<Class>/<file>            16,000 laboratory images
        splits/<split>/<Class>/<file>    train / val / test copies of the same images
        testing/<file>                   128 field images
        checkpoints_final_ablation/DE_anchor_config_final.json         (chain A)
        checkpoints_full_clahe/A4_shared_swin_v2_anchor_config.json    (chains X and Y)

Use --link to hard-link the split copies instead of copying them (same file system only).
"""
import argparse, csv, glob, json, os, shutil, zipfile


def extract(zip_path, member_prefix, dest, strip):
    with zipfile.ZipFile(zip_path) as z:
        for m in z.infolist():
            if m.is_dir() or not m.filename.startswith(member_prefix):
                continue
            target = os.path.join(dest, m.filename[len(strip):])
            os.makedirs(os.path.dirname(target), exist_ok=True)
            with z.open(m) as src, open(target, 'wb') as dst:
                shutil.copyfileobj(src, dst)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--zenodo', required=True, help='folder with the downloaded Zenodo files')
    ap.add_argument('--out', required=True, help='dataset folder to create (BASE_DIR in the notebooks)')
    ap.add_argument('--link', action='store_true', help='hard-link split copies instead of copying')
    a = ap.parse_args()
    z, out = a.zenodo, a.out
    os.makedirs(out, exist_ok=True)

    print('Extracting laboratory images ...')
    parts = sorted(glob.glob(f'{z}/MCC-02_lab_images*.zip'))
    assert parts, 'no MCC-02_lab_images*.zip found'
    for part in parts:
        extract(part, 'MCC-02_lab_images/', f'{out}/images', 'MCC-02_lab_images/')

    coco = json.load(open(f'{z}/MCC-02_annotations_coco.json'))
    for im in coco['images']:
        im['file_name'] = 'images/' + im['file_name']
    json.dump(coco, open(f'{out}/annotations_coco.json', 'w'))
    print(f"annotations_coco.json: {len(coco['images'])} images, {len(coco['annotations'])} annotations")

    print('Building split folders ...')
    n = 0
    with open(f'{z}/MCC-02_splits.csv', newline='') as f:
        for row in csv.DictReader(f):
            src = f"{out}/images/{row['file_name']}"
            dst = f"{out}/splits/{row['split']}/{row['file_name']}"
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            if not os.path.exists(dst):
                os.link(src, dst) if a.link else shutil.copy2(src, dst)
            n += 1
    print(f'splits/: {n} images')

    print('Extracting field images and anchor configurations ...')
    sup = f'{z}/MCC-02_field_and_supporting.zip'
    root = 'MCC-02_field_and_supporting/'
    extract(sup, root + 'field_set/images/', f'{out}/testing', root + 'field_set/images/')
    with zipfile.ZipFile(sup) as zz:
        for name, target in [('anchors/anchor_config_chainA.json', 'checkpoints_final_ablation/DE_anchor_config_final.json'),
                             ('anchors/anchor_config_chainXY.json', 'checkpoints_full_clahe/A4_shared_swin_v2_anchor_config.json')]:
            os.makedirs(os.path.dirname(f'{out}/{target}'), exist_ok=True)
            with open(f'{out}/{target}', 'wb') as dst:
                dst.write(zz.read(root + name))
    print(f'testing/: {len(os.listdir(f"{out}/testing"))} field images')
    print('Done. Set BASE_DIR in the notebooks to', os.path.abspath(out))


if __name__ == '__main__':
    main()
