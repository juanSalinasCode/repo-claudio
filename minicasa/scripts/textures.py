"""Genera texturas procedurales (PNG/JPG) para la mini casa."""
import numpy as np, os, sys
from PIL import Image, ImageDraw, ImageFilter
OUT = sys.argv[1] if len(sys.argv) > 1 else "tex"
os.makedirs(OUT, exist_ok=True)
rng = np.random.default_rng(7)

def noise(h, w, scale, octaves=4):
    acc = np.zeros((h, w)); amp = 1.0; tot = 0
    for o in range(octaves):
        s = max(1, int(scale / (2 ** o)))
        small = rng.random((h // s + 2, w // s + 2))
        im = Image.fromarray((small * 255).astype(np.uint8)).resize((w + s, h + s), Image.BICUBIC)
        acc += amp * np.asarray(im, float)[:h, :w] / 255; tot += amp; amp *= 0.5
    return acc / tot

def save(arr, name, q=88):
    Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8)).save(os.path.join(OUT, name), quality=q)

def grain(h, w, base, dark, freq=30, warp=40, stretch=(1, 8)):
    y, x = np.mgrid[0:h, 0:w].astype(float)
    n = noise(h, w, 64)
    v = np.sin((x / w * freq + n * warp / 10 + noise(h, w, 128) * 3) * np.pi)
    v = (v + 1) / 2
    v = v ** 3
    fine = noise(h, w, 4, 2) * 0.15
    t = np.clip(v * 0.7 + fine, 0, 1)[..., None]
    return np.array(base)[None, None] * (1 - t) + np.array(dark)[None, None] * t

# Multilaminado de pino (paredes y techo): vetas anchas tipo "plywood"
def plywood():
    h = w = 1024
    y, x = np.mgrid[0:h, 0:w].astype(float)
    n = noise(h, w, 200) * 6 + noise(h, w, 60) * 1.5
    rings = np.sin((x / 90 + n) * np.pi * 2 + np.sin(y / 300) * 2)
    rings = (rings + 1) / 2
    rings = np.clip((rings - 0.55) * 3, 0, 1)
    base = np.array([214, 168, 110]); dark = np.array([176, 118, 62])
    img = base * (1 - rings[..., None] * 0.75) + dark * (rings[..., None] * 0.75)
    img *= (0.93 + noise(h, w, 8, 2)[..., None] * 0.12)
    save(img, "plywood.jpg")

