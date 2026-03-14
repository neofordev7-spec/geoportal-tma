import { useMemo } from 'react';
import { GeoJSON, Tooltip } from 'react-leaflet';
import type {
  ViloyatCollection,
  TumanCollection,
  TumanStats,
} from '../types';
import { VILOYAT_COLORS } from '../types';
import { normalizeTumanName } from '../utils';

interface Props {
  viloyatGeo: ViloyatCollection;
  tumanlarGeo: TumanCollection;
  viloyatName: string;
  stats: TumanStats[];
  onSelect: (tumanName: string) => void;
}

export default function TumanlarLayer({
  viloyatGeo,
  tumanlarGeo,
  viloyatName,
  stats,
  onSelect,
}: Props) {
  // Viloyat chegarasini topish
  const viloyatFeature = viloyatGeo.features.find(
    (f) => f.properties.name === viloyatName
  );

  // Shu viloyatga tegishli tumanlar
  const tumanlar = useMemo(
    () => tumanlarGeo.features.filter((f) => f.properties.viloyat === viloyatName),
    [tumanlarGeo, viloyatName]
  );

  // Stats map
  const statsMap = useMemo(() => {
    const m = new Map<string, TumanStats>();
    for (const s of stats) {
      m.set(normalizeTumanName(s.nom), s);
    }
    return m;
  }, [stats]);

  return (
    <>
      {/* Viloyat chegarasi — dash line */}
      {viloyatFeature && (
        <GeoJSON
          key={`border-${viloyatName}`}
          data={viloyatFeature}
          style={{
            fillColor: 'transparent',
            fillOpacity: 0,
            color: '#64748b',
            weight: 3,
            dashArray: '8 4',
            opacity: 0.6,
          }}
        />
      )}

      {/* Tumanlar */}
      {tumanlar.map((feature, idx) => {
        const name = feature.properties.name;
        const normalized = normalizeTumanName(name);
        const stat = statsMap.get(normalized);
        const color = VILOYAT_COLORS[idx % VILOYAT_COLORS.length];
        return (
          <GeoJSON
            key={`tuman-${name}-${idx}`}
            data={feature}
            style={{
              fillColor: color,
              fillOpacity: 0.2,
              color: color,
              weight: 1.5,
              opacity: 0.7,
            }}
            eventHandlers={{
              click: () => onSelect(name),
              mouseover: (e) => {
                const layer = e.target;
                layer.setStyle({
                  fillOpacity: 0.45,
                  weight: 3,
                });
                layer.bringToFront();
              },
              mouseout: (e) => {
                const layer = e.target;
                layer.setStyle({
                  fillOpacity: 0.2,
                  weight: 1.5,
                });
              },
            }}
          >
            <Tooltip
              permanent
              direction="center"
              offset={[0, 0]}
              className="tuman-label"
            >
              <div className="text-center">
                <div>{name.replace(' Tumani', '').replace(' tumani', '')}</div>
                {stat && stat.maktablar_soni > 0 && (
                  <span
                    className="inline-block mt-0.5 px-1.5 py-0 rounded-full text-white text-[9px] font-bold"
                    style={{ backgroundColor: color }}
                  >
                    {stat.maktablar_soni}
                  </span>
                )}
              </div>
            </Tooltip>
          </GeoJSON>
        );
      })}
    </>
  );
}
