int gridSize = 20;
PVector[][] grid = new PVector[gridSize][gridSize];

void setup() {
  size(1000, 800, P3D);
  calculateSurface();
}

void draw() {
  background(255);
    // Зміщення початку координат до центру екрану
  translate(width / 2.5, height / 2.5, 0);
  // Зменшення масштабу для кращої видимості
  scale(2);
  // Товщина ліній для проекцій
  //strokeWeight(5);
  rotateX(PI/5);
  rotateY(PI/3);

    // Візуалізація поверхні з меншою товщиною сітки
  strokeWeight(0.5);  // Тонша сітка
  stroke(0);
  noFill();
  
  // Візуалізація поверхні
  for (int i = 0; i < gridSize - 1; i++) {
    for (int j = 0; j < gridSize - 1; j++) {
      beginShape();
      vertex(grid[i][j].x, grid[i][j].y, grid[i][j].z);
      vertex(grid[i+1][j].x, grid[i+1][j].y, grid[i+1][j].z);
      vertex(grid[i+1][j+1].x, grid[i+1][j+1].y, grid[i+1][j+1].z);
      vertex(grid[i][j+1].x, grid[i][j+1].y, grid[i][j+1].z);
      endShape(CLOSE);
    }
  }
// Відображення проекцій на площини x=0, y=0, z=0 з більшою товщиною точок
  strokeWeight(2);  // Товстіші точки
  drawProjections();
}

void calculateSurface() {
  // Приклад визначення крайових кривих
  PVector Q00 = new PVector(0, 0, 0);
  PVector Q10 = new PVector(200, 0, 0);
  PVector Q01 = new PVector(0, 200, 0);
  PVector Q11 = new PVector(200, 200, 200);

  for (int i = 0; i < gridSize; i++) {
    float u = float(i) / (gridSize - 1);
    for (int j = 0; j < gridSize; j++) {
      float v = float(j) / (gridSize - 1);
      grid[i][j] = kunsSurface(u, v, Q00, Q10, Q01, Q11);
    }
  }
}

PVector kunsSurface(float u, float v, PVector Q00, PVector Q10, PVector Q01, PVector Q11) {
  float x = (1 - u) * Q00.x + u * Q10.x + (1 - v) * Q01.x + v * Q11.x 
            - (1 - u) * (1 - v) * Q00.x - u * (1 - v) * Q10.x - (1 - u) * v * Q01.x - u * v * Q11.x;
  
  float y = (1 - u) * Q00.y + u * Q10.y + (1 - v) * Q01.y + v * Q11.y 
            - (1 - u) * (1 - v) * Q00.y - u * (1 - v) * Q10.y - (1 - u) * v * Q01.y - u * v * Q11.y;
  
  float z = (1 - u) * Q00.z + u * Q10.z + (1 - v) * Q01.z + v * Q11.z 
            - (1 - u) * (1 - v) * Q00.z - u * (1 - v) * Q10.z - (1 - u) * v * Q01.z - u * v * Q11.z;
  
  return new PVector(x, y, z);
}

void drawProjections() {
  // Проекція на x=0 (зелений колір)
  stroke(0, 255, 0); // Зелений
  for (int i = 0; i < gridSize; i++) {
    for (int j = 0; j < gridSize; j++) {
      point(0, grid[i][j].y, grid[i][j].z);
    }
  }

  // Проекція на y=0 (синій колір)
  stroke(0, 0, 255); // Синій
  for (int i = 0; i < gridSize; i++) {
    for (int j = 0; j < gridSize; j++) {
      point(grid[i][j].x, 0, grid[i][j].z);
    }
  }

  // Проекція на z=0 (червоний колір)
  stroke(255, 0, 0); // Червоний
  for (int i = 0; i < gridSize; i++) {
    for (int j = 0; j < gridSize; j++) {
      point(grid[i][j].x, grid[i][j].y, 0);
    }
  }
}
