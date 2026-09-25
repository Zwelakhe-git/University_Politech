import { scene, controls, camera, renderer } from "./init.js"
import { sphere, cube, task1 } from "./task1.js";
import { task2 } from "./task2.js";
import { task3 } from "./task3.js";
import { task4 } from "./task4.js";
// --- Цикл рендеринга ---
function animate() {
  requestAnimationFrame(animate);
  controls.update();
  renderer.render(scene, camera);
}

const meshes = [
    sphere, cube
];

// --- Обработка изменения окна ---
window.addEventListener('resize', () => {
  camera.aspect = window.innerWidth / window.innerHeight;
  camera.updateProjectionMatrix();
  renderer.setSize(window.innerWidth, window.innerHeight);
});

document.addEventListener('DOMContentLoaded', function(){
    animate();
    task1();
    // alert(JSON.stringify(scene.children.map(mesh => ({
    //     type: mesh.type,
    //     id: mesh.id,
    // }))));
    const segmentsRegulator = document.getElementById('segments-inp');
    segmentsRegulator?.setAttribute('data-mesh-id', scene.children.find(mesh => mesh.type === "Mesh").id ?? -1);
    segmentsRegulator?.addEventListener('change', function(){
        const meshId = this.dataset.meshId;
        const mesh = Array.from(scene.children).find(mesh => mesh.id == meshId);
        if(mesh){
            let type = mesh.type;
        } else {
            console.log("mesh " + meshId + " not found");
        }
    });
    const task1Btn = document.getElementById('task1-link');
    const task2Btn = document.getElementById('task2-link');
    const task3Btn = document.getElementById('task3-link');
    const task4Btn = document.getElementById('task4-link');
    let runBtn = document.getElementById('run-btn');
    
    document.querySelectorAll('.nav-item')?.forEach(lk => lk.addEventListener('click', function(){
        document.querySelectorAll('.nav-item')?.forEach(olk => olk.classList.remove('active'));
        lk.classList.add('active');
    }))
    task1Btn?.addEventListener('click', () => {
        task1();
    });
    task2Btn?.addEventListener('click', () => {
        task2();
    });
    task3Btn?.addEventListener('click', () => {
        task3();
    });
    task4Btn?.addEventListener('click', () => {
        task4();
    });
})
