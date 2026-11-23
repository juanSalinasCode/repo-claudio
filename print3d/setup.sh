#!/usr/bin/env bash
# Instala el kit de impresión 3D en el contenedor (Ubuntu 24.04). Idempotente.
#   - Blender 4.0 (apt, CLI `blender -b`) + Blender 5.3 como módulo Python (bpy) en /opt/3d/venv
#   - UltiMaker Cura 5.14 (AppImage extraída en /opt/3d/cura: CuraEngine + perfiles)
#   - PrusaSlicer 2.7 (apt, alternativa/verificación)
#   - Mesa/EGL para renders sin GPU
set -euo pipefail
CURA_VERSION="${CURA_VERSION:-5.14.0}"
mkdir -p /opt/3d

if ! command -v blender >/dev/null || ! command -v prusa-slicer >/dev/null; then
  apt-get update -qq
  DEBIAN_FRONTEND=noninteractive apt-get install -y -qq blender prusa-slicer xvfb \
    libegl1 libgl1-mesa-dri libgles2 libegl-mesa0 >/dev/null
fi

if [ ! -x /opt/3d/venv/bin/python ] || ! /opt/3d/venv/bin/python -c "import bpy" 2>/dev/null; then
  python3 -m venv /opt/3d/venv
  /opt/3d/venv/bin/pip install -q bpy trimesh manifold3d numpy-stl scipy networkx rtree
fi

if [ ! -x /opt/3d/cura/CuraEngine ]; then
  cd /opt/3d
  curl -sSL --retry 4 -o Cura.AppImage \
    "https://github.com/Ultimaker/Cura/releases/download/${CURA_VERSION}/UltiMaker-Cura-${CURA_VERSION}-linux-X64.AppImage"
  chmod +x Cura.AppImage
  ./Cura.AppImage --appimage-extract >/dev/null
  rm -rf cura && mv squashfs-root cura && rm -f Cura.AppImage
fi

echo "Blender apt: $(blender --version 2>/dev/null | head -1)"
echo "bpy venv:    $(/opt/3d/venv/bin/python -c 'import bpy;print(bpy.app.version_string)' 2>/dev/null)"
echo "Cura:        $(ls /opt/3d/cura/share/cura/resources/definitions/creality_ender3v2neo.def.json)"
echo "PrusaSlicer: $(prusa-slicer --help 2>&1 | head -1)"
