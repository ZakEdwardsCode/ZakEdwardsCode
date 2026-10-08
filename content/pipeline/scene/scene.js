// Three.js hero scenes, driven by Playwright.
//   await window.setupScene(cfg)   -> builds the scene (resolves once assets load)
//   window.renderAt(t, duration)   -> renders one deterministic frame
// cfg.kind: 'phone' | 'number' | 'cham3d' | 'cham2d'
import * as THREE from 'three';
import { RoundedBoxGeometry } from 'three/addons/geometries/RoundedBoxGeometry.js';
import { TextGeometry } from 'three/addons/geometries/TextGeometry.js';
import { Font } from 'three/addons/loaders/FontLoader.js';
import { TTFLoader } from 'three/addons/loaders/TTFLoader.js';
import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js';
import { RoomEnvironment } from 'three/addons/environments/RoomEnvironment.js';

let renderer, scene, camera, hero, cfg;
const base = { rx: 0, ry: 0, rz: 0, y: 0 };

function roundedRectShape(w, h, r) {
  const s = new THREE.Shape();
  const x = -w / 2, y = -h / 2;
  s.moveTo(x + r, y);
  s.lineTo(x + w - r, y); s.quadraticCurveTo(x + w, y, x + w, y + r);
  s.lineTo(x + w, y + h - r); s.quadraticCurveTo(x + w, y + h, x + w - r, y + h);
  s.lineTo(x + r, y + h); s.quadraticCurveTo(x, y + h, x, y + h - r);
  s.lineTo(x, y + r); s.quadraticCurveTo(x, y, x + r, y);
  return s;
}

function planarUVs(geo, w, h) {
  const pos = geo.attributes.position, uv = geo.attributes.uv;
  for (let i = 0; i < pos.count; i++) uv.setXY(i, pos.getX(i) / w + 0.5, pos.getY(i) / h + 0.5);
  uv.needsUpdate = true;
  return geo;
}

function blobShadow(width, depth, opacity = 0.32) {
  const c = document.createElement('canvas');
  c.width = c.height = 256;
  const g = c.getContext('2d');
  const grad = g.createRadialGradient(128, 128, 0, 128, 128, 128);
  grad.addColorStop(0, `rgba(10,6,30,${opacity})`);
  grad.addColorStop(0.55, `rgba(10,6,30,${opacity * 0.45})`);
  grad.addColorStop(1, 'rgba(10,6,30,0)');
  g.fillStyle = grad; g.fillRect(0, 0, 256, 256);
  const m = new THREE.Mesh(
    new THREE.PlaneGeometry(width, depth),
    new THREE.MeshBasicMaterial({ map: new THREE.CanvasTexture(c), transparent: true, depthWrite: false }),
  );
  m.rotation.x = -Math.PI / 2;
  return m;
}

async function loadTexture(url) {
  const tex = await new THREE.TextureLoader().loadAsync(url);
  tex.colorSpace = THREE.SRGBColorSpace;
  tex.anisotropy = renderer.capabilities.getMaxAnisotropy();
  return tex;
}

async function buildPhone() {
  const W = 0.8, H = 1.68, D = 0.1;
  const g = new THREE.Group();
  const frame = new THREE.Mesh(
    new RoundedBoxGeometry(W, H, D, 8, 0.12),
    new THREE.MeshPhysicalMaterial({ color: cfg.colors.frame || '#1c1830', metalness: 0.65, roughness: 0.3, clearcoat: 1, clearcoatRoughness: 0.15 }),
  );
  g.add(frame);
  const glass = new THREE.Mesh(new THREE.ShapeGeometry(roundedRectShape(W - 0.035, H - 0.035, 0.105), 12), new THREE.MeshBasicMaterial({ color: '#05040a' }));
  glass.position.z = D / 2 + 0.0008;
  g.add(glass);

  const SW = 0.735, SH = SW * (cfg.screenAspect || 844 / 390);
  const tex = await loadTexture(cfg.screenshotUrl);
  // cover-fit the screenshot to the screen shape, anchored to the top
  const img = tex.image, imgAspect = img.height / img.width, scrAspect = SH / SW;
  if (imgAspect > scrAspect) { tex.repeat.set(1, scrAspect / imgAspect); tex.offset.set(0, 1 - scrAspect / imgAspect); }
  else { tex.repeat.set(imgAspect / scrAspect, 1); tex.offset.set((1 - imgAspect / scrAspect) / 2, 0); }
  const screen = new THREE.Mesh(
    planarUVs(new THREE.ShapeGeometry(roundedRectShape(SW, SH, 0.085), 16), SW, SH),
    new THREE.MeshBasicMaterial({ map: tex, toneMapped: false }),
  );
  screen.position.z = D / 2 + 0.0016;
  g.add(screen);

  const island = new THREE.Mesh(new THREE.ShapeGeometry(roundedRectShape(0.2, 0.056, 0.028), 8), new THREE.MeshBasicMaterial({ color: '#000' }));
  island.position.set(0, SH / 2 - 0.05, D / 2 + 0.0024);
  g.add(island);

  // subtle glass sheen across the screen
  const sheen = new THREE.Mesh(
    new THREE.ShapeGeometry(roundedRectShape(SW, SH, 0.085), 16),
    new THREE.MeshPhysicalMaterial({ color: '#ffffff', transparent: true, opacity: 0.06, roughness: 0.05, metalness: 0, clearcoat: 1 }),
  );
  sheen.position.z = D / 2 + 0.003;
  g.add(sheen);

  const btnMat = frame.material;
  for (const [y, h, side] of [[0.42, 0.2, 1], [0.5, 0.09, -1], [0.33, 0.14, -1], [0.14, 0.14, -1]]) {
    const b = new THREE.Mesh(new RoundedBoxGeometry(0.02, h, 0.04, 2, 0.008), btnMat);
    b.position.set(side * (W / 2 + 0.006), y, 0);
    g.add(b);
  }
  Object.assign(base, { rx: -0.08, ry: -0.42, rz: 0.06, y: 0.04 });
  return { group: g, height: H, shadowW: 1.5, shadowY: -H / 2 - 0.16 };
}

