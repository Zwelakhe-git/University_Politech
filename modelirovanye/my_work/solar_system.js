import { scene, renderer, camera, controls, THREE } from "./init_scene.js";

const ambient = new THREE.AmbientLight(0xffffff, 0.25);
scene.add(ambient);

const sunRadius = 3;
const earthRadius = 1;
const moonRadius = 0.3;
const earthDistanceFromSun = 10;
const moonDistanceFromEarth = 2;

const yellow = 0xf0d804;
const sunLight = new THREE.PointLight(yellow, 1.5, 0, 0)
const sunGeo = new THREE.SphereGeometry(sunRadius, 24, 24)
const earthGeo = new THREE.SphereGeometry(earthRadius, 24, 24);
const moonGeo = new THREE.SphereGeometry(moonRadius, 24, 24);

const sunMaterial = new THREE.MeshBasicMaterial({ color: yellow });
const earthTexture = new THREE.TextureLoader().load("images/Screenshot_20260919-150839.png");
const earthMaterial = new THREE.MeshPhongMaterial({
    map: earthTexture,
    shininess: 10,
    color: 0x3377ff
});
const moonMaterial = new THREE.MeshPhongMaterial({
    shininess: 0,
    color: 0xcccccc
    
});

const earthPivot = new THREE.Object3D();
const moonPivot = new THREE.Object3D();

const sun = new THREE.Mesh(sunGeo, sunMaterial);
const earth = new THREE.Mesh(earthGeo, earthMaterial);
const moon = new THREE.Mesh(moonGeo, moonMaterial);

sunLight.position.set(0, 0, 0);
sunLight.castShadow = true;
sunLight.shadow.mapSize.set(1024, 1024);
sunLight.add(sun);
scene.add(sunLight)

earth.castShadow = true;
earth.receiveShadow = true;
earth.position.set(earthDistanceFromSun, 0, 0);
earthPivot.add(earth);

moon.castShadow = true;
moon.receiveShadow = true;
moon.position.set(moonDistanceFromEarth, 0, 0);
earth.add(moonPivot);
moonPivot.add(moon);

scene.add(earthPivot);

const clock = new THREE.Clock();

let earthOrbitAngle = 0;
let earthSpinAngle = 0;
let moonOrbitAngle = 0;
function animate(){
    requestAnimationFrame(animate);
    const dt = clock.getDelta();
    earthOrbitAngle += dt * 0.3;
    earthSpinAngle += dt * 0.3;
    moonOrbitAngle += dt * 0.8;
    //earthPivot.rotation.y = earthOrbitAngle;
    earth.rotation.y = earthSpinAngle;
    moonPivot.rotation.y = moonOrbitAngle;
    controls.update();
    renderer.render(scene, camera);
}

animate();
