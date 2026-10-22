import * as THREE from 'three';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';


const scene = new THREE.Scene();
scene.background = new THREE.Color(0x111111);

const camera = new THREE.PerspectiveCamera(
  60, window.innerWidth / window.innerHeight, 0.1, 1000
);
camera.position.set(9, 7, 12);
camera.lookAt(0, 0, 0);

const renderer = new THREE.WebGLRenderer({ antialias: true });
renderer.setSize(window.innerWidth, window.innerHeight);
renderer.setPixelRatio(window.devicePixelRatio);
renderer.shadowMap.enabled = true;
renderer.shadowMap.type = THREE.PCFSoftShadowMap;
document.body.appendChild(renderer.domElement);

const controls = new OrbitControls(camera, renderer.domElement);
controls.enableDamping = true;
controls.target.set(0, 0, 0);


const ambient = new THREE.AmbientLight(0xffffff, 0.25);
scene.add(ambient);

const pointLight = new THREE.PointLight(0xffffff, 1.5, 0, 2);
pointLight.position.set(5, 6, 5);
pointLight.castShadow = true;
pointLight.shadow.mapSize.set(1024, 1024);
scene.add(pointLight);

// Визуализация источника — маленькая сфера, чтобы его было видно
const lightMarker = new THREE.Mesh(
  new THREE.SphereGeometry(0.15, 16, 12),
  new THREE.MeshBasicMaterial({ color: 0xffffff })
);
pointLight.add(lightMarker);

function makeBrickTexture(size = 512) {
  const c = document.createElement('canvas');
  c.width = c.height = size;
  const ctx = c.getContext('2d');

  ctx.fillStyle = '#7a3b2e';
  ctx.fillRect(0, 0, size, size);

  const rows = 8;
  const cols = 4;
  const bh = size / rows;
  const bw = size / cols;
  const mortar = 6;

  for (let r = 0; r < rows; r++) {
    const offset = (r % 2) * (bw / 2);
    for (let ccol = -1; ccol < cols + 1; ccol++) {
      const x = ccol * bw + offset;
      const y = r * bh;

      const grad = ctx.createLinearGradient(x, y, x, y + bh);
      const shade = 150 + Math.floor(Math.random() * 40);
      grad.addColorStop(0, `rgb(${shade + 30},${shade - 40},${shade - 70})`);
      grad.addColorStop(1, `rgb(${shade - 20},${shade - 70},${shade - 90})`);
      ctx.fillStyle = grad;
      ctx.fillRect(x + mortar / 2, y + mortar / 2, bw - mortar, bh - mortar);

      // шум
      ctx.fillStyle = 'rgba(0,0,0,0.06)';
      for (let i = 0; i < 40; i++) {
        const nx = x + mortar / 2 + Math.random() * (bw - mortar);
        const ny = y + mortar / 2 + Math.random() * (bh - mortar);
        ctx.fillRect(nx, ny, 2, 2);
      }
    }
  }

  const tex = new THREE.CanvasTexture(c);
  tex.wrapS = tex.wrapT = THREE.RepeatWrapping;
  tex.repeat.set(2, 2);
  tex.colorSpace = THREE.SRGBColorSpace;
  return tex;
}

function makeBumpTexture(size = 512) {
  const c = document.createElement('canvas');
  c.width = c.height = size;
  const ctx = c.getContext('2d');

  ctx.fillStyle = '#000';
  ctx.fillRect(0, 0, size, size);

  const rows = 8, cols = 4;
  const bh = size / rows, bw = size / cols;
  const mortar = 6;

  for (let r = 0; r < rows; r++) {
    const offset = (r % 2) * (bw / 2);
    for (let ccol = -1; ccol < cols + 1; ccol++) {
      const x = ccol * bw + offset;
      const y = r * bh;
      ctx.fillStyle = '#cccccc';
      ctx.fillRect(x + mortar / 2, y + mortar / 2, bw - mortar, bh - mortar);
    }
  }

  const tex = new THREE.CanvasTexture(c);
  tex.wrapS = tex.wrapT = THREE.RepeatWrapping;
  tex.repeat.set(2, 2);
  return tex;
}

const cubeGeo = new THREE.BoxGeometry(3, 3, 3);
const cubeMat = new THREE.MeshPhongMaterial({
  map: makeBrickTexture(),
  bumpMap: makeBumpTexture(),
  bumpScale: 0.15,
  shininess: 0,          
  specular: 0x000000,
  color: 0xffffff
});
const cube = new THREE.Mesh(cubeGeo, cubeMat);
cube.castShadow = true;
cube.receiveShadow = true;
scene.add(cube);

const sphereGeo = new THREE.SphereGeometry(1.2, 48, 32);
const sphereMat = new THREE.MeshPhongMaterial({
  color: 0x33ccff,
  transparent: true,
  opacity: 0.6,          
  shininess: 80,
  specular: 0xffffff,
  side: THREE.DoubleSide,
  depthWrite: false
});
const sphere = new THREE.Mesh(sphereGeo, sphereMat);
sphere.castShadow = true;
sphere.position.set(0, 0, 5); // внутри куба
scene.add(sphere);

