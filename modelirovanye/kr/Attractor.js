import { THREE, scene } from "./init_scene.js";

/**
 * Аттрактор — ограниченная плоскость произвольной ориентации.
 * Если частица находится над (или под) плоскостью в пределах её границ
 * и расстояние до плоскости меньше range, на неё действует сила,
 * направленная по нормали к плоскости (в сторону плоскости).
 * Сила растёт по мере приближения: F = strength * (1 - d / range).
 * Вектор скорости частицы складывается с этим вектором (V += A * dt),
 * поэтому частица плавно поворачивает и разгоняется к плоскости.
 */
export class Attractor {
    constructor({
        position = new THREE.Vector3(0, -4, 0),
        rotation = new THREE.Euler(-Math.PI / 2, 0, 0),
        width = 14,
        height = 14,
        range = 6,
        strength = 6
    } = {}) {
        this.width = width;
        this.height = height;
        this.range = range;
        this.strength = strength;

        this.geometry = new THREE.PlaneGeometry(width, height, 14, 14);

        // Каркас плоскости
        this.material = new THREE.MeshBasicMaterial({
            color: 0x22aa88,
            side: THREE.DoubleSide,
            wireframe: true
        });
        this.mesh = new THREE.Mesh(this.geometry, this.material);

        // Полупрозрачная заливка, чтобы плоскость читалась лучше
        this.fill = new THREE.Mesh(
            this.geometry,
            new THREE.MeshBasicMaterial({
                color: 0x22aa88,
                side: THREE.DoubleSide,
                transparent: true,
                opacity: 0.08,
                depthWrite: false
            })
        );
        this.mesh.add(this.fill);

        this.mesh.position.copy(position);
        this.mesh.rotation.copy(rotation);
        scene.add(this.mesh);

        // Локальный базис плоскости в мировых координатах
        this.center = new THREE.Vector3();
        this.normal = new THREE.Vector3();
        this.axisU = new THREE.Vector3();
        this.axisV = new THREE.Vector3();
        this.updateBasis();

        this._rel = new THREE.Vector3();
        this._force = new THREE.Vector3();
    }

    updateBasis() {
        this.mesh.updateWorldMatrix(true, false);
        const q = new THREE.Quaternion();
        this.mesh.getWorldPosition(this.center);
        this.mesh.getWorldQuaternion(q);

        // PlaneGeometry лежит в плоскости XY, нормаль — ось Z
        this.normal.set(0, 0, 1).applyQuaternion(q);
        this.axisU.set(1, 0, 0).applyQuaternion(q);
        this.axisV.set(0, 1, 0).applyQuaternion(q);
    }

    // Знаковое расстояние до плоскости и попадание в её границы
    measure(point) {
        this._rel.subVectors(point, this.center);
        const distance = this._rel.dot(this.normal);
        const u = this._rel.dot(this.axisU);
        const v = this._rel.dot(this.axisV);
        const inside =
            Math.abs(u) <= this.width / 2 &&
            Math.abs(v) <= this.height / 2;
        return { distance, inside };
    }

    // Применить силу притяжения к частице (до шага интегрирования)
    applyForce(particle) {
        const { distance, inside } = this.measure(particle.position);
        particle.attractorSide = Math.sign(distance);

        if (particle.onSurface || !inside) return;

        const d = Math.abs(distance);
        if (d >= this.range || d < 1e-6) return;

        // Чем ближе к плоскости, тем больше сила
        const falloff = 1 - d / this.range;
        const magnitude = this.strength * falloff;

        // Направление — по нормали к плоскости, в сторону плоскости
        this._force
            .copy(this.normal)
            .multiplyScalar(-Math.sign(distance) * magnitude);

        particle.applyForce(this._force);
    }

    // После шага: если частица долетела до плоскости — она «прилипает»
    // и скользит по поверхности (нормальная составляющая скорости гасится)
    resolveContact(particle) {
        const { distance, inside } = this.measure(particle.position);
        if (!inside) {
            particle.onSurface = false;
            return;
        }

        const side = particle.attractorSide || Math.sign(distance);
        const offset = particle.size * 0.5;
        const crossed = Math.sign(distance) !== side;

        if (crossed || Math.abs(distance) < offset || particle.onSurface) {
            // Ставим частицу на поверхность с той стороны, откуда она пришла
            particle.position.addScaledVector(
                this.normal,
                side * offset - distance
            );

            // Убираем нормальную составляющую скорости
            const vn = particle.velocity.dot(this.normal);
            particle.velocity.addScaledVector(this.normal, -vn);

            // Трение при скольжении по плоскости
            particle.velocity.multiplyScalar(0.98);

            particle.onSurface = true;
        }
    }

    dispose() {
        scene.remove(this.mesh);
        this.geometry.dispose();
        this.material.dispose();
        this.fill.material.dispose();
    }
}
