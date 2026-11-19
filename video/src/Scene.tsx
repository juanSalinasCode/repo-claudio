import React from "react";
import { AbsoluteFill, interpolate, random, useCurrentFrame } from "remotion";
import { Character } from "./Character";

const OUT = "#1a0a2e";

const Aura: React.FC<{ power: number; t: number }> = ({ power, t }) => {
  const N = 26;
  const pts: string[] = [];
  for (let i = 0; i < N * 2; i++) {
    const a = (Math.PI * 2 * i) / (N * 2);
    const spike = i % 2 === 0;
    const r =
      (spike ? 520 + random(`a${i}`) * 220 : 340) * (0.55 + power * 0.65) +
      Math.sin(t * 0.5 + i) * 14;
    pts.push(`${(Math.cos(a) * r).toFixed(1)},${(Math.sin(a) * r * 1.15).toFixed(1)}`);
  }
  return (
    <g opacity={Math.min(1, power * 1.6)}>
      <polygon points={pts.join(" ")} fill="url(#aura)" filter="url(#soft)" />
      <polygon
        points={pts.map((p) => p.split(",").map((v) => (parseFloat(v) * 0.82).toFixed(1)).join(",")).join(" ")}
        fill="#e6ff6a"
        opacity={0.35}
      />
    </g>
  );
};

const Bolt: React.FC<{ seed: string; power: number }> = ({ seed, power }) => {
  const a = random(seed) * Math.PI * 2;
  const r0 = 430 + random(seed + "r") * 130;
  let x = Math.cos(a) * r0;
  let y = Math.sin(a) * r0;
  let d = `M ${x.toFixed(1)},${y.toFixed(1)}`;
  for (let k = 0; k < 6; k++) {
    x += Math.cos(a) * 70 + (random(seed + k) - 0.5) * 70;
    y += Math.sin(a) * 70 + (random(seed + k + "y") - 0.5) * 70;
    d += ` L ${x.toFixed(1)},${y.toFixed(1)}`;
  }
  return (
    <g opacity={power}>
      <path d={d} stroke={OUT} strokeWidth={20} fill="none" strokeLinecap="round" strokeLinejoin="round" />
      <path d={d} stroke="#fff6a8" strokeWidth={9} fill="none" strokeLinecap="round" strokeLinejoin="round" />
    </g>
  );
};

