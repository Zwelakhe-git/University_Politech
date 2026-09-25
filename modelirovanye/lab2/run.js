import { makeCheckerTexture } from "./utils.js";
import { THREE, scene, pointLight, lightMarker, controls, renderer, camera } from "./init.js";
const checkerTex = makeCheckerTexture();
const cubeMat = new THREE.MeshStandardMaterial({
  map: checkerTex,
  roughness: 1.0,    // максимально матовый
  metalness: 0.0
});
const cube = new THREE.Mesh(new THREE.BoxGeometry(1.6, 1.6, 1.6), cubeMat);
cube.position.set(-2.5, 0, 0);
scene.add(cube);


// ПОЛУПРОЗРАЧНАЯ СФЕРА
const sphereMat = new THREE.MeshPhongMaterial({
  color: 0x33aaff,
  transparent: true,
  opacity: 0.55,        // > 0.5 
  shininess: 60,
  specular: 0x666666,
  side: THREE.DoubleSide
});
const sphere = new THREE.Mesh(new THREE.SphereGeometry(0.9, 32, 24), sphereMat);
sphere.position.set(0, 0, 0);
scene.add(sphere);

const torusMat = new THREE.MeshPhongMaterial({
  color: 0xffcc33,
  shininess: 100,       // максимальный блик
  specular: 0xffffff    // белый яркий блик
});
const torus = new THREE.Mesh(new THREE.TorusGeometry(1.0, 0.35, 32, 64), torusMat);
torus.position.set(2.5, 0, 0);
torus.rotation.x = Math.PI / 2;
scene.add(torus);


const state = {
  angle: 0,
  color: new THREE.Color(0xffffff),
  intensity: 2.0
};

// Вращение источника
function updateLight() {
  state.angle += 0.01;
  const r = 6;
  pointLight.position.set(
    Math.cos(state.angle) * r,
    4,
    Math.sin(state.angle) * r
  );
  lightMarker.position.copy(pointLight.position);
}

// Клавиши:
//   R — случайный цвет света
//   W — белый
//   + / - — интенсивность
window.addEventListener('keydown', (e) => {
  switch (e.key.toLowerCase()) {
    case 'r':
      pointLight.color.setHSL(Math.random(), 0.9, 0.6);
      break;
    case 'w':
      pointLight.color.set(0xffffff);
      break;
    case '+':
    case '=':
      pointLight.intensity = Math.min(10, pointLight.intensity + 0.5);
      break;
    case '-':
      pointLight.intensity = Math.max(0, pointLight.intensity - 0.5);
      break;
  }
});

function animate() {
  requestAnimationFrame(animate);
  updateLight();               // источник «бегает» вокруг сцены
  torus.rotation.z += 0.01;    // лёгкое вращение тора для наглядности блика
  controls.update();
  renderer.render(scene, camera);
}
animate();

window.addEventListener('resize', () => {
  camera.aspect = window.innerWidth / window.innerHeight;
  camera.updateProjectionMatrix();
  renderer.setSize(window.innerWidth, window.innerHeight);
});