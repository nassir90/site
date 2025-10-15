
<div id="text-overlay">
    <h1>Chi<span style="text-shadow: 6px 6px 1px #aa0000;">naza</span> Uzoukwu</h1>
    <p class="subtext">Welcome to my corner of the web</p>
    <p class="socials">
        <a href="https://twitter.com/zoukwuberg" target="_blank"><i class="fab fa-x-twitter"></i></a>
        <a href="https://github.com/nassir90" target="_blank"><i class="fab fa-github"></i></a>
        <a href="https://www.linkedin.com/in/chinaza-uzoukwu-a33219228" target="_blank"><i class="fab fa-linkedin"></i></a>
        <a href="https://www.youtube.com/@ChinazaUzoukwu/"><i class="fa-brands fa-youtube"></i></a>
    </p>
</div>

<style>
    #text-overlay {
        display: flex;
        flex-direction: column;
        gap: 30px;
        position: absolute;
        top: 50%;
        left: 0;
        width: 50%;
        transform: translateY(-50%);
        color: white;
        z-index: 100;
        line-height: 1.6;
        text-align: center;
        padding: 0 40px;
        box-sizing: border-box;
        font-family: "Cormorant Garamond", "Times New Roman", serif;
        line-height: 0.9;
    }

    #text-overlay h1 {
        margin: 0 0 0 0;
        font-size: 70px;
        font-weight: normal;
    }

    #text-overlay .subtext {
        margin: 0;
        font-size: 35px;
    }

    .socials a {
        color: #ccc;
        margin: 0 8px;
        font-size: 1.5em;
        transition: color 0.2s;
    }

    .socials a:hover {
        color: #fff;
    }

@media (max-width: 768px) {
    #text-overlay {
        position: relative;
        width: 100%;
        top: 0;
        left: 0;
        transform: none;
        padding: 40px;
        text-align: center;
        order: -1;
        height: 50vh;
        /* Vertical Centering */
        display: flex;
        flex-direction: column;
        justify-content: center;
    }
}
</style>
