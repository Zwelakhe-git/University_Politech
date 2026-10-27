
import { THREE, scene, camera, renderer } from "./init_scene.js";
import { Emitter } from "./Emitter.js";
import { Particle } from "./Particle.js";
import { Attractor } from "./Attractor.js";
import { ease } from "./animationFunctions.js";


const particles = [];
const PARTICLE_COUNT = 300;
let isPaused = false;

// Цилиндр-эмиттер

const cylinderSolidMaterial =  new THREE.MeshPhongMaterial({
    color: 0xffffff,
    shininess: 60,
    specular: 0x666666
});

const cylinderBasicMaterial = new THREE.MeshBasicMaterial({
    color: 0x888888,
    wireframe: true
});

const cylinder = new THREE.Mesh(
    new THREE.CylinderGeometry(2, 2, 4, 32, 1, true),
    cylinderBasicMaterial
);

scene.add(cylinder);

const emitter = new Emitter(cylinder);

setTimeout(() => {
    const duration = 2000;
    const startTime = performance.now();
    const endPos = [3,2,1];
    function _animate(now){
        const t = Math.min((now - startTime) / duration, 1);
        const eased = ease(t);
        cylinder.position.set(3 * eased, 2 * eased, 1 * eased);

        cylinder.rotation.set(
            (Math.PI / 4) * eased,
            (Math.PI / 6) * eased,
            (Math.PI / 3) * eased
        );

        cylinder.scale.set(1.5 * eased, 2  * eased, 0.75  * eased);
        if(t < 1){
            requestAnimationFrame(_animate);
        }
    }
    requestAnimationFrame(_animate);
    

}, 2000);
const attractor = new Attractor(-5, 5, 4);

// Создаём частицу
function createParticle() {
    const { position, direction } = emitter.emit();
    return new Particle(position, direction);
}

// Заполняем систему частицами
for (let i = 0; i < PARTICLE_COUNT; i++) {
    const particle = createParticle();

    // Случайный начальный возраст позволяет увидеть
    // частицы на разных этапах жизни
    particle.age = Math.random() * particle.lifetime;

    particles.push(particle);
}

let previousTime = performance.now();


function animate(now) {
    requestAnimationFrame(animate);

    if (isPaused) {
        renderer.render(scene, camera);
        previousTime = now;
        return;
    }

    const dt = Math.min((now - previousTime) / 1000, 0.05);
    previousTime = now;

    for (let i = 0; i < particles.length; i++) {
        const particle = particles[i];

        if (particle.isDead()) {
            particle.dispose();
            particles[i] = createParticle();
        } else {
            attractor.updateParticle(particle, dt);
            particle.update(dt);
            attractor.resolveCollision(particle);
            if (particle.trailPositions.length > 0) {
                particle.trailPositions[
                    particle.trailPositions.length - 1
                ].copy(particle.position);

                particle.trailGeometry.setFromPoints(
                    particle.trailPositions
                );
            }
        }
    }

    renderer.render(scene, camera);
}


requestAnimationFrame(animate);


document.addEventListener('DOMContentLoaded', () => {
    const strengthSlider = document.getElementById("strength_slider");
    const strengthText = document.getElementById("strength_text");
    const pauseButton = document.getElementById("pause_button");

    function updateStrength(value) {
        attractor.strength = Number(value);
        strengthText.textContent = attractor.strength;
        strengthSlider.value = attractor.strength;
    }

    strengthSlider.addEventListener("input", () => {
        updateStrength(strengthSlider.value);
    });

    window.addEventListener("keydown", (event) => {
        if (event.key === "+" || event.key === "=") {
            updateStrength(
                Math.min(20, attractor.strength + 0.5)
            );
        }

        if (event.key === "-") {
            updateStrength(
                Math.max(0, attractor.strength - 0.5)
            );
        }
    });

    pauseButton.addEventListener("click", () => {
        isPaused = !isPaused;
        pauseButton.textContent = isPaused ? "Продолжить" : "Пауза";
    });
})


