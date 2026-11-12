import { useState } from 'react';
import { Barcode, Search, ShieldAlert } from 'lucide-react';
import { Card } from '../components';
import { lookupOpenFoodFacts, normalizeBarcode, readFoodCache, type FoodProduct } from '../../core/nutrition';

const CACHE_SHOW = 20;

export function NutritionPanel({ onToast }: { onToast: (message: string, tone?: 'info' | 'warn' | 'error' | 'ok') => void }) {
  const [code, setCode] = useState('');
  const [product, setProduct] = useState<FoodProduct | null>(null);
  const [loading, setLoading] = useState(false);
  const cache = readFoodCache();
  const cached = Object.values(cache).slice(-CACHE_SHOW).reverse();
  const [lastCode, setLastCode] = useState('');

  const search = async () => {
    if (normalizeBarcode(code).length < 8) {
      onToast('Entre un code-barres valide (8 à 14 chiffres)', 'warn');
      return;
    }
    setLoading(true);
    setLastCode(code);
    try {
      const result = await lookupOpenFoodFacts(code);
      setProduct(result);
      onToast(`${result.name} chargé depuis Open Food Facts`, 'ok');
    } catch (error) {
      onToast(`Open Food Facts: ${error instanceof Error ? error.message : 'erreur'}`, 'error');
    } finally {
      setLoading(false);
    }
  };

  return (
    <>
      <Card title="Nutrition & Open Food Facts" icon={<Barcode size={14} color="var(--accent)" />} subtitle="Aucune image ni code n’est envoyé sans action explicite">
        <div className="inline">
          <input className="field" style={{ border: '1px solid var(--line)', borderRadius: 8, padding: '7px 9px', background: '#081310' }} value={code} onChange={(event) => setCode(event.target.value)} placeholder="EAN · 3017620422003" onKeyDown={(event) => { if (event.key === 'Enter') void search(); }} />
          <button className="btn primary" style={{ flex: 'none' }} onClick={() => void search()} disabled={loading}>
            <Search size={13} /> {loading ? '…' : 'Chercher'}
          </button>
        </div>
        <div className="note" style={{ marginTop: 8 }}>
          Le scan caméra n’est pas encore branché : l’entrée manuelle et le cache local fonctionnent réellement. ZXing/BarcodeDetector viendra en plugin séparé.
        </div>
        {product && <ProductCard product={product} />}
      </Card>

      <Card title="Cache local récent" icon={<Barcode size={14} color="var(--accent-2)" />} subtitle={`${Object.keys(cache).length} produits · 7 jours`}>
        {cached.length === 0 ? (
          <div className="empty">Aucun produit en cache. Essaie le code <code>3017620422003</code>.</div>
        ) : (
          <div className="list">
            {cached.map((entry) => (
              <div className="row" key={entry.code}>
                <span className="score" style={{ background: nutriColor(entry.nutriScore) }}>{entry.nutriScore?.toUpperCase() || '?'}</span>
                <div className="grow"><div className="t">{entry.name}</div><div className="s">{entry.code}</div></div>
                <button className="btn small ghost" onClick={() => { setProduct(entry); onToast('Produit rechargé depuis le cache local', 'ok'); }}>Voir</button>
              </div>
            ))}
          </div>
        )}
        <div className="note warn" style={{ marginTop: 9 }}>
          <ShieldAlert size={11} style={{ verticalAlign: '-1px' }} /> Informations produit, pas conseil médical. Les allergènes sont fournis tels quels par Open Food Facts et peuvent être incomplets.
        </div>
      </Card>
    </>
  );
}

function ProductCard({ product }: { product: FoodProduct }) {
  return (
    <div className="product-card" style={{ marginTop: 10 }}>
      {product.imageUrl ? <img src={product.imageUrl} alt="" /> : <div className="grow" />}
      <div className="grow">
        <div className="name">{product.name}</div>
        {product.brand && <div className="brand">{product.brand}</div>}
        <div className="plugin-meta" style={{ marginTop: 5 }}>
          {product.nutriScore && <span className="tag">Nutri-Score {product.nutriScore.toUpperCase()}</span>}
          {product.novaGroup && <span className="tag">Nova {product.novaGroup}</span>}
        </div>
        {product.allergens && product.allergens.length > 0 && (
          <div className="brand" style={{ marginTop: 4 }}>Allergènes : {product.allergens.join(', ')}</div>
        )}
      </div>
    </div>
  );
}

function nutriColor(score?: string): string {
  switch ((score ?? '').toLowerCase()) {
    case 'a': return '#2ee59a';
    case 'b': return '#9fe870';
    case 'c': return '#ffd35c';
    case 'd': return '#ff9f45';
    case 'e': return '#ff6470';
    default: return '#4a635c';
  }
}