export const Scene: React.FC = () => {
  const frame = useCurrentFrame();
  const power = interpolate(frame, [28, 76], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });
  const flash = interpolate(frame, [74, 78, 92], [0, 0.95, 0], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });
  const textIn = interpolate(frame, [76, 90], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  // temblor mientras sube el poder
  const shake = frame > 28 ? 4 + power * 16 : 0;
  const sx = (random(`sx${frame}`) - 0.5) * shake;
  const sy = (random(`sy${frame}`) - 0.5) * shake;
  const scale = 0.78 + power * 0.12 + (frame > 78 ? Math.sin(frame * 0.5) * 0.012 : 0);

  const bgA = power > 0.05 ? "#1d7a3a" : "#4a2a8a";
  const bgB = power > 0.05 ? "#0b2d1d" : "#150a33";

  const rays = Array.from({ length: 36 }, (_, i) => {
    const a = (Math.PI * 2 * i) / 36 + frame * 0.004;
    const w = 0.07 + random(`r${i}`) * 0.06;
    const R = 2200;
    return `${(Math.cos(a - w) * R).toFixed(0)},${(Math.sin(a - w) * R).toFixed(0)} ${(Math.cos(a + w) * R).toFixed(0)},${(Math.sin(a + w) * R).toFixed(0)}`;
  });

  return (
    <AbsoluteFill style={{ background: "#0b0620" }}>
      <svg width={1080} height={1920} viewBox="0 0 1080 1920">
        <defs>
          <radialGradient id="bg" cx="50%" cy="52%" r="75%">
            <stop offset="0%" stopColor={bgA} />
            <stop offset="100%" stopColor={bgB} />
          </radialGradient>
          <radialGradient id="aura" cx="50%" cy="50%" r="50%">
            <stop offset="0%" stopColor="#f6ff7a" />
            <stop offset="55%" stopColor="#5df06a" />
            <stop offset="100%" stopColor="#12a84a" stopOpacity={0.2} />
          </radialGradient>
          <pattern id="dots" width="26" height="26" patternUnits="userSpaceOnUse" patternTransform="rotate(30)">
            <circle cx="13" cy="13" r="4.5" fill="#000" opacity="0.28" />
          </pattern>
          <filter id="soft" x="-30%" y="-30%" width="160%" height="160%">
            <feGaussianBlur stdDeviation="9" />
          </filter>
        </defs>

        <rect width="1080" height="1920" fill="url(#bg)" />
        <g transform="translate(540,930)" opacity={0.20 + power * 0.28}>
          {rays.map((p, i) => (
            <polygon key={i} points={`0,0 ${p}`} fill={i % 2 ? "#f6ff7a" : "#7dff9a"} />
          ))}
        </g>
        <rect width="1080" height="1920" fill="url(#dots)" />

        <g transform={`translate(${540 + sx},${1020 + sy}) scale(${scale})`}>
          <Aura power={power} t={frame} />
          <Character power={power} />
          {Array.from({ length: 5 }, (_, i) => (
            <Bolt key={i} seed={`b${i}-${Math.floor(frame / 3)}`} power={power > 0.4 ? 1 : 0} />
          ))}
        </g>

        {/* líneas de velocidad */}
        <g stroke="#fffbe0" strokeLinecap="round" opacity={0.15 + power * 0.55}>
          {Array.from({ length: 22 }, (_, i) => {
            const a = (Math.PI * 2 * i) / 22 + random(`s${i}`) * 0.2;
            const r1 = 560 + random(`s1${i}`) * 140;
            const r2 = r1 + 120 + random(`s2${i}`) * 260;
            return (
              <line
                key={i}
                x1={540 + Math.cos(a) * r1}
                y1={930 + Math.sin(a) * r1 * 1.3}
                x2={540 + Math.cos(a) * r2}
                y2={930 + Math.sin(a) * r2 * 1.3}
                strokeWidth={4 + random(`s3${i}`) * 8}
              />
            );
          })}
        </g>

        {/* globo superior */}
        <g transform={`translate(540,210) rotate(-4) scale(${0.6 + textIn * 0.4})`} opacity={textIn}>
          <path
            d="M -330,-70 L -270,-110 L -210,-70 L -140,-120 L -70,-72 L 0,-125 L 70,-72 L 140,-120 L 210,-70 L 270,-110 L 330,-70 L 300,0 L 340,70 L 270,60 L 210,110 L 140,62 L 70,112 L 0,62 L -70,110 L -140,62 L -210,110 L -270,60 L -340,70 L -300,0 Z"
            fill="#fff35c"
            stroke={OUT}
            strokeWidth={12}
            strokeLinejoin="round"
          />
          <text x={0} y={22} textAnchor="middle" fontFamily="Inter Display, Inter, sans-serif" fontWeight={900} fontSize={84} fill="#d1141c" stroke={OUT} strokeWidth={5} paintOrder="stroke">
            ¡¡GRAAAAH!!
          </text>
        </g>

        {/* grito */}
        <g transform={`translate(540,1690) rotate(-5) scale(${0.5 + textIn * 0.5})`} opacity={textIn}>
          <text x={8} y={14} textAnchor="middle" fontFamily="Inter Display, Inter, sans-serif" fontWeight={900} fontSize={124} fill="#12a84a" stroke={OUT} strokeWidth={28} strokeLinejoin="round" paintOrder="stroke">
            LAKAROTOOO!
          </text>
          <text x={0} y={0} textAnchor="middle" fontFamily="Inter Display, Inter, sans-serif" fontWeight={900} fontSize={124} fill="#ffe94a" stroke={OUT} strokeWidth={22} strokeLinejoin="round" paintOrder="stroke">
            LAKAROTOOO!
          </text>
        </g>

        <rect width="1080" height="1920" fill="#ffffff" opacity={flash} />
      </svg>
    </AbsoluteFill>
  );
};
