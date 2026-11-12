// Import adapter for the earlier independent OLYMPUS Studio v0.3 portable JSON.
// Converts pixel-positioned scenes to the current normalized canvas model.
// Preserves v0.3-only timeline/notes in legacyV03 (not interpreted as live actions).
const W = 1280, H = 720;
const clamp = n => Math.max(0, Math.min(1, Number.isFinite(Number(n)) ? Number(n) : 0));

export function migrateV03Project(data) {
  if (!data || data.app !== 'OLYMPUS Studio' || String(data.version || '') !== '0.3' || !Array.isArray(data.scenes) || data.scenes.length < 1 || data.scenes.length > 200) {
    throw new Error('Projet OLYMPUS v0.3 incompatible');
  }
  const assets = new Map((Array.isArray(data.assets) ? data.assets : []).filter(a => typeof a.id === 'string').map(a => [a.id, a]));
  const scenes = data.scenes.map((scene, n) => {
    if (!Array.isArray(scene.layers) || scene.layers.length > 1000) throw new Error('Calques v0.3 invalides');
    const layers = scene.layers.map((layer, i) => {
      const type = layer.type === 'shape' ? 'rect' : layer.type;
      const supported = ['text','rect','image','video'].includes(type) ? type : 'rect';
      const normalized = { id: String(layer.id || 'migrated-'+n+'-'+i), name: String(layer.name || 'Calque v0.3'), type: supported, x:clamp((Number(layer.x)||0)/W), y:clamp((Number(layer.y)||0)/H), w:clamp((Number(layer.w)||0)/W), h:clamp((Number(layer.h)||0)/H), color: String(layer.color || '#ffffff'), visible:layer.visible!==false, opacity: Number.isFinite(Number(layer.opacity)) ? Number(layer.opacity) : 1 };
      if (supported === 'text') {
        normalized.value = String(layer.text ?? layer.value ?? '');
        normalized.size = Number(layer.fontSize) || Math.min(65, Math.max(20, Math.round((Number(layer.h)||60)*0.67)));
      }
      if (supported === 'image' || supported === 'video') {
        const match = String(layer.src||'').match(/^asset:([\w.-]{1,150})$/);
        if (match && assets.has(match[1])) normalized.assetId=match[1];
      }
      if (supported !== type) normalized.name += ' [type non pris en charge]';
      return normalized;
    });
    return { id:String(scene.id||'migrated-scene-'+n), name:String(scene.name||'Scène v0.3'), layers };
  });
  const embeddedAssets=(Array.isArray(data.embeddedAssets) ? data.embeddedAssets : []).map(asset => {
    const metadata=assets.get(asset.id);
    return { id:String(asset.id||''), name:String(asset.filename || metadata?.filename || 'Média'), type:String(asset.type||metadata?.type||'application/octet-stream'), data_b64:String(asset.base64||''), size:Number.isInteger(metadata?.size) ? metadata.size : undefined };
  });
  return {
    format:'olympus-studio-project',schema:2,projectName:String(data.projectName||'Import OLYMPUS v0.3'),
    activeScene:String(data.activeScene||scenes[0].id),scenes,
    transcript:Array.isArray(data.meeting?.transcript)?data.meeting.transcript:[],
    embeddedAssets,
    legacyV03:{version:'0.3', meeting:data.meeting||{}, edit:data.edit||{}, automation:data.automation||{}, assets:data.assets||[]},
    migrationNote:'Positions v0.3 converties 1280x720→normalisées. Timeline/notes v0.3 préservées en legacyV03, mais non exécutées par le moteur actuel. Captions désactivés par défaut.',
  };
}