// Landscape "app window" for desktop screenshots: thin dark bezel, screenshot face, tilted.
async function buildPanel() {
  const tex = await loadTexture(cfg.screenshotUrl);
  const aspect = tex.image.height / tex.image.width;
  const SW = 2.3, SH = SW * aspect, B = 0.05, D = 0.06;
  const g = new THREE.Group();
  const frame = new THREE.Mesh(
    new RoundedBoxGeometry(SW + B * 2, SH + B * 2, D, 6, 0.06),
    new THREE.MeshPhysicalMaterial({ color: cfg.colors.frame || '#0d1b22', metalness: 0.5, roughness: 0.35, clearcoat: 1, clearcoatRoughness: 0.2 }),
  );
  g.add(frame);
  const screen = new THREE.Mesh(
    planarUVs(new THREE.ShapeGeometry(roundedRectShape(SW, SH, 0.035), 10), SW, SH),
    new THREE.MeshBasicMaterial({ map: tex, toneMapped: false }),
  );
  screen.position.z = D / 2 + 0.002;
  g.add(screen);
  Object.assign(base, { rx: -0.12, ry: -0.36, rz: 0.03, y: 0.05 });
  return { group: g, height: SH * 1.05, shadowW: SW * 1.2, shadowY: -SH / 2 - 0.22 };
}

async function buildNumber() {
  const loader = new TTFLoader();
  // CFF-flavoured .otf outlines wind the opposite way to TrueType; without this, counters (6, 8, 0) fill in
  loader.reversed = cfg.fontReversed ?? /\.otf$/i.test(cfg.fontUrl);
  const json = await loader.loadAsync(cfg.fontUrl);
  const font = new Font(json);
  const geo = new TextGeometry(String(cfg.text), {
    font, size: 1, depth: 0.34, curveSegments: 14,
    bevelEnabled: true, bevelThickness: 0.045, bevelSize: 0.028, bevelSegments: 6,
  });
  geo.computeBoundingBox();
  geo.center();
  const bb = geo.boundingBox;
  const front = new THREE.MeshPhysicalMaterial({ color: cfg.colors.primary, roughness: 0.28, metalness: 0.1, clearcoat: 1, clearcoatRoughness: 0.12 });
  const side = new THREE.MeshPhysicalMaterial({ color: cfg.colors.primaryDeep, roughness: 0.4, metalness: 0.15 });
  const mesh = new THREE.Mesh(geo, [front, side]);
  const g = new THREE.Group();
  g.add(mesh);
  const h = bb.max.y - bb.min.y, w = bb.max.x - bb.min.x;
  const s = Math.min(1.7 / h, 2.2 / w);
  g.scale.setScalar(s);
  Object.assign(base, { rx: -0.12, ry: -0.38, rz: 0.04, y: 0.02 });
  return { group: g, height: h * s, shadowW: w * s * 1.3, shadowY: -(h * s) / 2 - 0.14 };
}

async function buildCham3d() {
  const gltf = await new GLTFLoader().loadAsync(cfg.glbUrl);
  const model = gltf.scene;
  model.traverse((o) => {
    if (!o.isMesh) return;
    const mats = Array.isArray(o.material) ? o.material : [o.material];
    o.material = mats.map((m) => {
      const c = m.clone();
      if (!cfg.glbMaterialName || m.name === cfg.glbMaterialName) {
        if (c.color) c.color.set(cfg.mood.body);
        if (c.map && !cfg.glbMaterialName) c.map = null; // flat mood colour when no specific material is named
      }
      return c;
    });
    if (o.material.length === 1) o.material = o.material[0];
  });
  const box = new THREE.Box3().setFromObject(model);
  const size = box.getSize(new THREE.Vector3()), center = box.getCenter(new THREE.Vector3());
  const s = 1.7 / Math.max(size.y, size.x * 0.8);
  model.position.sub(center);
  const g = new THREE.Group();
  g.add(model);
  g.scale.setScalar(s);
  Object.assign(base, { rx: 0, ry: -0.5, rz: 0, y: 0 });
  return { group: g, height: size.y * s, shadowW: size.x * s * 1.2, shadowY: -(size.y * s) / 2 - 0.08 };
}

