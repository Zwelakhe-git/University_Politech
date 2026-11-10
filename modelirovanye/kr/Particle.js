import { THREE } from "./init_scene.js";

// Градиент цвета по относительному возрасту t = age / lifetime:
// синий (рождение) -> голубой -> жёлтый -> красный (смерть)
const COLOR_STOPS = [
    { t: 0.0,  color: new THREE.Color(0x2a5cff) },
    { t: 0.35, color: new THREE.Color(0x00e5ff) },
    { t: 0.7,  color: new THREE.Color(0xffd400) },
    { t: 1.0,  color: new THREE.Color(0xff2a00) }
];

export const TRAIL_MIN = 2;          // минимальная длина следа (по заданию)
export const TRAIL_MAX = 4;          // максимальная длина следа (по заданию)
const TRAIL_STEP = 0.06;             // как часто (сек) запоминается положение для следа

function lifetimeColor(t, target) {
    for (let i = 1; i < COLOR_STOPS.length; i++) {
        const a = COLOR_STOPS[i - 1];
        const b = COLOR_STOPS[i];
        if (t <= b.t) {
            const k = (t - a.t) / (b.t - a.t);
            return target.copy(a.color).lerp(b.color, k);
        }
    }
    return target.copy(COLOR_STOPS[COLOR_STOPS.length - 1].color);
}

/**
 * Частица — точка с массой. Набор свойств постоянен:
 * координаты, скорость, ускорение, масса, размер, цвет,
 * время жизни, наличие следа и сам след.
 */
export class Particle {
    constructor() {
        this.position = new THREE.Vector3();
        this.velocity = new THREE.Vector3();
        this.acceleration = new THREE.Vector3();

        this.mass = 1;
        this.size = 0.1;
        this.color = new THREE.Color();

        this.age = 0;
        this.lifetime = 1;
        this.alive = false;
        this.spawnDelay = 0;      // задержка перед рождением (чтобы частицы не рождались все разом)

        this.hasTrail = true;
        this.trailLength = TRAIL_MIN;
        this.trail = [];          // последние положения частицы
        this.trailTimer = 0;

        this.onSurface = false;   // частица «прилипла» к аттрактору
    }

    // Инициализация свойств начальными значениями при рождении
    spawn(position, direction) {
        this.position.copy(position);

        // Начальное направление — нормаль к поверхности эмиттера
        const speed = 2 + Math.random() * 1.5;
        this.velocity.copy(direction).multiplyScalar(speed);
        this.acceleration.set(0, 0, 0);

        this.mass = 0.8 + Math.random() * 0.4;
        this.size = 0.08 + Math.random() * 0.06;

        this.age = 0;
        this.lifetime = 4 + Math.random() * 3;
        this.alive = true;
        this.onSurface = false;

        this.hasTrail = true;
        // Длина следа — случайное целое от 2 до 4
        this.trailLength = TRAIL_MIN +
            Math.floor(Math.random() * (TRAIL_MAX - TRAIL_MIN + 1));
        this.trail.length = 0;
        this.trailTimer = 0;

        lifetimeColor(0, this.color);
    }

    // Сила, действующая на частицу: a = F / m
    applyForce(force) {
        this.acceleration.addScaledVector(force, 1 / this.mass);
    }

    // Ускорение, не зависящее от массы (например, гравитация)
    applyAcceleration(acc) {
        this.acceleration.add(acc);
    }

    update(dt) {
        this.age += dt;

        // Скорость = Скорость + Ускорение * dtime
        this.velocity.addScaledVector(this.acceleration, dt);
        // Позиция = Позиция + Скорость * dtime
        this.position.addScaledVector(this.velocity, dt);

        // Ускорение пересчитывается заново на каждом такте
        this.acceleration.set(0, 0, 0);

        // Цвет зависит от времени жизни
        const t = Math.min(this.age / this.lifetime, 1);
        lifetimeColor(t, this.color);

        // След: запоминаем положения через равные промежутки времени
        if (this.hasTrail) {
            this.trailTimer += dt;
            if (this.trailTimer >= TRAIL_STEP) {
                this.trailTimer = 0;
                this.trail.push(this.position.clone());
                if (this.trail.length > this.trailLength) {
                    this.trail.shift();
                }
            }
        }
    }

    isDead() {
        return this.age >= this.lifetime;
    }
}
