
```js
mesh.color.set(newColor);
mesh.position.set(newPosition);

const meshIds = [];
const meshes = []

function newMesh(){
    const myMesh;
    const meshId;

    meshes.push(myMesh);
    meshIdx = meshes.indexOf(myMesh);
    meshIds.push({
        meshid: meshIdx
    });
}

const meshColorInp = getElementById(meshColorInp);
meshColorInp.addEventListener('change', function(){
    const meshId = meshColorInp.dataset.meshId;
    const meshIdx = meshIds[`${meshId}`];
    const mesh = meshes[meshIdx];
    mesh.color.set(this.value);
})
```