const torusGeo = new THREE.TorusGeometry(1.6, 0.5, 32, 64);
const torusMat = new THREE.MeshPhongMaterial({
  color: 0xffaa22,
  shininess: 1000,       // максимальная полировка
  specular: 0xffffff,
  reflectivity: 1
});
const torus = new THREE.Mesh(torusGeo, torusMat);
torus.castShadow = true;
torus.receiveShadow = true;
torus.position.set(4.5, 0, 0);
torus.rotation.x = Math.PI / 2; // по заданию 3.4
scene.add(torus);

const tetraGeo = new THREE.TetrahedronGeometry(1.3, 0);
const tetraMat = new THREE.MeshPhongMaterial({
  color: 0x44ff88,
  shininess: 30,
  specular: 0x333333,
  flatShading: true
});
const tetra = new THREE.Mesh(tetraGeo, tetraMat);
tetra.castShadow = true;
tetra.receiveShadow = true;
tetra.position.set(-4.5, 0, 0);
tetra.translateZ(3); // по заданию 3.4 — сдвиг по Z
scene.add(tetra);


const ui = {
  color:        document.getElementById('light-color'),
  intensity:    document.getElementById('light-intensity'),
  intensityVal: document.getElementById('light-intensity-val'),
  x: document.getElementById('light-x'), xVal: document.getElementById('light-x-val'),
  y: document.getElementById('light-y'), yVal: document.getElementById('light-y-val'),
  z: document.getElementById('light-z'), zVal: document.getElementById('light-z-val'),
  toggleOrbit:  document.getElementById('toggle-orbit')
};

function syncLightFromUI() {
  pointLight.color.set(ui.color.value);
  pointLight.intensity = parseFloat(ui.intensity.value);
  pointLight.position.set(
    parseFloat(ui.x.value),
    parseFloat(ui.y.value),
    parseFloat(ui.z.value)
  );
  lightMarker.material.color.set(ui.color.value);

  ui.intensityVal.textContent = ui.intensity.value;
  ui.xVal.textContent = ui.x.value;
  ui.yVal.textContent = ui.y.value;
  ui.zVal.textContent = ui.z.value;
}

['input', 'change'].forEach(evt => {
  ui.color.addEventListener(evt, syncLightFromUI);
  ui.intensity.addEventListener(evt, syncLightFromUI);
  ui.x.addEventListener(evt, syncLightFromUI);
  ui.y.addEventListener(evt, syncLightFromUI);
  ui.z.addEventListener(evt, syncLightFromUI);
});
syncLightFromUI();


let orbiting = true;
let orbitAngle = 0;
const orbitRadius = 6;
const orbitHeight = 5;

ui.toggleOrbit.addEventListener('click', () => {
  orbiting = !orbiting;
  ui.toggleOrbit.textContent = orbiting
    ? '⏸ Остановить вращение'
    : '▶ Запустить вращение';
});


let shiftDown = false;
let mouseNDC = new THREE.Vector2(0, 0);

window.addEventListener('keydown', e => { if (e.key === 'Shift') shiftDown = true; });
window.addEventListener('keyup',   e => { if (e.key === 'Shift') shiftDown = false; });

window.addEventListener('mousemove', e => {
  mouseNDC.x = (e.clientX / window.innerWidth)  * 2 - 1;
  mouseNDC.y = -(e.clientY / window.innerHeight) * 2 + 1;
});


const clock = new THREE.Clock();

function animate() {
  requestAnimationFrame(animate);
  const dt = clock.getDelta();

  if (orbiting && !shiftDown) {
    orbitAngle += dt * 0.8;
    pointLight.position.set(
      Math.cos(orbitAngle) * orbitRadius,
      orbitHeight,
      Math.sin(orbitAngle) * orbitRadius
    );
    ui.x.value = pointLight.position.x.toFixed(1);
    ui.y.value = pointLight.position.y.toFixed(1);
    ui.z.value = pointLight.position.z.toFixed(1);
    ui.xVal.textContent = ui.x.value;
    ui.yVal.textContent = ui.y.value;
    ui.zVal.textContent = ui.z.value;
  } else if (shiftDown) {
    const vFov = (camera.fov * Math.PI) / 180;
    const dist = camera.position.length();
    const height = 2 * Math.tan(vFov / 2) * dist;
    const width = height * camera.aspect;

    const x = mouseNDC.x * width / 2;
    const y = mouseNDC.y * height / 2;

    pointLight.position.set(x, y, 0);

    ui.x.value = x.toFixed(1);
    ui.y.value = y.toFixed(1);
    ui.z.value = 4;
    ui.xVal.textContent = ui.x.value;
    ui.yVal.textContent = ui.y.value;
    ui.zVal.textContent = ui.z.value;
  }

  
  torus.rotation.z += dt * 0.3;

  controls.update();
  renderer.render(scene, camera);
}
animate();

window.addEventListener('resize', () => {
  camera.aspect = window.innerWidth / window.innerHeight;
  camera.updateProjectionMatrix();
  renderer.setSize(window.innerWidth, window.innerHeight);
});