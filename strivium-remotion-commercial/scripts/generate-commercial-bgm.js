const fs = require('fs');
const path = require('path');

const sampleRate = 48000;
const durationSec = 79.9;
const totalSamples = Math.floor(sampleRate * durationSec);

const left = new Float32Array(totalSamples);
const right = new Float32Array(totalSamples);

let seed = 123456789;
const rand = () => {
  seed = (1664525 * seed + 1013904223) >>> 0;
  return seed / 0xffffffff;
};

const clamp = (v, min, max) => Math.max(min, Math.min(max, v));

const panGains = (pan) => {
  const p = clamp(pan, -1, 1);
  const angle = (p + 1) * (Math.PI / 4);
  return [Math.cos(angle), Math.sin(angle)];
};

const addMono = (idx, sample, pan = 0) => {
  if (idx < 0 || idx >= totalSamples) return;
  const [lg, rg] = panGains(pan);
  left[idx] += sample * lg;
  right[idx] += sample * rg;
};

const addKick = (startSec, amp = 0.85) => {
  const start = Math.floor(startSec * sampleRate);
  const len = Math.floor(0.22 * sampleRate);
  let phase = 0;
  for (let n = 0; n < len; n++) {
    const idx = start + n;
    if (idx >= totalSamples) break;
    const t = n / sampleRate;
    const env = Math.exp(-t * 24);
    const freq = 160 * Math.exp(-t * 20) + 48;
    phase += (2 * Math.PI * freq) / sampleRate;
    const body = Math.sin(phase) * env;
    const click = (rand() * 2 - 1) * Math.exp(-t * 120);
    addMono(idx, (body * 0.92 + click * 0.08) * amp, 0);
  }
};

const addSnare = (startSec, amp = 0.42) => {
  const start = Math.floor(startSec * sampleRate);
  const len = Math.floor(0.2 * sampleRate);
  let phase = 0;
  for (let n = 0; n < len; n++) {
    const idx = start + n;
    if (idx >= totalSamples) break;
    const t = n / sampleRate;
    const env = Math.exp(-t * 18);
    phase += (2 * Math.PI * 196) / sampleRate;
    const tone = Math.sin(phase) * Math.exp(-t * 26);
    const noise = (rand() * 2 - 1) * env;
    addMono(idx, (noise * 0.8 + tone * 0.2) * amp, 0);
  }
};

const addHat = (startSec, amp = 0.18, pan = 0.2) => {
  const start = Math.floor(startSec * sampleRate);
  const len = Math.floor(0.08 * sampleRate);
  let lp = 0;
  for (let n = 0; n < len; n++) {
    const idx = start + n;
    if (idx >= totalSamples) break;
    const t = n / sampleRate;
    const env = Math.exp(-t * 65);
    const white = rand() * 2 - 1;
    lp = lp * 0.65 + white * 0.35;
    const hp = white - lp;
    addMono(idx, hp * env * amp, pan);
  }
};

const addBassNote = (startSec, freq, noteLenSec, amp = 0.28) => {
  const start = Math.floor(startSec * sampleRate);
  const len = Math.floor(noteLenSec * sampleRate);
  let phase = 0;
  for (let n = 0; n < len; n++) {
    const idx = start + n;
    if (idx >= totalSamples) break;
    const t = n / sampleRate;
    const attack = clamp(t / 0.012, 0, 1);
    const release = clamp((noteLenSec - t) / 0.08, 0, 1);
    const env = attack * release;

    phase += (2 * Math.PI * freq) / sampleRate;
    const s = Math.sin(phase);
    const tri = (2 / Math.PI) * Math.asin(Math.sin(phase));
    addMono(idx, (s * 0.7 + tri * 0.3) * env * amp, -0.08);
  }
};

const addArpNote = (startSec, freq, noteLenSec, amp = 0.11, pan = 0.25) => {
  const start = Math.floor(startSec * sampleRate);
  const len = Math.floor(noteLenSec * sampleRate);
  let phase = 0;
  let phase2 = 0;
  for (let n = 0; n < len; n++) {
    const idx = start + n;
    if (idx >= totalSamples) break;
    const t = n / sampleRate;
    const attack = clamp(t / 0.008, 0, 1);
    const release = clamp((noteLenSec - t) / 0.05, 0, 1);
    const env = attack * release;

    phase += (2 * Math.PI * freq) / sampleRate;
    phase2 += (2 * Math.PI * freq * 1.005) / sampleRate;
    const tri = (2 / Math.PI) * Math.asin(Math.sin(phase));
    const sin2 = Math.sin(phase2);
    addMono(idx, (tri * 0.72 + sin2 * 0.28) * env * amp, pan);
  }
};

