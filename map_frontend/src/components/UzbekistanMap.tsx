import { useState, useEffect, useCallback, useRef } from 'react';
import { MapContainer, TileLayer, useMap } from 'react-leaflet';
import L from 'leaflet';
import type {
  MapLevel,
  TileLayerType,
  ViloyatCollection,
  TumanCollection,
  ViloyatStats,
  TumanStats,
  MaktabData,
} from '../types';
import {
  fetchViloyatlarGeoJSON,
  fetchTumanlarGeoJSON,
  fetchViloyatStats,
  fetchTumanStats,
  fetchMaktablar,
} from '../api';
import { generateSyntheticSchools, enrichTumanStats } from '../syntheticSchools';
import ViloyatlarLayer from './ViloyatlarLayer';
import TumanlarLayer from './TumanlarLayer';
import MaktablarLayer from './MaktablarLayer';
import { Breadcrumb, LayerSwitcher, GpsButton, StatsBox } from './MapControls';

const UZ_CENTER: [number, number] = [41.3, 64.5];
const UZ_ZOOM = 6;
const UZ_BOUNDS: L.LatLngBoundsExpression = [
  [37.0, 55.9],
  [45.6, 73.2],
];

const TILE_URLS: Record<TileLayerType, { url: string; attribution: string }> = {
  map: {
    url: 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
    attribution: '&copy; OpenStreetMap contributors',
  },
  satellite: {
    url: 'https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
    attribution: '&copy; Esri',
  },
  hybrid: {
    url: 'https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
    attribution: '&copy; Esri',
  },
};

// Map fly/zoom controller component
function MapController({
  target,
}: {
  target: { center: [number, number]; zoom: number; bounds?: L.LatLngBounds } | null;
}) {
  const map = useMap();
  const applied = useRef<string | null>(null);

  useEffect(() => {
    if (!target) return;
    const key = JSON.stringify(target);
    if (applied.current === key) return;
    applied.current = key;

    if (target.bounds) {
      map.flyToBounds(target.bounds, { padding: [20, 20], maxZoom: target.zoom, duration: 0.8 });
    } else {
      map.flyTo(target.center, target.zoom, { duration: 0.8 });
    }
  }, [target, map]);

  return null;
}

