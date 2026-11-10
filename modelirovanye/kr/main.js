import { THREE, scene, camera, renderer, controls } from "./init_scene.js";
import { Emitter } from "./Emitter.js";
import { Attractor } from "./Attractor.js";
import { ParticleSystem } from "./ParticleSystem.js";
import { Knob } from "./Knob.js";

const PARTICLE_COUNT = 600;
const MAX_STRENGTH = 20;

// --- Цилиндр-эмиттер ---
const cylinder = new THREE.Mesh(
    new THREE.CylinderGeometry(1.5, 1.5, 3, 32, 1, false),
    new THREE.MeshBasicMaterial({ color: 0x888888, wireframe: true })
);
scene.add(cylinder);

const emitter = new Emitter(cylinder);
// Поворот эмиттера задаётся регуляторами на панели справа.
// Emitter.emit() каждый раз берёт текущую мировую матрицу цилиндра,
// поэтому частицы рождаются на поверхности и по нормали при любом повороте.

// --- Плоскость-аттрактор (ограниченная) ---
const ATTRACTOR_BASE_POSITION = new THREE.Vector3(0, -4, 0);
const ATTRACTOR_BASE_ROTATION = new THREE.Euler(-Math.PI / 2, 0, 0);   // горизонтальная

const attractor = new Attractor({
    position: ATTRACTOR_BASE_POSITION,
    rotation: ATTRACTOR_BASE_ROTATION,
    width: 16,
    height: 16,
    range: 7,
    strength: 6
});

// --- Дополнительная сила (сверх задания): гравитация, клавиша G ---
const gravity = new THREE.Vector3(0, -2, 0);
let gravityOn = false;

// --- Система частиц ---
const system = new ParticleSystem(PARTICLE_COUNT, emitter);
system.forces.push((p) => attractor.applyForce(p));
system.forces.push((p) => { if (gravityOn) p.applyAcceleration(gravity); });
system.contacts.push((p) => attractor.resolveContact(p));
system.setViewportHeight(window.innerHeight * renderer.getPixelRatio());

// --- Главный цикл ---
let isPaused = false;
let previousTime = performance.now();

function animate(now) {
    requestAnimationFrame(animate);

    // Дискретный такт времени dtime (ограничен, чтобы не было скачков)
    const dt = Math.min((now - previousTime) / 1000, 0.05);
    previousTime = now;

    if (!isPaused) system.update(dt);

    controls.update();
    renderer.render(scene, camera);
}
requestAnimationFrame(animate);

window.addEventListener("resize", () => {
    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(window.innerWidth, window.innerHeight);
    system.setViewportHeight(window.innerHeight * renderer.getPixelRatio());
});

// --- Интерфейс ---
const strengthSlider = document.getElementById("strength_slider");
const strengthText = document.getElementById("strength_text");
const pauseButton = document.getElementById("pause_button");
const gravityText = document.getElementById("gravity_text");
const trailsText = document.getElementById("trails_text");

function setStrength(value) {
    attractor.strength = Math.max(0, Math.min(MAX_STRENGTH, Number(value)));
    strengthText.textContent = attractor.strength;
    strengthSlider.value = attractor.strength;
}

function togglePause() {
    isPaused = !isPaused;
    pauseButton.textContent = isPaused ? "Продолжить" : "Пауза";
}

function updateStatus() {
    gravityText.textContent = gravityOn ? "вкл" : "выкл";
    trailsText.textContent = system.showTrails ? "вкл" : "выкл";
}

strengthSlider.addEventListener("input", () => setStrength(strengthSlider.value));
pauseButton.addEventListener("click", togglePause);

window.addEventListener("keydown", (event) => {
    if (event.target === strengthSlider && event.key.startsWith("Arrow")) return;

    switch (event.key) {
        case "+":
        case "=":
            setStrength(attractor.strength + 0.5);
            break;
        case "-":
        case "_":
            setStrength(attractor.strength - 0.5);
            break;
        case "g":
        case "G":
        case "п":
        case "П":
            gravityOn = !gravityOn;
            break;
        case "t":
        case "T":
        case "е":
        case "Е":
            system.showTrails = !system.showTrails;
            break;
        case " ":
            event.preventDefault();
            togglePause();
            break;
    }
    updateStatus();
});

setStrength(attractor.strength);
updateStatus();

// --- Вращение эмиттера: три регулятора (вокруг осей X, Y, Z) ---
const DEG = Math.PI / 180;
const emitterKnobsBox = document.getElementById("emitter_knobs");

const emitterKnobs = ["x", "y", "z"].map((axis) => new Knob(emitterKnobsBox, {
    label: `Ось ${axis.toUpperCase()}`,
    value: 0,
    onChange: (deg) => { cylinder.rotation[axis] = deg * DEG; }
}));

document.getElementById("emitter_reset").addEventListener("click", () => {
    emitterKnobs.forEach((k) => k.setValue(0));
});

// --- Положение аттрактора: координаты центра и наклон ---
const attractorState = {
    x: ATTRACTOR_BASE_POSITION.x,
    y: ATTRACTOR_BASE_POSITION.y,
    z: ATTRACTOR_BASE_POSITION.z,
    tiltX: 0,
    tiltZ: 0
};

const baseQuaternion = new THREE.Quaternion().setFromEuler(ATTRACTOR_BASE_ROTATION);
const tiltEuler = new THREE.Euler();
const tiltQuaternion = new THREE.Quaternion();

function applyAttractorTransform() {
    const s = attractorState;
    attractor.mesh.position.set(s.x, s.y, s.z);

    // Наклон относительно горизонтального положения (вокруг мировых осей X и Z)
    tiltEuler.set(s.tiltX * DEG, 0, s.tiltZ * DEG);
    tiltQuaternion.setFromEuler(tiltEuler);
    attractor.mesh.quaternion.copy(tiltQuaternion).multiply(baseQuaternion);

    attractor.updateBasis();

    // Плоскость сдвинулась — частицы, лежавшие на ней, отпускаем,
    // дальше их снова притянет по обычным правилам
    for (const p of system.particles) p.onSurface = false;
}

const axisSliders = ["x", "y", "z"].map((axis) => {
    const input = document.getElementById(`attr_${axis}`);
    const text = document.getElementById(`attr_${axis}_text`);
    const set = (v) => {
        attractorState[axis] = Number(v);
        input.value = v;
        text.textContent = Number(v).toFixed(1).replace(/\.0$/, "");
        applyAttractorTransform();
    };
    input.addEventListener("input", () => set(input.value));
    return { axis, set };
});

const attractorKnobsBox = document.getElementById("attractor_knobs");
const tiltKnobs = [
    new Knob(attractorKnobsBox, {
        label: "Наклон X",
        onChange: (deg) => { attractorState.tiltX = deg; applyAttractorTransform(); }
    }),
    new Knob(attractorKnobsBox, {
        label: "Наклон Z",
        onChange: (deg) => { attractorState.tiltZ = deg; applyAttractorTransform(); }
    })
];

document.getElementById("attractor_reset").addEventListener("click", () => {
    axisSliders.forEach(({ axis, set }) => set(ATTRACTOR_BASE_POSITION[axis]));
    tiltKnobs.forEach((k) => k.setValue(0));
});
