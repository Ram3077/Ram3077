let circleDiameter = 40;
let circleX = 130;
let circleY = 80;
let changeX = 4;
let changeY = 3;
let circleColor = 'white';

function setup() {
  createCanvas(1000, 200);
}

function draw() {
  clear()
  background('blue');
  fill(circleColor)
  ellipse(circleX, circleY, circleDiameter, circleDiameter);

  const radius = circleDiameter / 2

  if (circleX + radius > width || 
      circleX - radius < 0) {
    changeX *= -1;
  }
  if (circleY + radius > height ||
      circleY - radius < 0) {
    changeY *= -1;
  }

  circleX+=changeX;
  circleY+=changeY;
}

function mouseMoved() {
  circleColor = getRandomColor();
}

function getRandomNumber(start, end) {
  return Math.floor(Math.random() * (end - start + 1)) + start;
}

function getRandomColor() {
  const r = getRandomNumber(0, 255);
  const g = getRandomNumber(0, 255);
  const b = getRandomNumber(0, 255);
  return `rgb(${r},${g},${b})`;
}