import { useMemo } from 'react';
import { GeoJSON, CircleMarker, Popup } from 'react-leaflet';
import type { TumanCollection, MaktabData } from '../types';
import { getHealthColor, getHealthLabel } from '../utils';

interface Props {
  tumanlarGeo: TumanCollection;
  tumanName: string;
  viloyatName: string;
  maktablar: MaktabData[];
}

export default function MaktablarLayer({
  tumanlarGeo,
  tumanName,
  viloyatName,
  maktablar,
}: Props) {
  // Tuman chegarasini topish
  const tumanFeature = useMemo(
    () =>
      tumanlarGeo.features.find(
        (f) => f.properties.name === tumanName && f.properties.viloyat === viloyatName
      ),
    [tumanlarGeo, tumanName, viloyatName]
  );

  return (
    <>
      {/* Tuman chegarasi */}
      {tumanFeature && (
        <GeoJSON
          key={`tuman-border-${tumanName}`}
          data={tumanFeature}
          style={{
            fillColor: '#e2e8f0',
            fillOpacity: 0.1,
            color: '#475569',
            weight: 2.5,
            dashArray: '6 3',
          }}
        />
      )}

      {/* Maktab markerlari */}
      {maktablar.map((maktab) => {
        const color = getHealthColor(maktab.mamnuniyat_foizi);
        const label = getHealthLabel(maktab.mamnuniyat_foizi);

        return (
          <CircleMarker
            key={maktab.id}
            center={[maktab.lat, maktab.lng]}
            radius={10}
            pathOptions={{
              fillColor: color,
              fillOpacity: 0.9,
              color: '#fff',
              weight: 2,
            }}
          >
            <Popup>
              <div className="min-w-[220px]">
                <h3 className="font-bold text-sm text-gray-900 mb-2">{maktab.nom}</h3>
                <div className="space-y-1.5 text-xs">
                  <div className="flex justify-between">
                    <span className="text-gray-500">Holat:</span>
                    <span className="font-semibold" style={{ color }}>
                      {label}
                    </span>
                  </div>
                  {maktab.mamnuniyat_foizi !== null && (
                    <div className="flex justify-between">
                      <span className="text-gray-500">Mamnuniyat:</span>
                      <span className="font-semibold">{maktab.mamnuniyat_foizi}%</span>
                    </div>
                  )}
                  <div className="flex justify-between">
                    <span className="text-gray-500">Va'dalar:</span>
                    <span className="font-semibold">{maktab.vaadalar_soni}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-gray-500">Tekshiruvlar:</span>
                    <span className="font-semibold">{maktab.jami_tekshiruv}</span>
                  </div>
                  {maktab.jami_tekshiruv > 0 && (
                    <div className="flex gap-2 mt-1">
                      <span className="text-green-600">
                        {maktab.bajarildi} bajarildi
                      </span>
                      <span className="text-red-500">
                        {maktab.muammo} muammo
                      </span>
                    </div>
                  )}

                  {/* Progress bar */}
                  {maktab.mamnuniyat_foizi !== null && (
                    <div className="mt-2">
                      <div className="w-full bg-gray-200 rounded-full h-2">
                        <div
                          className="h-2 rounded-full transition-all"
                          style={{
                            width: `${maktab.mamnuniyat_foizi}%`,
                            backgroundColor: color,
                          }}
                        />
                      </div>
                    </div>
                  )}
                </div>

                <a
                  href={`/tma/maktablar/${maktab.id}/`}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="mt-3 block w-full text-center bg-blue-600 text-white text-xs font-medium py-1.5 rounded-lg hover:bg-blue-700 transition-colors no-underline"
                >
                  Batafsil ko'rish
                </a>
              </div>
            </Popup>
          </CircleMarker>
        );
      })}
    </>
  );
}