def floor():
    h = w = 1024
    img = np.zeros((h, w, 3))
    pw = 128  # 8 tablas
    for i in range(w // pw):
        tone = rng.uniform(0.9, 1.08)
        g = grain(h, pw, [222, 170, 112], [190, 132, 78], freq=6, warp=20) * tone
        off = rng.integers(0, h)
        g = np.roll(g, off, axis=0)
        img[:, i * pw:(i + 1) * pw] = g
        img[:, i * pw:i * pw + 2] *= 0.6
        j = rng.integers(100, h - 100); img[j:j + 2, i * pw:(i + 1) * pw] *= 0.6
    save(img, "floor.jpg")

def cabinet():
    h = w = 512
    img = grain(h, w, [168, 98, 52], [120, 64, 30], freq=10, warp=25)
    save(img, "cabinet.jpg")

def siding():
    h = w = 512
    img = np.ones((h, w, 3)) * np.array([58, 60, 64])
    img *= (0.92 + noise(h, w, 16, 3)[..., None] * 0.14)
    for i in range(0, w, 64):  # listones verticales (board & batten)
        img[:, i:i + 10] = img[:, i:i + 10] * 0.75 + 8
        img[:, i + 10:i + 12] *= 0.55
    save(img, "siding.jpg")

def marble():
    h = w = 1024
    y, x = np.mgrid[0:h, 0:w].astype(float)
    n = noise(h, w, 180) * 8 + noise(h, w, 40) * 2
    v = np.abs(np.sin((x + y) / 160 + n))
    veins = np.clip(1 - v * 9, 0, 1) ** 1.5
    img = np.ones((h, w, 3)) * 240 - veins[..., None] * np.array([120, 120, 125])
    img -= noise(h, w, 30)[..., None] * 12
    for k in range(0, w, 512):  # juntas de baldosa 60x60
        img[:, k:k + 2] = 200; img[k:k + 2, :] = 200
    save(img, "marble.jpg")

def mural():
    w = h = 1024
    im = Image.new("RGB", (w, h), (216, 172, 112))
    d = ImageDraw.Draw(im)
    cols = [(236, 120, 110), (120, 205, 190), (40, 160, 90), (248, 244, 236), (232, 150, 140), (216, 172, 112)]
    pts = [(x, y) for x in range(-128, w + 256, 170) for y in range(-128, h + 256, 150)]
    jit = [(x + rng.integers(-60, 60), y + rng.integers(-60, 60)) for x, y in pts]
    cols_n = len(range(-128, h + 256, 150))
    for i in range(len(jit) - cols_n - 1):
        if (i + 1) % cols_n == 0: continue
        a, b, c, e = jit[i], jit[i + 1], jit[i + cols_n], jit[i + cols_n + 1]
        d.polygon([a, b, c], fill=cols[rng.integers(len(cols))])
        d.polygon([b, e, c], fill=cols[rng.integers(len(cols))])
        d.line([a, b, c, a], fill=(200, 150, 95), width=3)
    im = im.filter(ImageFilter.GaussianBlur(0.8))
    im.save(os.path.join(OUT, "mural.jpg"), quality=88)

def white_planks():
    h = w = 512
    img = np.ones((h, w, 3)) * 244 - noise(h, w, 20)[..., None] * 8
    for j in range(0, h, 64):
        img[j:j + 3] *= 0.82
    save(img, "white_planks.jpg")

def grass():
    h = w = 512
    n = noise(h, w, 40) * 0.6 + noise(h, w, 4, 2) * 0.4
    img = np.stack([70 + n * 60, 110 + n * 70, 40 + n * 30], -1)
    save(img, "grass.jpg")

def roof():
    h = w = 512
    img = np.ones((h, w, 3)) * np.array([45, 47, 50])
    for i in range(0, w, 96):
        img[:, i:i + 6] = np.array([75, 78, 82])
    img *= (0.95 + noise(h, w, 30)[..., None] * 0.1)
    save(img, "roof.jpg")

def deck():
    h = w = 512
    img = np.zeros((h, w, 3))
    for j in range(0, h, 64):
        g = grain(64, w, [92, 88, 84], [64, 60, 58], freq=4, warp=10).transpose(1, 0, 2)
        g = np.asarray(Image.fromarray(g.astype(np.uint8)).resize((w, 64)))
        img[j:j + 64] = g * rng.uniform(0.9, 1.1)
        img[j:j + 4] *= 0.4
    save(img, "deck.jpg")

def rug():
    w, h = 512, 768
    im = Image.new("RGB", (w, h), (150, 60, 50)); d = ImageDraw.Draw(im)
    d.rectangle([20, 20, w - 20, h - 20], outline=(230, 210, 170), width=18)
    d.rectangle([60, 60, w - 60, h - 60], outline=(40, 50, 80), width=10)
    for k in range(6):
        cy = 140 + k * 100
        d.polygon([(w // 2, cy - 45), (w // 2 + 70, cy), (w // 2, cy + 45), (w // 2 - 70, cy)], fill=(230, 210, 170))
        d.polygon([(w // 2, cy - 22), (w // 2 + 35, cy), (w // 2, cy + 22), (w // 2 - 35, cy)], fill=(40, 50, 80))
    im.save(os.path.join(OUT, "rug.jpg"), quality=85)

def chalk():
    h = w = 256
    img = np.ones((h, w, 3)) * 30 + noise(h, w, 10)[..., None] * 14
    save(img, "chalk.jpg")

def bark():
    h = w = 256
    img = grain(h, w, [95, 75, 55], [55, 42, 30], freq=14, warp=30)
    save(img, "bark.jpg")

for f in [plywood, floor, cabinet, siding, marble, mural, white_planks, grass, roof, deck, rug, chalk, bark]:
    f(); print("ok", f.__name__)