async function buildCham2d() {
  const tex = await loadTexture(cfg.imageUrl);
  const aspect = tex.image.width / tex.image.height;
  const H = 1.6, W = H * aspect;
  const g = new THREE.Group();
  // stacked slices give the flat illustration a physical edge when it turns
  const layers = 10;
  for (let i = 0; i < layers; i++) {
    const k = i === 0 ? 1 : 0.55;
    const m = new THREE.Mesh(
      new THREE.PlaneGeometry(W, H),
      new THREE.MeshBasicMaterial({ map: tex, transparent: true, alphaTest: 0.5, color: new THREE.Color(k, k, k), toneMapped: false, side: THREE.DoubleSide }),
    );
    m.position.z = -i * 0.006;
    g.add(m);
  }
  Object.assign(base, { rx: 0, ry: -0.18, rz: 0, y: 0 });
  return { group: g, height: H, shadowW: W * 1.1, shadowY: -H / 2 - 0.06 };
}

window.setupScene = async (config) => {
  cfg = config;
  const { width, height } = cfg;
  document.body.style.background = cfg.background || 'transparent';
  document.getElementById('stage').style.cssText = `width:${width}px;height:${height}px`;
  if (cfg.overlayHtml) document.getElementById('overlay').innerHTML = cfg.overlayHtml;
  if (cfg.overlayCss) { const st = document.createElement('style'); st.textContent = cfg.overlayCss; document.head.appendChild(st); }

  renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true, preserveDrawingBuffer: true });
  renderer.setPixelRatio(1);
  renderer.setSize(width, height);
  renderer.setClearColor(0x000000, 0);
  renderer.toneMapping = THREE.ACESFilmicToneMapping;
  renderer.toneMappingExposure = 1.05;
  renderer.outputColorSpace = THREE.SRGBColorSpace;
  document.getElementById('stage').prepend(renderer.domElement);

  scene = new THREE.Scene();
  const pmrem = new THREE.PMREMGenerator(renderer);
  scene.environment = pmrem.fromScene(new RoomEnvironment(), 0.04).texture;

  // studio lighting: warm key, cool brand-coloured rim, soft fill
  const key = new THREE.DirectionalLight('#ffffff', 2.2); key.position.set(3, 4, 5); scene.add(key);
  const rim = new THREE.DirectionalLight(cfg.colors.rim || cfg.colors.primary, 2.4); rim.position.set(-4, 2.5, -3); scene.add(rim);
  scene.add(new THREE.HemisphereLight('#ffffff', '#c9c2e8', 0.5));

  const builders = { phone: buildPhone, panel: buildPanel, number: buildNumber, cham3d: buildCham3d, cham2d: buildCham2d };
  const built = await builders[cfg.kind]();
  hero = built.group;
  scene.add(hero);
  const shadow = blobShadow(built.shadowW, built.shadowW * 0.38);
  shadow.position.y = built.shadowY;
  scene.add(shadow);

  camera = new THREE.PerspectiveCamera(28, width / height, 0.1, 50);
  // frame the hero so it fills cfg.fill of the viewport height (or width on wide frames)
  const fill = cfg.fill || 0.82;
  const visH = (built.height + 0.5) / fill;
  const dist = Math.max(visH / 2 / Math.tan(THREE.MathUtils.degToRad(14)), (visH * 0.62) / (width / height) / 2 / Math.tan(THREE.MathUtils.degToRad(14)));
  camera.position.set(0, 0.25, dist);
  camera.lookAt(0, -0.08, 0);
  // shiftY > 0 moves the hero down the frame (leaves room for overlay text)
  if (cfg.shiftY) camera.setViewOffset(width, height, 0, -cfg.shiftY * height, width, height);
  if (document.fonts) await document.fonts.ready;
  window.renderAt(0, 1);
  return true;
};

window.renderAt = (t, duration) => {
  const phase = Math.sin((2 * Math.PI * t) / duration);
  const sway = cfg.sway ?? 0.32;
  hero.rotation.set(base.rx + 0.03 * Math.cos((2 * Math.PI * t) / duration), base.ry + sway * phase, base.rz);
  hero.position.y = base.y + 0.025 * Math.sin((4 * Math.PI * t) / duration);
  renderer.render(scene, camera);
};
