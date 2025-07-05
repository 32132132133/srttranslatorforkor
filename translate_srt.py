#!/usr/bin/env python
"""
translate_srt.py  ── RTX 3080 Ti 전용 오프라인 SRT 번역기
───────────────────────────────────────────────────────────
● 모델 : facebook/m2m100_418M   (.safetensors 로드 → CVE-2025-32434 안전)
● 프리셋
    hi  ─ 줄당(batch=1)  · 최고 품질
    mid ─ batch=4        · 2× 속도
    low ─ batch=8        · 3× 속도(3080 Ti VRAM 8 GB 정도)
● 공통 기능
    ▸ FP16 사용 (VRAM 절감)           ▸ 긴 줄 자동 분할(120자)  
    ▸ 반복 억제(no_repeat, penalty)   ▸ 오버런 시 batch 1로 자동 재시도
    ▸ tqdm 진행률 + ETA

사용 예
    python translate_srt.py in.srt out.srt -i ja -o ko -p mid
───────────────────────────────────────────────────────────
"""

import argparse
import gc
import time
from pathlib import Path

import pysrt
import torch
import tqdm
from transformers import M2M100ForConditionalGeneration, M2M100Tokenizer

# ────────── 전역 상수 ──────────
MODEL_ID = "facebook/m2m100_418M"
DEVICE = torch.device("cuda", 0)        # 3080 Ti GPU 0
MAX_LEN = 400                            # 최대 디코딩 토큰
SPLIT_LEN = 120                          # 한 줄 120자 초과 시 임시 분할
REPEAT_N = 3                             # 3-gram 반복 금지
REPEAT_P = 1.2                           # repetition penalty

# 프리셋 → (batch_size, beam)
PRESET_CFG = {
    "hi": (1, 4),
    "mid": (4, 4),
    "low": (8, 3),
}


# ────────── 유틸 ──────────
def split_long(text: str, limit: int = SPLIT_LEN) -> list[str]:
    if len(text) <= limit:
        return [text]
    chunks, buf = [], ""
    for word in text.split():
        if len(buf) + len(word) + 1 > limit:
            chunks.append(buf.strip())
            buf = ""
        buf += word + " "
    chunks.append(buf.strip())
    return chunks


# ────────── 모델 로드 ──────────
def load_model() -> tuple[M2M100Tokenizer, M2M100ForConditionalGeneration]:
    tok = M2M100Tokenizer.from_pretrained(MODEL_ID)
    mdl = (
        M2M100ForConditionalGeneration.from_pretrained(
            MODEL_ID, use_safetensors=True, low_cpu_mem_usage=False
        )
        .to_empty(device=DEVICE)
        .half()
    )
    return tok, mdl


# ────────── 메인 번역 루프 ──────────
def translate(src: Path, dst: Path, src_lg: str, tgt_lg: str, preset: str) -> None:
    batch_size, beams = PRESET_CFG[preset]
    tok, mdl = load_model()
    tok.src_lang = src_lg
    tgt_id = tok.get_lang_id(tgt_lg)

    subs = pysrt.open(src, encoding="utf-8")
    total, idx = len(subs), 0
    bar = tqdm.tqdm(total=total, unit=" line", desc=f"{preset.upper()} batch={batch_size}")

    while idx < total:
        step = min(batch_size, total - idx)
        group = subs[idx : idx + step]

        # ① 입력 전처리(분할)
        texts, mapping = [], []  # mapping: chunk 갯수 기록
        for s in group:
            parts = split_long(s.text)
            mapping.append(len(parts))
            texts.extend(parts)

        try:
            # ② 추론
            enc = tok(texts, return_tensors="pt", padding=True, truncation=True).to(DEVICE)
            out = mdl.generate(
                **enc,
                forced_bos_token_id=tgt_id,
                max_length=MAX_LEN,
                num_beams=beams,
                no_repeat_ngram_size=REPEAT_N,
                repetition_penalty=REPEAT_P,
            )
            outs = tok.batch_decode(out, skip_special_tokens=True)

            # ③ 결과 합치기(분할 복원)
            k = 0
            for s, parts in zip(group, mapping):
                s.text = " ".join(outs[k : k + parts])
                k += parts

            idx += step
            bar.update(step)

        except RuntimeError as e:
            if "CUDA out of memory" in str(e) and batch_size > 1:
                torch.cuda.empty_cache()
                gc.collect()
                batch_size = 1  # 줄여서 재시도
                continue
            raise

    bar.close()
    subs.save(dst, encoding="utf-8")
    print(f"\n✓ {preset.upper()} preset | Saved → {dst}")


# ────────── CLI ──────────
def cli():
    ap = argparse.ArgumentParser(description="RTX 3080 Ti GPU SRT translator")
    ap.add_argument("src", type=Path)
    ap.add_argument("dst", type=Path)
    ap.add_argument("-i", "--src_lang", default="ja")
    ap.add_argument("-o", "--tgt_lang", default="ko")
    ap.add_argument(
        "-p",
        "--preset",
        choices=["hi", "mid", "low"],
        default="hi",
        help="hi=고급, mid=중급, low=저급",
    )
    args = ap.parse_args()
    t0 = time.time()
    translate(args.src, args.dst, args.src_lang, args.tgt_lang, args.preset)
    print(f"Total time: {time.time() - t0:.1f}s")


if __name__ == "__main__":
    cli()
