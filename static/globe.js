import Globe from globe.gl;

// globe.js
document.addEventListener("DOMContentLoaded", function() {
    const container = document.getElementById('globe-container');
    const width = container.clientWidth;
    const height = container.clientHeight;

    // Create a scene
    const scene = new THREE.Scene();

    // Create a camera
    const camera = new THREE.PerspectiveCamera(75, width / height, 0.1, 1000);
    camera.position.z = 5;

    // Create a renderer
    const renderer = new THREE.WebGLRenderer();
    renderer.setSize(width, height);
    container.appendChild(renderer.domElement);

    // Create a sphere (globe)
    const geometry = new THREE.SphereGeometry(2, 32, 32);
    const material = new THREE.MeshBasicMaterial({
        color: 0x0000ff,
        wireframe: true
    });
    const globe = new THREE.Mesh(geometry, material);
    scene.add(globe);

    // Animation loop
    function animate() {
        requestAnimationFrame(animate);
        globe.rotation.x += 0.01;
        globe.rotation.y += 0.01;
        renderer.render(scene, camera);
    }

    animate();
});