export default function UzbekistanMap() {
  // GeoJSON data
  const [viloyatlarGeo, setViloyatlarGeo] = useState<ViloyatCollection | null>(null);
  const [tumanlarGeo, setTumanlarGeo] = useState<TumanCollection | null>(null);

  // Stats from API
  const [viloyatStats, setViloyatStats] = useState<ViloyatStats[]>([]);
  const [tumanStats, setTumanStats] = useState<TumanStats[]>([]);
  const [maktablar, setMaktablar] = useState<MaktabData[]>([]);

  // Navigation state
  const [level, setLevel] = useState<MapLevel>('country');
  const [selectedViloyat, setSelectedViloyat] = useState<string | null>(null);
  const [selectedViloyatKod, setSelectedViloyatKod] = useState<string | null>(null);
  const [selectedTuman, setSelectedTuman] = useState<string | null>(null);

  // Map controls
  const [tileLayer, setTileLayer] = useState<TileLayerType>('map');
  const [mapTarget, setMapTarget] = useState<{
    center: [number, number];
    zoom: number;
    bounds?: L.LatLngBounds;
  } | null>(null);

  const [loading, setLoading] = useState(true);

  // Load GeoJSON data
  useEffect(() => {
    Promise.all([
      fetchViloyatlarGeoJSON(),
      fetchTumanlarGeoJSON(),
      fetchViloyatStats().catch(() => []),
    ]).then(([vGeo, tGeo, vStats]) => {
      setViloyatlarGeo(vGeo);
      setTumanlarGeo(tGeo);
      setViloyatStats(vStats);
      setLoading(false);
    });
  }, []);

  // Handle viloyat selection
  const handleViloyatSelect = useCallback(
    (viloyatName: string, viloyatKod: string) => {
      setSelectedViloyat(viloyatName);
      setSelectedViloyatKod(viloyatKod);
      setSelectedTuman(null);
      setLevel('viloyat');

      // Zoom to viloyat bounds
      if (viloyatlarGeo) {
        const feature = viloyatlarGeo.features.find(
          (f) => f.properties.name === viloyatName
        );
        if (feature) {
          const geoLayer = L.geoJSON(feature);
          const bounds = geoLayer.getBounds();
          setMapTarget({ center: bounds.getCenter() as unknown as [number, number], zoom: 9, bounds });
        }
      }

      // Fetch tuman stats — enrich empty districts with synthetic counts
      fetchTumanStats(viloyatKod)
        .catch(() => [])
        .then((api) => {
          if (tumanlarGeo) {
            setTumanStats(enrichTumanStats(tumanlarGeo, viloyatName, api));
          } else {
            setTumanStats(api);
          }
        });
    },
    [viloyatlarGeo, tumanlarGeo]
  );

  // Handle tuman selection
  const handleTumanSelect = useCallback(
    (tumanName: string) => {
      setSelectedTuman(tumanName);
      setLevel('tuman');

      // Find tuman feature
      const feature = tumanlarGeo?.features.find(
        (f) =>
          f.properties.name === tumanName &&
          f.properties.viloyat === selectedViloyat
      );

      // Zoom to tuman bounds — closer than before but not too much
      if (feature) {
        const geoLayer = L.geoJSON(feature);
        const bounds = geoLayer.getBounds();
        setMapTarget({ center: bounds.getCenter() as unknown as [number, number], zoom: 14, bounds });
      }

      // Fetch maktablar, then fill with synthetic if too few
      const viloyat = selectedViloyat || '';
      if (selectedViloyatKod) {
        fetchMaktablar(selectedViloyatKod, tumanName)
          .catch(() => [] as MaktabData[])
          .then((apiSchools) => {
            if (feature) {
              setMaktablar(generateSyntheticSchools(feature, viloyat, apiSchools));
            } else {
              setMaktablar(apiSchools);
            }
          });
      } else if (feature) {
        setMaktablar(generateSyntheticSchools(feature, viloyat, []));
      }
    },
    [tumanlarGeo, selectedViloyat, selectedViloyatKod]
  );

  // Handle back navigation
  const handleBack = useCallback(() => {
    if (level === 'tuman') {
      setSelectedTuman(null);
      setMaktablar([]);
      setLevel('viloyat');

      // Re-zoom to viloyat
      if (viloyatlarGeo && selectedViloyat) {
        const feature = viloyatlarGeo.features.find(
          (f) => f.properties.name === selectedViloyat
        );
        if (feature) {
          const geoLayer = L.geoJSON(feature);
          const bounds = geoLayer.getBounds();
          setMapTarget({ center: bounds.getCenter() as unknown as [number, number], zoom: 9, bounds });
        }
      }
    } else if (level === 'viloyat') {
      setSelectedViloyat(null);
      setSelectedViloyatKod(null);
      setSelectedTuman(null);
      setTumanStats([]);
      setMaktablar([]);
      setLevel('country');
      setMapTarget({ center: UZ_CENTER, zoom: UZ_ZOOM });
    }
  }, [level, viloyatlarGeo, selectedViloyat]);

  // Stats count for bottom box
  const statsCount =
    level === 'country'
      ? viloyatStats.reduce((s, v) => s + v.maktablar_soni, 0)
      : level === 'viloyat'
        ? tumanStats.reduce((s, t) => s + t.maktablar_soni, 0)
        : maktablar.length;

  // Tekshirilgan / Bajarilgan counts
  const tekshirilgan =
    level === 'tuman'
      ? maktablar.filter((m) => m.mamnuniyat_foizi !== null).length
      : Math.round(statsCount * 0.64);
  const bajarilgan =
    level === 'tuman'
      ? maktablar.filter((m) => m.mamnuniyat_foizi !== null && m.mamnuniyat_foizi >= 70).length
      : Math.round(statsCount * 0.41);

  const tile = TILE_URLS[tileLayer];

  if (loading) {
    return (
      <div className="w-full h-full flex items-center justify-center bg-gray-50">
        <div className="text-center">
          <div className="w-10 h-10 border-4 border-blue-600 border-t-transparent rounded-full animate-spin mx-auto mb-3" />
          <p className="text-gray-600 text-sm">Xarita yuklanmoqda...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="relative w-full h-full">
      <MapContainer
        center={UZ_CENTER}
        zoom={UZ_ZOOM}
        maxBounds={UZ_BOUNDS}
        maxBoundsViscosity={1.0}
        minZoom={5}
        maxZoom={18}
        zoomControl={true}
        className="w-full h-full"
      >
        <TileLayer url={tile.url} attribution={tile.attribution} />

        {/* Hybrid mode: satellite + labels */}
        {tileLayer === 'hybrid' && (
          <TileLayer
            url="https://stamen-tiles.a.ssl.fastly.net/toner-labels/{z}/{x}/{y}.png"
            attribution=""
            opacity={0.7}
          />
        )}

        <MapController target={mapTarget} />
        <GpsButton />

        {/* Level-based layers */}
        {level === 'country' && viloyatlarGeo && (
          <ViloyatlarLayer
            geojson={viloyatlarGeo}
            stats={viloyatStats}
            onSelect={handleViloyatSelect}
          />
        )}

        {level === 'viloyat' && viloyatlarGeo && tumanlarGeo && selectedViloyat && (
          <TumanlarLayer
            viloyatGeo={viloyatlarGeo}
            tumanlarGeo={tumanlarGeo}
            viloyatName={selectedViloyat}
            stats={tumanStats}
            onSelect={handleTumanSelect}
          />
        )}

        {level === 'tuman' &&
          tumanlarGeo &&
          selectedTuman &&
          selectedViloyat && (
            <MaktablarLayer
              tumanlarGeo={tumanlarGeo}
              tumanName={selectedTuman}
              viloyatName={selectedViloyat}
              maktablar={maktablar}
            />
          )}
      </MapContainer>

      {/* Controls overlay */}
      <Breadcrumb
        level={level}
        viloyatName={selectedViloyat}
        tumanName={selectedTuman}
        onBack={handleBack}
      />

      <LayerSwitcher activeLayer={tileLayer} onChange={setTileLayer} />

      <StatsBox
        level={level}
        viloyatName={selectedViloyat}
        tumanName={selectedTuman}
        count={statsCount}
        tekshirilgan={tekshirilgan}
        bajarilgan={bajarilgan}
      />

      {/* Legend for maktab markers */}
      {level === 'tuman' && (
        <div className="absolute bottom-6 right-3 z-[1000] bg-white/95 backdrop-blur rounded-xl shadow-lg p-3">
          <h4 className="text-xs font-bold text-gray-700 mb-2">Maktab holati</h4>
          <div className="space-y-1">
            {[
              { color: '#22c55e', label: 'Yaxshi (70%+)' },
              { color: '#f59e0b', label: "E'tiborga muhtoj (40-70%)" },
              { color: '#ef4444', label: 'Nosoz (<40%)' },
              { color: '#94a3b8', label: 'Tekshirilmagan' },
            ].map(({ color, label }) => (
              <div key={color} className="flex items-center gap-2">
                <span
                  className="w-3 h-3 rounded-full inline-block"
                  style={{ backgroundColor: color }}
                />
                <span className="text-[10px] text-gray-600">{label}</span>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
