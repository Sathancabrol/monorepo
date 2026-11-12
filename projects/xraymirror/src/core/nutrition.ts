export interface FoodProduct {
  code: string;
  name: string;
  brand?: string;
  nutriScore?: string;
  novaGroup?: number;
  categories?: string;
  allergens?: string[];
  imageUrl?: string;
  fetchedAt: number;
}

const CACHE_KEY = 'xraymirror.off.v1';

/** Tiny local cache: never let a network outage or CORS issue break the panel. */
export function readFoodCache(): Record<string, FoodProduct> {
  try {
    return JSON.parse(localStorage.getItem(CACHE_KEY) ?? '{}') as Record<string, FoodProduct>;
  } catch {
    return {};
  }
}

export function writeFoodCache(cache: Record<string, FoodProduct>): void {
  try {
    localStorage.setItem(CACHE_KEY, JSON.stringify(cache));
  } catch {
    // Ignore quota errors.
  }
}

export function normalizeBarcode(value: string): string {
  return value.replace(/\D/g, '').slice(0, 14);
}

/**
 * Open Food Facts lookup. Runs only on explicit user action, with the barcode
 * the user typed/scanned. No camera frame leaves the machine.
 */
export async function lookupOpenFoodFacts(barcode: string, fetchImpl: typeof fetch = fetch): Promise<FoodProduct> {
  const code = normalizeBarcode(barcode);
  if (code.length < 8) throw new Error('Code-barres trop court');
  const cache = readFoodCache();
  const cached = cache[code];
  if (cached && Date.now() - cached.fetchedAt < 7 * 24 * 3600 * 1000) return cached;

  const url = `https://world.openfoodfacts.org/api/v2/product/${code}.json?fields=code,product_name,brands,nutriscore_grade,nova_group,categories,allergens,image_front_small_url`;
  const response = await fetchImpl(url, { headers: { Accept: 'application/json' } });
  if (!response.ok) throw new Error(`Open Food Facts HTTP ${response.status}`);
  const payload = (await response.json()) as {
    status: number;
    product?: Record<string, unknown>;
  };
  if (payload.status !== 1 || !payload.product) throw new Error('Produit introuvable');

  const product = payload.product;
  const item: FoodProduct = {
    code,
    name: String(product.product_name || 'Produit sans nom'),
    brand: String(product.brands || ''),
    nutriScore: String(product.nutriscore_grade || ''),
    novaGroup: Number(product.nova_group || 0) || undefined,
    categories: String(product.categories || ''),
    allergens: String(product.allergens || '')
      .split(',')
      .map((allergen) => allergen.trim())
      .filter(Boolean),
    imageUrl: String(product.image_front_small_url || ''),
    fetchedAt: Date.now(),
  };
  cache[code] = item;
  writeFoodCache(cache);
  return item;
}
