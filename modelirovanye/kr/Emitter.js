
import { THREE } from "./init_scene.js";

export class Emitter {
    constructor(mesh) {
        this.mesh = mesh;

        const params = mesh.geometry.parameters;

        this.radiusTop = params.radiusTop;
        this.radiusBottom = params.radiusBottom;
        this.height = params.height;
    }

    emit() {
        const rt = this.radiusTop;
        const rb = this.radiusBottom;
        const h = this.height;

        // Площади боковой поверхности и торцов
        const slantHeight = Math.sqrt(
            h * h + (rb - rt) ** 2
        );

        const sideArea = Math.PI * (rt + rb) * slantHeight;
        const topArea = Math.PI * rt * rt;
        const bottomArea = Math.PI * rb * rb;

        const totalArea = sideArea + topArea + bottomArea;
        const choice = Math.random() * totalArea;

        let position;
        let direction;

        if (choice < sideArea) {
            // Боковая поверхность
            const angle = Math.random() * Math.PI * 2;
            const y = (Math.random() - 0.5) * h;

            // Радиус зависит от высоты
            const t = (y + h / 2) / h;
            const radius = rb + (rt - rb) * t;

            position = new THREE.Vector3(
                radius * Math.cos(angle),
                y,
                radius * Math.sin(angle)
            );

            // Нормаль боковой поверхности
            direction = new THREE.Vector3(
                Math.cos(angle),
                (rb - rt) / h,
                Math.sin(angle)
            ).normalize();

        } else if (choice < sideArea + topArea) {
            // Верхний торец
            const angle = Math.random() * Math.PI * 2;
            const radius = rt * Math.sqrt(Math.random());

            position = new THREE.Vector3(
                radius * Math.cos(angle),
                h / 2,
                radius * Math.sin(angle)
            );

            direction = new THREE.Vector3(0, 1, 0);

        } else {
            // Нижний торец
            const angle = Math.random() * Math.PI * 2;
            const radius = rb * Math.sqrt(Math.random());

            position = new THREE.Vector3(
                radius * Math.cos(angle),
                -h / 2,
                radius * Math.sin(angle)
            );

            direction = new THREE.Vector3(0, -1, 0);
        }

        // Учитываем актуальные трансформации меша и его родителей
        this.mesh.updateWorldMatrix(true, false);

        position.applyMatrix4(this.mesh.matrixWorld);

        // Преобразуем нормаль с учётом вращения и масштаба
        const normalMatrix = new THREE.Matrix3()
            .getNormalMatrix(this.mesh.matrixWorld);

        direction.applyMatrix3(normalMatrix).normalize();

        return { position, direction };
    }
}
