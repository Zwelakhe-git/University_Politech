import { scene, THREE } from "./init.js";

const ambient = new THREE.AmbientLight(0xffffff, 0.15);
scene.add(ambient);

// Точечный источник — его параметры будем менять
const pointLight = new THREE.PointLight(0xffffff, 2.0, 100);
pointLight.position.set(5, 6, 5);
scene.add(pointLight);

// Визуализация положения источника — маленькая сфера
const lightMarker = new THREE.Mesh(
  new THREE.SphereGeometry(0.1, 12, 8),
  new THREE.MeshBasicMaterial({ color: 0xffff88 })
);

export function addLight(){
    scene.add(lightMarker);
}
export { lightMarker }