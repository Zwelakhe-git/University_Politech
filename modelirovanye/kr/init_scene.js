import * as THREE from 'three';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';

// --- Сцена ---
const scene = new THREE.Scene();
scene.background = new THREE.Color(0x111111);

// --- Камера ---
const camera = new THREE.PerspectiveCamera(
  60, window.innerWidth / window.innerHeight, 0.1, 1000
);
camera.position.set(9, 7, 14);
camera.lookAt(0, 0, 0);

// --- Рендерер ---
const renderer = new THREE.WebGLRenderer({ antialias: true });
renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
renderer.setSize(window.innerWidth, window.innerHeight);
document.body.appendChild(renderer.domElement);

// --- Управление мышью (вращение камеры) ---
const controls = new OrbitControls(camera, renderer.domElement);
controls.enableDamping = true;

// Цикл отрисовки один — в main.js

export { scene, THREE, controls, camera, renderer };
