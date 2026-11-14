// Metadata-only preflight for importing an EDIT interchange manifest.
// Never interpret an assetId as a path, URL or permission to fetch media.
import { validateEditInterchange } from './edit-interchange.js';

export function inspectEditInterchangeAssets(manifest, availableAssetIds) {
  const safe = validateEditInterchange(manifest);
  if (!Array.isArray(availableAssetIds) || availableAssetIds.some(
    id => typeof id !== 'string' || !id.trim()
  )) throw new TypeError('Available asset IDs must be an array of nonempty strings');
  const available = new Set(availableAssetIds);
  const referenced = [...new Set([
    ...safe.segments.map(segment => segment.assetId),
    ...(safe.soundtrack ? [safe.soundtrack.assetId] : []),
  ])];
  const missing = referenced.filter(id => !available.has(id));
  return {
    ready: missing.length === 0,
    referencedAssetIds: referenced,
    missingAssetIds: missing,
    clips: safe.segments.length,
  };
}
