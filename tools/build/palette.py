# -*- coding: utf-8 -*-
"""4分野の色が「見分けられるか」を測る。目視では判定できないので必ず機械で通す。

   OKLab に変換して、色覚型（1型・2型・3型）をシミュレートしたうえで
   全ペアの距離を測る。判定の基準は dataviz の検証器に合わせている。

     通常視 ΔE < 15   … 落とす（色覚に関係なく見分けにくい）
     色覚型 ΔE < 6    … 警告（ラベルなど色以外の手掛かりが必須）
"""
import re, sys, os, itertools, math

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
TPL = os.path.join(ROOT, 'app', 'template.html')
NAMES = ['法令', '貸付実務', '資金需要者保護', '財務会計']
NV_FLOOR, CVD_FLOOR = 15.0, 6.0


def srgb_to_lin(c):
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


def hex_to_oklab(h):
    r, g, b = (srgb_to_lin(int(h[i:i + 2], 16) / 255) for i in (1, 3, 5))
    l = (0.4122214708 * r + 0.5363325363 * g + 0.0514459929 * b) ** (1 / 3)
    m = (0.2119034982 * r + 0.6806995451 * g + 0.1073969566 * b) ** (1 / 3)
    s = (0.0883024619 * r + 0.2817188376 * g + 0.6299787005 * b) ** (1 / 3)
    return (0.2104542553 * l + 0.7936177850 * m - 0.0040720468 * s,
            1.9779984951 * l - 2.4285922050 * m + 0.4505937099 * s,
            0.0259040371 * l + 0.7827717662 * m - 0.8086757660 * s)


# Brettel/Viénot 系の簡易 LMS 変換で色覚型をシミュレートする
def simulate(h, kind):
    r, g, b = (srgb_to_lin(int(h[i:i + 2], 16) / 255) for i in (1, 3, 5))
    L = 0.31399022 * r + 0.63951294 * g + 0.04649755 * b
    M = 0.15537241 * r + 0.75789446 * g + 0.08670142 * b
    S = 0.01775239 * r + 0.10944209 * g + 0.87256922 * b
    if kind == 'protan':
        L = 1.05118294 * M - 0.05116099 * S
    elif kind == 'deutan':
        M = 0.9513092 * L + 0.04866992 * S
    else:
        S = -0.86744736 * L + 1.86727089 * M
    r2 = 5.47221206 * L - 4.6419601 * M + 0.16963708 * S
    g2 = -1.1252419 * L + 2.29317094 * M - 0.1678952 * S
    b2 = 0.02980165 * L - 0.19318073 * M + 1.16364789 * S
    f = lambda u: max(0, min(1, u))
    g_ = lambda u: 12.92 * u if u <= 0.0031308 else 1.055 * (u ** (1 / 2.4)) - 0.055
    return '#' + ''.join(f'{round(f(g_(f(x))) * 255):02X}' for x in (r2, g2, b2))


def dE(a, b):
    A, B = hex_to_oklab(a), hex_to_oklab(b)
    return 100 * math.dist(A, B)


def palette_of(block):
    m = dict(re.findall(r'--(pri|acc|ok|vio):(#[0-9A-Fa-f]{6})', block))
    return [m.get('pri'), m.get('acc'), m.get('ok'), m.get('vio')]


def main():
    src = open(TPL, encoding='utf-8').read()
    css = src.split('<style>', 1)[1].split('</style>', 1)[0]
    light = palette_of(css.split(':root{', 1)[1].split('}', 1)[0])
    dark = palette_of(css.split('@media (prefers-color-scheme:dark){:root{', 1)[1].split('}', 1)[0])

    fails, warns = [], []
    for mode, pal in [('ライト', light), ('ダーク', dark)]:
        if not all(pal):
            fails.append(f'{mode}: 4色を読み取れない {pal}')
            continue
        print(f'■ {mode}　' + '　'.join(f'{n} {c}' for n, c in zip(NAMES, pal)))
        worst_nv = (99, '')
        worst_cvd = (99, '', '')
        for (i, a), (j, b) in itertools.combinations(list(enumerate(pal)), 2):
            nv = dE(a, b)
            if nv < worst_nv[0]:
                worst_nv = (nv, f'{NAMES[i]}↔{NAMES[j]}')
            for kind in ('protan', 'deutan', 'tritan'):
                d = dE(simulate(a, kind), simulate(b, kind))
                if d < worst_cvd[0]:
                    worst_cvd = (d, f'{NAMES[i]}↔{NAMES[j]}', kind)
        print(f'   通常視の最小 ΔE {worst_nv[0]:.1f}（{worst_nv[1]}）'
              f'　色覚型の最小 ΔE {worst_cvd[0]:.1f}（{worst_cvd[1]} / {worst_cvd[2]}）')
        if worst_nv[0] < NV_FLOOR:
            fails.append(f'{mode}: {worst_nv[1]} が通常視で ΔE {worst_nv[0]:.1f}（下限 {NV_FLOOR}）')
        if worst_cvd[0] < CVD_FLOOR:
            warns.append(f'{mode}: {worst_cvd[1]} が {worst_cvd[2]} で ΔE {worst_cvd[0]:.1f}'
                         f'（色以外の手掛かりが必須）')

    for w in warns:
        print('   ⚠', w)
    if fails:
        for f in fails:
            print('   ✗', f)
        return 1
    print('   分野の色はすべて見分けられる。'
          + ('警告あり（各色には必ず分野名を添えている）' if warns else ''))
    return 0


if __name__ == '__main__':
    sys.exit(main())
