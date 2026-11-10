import { THREE, scene } from "./init_scene.js";
import { Particle, TRAIL_MAX } from "./Particle.js";

// Частица рисуется маленьким кругом (point sprite), а не объёмной фигурой.
// Размер и цвет у каждой частицы свои.
const vertexShader = /* glsl */ `
    attribute float pSize;
    attribute vec3 pColor;
    uniform float scale;
    varying vec3 vColor;

    void main() {
        vColor = pColor;
        vec4 mvPosition = modelViewMatrix * vec4(position, 1.0);
        gl_PointSize = pSize * scale / -mvPosition.z;
        gl_Position = projectionMatrix * mvPosition;
    }
`;

const fragmentShader = /* glsl */ `
    varying vec3 vColor;

    void main() {
        float r = length(gl_PointCoord - vec2(0.5));
        if (r > 0.5) discard;
        float alpha = smoothstep(0.5, 0.3, r);
        gl_FragColor = vec4(vColor, alpha);
    }
`;

export class ParticleSystem {
    constructor(count, emitter) {
        this.count = count;
        this.emitter = emitter;
        this.forces = [];          // функции (particle) => void
        this.contacts = [];        // функции (particle) => void
        this.showTrails = true;

        this.particles = [];
        for (let i = 0; i < count; i++) {
            const p = new Particle();
            // Рождение частиц растянуто во времени,
            // чтобы поток был равномерным
            p.spawnDelay = Math.random() * 5;
            this.particles.push(p);
        }

        // --- Буферы для точек ---
        this.positions = new Float32Array(count * 3);
        this.colors = new Float32Array(count * 3);
        this.sizes = new Float32Array(count);

        this.pointsGeometry = new THREE.BufferGeometry();
        this.pointsGeometry.setAttribute("position", new THREE.BufferAttribute(this.positions, 3));
        this.pointsGeometry.setAttribute("pColor", new THREE.BufferAttribute(this.colors, 3));
        this.pointsGeometry.setAttribute("pSize", new THREE.BufferAttribute(this.sizes, 1));

        this.pointsMaterial = new THREE.ShaderMaterial({
            uniforms: { scale: { value: 1 } },
            vertexShader,
            fragmentShader,
            transparent: true,
            depthWrite: false
        });

        this.points = new THREE.Points(this.pointsGeometry, this.pointsMaterial);
        this.points.frustumCulled = false;
        scene.add(this.points);

        // --- Буферы для следов (отрезки между последними положениями) ---
        const maxSegments = count * TRAIL_MAX;
        this.trailPositions = new Float32Array(maxSegments * 2 * 3);
        this.trailColors = new Float32Array(maxSegments * 2 * 3);

        this.trailGeometry = new THREE.BufferGeometry();
        this.trailGeometry.setAttribute("position", new THREE.BufferAttribute(this.trailPositions, 3));
        this.trailGeometry.setAttribute("color", new THREE.BufferAttribute(this.trailColors, 3));

        this.trailMaterial = new THREE.LineBasicMaterial({
            vertexColors: true,
            transparent: true,
            opacity: 0.9,
            depthWrite: false
        });

        this.trails = new THREE.LineSegments(this.trailGeometry, this.trailMaterial);
        this.trails.frustumCulled = false;
        scene.add(this.trails);
    }

    setViewportHeight(height) {
        // Пересчёт размера точки из мировых единиц в пиксели (fov = 60°)
        this.pointsMaterial.uniforms.scale.value = height / (2 * Math.tan(Math.PI / 6));
    }

    respawn(p) {
        const { position, direction } = this.emitter.emit();
        p.spawn(position, direction);
    }

    update(dt) {
        for (const p of this.particles) {
            if (!p.alive) {
                p.spawnDelay -= dt;
                if (p.spawnDelay <= 0) this.respawn(p);
                continue;
            }

            // По окончании жизни частица исчезает и рождается новая
            if (p.isDead()) {
                this.respawn(p);
                continue;
            }

            for (const force of this.forces) force(p);
            p.update(dt);
            for (const contact of this.contacts) contact(p);
        }
        this.writeBuffers();
    }

    writeBuffers() {
        let seg = 0;
        const tp = this.trailPositions;
        const tc = this.trailColors;

        const putVertex = (index, pos, color, k) => {
            tp[index * 3] = pos.x;
            tp[index * 3 + 1] = pos.y;
            tp[index * 3 + 2] = pos.z;
            // След затухает к хвосту (темнеет до цвета фона)
            tc[index * 3] = color.r * k;
            tc[index * 3 + 1] = color.g * k;
            tc[index * 3 + 2] = color.b * k;
        };

        for (let i = 0; i < this.count; i++) {
            const p = this.particles[i];

            this.positions[i * 3] = p.position.x;
            this.positions[i * 3 + 1] = p.position.y;
            this.positions[i * 3 + 2] = p.position.z;
            this.colors[i * 3] = p.color.r;
            this.colors[i * 3 + 1] = p.color.g;
            this.colors[i * 3 + 2] = p.color.b;
            this.sizes[i] = p.alive ? p.size : 0;

            if (!p.alive || !p.hasTrail || !this.showTrails) continue;

            // Цепочка: trail[0] -> trail[1] -> ... -> текущее положение
            const pts = p.trail;
            const n = pts.length;
            for (let j = 0; j < n; j++) {
                const a = pts[j];
                const b = j + 1 < n ? pts[j + 1] : p.position;
                const ka = (j + 1) / (n + 1);
                const kb = (j + 2) / (n + 1);
                putVertex(seg * 2, a, p.color, ka);
                putVertex(seg * 2 + 1, b, p.color, kb);
                seg++;
            }
        }

        this.pointsGeometry.attributes.position.needsUpdate = true;
        this.pointsGeometry.attributes.pColor.needsUpdate = true;
        this.pointsGeometry.attributes.pSize.needsUpdate = true;

        this.trailGeometry.setDrawRange(0, seg * 2);
        this.trailGeometry.attributes.position.needsUpdate = true;
        this.trailGeometry.attributes.color.needsUpdate = true;
    }
}
