#!/usr/bin/env bash
# Instala Kokoro TTS (versión ONNX) en esta máquina: venv con Python 3.12 + modelo (~350 MB).
# Uso: bash kokoro/setup.sh
set -euo pipefail

VENV="${KOKORO_VENV:-$HOME/kokoro-venv}"
MODELS="${KOKORO_MODELS:-$HOME/kokoro-models}"
BASE="https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0"

# espeak-ng (fonemas); en Linux con apt
if ! command -v espeak-ng >/dev/null 2>&1 && command -v apt-get >/dev/null 2>&1; then
  apt-get install -y -qq espeak-ng || (apt-get update -qq && apt-get install -y -qq espeak-ng)
fi

# Python 3.12 (kokoro no soporta 3.13 todavía)
PY=$(command -v python3.12 || true)
if [ ! -x "$VENV/bin/python" ]; then
  if command -v uv >/dev/null 2>&1; then
    uv venv -q -p "${PY:-3.12}" "$VENV"
  else
    "${PY:?Se necesita python3.12}" -m venv "$VENV"
  fi
fi
if command -v uv >/dev/null 2>&1; then
  VIRTUAL_ENV="$VENV" uv pip install -q kokoro-onnx soundfile
else
  "$VENV/bin/pip" install -q kokoro-onnx soundfile
fi

mkdir -p "$MODELS"
for f in kokoro-v1.0.onnx voices-v1.0.bin; do
  [ -s "$MODELS/$f" ] || curl -sSL -o "$MODELS/$f" "$BASE/$f"
done

echo "Kokoro listo. Prueba: $VENV/bin/python kokoro/tts.py \"Hola mundo\""
