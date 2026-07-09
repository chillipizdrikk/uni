import javax.swing.*;
import java.awt.*;
import java.awt.event.MouseAdapter;
import java.awt.event.MouseEvent;
import java.util.Random;

class StrofoidGraph extends JPanel {

    private static final int VARIANT_NUMBER = 9;
    private static final String AUTHOR_NAME = "Тригуб";
    private static final int A = 3;

    // Початкові параметри графіка
    private Color graphColor = Color.MAGENTA;
    private Stroke graphStroke = new BasicStroke(2);
    private float strokeWidth = 2;

    public StrofoidGraph() {
        addMouseListener(new MouseAdapter() {
            @Override
            public void mouseClicked(MouseEvent e) {
                randomizeGraphStyle();
                repaint();
            }
        });
    }

    // Метод для випадкової зміни кольору, стилю і товщини лінії графіка
    private void randomizeGraphStyle() {
        Random random = new Random();

        graphColor = new Color(random.nextInt(256), random.nextInt(256), random.nextInt(256));
        strokeWidth = random.nextFloat() * 4 + 1; // Від 1 до 5

        int style = random.nextInt(3); // Збільшили до 4 для нових стилів
        switch (style) {
            case 0 -> graphStroke = new BasicStroke(strokeWidth); // суцільна
            case 1 -> graphStroke = new BasicStroke(strokeWidth, BasicStroke.CAP_BUTT, BasicStroke.JOIN_BEVEL, 0, new float[]{10f, 10f}, 0); // пунктир
            case 2 -> graphStroke = new BasicStroke(strokeWidth, BasicStroke.CAP_BUTT, BasicStroke.JOIN_BEVEL, 0, new float[]{10f, 5f, 2f, 5f}, 0); // штрих-пунктир
        }
    }

    // Метод для малювання графіка строфоїди
    @Override
    protected void paintComponent(Graphics g) {
        super.paintComponent(g);

        Graphics2D g2 = (Graphics2D) g;
        int width = getWidth();
        int height = getHeight();

        // Виведення прізвища і номера варіанта в лівому верхньому куті
        g2.setColor(Color.BLACK);
        g2.drawString(AUTHOR_NAME + " - Варіант №" + VARIANT_NUMBER, 10, 20);

        // Малюємо осі координат
        drawAxes(g2, width, height);

        // Малюємо графік строфоїди
        drawStrofoid(g2, width, height);
    }

    // Метод для малювання осей координат
    private void drawAxes(Graphics2D g2, int width, int height) {
        g2.setColor(Color.BLACK);
        g2.setStroke(new BasicStroke(2));

        // Вертикальна вісь
        g2.drawLine(width / 2, 0, width / 2, height);
        // Горизонтальна вісь
        g2.drawLine(0, height / 2, width, height / 2);
    }

    private void drawStrofoid(Graphics2D g2, int width, int height) {
        g2.setColor(graphColor); // Колір графіка
        g2.setStroke(graphStroke); // Стиль і товщина лінії графіка

        int centerX = width / 2;
        int centerY = height / 2;
        double scale = Math.min(width, height) / 10.0; // Масштабування графіка

        // Верхня частина графіка
        double prevX = -A + 0.01; // Змінили крок
        double prevY = Math.sqrt(prevX * prevX * ((A + prevX) / (A - prevX)));
        for (double x = -A + 0.01; x < A; x += 0.01) { // Змінили крок
            double temp = (A + x) / (A - x); // Обчислюємо значення під коренем
            if (temp >= 0) { // Перевірка на невизначеність
                double y = Math.sqrt(x * x * temp);

                int pixelX1 = (int) (centerX + prevX * scale);
                int pixelY1 = (int) (centerY - prevY * scale);
                int pixelX2 = (int) (centerX + x * scale);
                int pixelY2 = (int) (centerY - y * scale);

                g2.drawLine(pixelX1, pixelY1, pixelX2, pixelY2); // Малюємо верхню частину

                prevX = x;
                prevY = y;
            }
        }

        // Нижня частина графіка
        prevX = -A + 0.01; // Змінили крок
        prevY = Math.sqrt(prevX * prevX * ((A + prevX) / (A - prevX)));
        for (double x = -A + 0.01; x < A; x += 0.01) { // Змінили крок
            double temp = (A + x) / (A - x); // Обчислюємо значення під коренем
            if (temp >= 0) { // Перевірка на невизначеність
                double y = Math.sqrt(x * x * temp);

                int pixelX1 = (int) (centerX + prevX * scale);
                int pixelY1 = (int) (centerY + prevY * scale);
                int pixelX2 = (int) (centerX + x * scale);
                int pixelY2 = (int) (centerY + y * scale);

                g2.drawLine(pixelX1, pixelY1, pixelX2, pixelY2); // Малюємо нижню частину

                prevX = x;
                prevY = y;
            }
        }
    }


    // Створення вікна для відображення графіка
    private static void createAndShowGUI() {
        JFrame frame = new JFrame("Графік строфоїди");
        frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        frame.setSize(800, 600);
        frame.setResizable(true); // Дозволяємо зміну розміру вікна

        StrofoidGraph graphPanel = new StrofoidGraph();
        frame.add(graphPanel);
        frame.setVisible(true);
    }

    public static void main(String[] args) {
        SwingUtilities.invokeLater(StrofoidGraph::createAndShowGUI);
    }
}
