
import { THREE, scene } from "./init_scene.js";

export class Particle {
    constructor(position, direction) {
        this.position = position.clone();
        this.velocity = direction.clone().multiplyScalar(5);

        this.age = 0;
        this.lifetime = 5 + Math.random() * 3;

        this.geometry = new THREE.SphereGeometry(0.08, 8, 8);
        this.material = new THREE.MeshBasicMaterial({
            color: 0x0088ff
        });

        this.mesh = new THREE.Mesh(this.geometry, this.material);
        this.mesh.position.copy(this.position);
        scene.add(this.mesh);

        // Храним три последних положения частицы
        this.trailLength = 3;
        this.trailPositions = [];

        this.trailGeometry = new THREE.BufferGeometry();
        this.trailMaterial = new THREE.LineBasicMaterial({
            color: 0x0088ff
        });

        this.trail = new THREE.Line(
            this.trailGeometry,
            this.trailMaterial
        );

        scene.add(this.trail);
    }

    update(dt) {
        this.age += dt;

        this.position.addScaledVector(this.velocity, dt);
        this.mesh.position.copy(this.position);

        const t = Math.min(this.age / this.lifetime, 1);

        this.material.color.setRGB(t, 0, 1 - t);
        this.trailMaterial.color.copy(this.material.color);

        // Запоминаем новое положение
        this.trailPositions.push(this.position.clone());

        // Удаляем старые положения
        if (this.trailPositions.length > this.trailLength) {
            this.trailPositions.shift();
        }

        // Обновляем геометрию линии
        this.trailGeometry.setFromPoints(this.trailPositions);
    }

    isDead() {
        return this.age >= this.lifetime;
    }

    dispose() {
        scene.remove(this.mesh);
        scene.remove(this.trail);

        this.geometry.dispose();
        this.material.dispose();

        this.trailGeometry.dispose();
        this.trailMaterial.dispose();
    }
}
