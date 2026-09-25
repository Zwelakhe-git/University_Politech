import { scene, THREE } from "./init.js";
import { sphere } from "./task1.js";

const torusGeometry = new THREE.TorusGeometry(1.0, 0.35, 10, 32);

const torusMaterial = new THREE.MeshBasicMaterial({
color: 0xff44aa,
wireframe: true
});
const torus = new THREE.Mesh(torusGeometry, torusMaterial);
torus.position.set(-4, 0, 0);   


const tetraGeometry = new THREE.TetrahedronGeometry(1.2, 0);

const tetraMaterial = new THREE.MeshBasicMaterial({
color: 0x44ff88, 
wireframe: true
});

const tetra = new THREE.Mesh(tetraGeometry, tetraMaterial);
tetra.position.set(4, 0, 0);

export function task3(){
    scene.remove(sphere);
    scene.children.forEach(mesh => {
        if(mesh.type === "Mesh"){
            scene.remove(mesh);
        }
    })
    scene.add(torus);

    scene.add(tetra);
}
export { tetra, torus }