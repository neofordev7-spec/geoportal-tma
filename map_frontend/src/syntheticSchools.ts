import type { TumanFeature, TumanCollection, MaktabData, TumanStats } from './types';

/* ── Seeded PRNG (deterministic per-tuman) ── */
function seededRandom(seed: number) {
  let s = seed;
  return () => {
    s = (s * 1664525 + 1013904223) & 0xffffffff;
    return (s >>> 0) / 0xffffffff;
  };
}

function hashStr(str: string): number {
  let h = 0;
  for (let i = 0; i < str.length; i++) h = ((h << 5) - h + str.charCodeAt(i)) | 0;
  return Math.abs(h);
}

/* ── Point-in-polygon (ray casting) ── */
function pointInPolygon(lat: number, lng: number, ring: number[][]): boolean {
  let inside = false;
  for (let i = 0, j = ring.length - 1; i < ring.length; j = i++) {
    const yi = ring[i][0], xi = ring[i][1]; // GeoJSON = [lng, lat]
    const yj = ring[j][0], xj = ring[j][1];
    if ((yi > lng) !== (yj > lng) && lat < ((xj - xi) * (lng - yi)) / (yj - yi) + xi) {
      inside = !inside;
    }
  }
  return inside;
}

/* ── Polygon area (Shoelace, approximate sq-degrees) ── */
function ringArea(ring: number[][]): number {
  let a = 0;
  for (let i = 0, j = ring.length - 1; i < ring.length; j = i++) {
    a += (ring[j][0] + ring[i][0]) * (ring[j][1] - ring[i][1]);
  }
  return Math.abs(a / 2);
}

/* ── Extract outer rings from feature geometry ── */
function outerRings(feature: TumanFeature): number[][][] {
  const g = feature.geometry as any;
  if (g.type === 'Polygon') return [g.coordinates[0]];
  if (g.type === 'MultiPolygon') return g.coordinates.map((p: number[][][]) => p[0]);
  return [];
}

/* ── Target school count for a tuman based on area ── */
export function targetSchoolCount(feature: TumanFeature): number {
  const rings = outerRings(feature);
  if (!rings.length) return 10;
  const area = Math.max(...rings.map(ringArea));
  // area ranges from ~0.001 (tiny city district) to ~2.0 (huge rural tuman)
  // map to 8–15 schools
  const count = Math.round(8 + Math.min(7, area * 4));
  return Math.max(8, Math.min(15, count));
}

/* ── Generate synthetic schools inside a tuman polygon ── */
export function generateSyntheticSchools(
  feature: TumanFeature,
  viloyatName: string,
  existing: MaktabData[],
): MaktabData[] {
  const rings = outerRings(feature);
  if (!rings.length) return existing;

  const ring = rings.reduce((a, b) => (ringArea(a) > ringArea(b) ? a : b));
  const target = targetSchoolCount(feature);
  if (existing.length >= target) return existing;

  const tumanName = feature.properties.name;
  const rand = seededRandom(hashStr(tumanName + viloyatName));

  // Bounding box (shrunk 12 % to keep markers away from border)
  let minLat = Infinity, maxLat = -Infinity, minLng = Infinity, maxLng = -Infinity;
  for (const c of ring) {
    if (c[0] < minLng) minLng = c[0];
    if (c[0] > maxLng) maxLng = c[0];
    if (c[1] < minLat) minLat = c[1];
    if (c[1] > maxLat) maxLat = c[1];
  }
  const padLat = (maxLat - minLat) * 0.12;
  const padLng = (maxLng - minLng) * 0.12;
  minLat += padLat; maxLat -= padLat;
  minLng += padLng; maxLng -= padLng;

  const needed = target - existing.length;
  const synth: MaktabData[] = [];
  let tries = 0;

  while (synth.length < needed && tries < needed * 80) {
    tries++;
    const lat = minLat + rand() * (maxLat - minLat);
    const lng = minLng + rand() * (maxLng - minLng);
    if (!pointInPolygon(lat, lng, ring)) continue;

    const idx = synth.length + existing.length + 1;
    const id = -(idx + hashStr(tumanName) % 100000);
    const r = rand();
    const foiz = r < 0.12 ? null : Math.round(30 + rand() * 60);
    const jami = Math.round(2 + rand() * 8);
    const done = Math.round(rand() * jami * 0.7);
    const prob = Math.round(rand() * (jami - done));

    synth.push({
      id,
      nom: `${idx}-sonli umumta'lim maktabi`,
      viloyat: viloyatName,
      tuman: tumanName,
      manzil: `${tumanName}, ${viloyatName}`,
      rasm_url: '',
      lat,
      lng,
      jami_tekshiruv: jami,
      bajarildi: done,
      muammo: prob,
      mamnuniyat_foizi: foiz,
      holat: foiz === null ? 'tekshirilmagan' : foiz >= 70 ? 'yaxshi' : foiz >= 40 ? 'etiborga_muhtoj' : 'nosoz',
      holat_rangi: foiz === null ? '#94a3b8' : foiz >= 70 ? '#22c55e' : foiz >= 40 ? '#f59e0b' : '#ef4444',
      vaadalar_soni: Math.round(1 + rand() * 5),
    });
  }

  return [...existing, ...synth];
}

/* ── Enrich tuman stats: ensure every tuman has a school count ── */
export function enrichTumanStats(
  tumanlarGeo: TumanCollection,
  viloyatName: string,
  apiStats: TumanStats[],
): TumanStats[] {
  const tumans = tumanlarGeo.features.filter((f) => f.properties.viloyat === viloyatName);
  const statsMap = new Map(apiStats.map((s) => [s.nom.toLowerCase().trim(), s]));

  return tumans.map((f) => {
    const name = f.properties.name;
    const key = name.toLowerCase().trim();
    const existing = statsMap.get(key);
    if (existing && existing.maktablar_soni > 0) return existing;

    const count = targetSchoolCount(f);
    return {
      nom: name,
      maktablar_soni: existing ? existing.maktablar_soni || count : count,
      vaadalar_soni: existing ? existing.vaadalar_soni : Math.round(count * 3),
    };
  });
}
