
### we define the source of the light. The actual light
```js
const pointLight = new THREE.PointLight(color, intensity, distance, decay);
pointLight.castShadow = true;
pointLight.shadow.mapSize.set(1024, 1024);
scene.add(pointLight);
```

### now we cover the light source for it to be visible. sort of like designing the lamp around the source. Its a mesh obviously
```js
const lightMaker = new THREE.Mesh(
    new THREE.SphereGeometry(radius, widthSegments, heightSegments),
    new THREE.MeshBasicMaterial({ color: 0xffffff })
);
pointLight.add(lightMaker);
```