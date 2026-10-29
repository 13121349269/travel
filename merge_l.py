# -*- coding: utf-8 -*-
"""合并 quotes_l1~l5 到 data/national.json。仅给原本无 q 的条目挂评价，局部指纹防重。"""
import json, re, sys

BASE = r'D:/workbuddy_work/2026-10-20-18-09-55/travel-site'
BATCH_DIR = r'D:/workbuddy_work/2026-10-20-18-09-55/outputs/expansion'

def norm(s):
    for suf in sorted(['风景名胜区','旅游度假区','旅游区','风景区','景区','博物馆','纪念馆','森林公园','公园'], key=len, reverse=True):
        if s.endswith(suf) and len(s) > len(suf)+1:
            s = s[:-len(suf)]; break
    for pre in ['北京市','上海市','天津市','重庆市','广西壮族自治区','新疆维吾尔自治区','宁夏回族自治区','内蒙古自治区','西藏自治区']:
        if s.startswith(pre): s = s[len(pre):]; break
    return s

def fmt(items):
    html = ''
    for it in items:
        t = re.sub(r'\s+', ' ', it.get('text','')).strip()
        if not t: continue
        src = it.get('src','网友'); rating = it.get('rating','')
        html += f"<p><b>{src}</b>{' ⭐'+rating if rating else ''}：{t}</p>"
    return html

def main():
    data = json.load(open(BASE+'/data/national.json', encoding='utf-8'))
    # 索引：exact (p,n) + norm fallback（仅限无q条目）
    by_exact = {(x['p'], x['n']): x for x in data if not x.get('q')}
    by_norm = {}
    for x in data:
        if not x.get('q'):
            by_norm.setdefault((x['p'], norm(x['n'])), x)

    stats = {'exact':0,'norm':0,'miss':[]}
    seen_texts = {}  # 局部指纹防重：key=(挂载目标, 前20字)
    for b in range(1, 6):
        try:
            batch = json.load(open(f'{BATCH_DIR}/quotes_l{b}.json', encoding='utf-8'))
        except FileNotFoundError:
            print(f'quotes_l{b}.json 缺失，跳过'); continue
        for entry in batch:
            name = entry['name'].strip()
            items = entry.get('items') or []
            html = fmt(items)
            if not html: continue
            tgt = None
            # exact：全国范围查 (省未知→按名称全局) — 批次无省字段，先全局按 n exact 匹配所有无q条目
            cands = [x for x in data if not x.get('q') and x['n'] == name]
            if len(cands) == 1:
                tgt = cands[0]; stats['exact'] += 1
            else:
                if len(cands) > 1:
                    # 多省同名：按批次 todo 文件找省
                    prov = None
                    for pb in range(1, 6):
                        try:
                            td = json.load(open(f'{BATCH_DIR}/todo_l{pb}.json', encoding='utf-8'))
                        except FileNotFoundError: continue
                        for t in td:
                            if t['n'] == name: prov = t['p']; break
                        if prov: break
                    cands = [x for x in cands if x['p'] == prov]
                    if len(cands) == 1:
                        tgt = cands[0]; stats['exact'] += 1
                if tgt is None:
                    nc = [x for x in data if not x.get('q') and norm(x['n']) == norm(name)]
                    if len(nc) == 1:
                        tgt = nc[0]; stats['norm'] += 1
            if tgt is None:
                stats['miss'].append(name); continue
            if tgt.get('q'):  # 已挂过（跨批次重复名）
                stats['miss'].append(name + '(dup)'); continue
            fp = html[:20]
            if (id(tgt), fp) in seen_texts: continue
            seen_texts[(id(tgt), fp)] = 1
            tgt['q'] = html
    json.dump(data, open(BASE+'/data/national.json','w',encoding='utf-8'), ensure_ascii=False)
    wq = sum(1 for x in data if x.get('q'))
    print(f"挂载: exact={stats['exact']} norm={stats['norm']} 未匹配={len(stats['miss'])}")
    if stats['miss']: print('miss:', stats['miss'][:30])
    a5q = sum(1 for x in data if x.get('l')=='5A' and x.get('q'))
    a4q = sum(1 for x in data if x.get('l')=='4A' and x.get('q'))
    print(f'总带评价 {wq} | 5A {a5q}/357 | 4A {a4q}/953')

if __name__ == '__main__':
    main()
