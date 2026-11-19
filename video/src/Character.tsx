import React from "react";
import { random } from "remotion";

const OUT = "#1a0a2e";
const SKIN = "#e9a56b";
const SKIN_D = "#c97f47";

const mix = (a: string, b: string, t: number) => {
  const pa = [1, 3, 5].map((i) => parseInt(a.slice(i, i + 2), 16));
  const pb = [1, 3, 5].map((i) => parseInt(b.slice(i, i + 2), 16));
  const c = pa.map((v, i) => Math.round(v + (pb[i] - v) * t));
  return `rgb(${c[0]},${c[1]},${c[2]})`;
};

/** Personaje caricaturesco original. power: 0 = normal, 1 = transformado. */
export const Character: React.FC<{ power: number }> = ({ power }) => {
  const hair = mix("#24331c", "#ffe94a", Math.min(1, power * 1.4));
  const hairOut = OUT;

  // Pelo: pocos picos gruesos que crecen con el poder
  const N = 7;
  const pts: string[] = [];
  for (let i = 0; i < N; i++) {
    const a = Math.PI * (1.06 + (0.88 * (i + 0.5)) / N);
    const len = 110 + 210 * power + random(`h${i}`) * 70 * (0.4 + power);
    pts.push(
      `${(Math.cos(a) * (150 + len * 0.45) + (i - 3) * 10).toFixed(1)},${(Math.sin(a) * (165 + len)).toFixed(1)}`
    );
    const v = Math.PI * (1.06 + (0.88 * (i + 1)) / N);
    if (i < N - 1)
      pts.push(`${(Math.cos(v) * 150).toFixed(1)},${(Math.sin(v) * 165).toFixed(1)}`);
  }
  const hairPath = `M -140,10 L -150,-60 L ${pts.join(" L ")} L 150,-60 L 140,10 C 70,-75 -70,-75 -140,10 Z`;

  // Brazos: codo y puño
  const arm = (s: 1 | -1) => (
    <g>
      <polyline
        points={`${s * 255},-120 ${s * 430},-40 ${s * 395},110`}
        fill="none"
        stroke={OUT}
        strokeWidth={168}
        strokeLinecap="round"
        strokeLinejoin="round"
      />
      <polyline
        points={`${s * 255},-120 ${s * 430},-40 ${s * 395},110`}
        fill="none"
        stroke={SKIN}
        strokeWidth={140}
        strokeLinecap="round"
        strokeLinejoin="round"
      />
      <ellipse cx={s * 430} cy={-30} rx={44} ry={30} fill={SKIN_D} opacity={0.5} />
      <circle cx={s * 395} cy={150} r={78} fill={SKIN} stroke={OUT} strokeWidth={14} />
      <path
        d={`M ${s * 360},130 Q ${s * 395},112 ${s * 430},130 M ${s * 356},158 Q ${s * 395},140 ${s * 434},158`}
        stroke={OUT}
        strokeWidth={8}
        fill="none"
        strokeLinecap="round"
      />
    </g>
  );

  return (
    <g>
      {/* piernas */}
      <g stroke={OUT} strokeWidth={14} strokeLinejoin="round">
        <rect x={-150} y={190} width={125} height={175} rx={38} fill={SKIN} />
        <rect x={25} y={190} width={125} height={175} rx={38} fill={SKIN} />
        <ellipse cx={-92} cy={382} rx={92} ry={36} fill="#3b2a55" />
        <ellipse cx={92} cy={382} rx={92} ry={36} fill="#3b2a55" />
      </g>
      {/* short */}
      <path
        d="M -215,120 L 215,120 L 235,265 L 150,285 L 100,235 L 40,270 L 0,235 L -40,270 L -100,235 L -150,285 L -235,265 Z"
        fill="#6a3fb3"
        stroke={OUT}
        strokeWidth={14}
        strokeLinejoin="round"
      />
      <rect x={-215} y={108} width={430} height={44} rx={14} fill="#ffd23f" stroke={OUT} strokeWidth={14} />

      {arm(-1)}
      {arm(1)}

      {/* torso */}
      <path
        d="M -285,-175 Q -330,-20 -205,125 L 205,125 Q 330,-20 285,-175 Q 0,-265 -285,-175 Z"
        fill={SKIN}
        stroke={OUT}
        strokeWidth={14}
        strokeLinejoin="round"
      />
      <path
        d="M -150,-95 Q -75,-45 -8,-95 M 8,-95 Q 75,-45 150,-95 M 0,-110 L 0,100 M -95,15 L 95,15 M -80,70 L 80,70"
        stroke={SKIN_D}
        strokeWidth={9}
        fill="none"
        strokeLinecap="round"
      />

      {/* cabeza */}
      <g transform="translate(0,-285)">
        <path d={hairPath} fill={hair} stroke={hairOut} strokeWidth={13} strokeLinejoin="round" />
        <ellipse cx={0} cy={-8} rx={146} ry={156} fill={hair} stroke={hairOut} strokeWidth={13} />
        <ellipse cx={0} cy={0} rx={120} ry={136} fill={SKIN} stroke={OUT} strokeWidth={14} />
        {/* flequillo */}
        <path
          d="M -118,-30 A 120 136 0 0 1 118,-30 L 96,-62 L 62,-38 L 30,-84 L -6,-44 L -40,-86 L -76,-46 Z"
          fill={hair}
          stroke={hairOut}
          strokeWidth={11}
          strokeLinejoin="round"
        />
        {/* ojos en blanco */}
        <path d="M -92,-20 L -18,-4 L -22,30 L -88,22 Z" fill="#fffbe0" stroke={OUT} strokeWidth={9} strokeLinejoin="round" />
        <path d="M 92,-20 L 18,-4 L 22,30 L 88,22 Z" fill="#fffbe0" stroke={OUT} strokeWidth={9} strokeLinejoin="round" />
        {/* cejas furiosas */}
        <path d="M -110,-52 L -12,-18" stroke={OUT} strokeWidth={22} strokeLinecap="round" />
        <path d="M 110,-52 L 12,-18" stroke={OUT} strokeWidth={22} strokeLinecap="round" />
        {/* nariz */}
        <path d="M -8,28 Q 0,48 12,38" stroke={SKIN_D} strokeWidth={9} fill="none" strokeLinecap="round" />
        {/* boca: sonrisa enorme con dientes */}
        <path d="M -78,68 Q 0,140 78,68 Q 0,88 -78,68 Z" fill="#5a0f1c" stroke={OUT} strokeWidth={10} strokeLinejoin="round" />
        <path d="M -60,76 Q 0,112 60,76 L 60,86 Q 0,118 -60,86 Z" fill="#fffbe0" />
        {/* vena de la frente */}
        <path
          d={`M 60,-95 q 12,18 -2,30 q -12,12 4,26`}
          stroke="#b0442a"
          strokeWidth={8}
          fill="none"
          strokeLinecap="round"
          opacity={0.4 + power * 0.6}
        />
        {/* gota de sudor cómica */}
        <path d="M -150,-70 q 22,34 0,50 q -22,-16 0,-50 Z" fill="#aee8ff" stroke={OUT} strokeWidth={7} />
      </g>
    </g>
  );
};
