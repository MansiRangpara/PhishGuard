const canvas = document.getElementById('hyperspeed-bg');
const ctx = canvas.getContext('2d');

let stars = [];
let speed = 2;

function resizeCanvas() {
  canvas.width = window.innerWidth;
  canvas.height = window.innerHeight;
}
window.addEventListener('resize', resizeCanvas);
resizeCanvas();

function initStars(count = 200) {
  stars = [];
  for (let i = 0; i < count; i++) {
    stars.push({ x: Math.random() * canvas.width, y: Math.random() * canvas.height, z: Math.random() * canvas.width });
  }
}
initStars();

function animate() {
  ctx.fillStyle = 'black';
  ctx.fillRect(0, 0, canvas.width, canvas.height);

  ctx.fillStyle = 'white';
  stars.forEach(star => {
    star.z -= speed;
    if (star.z <= 0) star.z = canvas.width;

    let sx = (star.x - canvas.width / 2) * (canvas.width / star.z) + canvas.width / 2;
    let sy = (star.y - canvas.height / 2) * (canvas.width / star.z) + canvas.height / 2;

    ctx.fillRect(sx, sy, 2, 2);
  });

  requestAnimationFrame(animate);
}
animate();
