import { scene, THREE } from "./init.js";


const cubeGeometry = new THREE.BoxGeometry(2, 2, 2);

const cubeMaterial = new THREE.MeshBasicMaterial({
color: 0x00ffff,   // голубой
wireframe: true
});

const cube = new THREE.Mesh(cubeGeometry, cubeMaterial);
cube.position.set(0, 0, 0); 


const sphereGeometry = new THREE.SphereGeometry(0.8, 24, 16);

const sphereMaterial = new THREE.MeshBasicMaterial({
color: 0xffaa00,  
wireframe: true
});

const sphere = new THREE.Mesh(sphereGeometry);
sphere.material = sphereMaterial;
sphere.position.set(0, 0, 0);  // тоже в центре — значит внутри куба

export function task1(){
    scene.children.forEach(mesh => {
        
        if(mesh.type === "Mesh"){
            scene.remove(mesh);
        }
    })
    scene.add(cube);
    scene.add(sphere);
}

export { sphere, cube }