const addPadNote = (startSec, freq, noteLenSec, amp = 0.08, pan = 0) => {
  const start = Math.floor(startSec * sampleRate);
  const len = Math.floor(noteLenSec * sampleRate);
  let phase1 = 0;
  let phase2 = 0;
  let phase3 = 0;
  for (let n = 0; n < len; n++) {
    const idx = start + n;
    if (idx >= totalSamples) break;
    const t = n / sampleRate;
    const attack = clamp(t / 0.25, 0, 1);
    const release = clamp((noteLenSec - t) / 0.45, 0, 1);
    const env = attack * release;

    phase1 += (2 * Math.PI * freq) / sampleRate;
    phase2 += (2 * Math.PI * freq * 0.997) / sampleRate;
    phase3 += (2 * Math.PI * freq * 2) / sampleRate;

    const blend =
      Math.sin(phase1) * 0.58 +
      Math.sin(phase2) * 0.27 +
      Math.sin(phase3) * 0.15;

    addMono(idx, blend * env * amp, pan);
  }
};

const tempo = 126;
const beat = 60 / tempo;
const bar = beat * 4;

const progression = [
  { bass: 55.0, chord: [220.0, 261.63, 329.63] },
  { bass: 43.65, chord: [174.61, 220.0, 261.63] },
  { bass: 65.41, chord: [261.63, 329.63, 392.0] },
  { bass: 49.0, chord: [196.0, 246.94, 293.66] },
];

const arpPattern = [0, 1, 2, 1, 0, 2, 1, 2];

const bars = Math.ceil(durationSec / bar);
for (let barIndex = 0; barIndex < bars; barIndex++) {
  const barStart = barIndex * bar;
  const step = progression[barIndex % progression.length];

  step.chord.forEach((freq, i) => {
    addPadNote(barStart, freq, bar * 0.96, 0.065, -0.2 + i * 0.2);
    addPadNote(barStart, freq * 2, bar * 0.8, 0.025, 0.2 - i * 0.2);
  });

  for (let b = 0; b < 4; b++) {
    const beatStart = barStart + b * beat;
    addKick(beatStart, b === 0 ? 0.92 : 0.82);

    if (b === 1 || b === 3) {
      addSnare(beatStart, 0.45);
    }

    addBassNote(beatStart, step.bass * (b === 2 ? 1.12 : 1), beat * 0.92, 0.29);

    const offBeat = beatStart + beat * 0.5;
    addHat(offBeat, 0.15, 0.35);
    addHat(beatStart + beat * 0.75, 0.12, -0.35);

    for (let s = 0; s < 2; s++) {
      const subStart = beatStart + s * (beat / 2);
      const idx = (barIndex * 8 + b * 2 + s) % arpPattern.length;
      const note = step.chord[arpPattern[idx]];
      const octaveBoost = (barIndex + b + s) % 2 === 0 ? 2 : 1;
      const pan = s === 0 ? -0.22 : 0.22;
      addArpNote(subStart, note * octaveBoost, beat * 0.45, 0.105, pan);
    }
  }
}

for (let i = 0; i < totalSamples; i++) {
  const t = i / sampleRate;

  const fadeIn = clamp(t / 1.6, 0, 1);
  const fadeOut = clamp((durationSec - t) / 2.4, 0, 1);
  const masterFade = fadeIn * fadeOut;

  const sidechain = 1 - 0.2 * Math.exp(-(t % beat) * 16);

  left[i] *= masterFade * sidechain;
  right[i] *= masterFade * sidechain;

  left[i] = Math.tanh(left[i] * 1.35);
  right[i] = Math.tanh(right[i] * 1.35);
}

let peak = 0;
for (let i = 0; i < totalSamples; i++) {
  const a = Math.abs(left[i]);
  const b = Math.abs(right[i]);
  if (a > peak) peak = a;
  if (b > peak) peak = b;
}
const targetPeak = 0.88;
const gain = peak > 0 ? targetPeak / peak : 1;

const buffer = Buffer.alloc(totalSamples * 4);
for (let i = 0; i < totalSamples; i++) {
  const l = clamp(left[i] * gain, -1, 1);
  const r = clamp(right[i] * gain, -1, 1);
  const li = Math.round(l * 32767);
  const ri = Math.round(r * 32767);
  buffer.writeInt16LE(li, i * 4);
  buffer.writeInt16LE(ri, i * 4 + 2);
}

const dataSize = buffer.length;
const header = Buffer.alloc(44);
header.write('RIFF', 0);
header.writeUInt32LE(36 + dataSize, 4);
header.write('WAVE', 8);
header.write('fmt ', 12);
header.writeUInt32LE(16, 16);
header.writeUInt16LE(1, 20);
header.writeUInt16LE(2, 22);
header.writeUInt32LE(sampleRate, 24);
header.writeUInt32LE(sampleRate * 4, 28);
header.writeUInt16LE(4, 32);
header.writeUInt16LE(16, 34);
header.write('data', 36);
header.writeUInt32LE(dataSize, 40);

const outputPath = path.resolve(
  __dirname,
  '..',
  'public',
  'strivium-commercial-bgm-animated.wav',
);

fs.writeFileSync(outputPath, Buffer.concat([header, buffer]));
console.log(`Created ${outputPath}`);
console.log(`Duration: ${durationSec}s | Samples: ${totalSamples} | Peak gain: ${gain.toFixed(4)}`);
