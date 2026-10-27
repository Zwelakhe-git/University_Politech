import * as THREE from 'three';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';

// --- Сцена ---
const scene = new THREE.Scene();
scene.background = new THREE.Color(0x111111);
const ambient = new THREE.AmbientLight(0xffffff, 0.15)
// --- Камера ---
const camera = new THREE.PerspectiveCamera(
  60, window.innerWidth / window.innerHeight, 0.1, 1000
);
camera.position.set(5, 5, 8);
camera.lookAt(0, 0, 0);


// --- Рендерер ---
const renderer = new THREE.WebGLRenderer({ antialias: true });
renderer.setSize(window.innerWidth, window.innerHeight);
document.body.appendChild(renderer.domElement);

// --- Управление мышью (вращение камеры) ---
const controls = new OrbitControls(camera, renderer.domElement);
controls.enableDamping = true;

// --- Вспомогательные оси ---
//scene.add(new THREE.AxesHelper(3));

function init_animate() {
  requestAnimationFrame(init_animate);
  controls.update();
  renderer.render(scene, camera);
}

window.addEventListener('resize', () => {
  camera.aspect = window.innerWidth / window.innerHeight;
  camera.updateProjectionMatrix();
  renderer.setSize(window.innerWidth, window.innerHeight);
});

document.addEventListener('DOMContentLoaded', function(){
    init_animate();
    
})

const pointLight = new THREE.PointLight(0xffffff, 180, 100, 2);
pointLight.position.set(0, 8, 5);
pointLight.castShadow = true;
pointLight.shadow.mapSize.set(2048, 2048);
pointLight.shadow.camera.near = 0.1;
pointLight.shadow.camera.far = 40;
pointLight.shadow.bias = -0.0002;
pointLight.shadow.normalBias = 0.025;
pointLight.shadow.radius = 4;
//scene.add(pointLight);

const lightMarker = new THREE.Mesh(
  new THREE.SphereGeometry(0.16, 16, 12),
  new THREE.MeshBasicMaterial({ color: 0xffffff })
);
pointLight.add(lightMarker);


export { scene, THREE, controls, camera, renderer }