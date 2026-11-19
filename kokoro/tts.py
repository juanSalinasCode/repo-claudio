#!/usr/bin/env python3
"""Texto a voz con Kokoro-82M (versión ONNX).

Ejemplos:
  python kokoro/tts.py "Hola, ¿cómo estás?"
  python kokoro/tts.py -f guion.txt -v em_alex -s 1.1 -o audio/guion.mp3
  python kokoro/tts.py --voces

Voces en español: ef_dora (mujer), em_alex (hombre), em_santa (hombre).
Instalación previa: bash kokoro/setup.sh
"""
import argparse
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

import soundfile as sf
from kokoro_onnx import Kokoro

MODELS = Path(os.environ.get("KOKORO_MODELS", Path.home() / "kokoro-models"))


def main() -> None:
    ap = argparse.ArgumentParser(description="Texto a voz con Kokoro")
    ap.add_argument("texto", nargs="?", help="texto a leer")
    ap.add_argument("-f", "--archivo", help="leer el texto desde un archivo")
    ap.add_argument("-v", "--voz", default="ef_dora", help="voz (por defecto ef_dora)")
    ap.add_argument("-s", "--velocidad", type=float, default=1.0, help="0.5 a 2.0")
    ap.add_argument("-l", "--idioma", default="es", help="es, en-us, en-gb, fr-fr, it, pt-br...")
    ap.add_argument("-o", "--salida", default="audio/salida.mp3", help=".mp3 o .wav")
    ap.add_argument("--voces", action="store_true", help="listar voces y salir")
    a = ap.parse_args()

    k = Kokoro(str(MODELS / "kokoro-v1.0.onnx"), str(MODELS / "voices-v1.0.bin"))
    if a.voces:
        print("\n".join(k.get_voices()))
        return

    texto = Path(a.archivo).read_text(encoding="utf-8") if a.archivo else a.texto
    if not texto:
        ap.error("pasa un texto o -f archivo")

    audio, sr = k.create(texto, voice=a.voz, speed=a.velocidad, lang=a.idioma)
    out = Path(a.salida)
    out.parent.mkdir(parents=True, exist_ok=True)

    if out.suffix.lower() == ".mp3" and shutil.which("ffmpeg"):
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
            sf.write(tmp.name, audio, sr)
        subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", tmp.name, "-b:a", "96k", str(out)], check=True)
        os.unlink(tmp.name)
    else:
        if out.suffix.lower() == ".mp3":
            out = out.with_suffix(".wav")
            print("ffmpeg no está instalado; guardo en WAV", file=sys.stderr)
        sf.write(str(out), audio, sr)

    print(f"{out} ({len(audio) / sr:.1f} s, voz {a.voz})")


if __name__ == "__main__":
    main()
