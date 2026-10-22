import * as THREE from 'three';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';

// --- Сцена ---
const scene = new THREE.Scene();
scene.background = new THREE.Color(0x111111);

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
scene.add(new THREE.AxesHelper(3));

export { scene, THREE, controls, camera, renderer }