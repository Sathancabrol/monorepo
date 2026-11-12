import { useEffect, useState } from 'react';
import { Database, HardDrive, Server, Wifi, WifiOff } from 'lucide-react';
import { Card } from '../components';
import { ModelResolver, type ModelDefinition } from '../../core/modelManager';

type Inspected = ModelDefinition & { source: 'local' | 'remote' | 'unknown' };

export function ModelsPanel({ engineStatus }: { engineStatus: Record<string, string> }) {
  const [models, setModels] = useState<Inspected[]>([]);
  const [checking, setChecking] = useState(false);

  const inspect = async () => {
    setChecking(true);
    try {
      const resolver = new ModelResolver();
      setModels(await resolver.inspect());
    } finally {
      setChecking(false);
    }
  };

  useEffect(() => {
    void inspect();
  }, []);

  return (
    <>
      <Card
        title="Model Hub"
        icon={<Database size={14} color="var(--accent)" />}
        subtitle={`MediaPipe ${engineStatus.face === 'prêt' ? 'chargé' : 'en attente'}`}
        actions={<button className="btn small" onClick={() => void inspect()} disabled={checking}>{checking ? '…' : 'Revérifier'}</button>}
      >
        <div className="list">
          {models.map((model) => (
            <div className="row" key={model.id}>
              {model.source === 'local' ? <HardDrive size={13} color="var(--ok)" /> : <Server size={13} color="var(--warn)" />}
              <div className="grow">
                <div className="t">{model.id}</div>
                <div className="s">{model.description}</div>
              </div>
              <div style={{ textAlign: 'right' }}>
                <span className="tag">{Math.round(model.bytes / 1_000_000)} Mo</span>
                <div className="s" style={{ marginTop: 2 }}>{model.source === 'local' ? 'cache local' : model.source === 'remote' ? 'distant' : '?'}</div>
              </div>
            </div>
          ))}
          {models.length === 0 && <div className="empty">Vérification en cours…</div>}
        </div>
        <div className="note" style={{ marginTop: 9 }}>
          Le cache est détecté par une requête HEAD sur <code>models/&lt;id&gt;.task</code>. Si absent, l’URL Google épinglée est utilisée. Les SHA-256 restent <strong>PENDING</strong> tant qu’ils ne sont pas calculés sur une machine connectée.
        </div>
      </Card>

      <Card title="Licences & provenance" icon={<Wifi size={14} color="var(--accent-2)" />}>
        <div className="list">
          <div className="row"><WifiOff size={13} color="var(--ok)" /><div className="grow"><div className="t">Traitement vidéo</div><div className="s">100 % local, aucun envoi de frames</div></div></div>
          <div className="row"><Wifi size={13} color="var(--warn)" /><div className="grow"><div className="t">Téléchargement des modèles</div><div className="s">Google MediaPipe, Apache-2.0</div></div></div>
          <div className="row"><Wifi size={13} color="var(--warn)" /><div className="grow"><div className="t">Open Food Facts</div><div className="s">Réseau uniquement sur action explicite</div></div></div>
        </div>
        <div className="note warn" style={{ marginTop: 9 }}>
          Le code de ce socle est expérimental et n’est pas un audit de sécurité. Une application grand public devra vérifier les licences des modèles, les empreintes et la politique de confidentialité.
        </div>
      </Card>
    </>
  );
}
