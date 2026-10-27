
import { THREE, scene } from "./init_scene.js";

export class Attractor {
    constructor(y = -3, range = 5, strength = 4) {
        this.position = new THREE.Vector3(0, y, 0);
        this.range = range;
        this.strength = strength;

        this.geometry = new THREE.PlaneGeometry(12, 12);

        this.material = new THREE.MeshBasicMaterial({
            color: 0x22aa88,
            side: THREE.DoubleSide,
            wireframe: true
        });

        this.mesh = new THREE.Mesh(
            this.geometry,
            this.material
        );

        this.mesh.rotation.x = -Math.PI / 4;
        this.mesh.position.copy(this.position);

        scene.add(this.mesh);
    }

    updateParticle(particle, dt) {
        const distance = particle.position.y - this.position.y;

        // Плоскость притягивает частицы только сверху
        if (distance <= 0 || distance >= this.range) {
            return;
        }

        // Сила возрастает при приближении к плоскости
        const factor = 1 - distance / this.range;
        const acceleration = this.strength * factor;

        // Постепенно изменяем вертикальную скорость
        particle.velocity.y -= acceleration * dt;

        // Удерживаем горизонтальную скорость,
        // чтобы частицы двигались по плавным траекториям
        particle.velocity.x *= 1;
        particle.velocity.z *= 1;
    }

    
    resolveCollision(particle) {
        const particleRadius = 0.08;
        const halfWidth = 6;
        const halfDepth = 6;

        const planeY = this.position.y + particleRadius;

        // Проверяем, находится ли частица над плоскостью
        const insidePlane =
            Math.abs(particle.position.x - this.position.x) <= halfWidth &&
            Math.abs(particle.position.z - this.position.z) <= halfDepth;

        if (insidePlane && particle.position.y < planeY) {
            particle.position.y = planeY;

            if (particle.velocity.y < 0) {
                particle.velocity.y = 0;
            }
        }
    }


    dispose() {
        scene.remove(this.mesh);
        this.geometry.dispose();
        this.material.dispose();
    }
}
