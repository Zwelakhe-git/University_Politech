import * as THREE from 'three';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';

// --- Сцена, камера, рендерер ---
const scene = new THREE.Scene();
scene.background = new THREE.Color(0x1a1a1a);

const camera = new THREE.PerspectiveCamera(
  60, window.innerWidth / window.innerHeight, 0.1, 1000
);
camera.position.set(5, 5, 8);
camera.lookAt(0, 0, 0);

const renderer = new THREE.WebGLRenderer({ antialias: true });
renderer.setSize(window.innerWidth, window.innerHeight);
renderer.shadowMap.enabled = true;   // тени (на будущее)
document.body.appendChild(renderer.domElement);

const controls = new OrbitControls(camera, renderer.domElement);
controls.enableDamping = true;

scene.add(new THREE.AxesHelper(3));

// ОСВЕЩЕНИЕ
const ambient = new THREE.AmbientLight(0xffffff, 0.15);
scene.add(ambient);

// Точечный источник
const pointLight = new THREE.PointLight(0xffffff, 2.0, 100);
pointLight.position.set(5, 6, 5);
scene.add(pointLight);

// Визуализация положения источника
const lightMarker = new THREE.Mesh(
  new THREE.SphereGeometry(0.1, 12, 8),
  new THREE.MeshBasicMaterial({ color: 0xffff88 })
);
scene.add(lightMarker);

export { scene, pointLight, THREE, lightMarker, controls, camera, renderer }