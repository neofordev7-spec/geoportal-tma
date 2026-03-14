import type { FeatureCollection, Feature, Geometry } from 'geojson';

export interface ViloyatProperties {
  name: string;
  name_en: string;
}

export interface TumanProperties {
  name: string;
  name_en: string;
  name_uz: string;
  viloyat: string;
}

export type ViloyatFeature = Feature<Geometry, ViloyatProperties>;
export type TumanFeature = Feature<Geometry, TumanProperties>;
export type ViloyatCollection = FeatureCollection<Geometry, ViloyatProperties>;
export type TumanCollection = FeatureCollection<Geometry, TumanProperties>;

export interface MaktabData {
  id: number;
  nom: string;
  viloyat: string;
  tuman: string;
  manzil: string;
  rasm_url: string;
  lat: number;
  lng: number;
  jami_tekshiruv: number;
  bajarildi: number;
  muammo: number;
  mamnuniyat_foizi: number | null;
  holat: string;
  holat_rangi: string;
  vaadalar_soni: number;
}

export interface ViloyatStats {
  kod: string;
  nom: string;
  lat: number;
  lng: number;
  maktablar_soni: number;
  vaadalar_soni: number;
}

export interface TumanStats {
  nom: string;
  maktablar_soni: number;
  vaadalar_soni: number;
}

export type MapLevel = 'country' | 'viloyat' | 'tuman';

export type TileLayerType = 'map' | 'satellite' | 'hybrid';

// Viloyat code to GeoJSON name mapping
export const VILOYAT_KOD_TO_NAME: Record<string, string> = {
  toshkent_sh: 'Toshkent shahar',
  toshkent_v: 'Toshkent viloyati',
  samarqand: 'Samarqand viloyati',
  fargona: "Farg'ona viloyati",
  andijon: 'Andijon viloyati',
  namangan: 'Namangan viloyati',
  buxoro: 'Buxoro viloyati',
  xorazm: 'Xorazm viloyati',
  qashqadaryo: 'Qashqadaryo viloyati',
  surxondaryo: 'Surxondaryo viloyati',
  jizzax: 'Jizzax viloyati',
  sirdaryo: 'Sirdaryo viloyati',
  navoiy: 'Navoiy viloyati',
  qoraqalpogiston: "Qoraqolpog'iston Respublikasi",
};

export const VILOYAT_NAME_TO_KOD: Record<string, string> = Object.fromEntries(
  Object.entries(VILOYAT_KOD_TO_NAME).map(([k, v]) => [v, k])
);

// Viloyat colors
export const VILOYAT_COLORS: string[] = [
  '#3b82f6', '#22c55e', '#f59e0b', '#ef4444', '#8b5cf6',
  '#06b6d4', '#ec4899', '#14b8a6', '#f97316', '#6366f1',
  '#84cc16', '#e11d48', '#0ea5e9', '#a855f7',
];
