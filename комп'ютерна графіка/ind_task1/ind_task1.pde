float c = 400; // Відстань між точками
PVector A, B; 
int caseNum = 1; // Початковий випадок

void setup() {
  size(1000, 700);
  A = new PVector(width / 2 - c / 2, height / 2);
  B = new PVector(width / 2 + c / 2, height / 2);
  
  textSize(20); // Розмір тексту
  noLoop(); // Малюємо лише при натисканні кнопки
}

void draw() {
  background(255);
  
  // Малюємо дві фіксовані точки
  fill(0);
  ellipse(A.x, A.y, 10, 10);
  ellipse(B.x, B.y, 10, 10);
  
  // Відображаємо поточний випадок
  fill(0);
  String caseText = "";
  
  switch (caseNum) {
    case 1:
      caseText = "Випадок 1: p = c^2 / 4";
      drawSet(sq(c) / 4, color(100, 50, 200), 5); 
      break;
    case 2:
      caseText = "Випадок 2: p < c^2 / 4";
      drawSet(sq(c) / 4 - 50, color(0, 255, 0), 5);
      break;
    case 3:
      caseText = "Випадок 3: c^2 / 4 < p < c^2 / 2";
      drawSet((sq(c) / 4 + sq(c) / 2) / 2, color(0, 0, 255), 5); 
      break;
    case 4:
      caseText = "Випадок 4: p > c^2 / 4";
      drawSet(sq(c) / 2 + 50, color(255, 0, 0), 5); 
      break;
  }
  
  // Виводимо текст випадку в лівому верхньому куті
  fill(0);
  text(caseText, 10, 30);
}

// Функція для малювання множини точок
void drawSet(float p, color col, float size) {
  stroke(col);
  fill(col);
  
  for (float x = 0; x < width; x += 1) {
    for (float y = 0; y < height; y += 1) {
      float distA = dist(x, y, A.x, A.y);
      float distB = dist(x, y, B.x, B.y);
      
      // Якщо добуток відстаней дорівнює p, малюємо точку
      if (abs(distA * distB - p) < 1) {
        ellipse(x, y, size, size); 
      }
    }
  }
}

// Обробка натискання клавіш
void keyPressed() {
  if (key == '1') {
    caseNum = 1; 
  } else if (key == '2') {
    caseNum = 2; 
  } else if (key == '3') {
    caseNum = 3;
  } else if (key == '4') {
    caseNum = 4; 
  }
  
  redraw(); // Оновлюємо зображення
}
