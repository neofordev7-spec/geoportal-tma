import type {
  MaktabData,
  ViloyatStats,
  TumanStats,
  ViloyatCollection,
  TumanCollection,
} from './types';

const API_BASE = '/api';

export async function fetchViloyatlarGeoJSON(): Promise<ViloyatCollection> {
  const res = await fetch('/uz-viloyatlar.geojson');
  return res.json();
}

export async function fetchTumanlarGeoJSON(): Promise<TumanCollection> {
  const res = await fetch('/uz-tumanlar.geojson');
  return res.json();
}

export async function fetchViloyatStats(): Promise<ViloyatStats[]> {
  const res = await fetch(`${API_BASE}/viloyatlar/`);
  const data = await res.json();
  return data;
}

export async function fetchTumanStats(viloyatKod: string): Promise<TumanStats[]> {
  const res = await fetch(`${API_BASE}/tumanlari/?viloyat=${viloyatKod}`);
  const data = await res.json();
  return data;
}

export async function fetchMaktablar(
  viloyatKod?: string,
  tuman?: string
): Promise<MaktabData[]> {
  const params = new URLSearchParams();
  if (viloyatKod) params.set('viloyat', viloyatKod);
  if (tuman) params.set('tuman', tuman);
  const res = await fetch(`${API_BASE}/maktablar/?${params}`);
  const data = await res.json();
  return data.maktablar || [];
}

export async function fetchMaktabDetail(id: number) {
  const res = await fetch(`${API_BASE}/maktablar/${id}/`);
  return res.json();
}
