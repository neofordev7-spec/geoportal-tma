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

  const pct = count > 0 ? Math.round((bajarilgan / count) * 100) : 0;

  return (
    <div className="absolute bottom-4 left-3 right-3 z-[1000] bg-white/90 backdrop-blur-lg rounded-2xl shadow-lg px-4 py-2.5 flex items-center gap-3">
      <div className="flex-shrink-0">
        <p className="text-[10px] font-semibold text-gray-400 leading-tight">{title}</p>
        <p className="text-lg font-black text-gray-900 leading-tight">{count} <span className="text-[10px] font-semibold text-gray-400">ob'yekt</span></p>
      </div>
      <div className="h-8 w-px bg-gray-200 flex-shrink-0" />
      <div className="flex items-center gap-3 flex-1 min-w-0">
        <div className="flex items-center gap-1.5">
          <span className="w-2 h-2 rounded-full bg-emerald-500 flex-shrink-0" />
          <span className="text-xs font-bold text-gray-700">{tekshirilgan}</span>
          <span className="text-[9px] text-gray-400 hidden sm:inline">tekshirilgan</span>
        </div>
        <div className="flex items-center gap-1.5">
          <span className="w-2 h-2 rounded-full bg-blue-500 flex-shrink-0" />
          <span className="text-xs font-bold text-gray-700">{bajarilgan}</span>
          <span className="text-[9px] text-gray-400 hidden sm:inline">bajarilgan</span>
        </div>
      </div>
      <div className="flex-shrink-0 w-10 h-10 rounded-full border-[3px] border-blue-100 flex items-center justify-center relative">
        <svg className="absolute inset-0 w-full h-full -rotate-90" viewBox="0 0 36 36">
          <circle cx="18" cy="18" r="15" fill="none" stroke="#dbeafe" strokeWidth="3" />
          <circle cx="18" cy="18" r="15" fill="none" stroke="#3b82f6" strokeWidth="3"
            strokeDasharray={`${pct * 0.942} 100`} strokeLinecap="round" />
        </svg>
        <span className="text-[9px] font-black text-blue-600">{pct}%</span>
      </div>
    </div>
  );
}

interface HomeButtonProps {
  onHomeClick: () => void;
}

export function HomeButton({ onHomeClick }: HomeButtonProps) {
  return (
    <button
      onClick={onHomeClick}
      className="absolute bottom-36 right-3 z-[1000] w-10 h-10 bg-white rounded-lg shadow-lg flex items-center justify-center hover:bg-gray-50 transition-colors cursor-pointer"
      title="Mening tumanim"
    >
      <svg className="w-5 h-5 text-indigo-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-4 0a1 1 0 01-1-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 01-1 1h-2z" />
      </svg>
    </button>
  );
}
