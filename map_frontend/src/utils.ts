import type { Feature, Geometry, Position } from 'geojson';

/**
 * Tuman nomini normallashtirish — GeoJSON va backend o'rtasidagi farqlarni yo'qotish
 */
export function normalizeTumanName(name: string): string {
  let s = name.toLowerCase().trim();

  // Maxsus belgilarni olib tashlash
  s = s.replace(/[ʻʼ''`\u02BB\u02BC]/g, "'");

  // O'zbek harflarini almashtirish
  s = s.replace(/ó/g, 'o');
  s = s.replace(/ú/g, 'u');
  s = s.replace(/á/g, 'a');
  s = s.replace(/ń/g, 'n');
  s = s.replace(/ı/g, 'i');
  s = s.replace(/w/g, 'v');

  // Qo'shimchalarni olib tashlash
  s = s
    .replace(/\s*(tumani|tuman|rayoni|shahri|shahar|qalasi|district)\s*/gi, '')
    .trim();

  // Bo'sh joylarni normalize qilish
  s = s.replace(/\s+/g, ' ').trim();

  return s;
}

// Alias mapping
const TUMAN_ALIASES: Record<string, string> = {
  'past dargom': 'pastdargom',
  'pastdarg\'om': 'pastdargom',
  nokis: 'nukus',
  'no\'kis': 'nukus',
  'toshkent': 'toshkent',
};

export function matchTumanName(name1: string, name2: string): boolean {
  let n1 = normalizeTumanName(name1);
  let n2 = normalizeTumanName(name2);

  // Check direct aliases
  n1 = TUMAN_ALIASES[n1] || n1;
  n2 = TUMAN_ALIASES[n2] || n2;

  return n1 === n2;
}

/**
 * GeoJSON Feature dan centroid hisoblash
 */
export function getCentroid(feature: Feature<Geometry>): [number, number] {
  const coords = getAllCoordinates(feature.geometry);
  if (coords.length === 0) return [41.3, 64.5];

  let sumLat = 0;
  let sumLng = 0;
  for (const [lng, lat] of coords) {
    sumLat += lat;
    sumLng += lng;
  }
  return [sumLat / coords.length, sumLng / coords.length];
}

function getAllCoordinates(geometry: Geometry): Position[] {
  const coords: Position[] = [];

  function extract(arr: unknown): void {
    if (!Array.isArray(arr)) return;
    if (typeof arr[0] === 'number' && typeof arr[1] === 'number') {
      coords.push(arr as Position);
      return;
    }
    for (const item of arr) {
      extract(item);
    }
  }

  if ('coordinates' in geometry) {
    extract(geometry.coordinates);
  } else if (geometry.type === 'GeometryCollection') {
    for (const geom of geometry.geometries) {
      const sub = getAllCoordinates(geom);
      coords.push(...sub);
    }
  }

  return coords;
}

/**
 * Health score ga qarab rang
 */
export function getHealthColor(foiz: number | null): string {
  if (foiz === null) return '#94a3b8';
  if (foiz >= 70) return '#22c55e';
  if (foiz >= 40) return '#f59e0b';
  return '#ef4444';
}

export function getHealthLabel(foiz: number | null): string {
  if (foiz === null) return 'Tekshirilmagan';
  if (foiz >= 70) return 'Yaxshi';
  if (foiz >= 40) return "E'tiborga muhtoj";
  return 'Nosoz';
}
