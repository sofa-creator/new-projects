"""Extract dominant colours from reference images with k-means. Usage: python3 palette-from-images.py out.json img1 img2 ..."""
import sys, json, numpy as np
from PIL import Image
def kmeans(px, k, iters=30, seed=1):
    rng = np.random.default_rng(seed)
    c = px[rng.choice(len(px), k, replace=False)].astype(float)
    for _ in range(iters):
        d = ((px[:, None, :] - c[None]) ** 2).sum(-1)
        lab = d.argmin(1)
        for i in range(k):
            m = px[lab == i]
            if len(m): c[i] = m.mean(0)
    d = ((px[:, None, :] - c[None]) ** 2).sum(-1); lab = d.argmin(1)
    share = np.bincount(lab, minlength=k) / len(px)
    order = share.argsort()[::-1]
    return [(tuple(int(round(v)) for v in c[i]), float(share[i])) for i in order]
out = {}
for path in sys.argv[2:]:
    im = Image.open(path).convert('RGB')
    im.thumbnail((240, 240))
    px = np.asarray(im).reshape(-1, 3)
    out[path.split('/')[-1]] = [{'hex': '#%02X%02X%02X' % c, 'share': round(s, 3)} for c, s in kmeans(px, 7)]
json.dump(out, open(sys.argv[1], 'w'), indent=1)
for k, v in out.items(): print(k, ' '.join(f"{d['hex']}({int(d['share']*100)}%)" for d in v))
