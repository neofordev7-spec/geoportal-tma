import { useMemo } from 'react';
import { GeoJSON, Tooltip } from 'react-leaflet';
import type { ViloyatCollection, ViloyatStats } from '../types';
import { VILOYAT_COLORS, VILOYAT_NAME_TO_KOD } from '../types';

interface Props {
  geojson: ViloyatCollection;
  stats: ViloyatStats[];
  onSelect: (viloyatName: string, viloyatKod: string) => void;
}

export default function ViloyatlarLayer({ geojson, stats, onSelect }: Props) {
  const statsMap = useMemo(() => {
    const m = new Map<string, ViloyatStats>();
    for (const s of stats) m.set(s.kod, s);
    return m;
  }, [stats]);

  return (
    <>
      {geojson.features.map((feature, idx) => {
        const name = feature.properties.name;
        const kod = VILOYAT_NAME_TO_KOD[name] || '';
        const stat = statsMap.get(kod);
        const color = VILOYAT_COLORS[idx % VILOYAT_COLORS.length];
        return (
          <GeoJSON
            key={name}
            data={feature}
            style={{
              fillColor: color,
              fillOpacity: 0.2,
              color: color,
              weight: 2,
              opacity: 0.8,
            }}
            eventHandlers={{
              click: () => onSelect(name, kod),
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
                  weight: 2,
                });
              },
            }}
          >
            <Tooltip
              permanent
              direction="center"
              offset={[0, 0]}
              className="viloyat-label"
            >
              <div className="text-center">
                <div>{name.replace(' viloyati', '').replace(' shahar', ' sh.')}</div>
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
