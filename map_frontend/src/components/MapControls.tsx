import { useMap } from 'react-leaflet';
import type { TileLayerType, MapLevel } from '../types';

interface BreadcrumbProps {
  level: MapLevel;
  viloyatName: string | null;
  tumanName: string | null;
  onBack: () => void;
}

export function Breadcrumb({ level, viloyatName, tumanName, onBack }: BreadcrumbProps) {
  if (level === 'country') return null;

  return (
    <div className="absolute top-3 left-14 z-[1000] flex items-center gap-1 bg-white/95 backdrop-blur rounded-lg shadow-lg px-3 py-2 text-sm">
      <button
        onClick={onBack}
        className="flex items-center gap-1 text-blue-600 hover:text-blue-800 font-medium cursor-pointer"
      >
        <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
        </svg>
        Orqaga
      </button>
      <span className="text-gray-400 mx-1">/</span>
      <span className="text-gray-600">O'zbekiston</span>
      {viloyatName && (
        <>
          <span className="text-gray-400 mx-1">/</span>
          <span className={level === 'viloyat' ? 'text-gray-900 font-semibold' : 'text-gray-600'}>
            {viloyatName}
          </span>
        </>
      )}
      {tumanName && (
        <>
          <span className="text-gray-400 mx-1">/</span>
          <span className="text-gray-900 font-semibold">{tumanName}</span>
        </>
      )}
    </div>
  );
}

interface LayerSwitcherProps {
  activeLayer: TileLayerType;
  onChange: (layer: TileLayerType) => void;
}

export function LayerSwitcher({ activeLayer, onChange }: LayerSwitcherProps) {
  const layers: { key: TileLayerType; label: string }[] = [
    { key: 'map', label: 'Xarita' },
    { key: 'satellite', label: 'Sputnik' },
    { key: 'hybrid', label: 'Gibrid' },
  ];

  return (
    <div className="absolute top-3 right-3 z-[1000] flex bg-white/95 backdrop-blur rounded-lg shadow-lg overflow-hidden">
      {layers.map(({ key, label }) => (
        <button
          key={key}
          onClick={() => onChange(key)}
          className={`px-3 py-1.5 text-xs font-medium transition-colors cursor-pointer ${
            activeLayer === key
              ? 'bg-blue-600 text-white'
              : 'text-gray-700 hover:bg-gray-100'
          }`}
        >
          {label}
        </button>
      ))}
    </div>
  );
}

export function GpsButton() {
  const map = useMap();

  const handleGps = () => {
    map.locate({ setView: true, maxZoom: 14 });
  };

  return (
    <button
      onClick={handleGps}
      className="absolute bottom-24 right-3 z-[1000] w-10 h-10 bg-white rounded-lg shadow-lg flex items-center justify-center hover:bg-gray-50 transition-colors cursor-pointer"
      title="Mening joylashuvim"
    >
      <svg className="w-5 h-5 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8c-2.21 0-4 1.79-4 4s1.79 4 4 4 4-1.79 4-4-1.79-4-4-4z" />
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 2v2m0 16v2M2 12h2m16 0h2" />
      </svg>
    </button>
  );
}

interface StatsBoxProps {
  level: MapLevel;
  viloyatName: string | null;
  tumanName: string | null;
  count: number;
  tekshirilgan: number;
  bajarilgan: number;
}

export function StatsBox({ level, viloyatName, tumanName, count, tekshirilgan, bajarilgan }: StatsBoxProps) {
  const title =
    level === 'country'
      ? "O'zbekiston"
      : level === 'viloyat'
        ? viloyatName || ''
        : tumanName || '';

  return (
    <div className="absolute bottom-6 left-3 z-[1000] bg-white/95 backdrop-blur rounded-xl shadow-lg p-4 min-w-[220px]">
      <h3 className="text-sm font-bold text-gray-900 mb-2">{title}</h3>
      <div className="flex items-end gap-2 mb-2">
        <span className="text-2xl font-bold text-blue-600">{count}</span>
        <span className="text-xs text-gray-500 pb-1">ob'yekt</span>
      </div>
      <div className="grid grid-cols-2 gap-2 text-xs">
        <div className="bg-emerald-50 rounded-lg px-2 py-1.5 text-center">
          <div className="font-bold text-emerald-600">{tekshirilgan}</div>
          <div className="text-emerald-500/80 text-[10px]">tekshirilgan</div>
        </div>
        <div className="bg-blue-50 rounded-lg px-2 py-1.5 text-center">
          <div className="font-bold text-blue-600">{bajarilgan}</div>
          <div className="text-blue-500/80 text-[10px]">bajarilgan</div>
        </div>
      </div>
    </div>
  );
}
