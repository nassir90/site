<div id="content-section">
    <p>I'm Chinaza. I'm a computer science graduate from Trinity College Dublin. I'm interested in robotics, software development (especially in the face of AI), computer graphics and the linux desktop.</p>

    <p>In college I spent most of my time serving as the technical lead of <a href="https://formulatrinity.ie" rel="external">Formula Trinity Autonomous (FTA)</a>. Summer breaks were spent doing internships at Evervault and SIG.</p>

    <p>Now that I've <s>been laid off from FTA</s> graduated, I've been spending time working on this website and on other to be released side projects. Stay tuned!</p>

    <center><small><i>I'm visiting SF in November. Would love to meet engineers and founders. Please contact me if interested!</i></small></center>

    <h2>Previous Projects</h2>
    <p>Some of the code I wrote while on FTA can be found in the <a href="https://github.com/FT-Autonomous/">Formula Trinity GitHub Organisation</a>. Other work I did as the technical lead includes:</p>

        <ul>
            <li>Trained computer vision models (CGNET, YOLOv5 -> YOLOv8) using NVIDIA compute.</li>
            <li><a href="https://github.com/FT-Autonomous/fta_perception_ros/tree/main/src/ft_cluster_cpp">Wrote a GPU-accelerated clustering algorithm</a> in C++ with OpenGL Compute Shaders.</li>
            <li>Integrated an NVIDIA Jetson AGX into a mobile testing rig, designing the power system for E2E autonomous driving. <a href="https://github.com/FT-Autonomous/ft_rig">Used the AGX's GPIO ports for motor control.</a></li>
            <li>Optimized YOLO models on NVIDIA Jetson Nanos using the TensorRT framework.</li>
            <li>Collaborated on a sensor fusion pipeline, merging YOLO with LiDAR, contributing to a 1st place design presentation win.</li>
            <li>Collected on-track datasets as ROS2 bags.</li>
        </ul>
    
    <!-- First block of images -->
    <div class="first-image-block">
        <img class="banner" src="/images/memories1.png" alt="Team Memories 2023/2024">
        <img class="banner" src="/images/memories2.png" alt="Team Memories 2024/2025">
        <img src="/images/RIGB.png" alt="AI Testing Rig B">
        <img src="/images/calib.png" alt="Sensor Fusion Calibration Visual">
    </div>

    <p><a href="https://github.com/FT-Autonomous/ft_grandprix">AI Grand Prix</a> is an open-source <a href="https://github.com/google-deepmind/mujoco/">MuJoCo</a> based simulator for autonomous racing. It's inspired by the F1Tenth competition. I collaborated with Formula Trinity's business operations team to host a successful hackathon where people could run the simulator and try to make their own self driving racecars.</p>

    <!-- Technical images arranged in a grid -->
    <div class="technical-gallery lower">
        <img src="/images/aigp1.png" alt="AI GP Simulator Screenshot 1">
        <img src="/images/aigp2.png" alt="AI GP Simulator Screenshot 2">
        <img src="/images/aigp3.png" alt="AI GP Simulator Screenshot 3">
        <img src="/images/aigp4.png" alt="AI GP Simulator Screenshot 4">
    </div>
</div>

<style>
    #content-section {
        padding: 40px 10%;
        color: #eee;
        /* background-color: #1a1a1a; */
        font-family: "Times New Roman", serif;
        font-size: 28px;
        line-height: 1.8;
        margin-bottom: 40px;
    }

    s {
        color: gray;
    }

    a {
        color: #aaa; /* muted gray */
        transition: color 0.2s ease, text-shadow 0.2s ease;
    }

    a:hover,
    a:focus {
        color: #ddd; /* lighter on hover */
        text-shadow: 0 0 4px rgba(255, 255, 255, 0.3);
    }

    a:visited {
        color: #999; /* slightly darker for visited links */
    }

    a:active {
        color: #ccc;
        text-shadow: 0 0 6px rgba(255, 255, 255, 0.4);
    }

    @media (max-width: 768px) {
        #content-section {
            padding: 20px 40px;
            font-size: 18px;
        }
    }

    /* Layout Styling */

    img {
        display: block;
        width: 100%;
    }

    .first-image-block {
        display: grid;
        grid-template-columns: 1fr 1fr repeat(2, 0.75fr); /* 3 columns for desktop */
        gap: 20px;
        margin-top: 30px;
        margin-bottom: 40px;
    }

    .first-image-block img {
        height: 100%;
        object-fit: cover;
    }

    .lower {
        display: grid;
        grid-template-columns: repeat(4, 1fr); 
        gap: 20px;
    }

    .lower img {
        height: 100%;
        object-fit: cover;
    }

    @media (max-width: 768px) {
        #content-section {
            padding: 20px 40px;
            font-size: 18px;
        }

        .first-image-block {
            grid-template-columns: repeat(2, 1fr); /* Single column for mobile */
        }

        .technical-gallery, .lower {
            grid-template-columns: repeat(2, 1fr); /* Single column for mobile */
        }
    }
</style>
