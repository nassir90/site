<div bind:this={container} class="visualization-wrapper">
    <canvas bind:this={canvas}></canvas>
    {#if DEBUG_MODE}
        <button id="export-btn">Export Camera</button>
    {/if}
</div>

<style>
    .visualization-wrapper {
        height: 100%;
        width: 100%;
    }

    canvas {
        z-index: -100;
        display: block;
    }
    #export-btn {
        position: absolute;
        top: 20px;
        right: 20px;
        padding: 10px 20px;
        background: white;
        color: black;
        border: none;
        border-radius: 5px;
        cursor: pointer;
        font-size: 14px;
        z-index: 100;
    }
    #export-btn:hover {
        background: gray;
    }

    @media (max-width: 768px) {
        .visualization-wrapper {
            height: 50vh;
        }
    }
</style>

<script lang="ts">
    import * as THREE from 'three';
    import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls.js';
    import { onMount } from 'svelte';

    // Debug mode - set to true to show export button
    let DEBUG_MODE = false;

    // Dropout parameter - percentage of points to render (0.0 to 1.0)
    const DROPOUT_RATE = 1.0; // 10% of points will be rendered

    const mobileCameraConfig = {
  "position": {
    "x": 0.35057161919599206,
    "y": -0.4135555774766815,
    "z": 1.918463979987243
  },
  "target": {
    "x": 0.4005608605773236,
    "y": 0.8608559852312732,
    "z": 0.7328656556766946
  },
  "fov": 75
};

    // Camera configuration - modify these values to set initial view
    const cameraConfig = {
        "position": {
            "x": -0.16460022675053126,
            "y": -0.6228621995655184,
            "z": 2.2373369015612683
        },
        "target": {
            "x": -0.24632319124295435,
            "y": 0.8274498897248066,
            "z": 0.6926157919499376
        },
        "fov": 75
    };

    let container: HTMLDivElement;
    let canvas: HTMLCanvasElement;
    let controls: OrbitControls;

    onMount(async () => {
        const isMobile = window.matchMedia('(max-width: 768px)').matches;
        const activeCameraConfig = isMobile ? mobileCameraConfig : cameraConfig;

        const scene = new THREE.Scene();
        scene.background = new THREE.Color(0x111111);

        const camera = new THREE.PerspectiveCamera(activeCameraConfig.fov, container.clientWidth / container.clientHeight, 0.1, 1000);
        camera.position.set(activeCameraConfig.position.x, activeCameraConfig.position.y, activeCameraConfig.position.z);

        const renderer = new THREE.WebGLRenderer({ canvas: canvas, antialias: true });
        renderer.setSize(container.clientWidth, container.clientHeight);

        controls = new OrbitControls(camera, renderer.domElement);
        controls.target.set(activeCameraConfig.target.x, activeCameraConfig.target.y, activeCameraConfig.target.z);
        controls.update();

        async function loadPointsBin(url: string) {
            const res = await fetch(url);
            const buffer = await res.arrayBuffer();
            const floats = new Float32Array(buffer);

            const points = [];
            for (let i = 0; i < floats.length; i += 3) {
                points.push({ x: floats[i], y: floats[i + 1], z: floats[i + 2] });
            }

            return points;
        }

        async function loadPointCloud() {
            const data = await loadPointsBin('/pointcloud_capture.bin');
            return data;
        }

        function createPointCloud(points: { x: number, y: number, z: number }[]) {
            const geometry = new THREE.BufferGeometry();
            
            const filteredPoints = points.filter(p => {
                const distance = Math.sqrt(p.x * p.x + p.y * p.y + p.z * p.z);
                if (distance > 2.0) return false;
                
                return Math.random() < DROPOUT_RATE;
            });
            
            const positions = new Float32Array(filteredPoints.length * 3);
            const originalPositions = new Float32Array(filteredPoints.length * 3);
            
            for (let i = 0; i < filteredPoints.length; i++) {
                positions[3*i] = filteredPoints[i].x;
                positions[3*i + 1] = filteredPoints[i].y;
                positions[3*i + 2] = filteredPoints[i].z;
                
                originalPositions[3*i] = filteredPoints[i].x;
                originalPositions[3*i + 1] = filteredPoints[i].y;
                originalPositions[3*i + 2] = filteredPoints[i].z;
            }
            
            geometry.setAttribute('position', new THREE.BufferAttribute(positions, 3));
            geometry.userData.originalPositions = originalPositions;

            const material = new THREE.PointsMaterial({ color: 0xFFFFFF, size: 0.0015, transparent: true, opacity: 1.0 });
            return new THREE.Points(geometry, material);
        }

        const points = await loadPointCloud();
        const pointCloud = createPointCloud(points);
        scene.add(pointCloud);
        
        const raycaster = new THREE.Raycaster();
        raycaster.params.Points.threshold = 0.10;
        const mouse = new THREE.Vector2();
        let mouseWorldPos = new THREE.Vector3();
        let isMouseOverPointCloud = false;
        let touchWorldPos = new THREE.Vector3();
        let windIntensity = 0;
        let lastMouseMoveTime = 0;
        let lastTouchMoveTime = 0;
        const windFadeInDuration = 1000;
        const windFadeOutDelay = 2000;
        const windFadeOutDuration = 1500;
        
        let lastRaycastTime = 0;
        const raycastThrottle = 16;
        
        function onMouseMove(event: MouseEvent) {
            const now = Date.now();
            lastMouseMoveTime = now;
            
            const rect = container.getBoundingClientRect();
            mouse.x = ((event.clientX - rect.left) / rect.width) * 2 - 1;
            mouse.y = -((event.clientY - rect.top) / rect.height) * 2 + 1;
            
                        raycaster.setFromCamera(mouse, camera);
            
                        
            
                        const intersects = raycaster.intersectObject(pointCloud);
            
                                    if (intersects.length > 0) {
            
                                        mouseWorldPos.copy(intersects[0].point);
            
                                        isMouseOverPointCloud = true;
            
                                    } else {
            
                                        // If no intersection, project mouse position onto a plane at the depth of the controls target
            
                                        const targetDistance = camera.position.distanceTo(controls.target);
            
                                        raycaster.ray.at(targetDistance, mouseWorldPos);
            
                                        isMouseOverPointCloud = false;
            
                                    }
        }
        
        let isTouched = false;

        function onTouchStart(event: TouchEvent) {
            isTouched = true;
            lastTouchMoveTime = Date.now();
            event.preventDefault(); // Prevent scrolling
        }

        function onTouchMove(event: TouchEvent) {
            if (!isTouched) return;
            const now = Date.now();
            lastTouchMoveTime = now;

            const touch = event.touches[0];
            const rect = container.getBoundingClientRect();
            mouse.x = ((touch.clientX - rect.left) / rect.width) * 2 - 1;
            mouse.y = -((touch.clientY - rect.top) / rect.height) * 2 + 1;

            if (now - lastRaycastTime > raycastThrottle) {
                lastRaycastTime = now;
                
                raycaster.setFromCamera(mouse, camera);
                
                const intersects = raycaster.intersectObject(pointCloud);
                if (intersects.length > 0) {
                    touchWorldPos.copy(intersects[0].point);
                }
            }
        }

        function onTouchEnd() {
            isTouched = false;
        }

        let isDragging = false;

        const onMouseDown = () => {
            isDragging = true;
        };

        const onMouseUp = () => {
            isDragging = false;
        };

        container.addEventListener('mousedown', onMouseDown);
        container.addEventListener('mouseup', onMouseUp);
        container.addEventListener('mousemove', onMouseMove, { passive: true });

        container.addEventListener('touchstart', onTouchStart, { passive: false });
        container.addEventListener('touchmove', onTouchMove, { passive: false });
        container.addEventListener('touchend', onTouchEnd, { passive: true });
        
        let time = 0;
        let windStartTime = 0;
        let isFadingIn = false;
        
        const FLUTTER_TABLE_SIZE = 1024;
        const flutterTable1 = new Float32Array(FLUTTER_TABLE_SIZE);
        const flutterTable2 = new Float32Array(FLUTTER_TABLE_SIZE);
        const flutterTable3 = new Float32Array(FLUTTER_TABLE_SIZE);
        for (let i = 0; i < FLUTTER_TABLE_SIZE; i++) {
            const angle = (i / FLUTTER_TABLE_SIZE) * Math.PI * 2;
            flutterTable1[i] = Math.sin(angle) * 0.003;
            flutterTable2[i] = Math.sin(angle) * 0.002;
            flutterTable3[i] = Math.sin(angle) * 0.0025;
        }
        
        function applyDistortion() {
            const now = Date.now();
            let currentWindIntensity = 0;
            let activeWorldPos = new THREE.Vector3();
            let isActiveInteraction = false;
            let activeLastMoveTime = 0;

            if (isMobile) {
                activeWorldPos = touchWorldPos;
                isActiveInteraction = isTouched;
                activeLastMoveTime = lastTouchMoveTime;
            } else { // Desktop
                activeWorldPos = mouseWorldPos;
                isActiveInteraction = isMouseOverPointCloud;
                activeLastMoveTime = lastMouseMoveTime;
            }
            
            if (isActiveInteraction) {
                currentWindIntensity = 1; // Max intensity during active interaction
                windStartTime = now;
                isFadingIn = true;
            } else {
                const timeSinceLastActivity = now - activeLastMoveTime;
                if (timeSinceLastActivity < windFadeOutDelay) {
                    if (!isFadingIn) {
                        windStartTime = now;
                        isFadingIn = true;
                    }
                    const fadeInProgress = Math.min((now - windStartTime) / windFadeInDuration, 1);
                    currentWindIntensity = fadeInProgress * fadeInProgress * (3 - 2 * fadeInProgress);
                } else {
                    isFadingIn = false;
                    const fadeOutProgress = Math.min((timeSinceLastActivity - windFadeOutDelay) / windFadeOutDuration, 1);
                    const fadeOutEased = fadeOutProgress * fadeOutProgress * (3 - 2 * fadeOutProgress);
                    currentWindIntensity = 1 - fadeOutEased;
                }
            }
            
            if (currentWindIntensity <= 0.001) {
                windIntensity = 0;
                return;
            }

            windIntensity = currentWindIntensity;
            
            time += 0.016;
            const positions = pointCloud.geometry.attributes.position.array as Float32Array;
            const originalPositions = pointCloud.geometry.userData.originalPositions;
            const distortionRadius = 0.35;
            const distortionRadiusSq = distortionRadius * distortionRadius;
            const distortionStrength = 0.05;
            const invDistortionRadius = 1 / distortionRadius;
            
            const tableIndex1 = ((time * 2.5) % (Math.PI * 2)) / (Math.PI * 2) * FLUTTER_TABLE_SIZE;
            const tableIndex2 = ((time * 3.2) % (Math.PI * 2)) / (Math.PI * 2) * FLUTTER_TABLE_SIZE;
            const tableIndex3 = ((time * 1.8) % (Math.PI * 2)) / (Math.PI * 2) * FLUTTER_TABLE_SIZE;
            
            const mouseX = activeWorldPos.x;
            const mouseY = activeWorldPos.y;
            const mouseZ = activeWorldPos.z;
            
            const numPoints = positions.length / 3;
            
            for (let i = 0; i < positions.length; i += 3) {
                const originalX = originalPositions[i];
                const originalY = originalPositions[i + 1];
                const originalZ = originalPositions[i + 2];
                
                const dx = originalX - mouseX;
                const dy = originalY - mouseY;
                const dz = originalZ - mouseZ;
                const distanceSq = dx * dx + dy * dy + dz * dz;
                
                const pointIndex = (i / 3) / numPoints;
                const idx1 = ((tableIndex1 + pointIndex * 102.4) | 0) % FLUTTER_TABLE_SIZE;
                const idx2 = ((tableIndex2 + pointIndex * 153.6) | 0) % FLUTTER_TABLE_SIZE;
                const idx3 = ((tableIndex3 + pointIndex * 81.92) | 0) % FLUTTER_TABLE_SIZE;
                
                const flutterAmount = (flutterTable1[idx1] + flutterTable2[idx2] + flutterTable3[idx3]) * windIntensity;
                
                if (distanceSq < distortionRadiusSq) {
                    const distance = Math.sqrt(distanceSq);
                    const influence = 1 - distance * invDistortionRadius;
                    const easedInfluence = influence * influence * influence;
                    
                    const pushAmount = distortionStrength * easedInfluence;
                    const invDistance = 1 / (distance + 0.0001);
                    const dirX = dx * invDistance;
                    const dirY = dy * invDistance;
                    const dirZ = dz * invDistance;
                    
                    positions[i] = originalX + dirX * pushAmount + flutterAmount;
                    positions[i + 1] = originalY + dirY * pushAmount + flutterAmount * 0.8;
                    positions[i + 2] = originalZ + dirZ * pushAmount + flutterAmount * 1.2;
                } else {
                    positions[i] = originalX + flutterAmount;
                    positions[i + 1] = originalY + flutterAmount * 0.8;
                    positions[i + 2] = originalZ + flutterAmount * 1.2;
                }
            }
            
            pointCloud.geometry.attributes.position.needsUpdate = true;
        }

        const exportBtn = document.getElementById('export-btn');
        if (exportBtn) {
            exportBtn.addEventListener('click', () => {
                const config = {
                    position: {
                        x: camera.position.x,
                        y: camera.position.y,
                        z: camera.position.z
                    },
                    target: {
                        x: controls.target.x,
                        y: controls.target.y,
                        z: controls.target.z
                    },
                    fov: camera.fov
                };
                
                const json = JSON.stringify(config, null, 2);
                console.log('Camera Configuration:');
                console.log(json);
                
                navigator.clipboard.writeText(json).then(() => {
                    alert('Camera parameters copied to clipboard!');
                }).catch(err => {
                    alert('Camera parameters logged to console');
                });
            });
        }

        const animationInterval = 75;
        
        function animate() {
            const isMobile = window.matchMedia('(max-width: 768px)').matches;
            const activeCameraConfig = isMobile ? mobileCameraConfig : cameraConfig;
            controls.target.set(activeCameraConfig.target.x, activeCameraConfig.target.y, activeCameraConfig.target.z);
            camera.position.set(activeCameraConfig.position.x, activeCameraConfig.position.y, activeCameraConfig.position.z);

            if (container.clientWidth !== camera.aspect * container.clientHeight) {
                camera.aspect = container.clientWidth / container.clientHeight;
                camera.updateProjectionMatrix();
                renderer.setSize(container.clientWidth, container.clientHeight);
            }

            controls.update();
            applyDistortion();
            renderer.render(scene, camera);
        }

        const intervalId = setInterval(animate, animationInterval);

        return () => {
            window.removeEventListener('mousemove', onMouseMove);
            clearInterval(intervalId);
        }
    });

    $: if (controls) {
        controls.enabled = DEBUG_MODE;
    }
</script>
