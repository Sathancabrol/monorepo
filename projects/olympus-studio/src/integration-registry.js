// OLYMPUS integration contracts: explicit capabilities, never infer operational status from a port.
export const SPACE_INTEGRATIONS = Object.freeze([
  {space:'LIVE',engine:'OBS Studio',transport:'obs-websocket v5',endpoint:'ws://127.0.0.1:4455',contract:'scene/record commands + events',status:'mock-tested'},
  {space:'EDIT',engine:'OLYMPUS storyboard + browser MediaRecorder',transport:'local ES modules',endpoint:null,contract:'clips/assets -> WebM VP8/Opus',status:'intermittent-av'},
  {space:'GENERATE',engine:'ComfyUI',transport:'HTTP API',endpoint:'http://127.0.0.1:8188',contract:'workflow JSON -> prompt_id -> outputs',status:'http-mock-tested'},
  {space:'XR',engine:'X-Ray Mirror / MediaPipe',transport:'adapter pending',endpoint:null,contract:'timestamped pose/gesture events',status:'not-integrated'},
  {space:'AUDIO',engine:'WebAudio / Sherpa-ONNX',transport:'adapter pending',endpoint:null,contract:'PCM/WAV -> track/transcript',status:'partial'},
  {space:'MEETING',engine:'Sherpa-ONNX VoiceStudio',transport:'adapter pending',endpoint:null,contract:'audio -> transcript/SRT',status:'partial'},
  {space:'CAPTURE',engine:'COLMAP / photogrammetry',transport:'adapter pending',endpoint:null,contract:'images -> camera/mesh metadata',status:'not-integrated'},
  {space:'CINEMA',engine:'Blender / Three.js',transport:'adapter pending',endpoint:null,contract:'scene/camera -> rendered media',status:'not-integrated'},
  {space:'AUTOMATE',engine:'Hermes / Chronos',transport:'adapter pending',endpoint:null,contract:'authorized task -> result/events',status:'not-integrated'},
  {space:'GRAPHICS',engine:'Canvas / SVG',transport:'local UI',endpoint:null,contract:'layers -> composited frames',status:'partial'},
  {space:'LIBRARY',engine:'IndexedDB',transport:'browser storage',endpoint:null,contract:'assetId -> Blob + portable manifest',status:'chromium-tested'},
  {space:'CONTROL',engine:'OLYMPUS diagnostics',transport:'local HTTP',endpoint:'/api/health',contract:'read-only service probes',status:'http-tested'}
]);
export function integrationSnapshot(probes={}) {
  return SPACE_INTEGRATIONS.map(item=>({
    ...item,
    reachable: item.space==='LIVE' ? (probes.obs===true) : item.space==='GENERATE' ? (probes.comfyui===true) : null,
    // A listening port does not establish authentication, API compatibility or end-to-end function.
    operationallyVerified: false
  }));
}
