using System;
using System.Drawing;
using System.Threading;
using System.Windows.Forms;

namespace lab4__forms_
{
    public partial class Form1 : Form
    {
        public Form1()
        {
            InitializeComponent();

            // Встановлюємо розмір головного вікна
            this.Size = new Size(900, 700);

            // Встановлюємо позицію для головного вікна
            this.StartPosition = FormStartPosition.Manual; 
            this.Location = new Point(250, 50); 

            this.Load += Form1_Load; // Додаємо обробник події Load
        }

        private void Form1_Load(object sender, EventArgs e)
        {
            // Відкриваємо всі форми при запуску
            OpenBallForm();
            OpenRectangleForm();
            OpenSineWaveForm();
            OpenRotationForm();
        }

        private void OpenBallForm()
        {
            BallForm ballForm = new BallForm
            {
                StartPosition = FormStartPosition.Manual,
                Location = new Point(300, 100), // Встановлюємо позицію для кульки
                Owner = this // Встановлюємо головне вікно як батьківське
            };
            ballForm.Show();
        }

        private void OpenRectangleForm()
        {
            RectangleForm rectangleForm = new RectangleForm
            {
                StartPosition = FormStartPosition.Manual,
                Location = new Point(700, 100), // Встановлюємо позицію для прямокутника
                Owner = this // Встановлюємо головне вікно як батьківське
            };
            rectangleForm.Show();
        }

        private void OpenSineWaveForm()
        {
            SineWaveForm sineWaveForm = new SineWaveForm
            {
                StartPosition = FormStartPosition.Manual,
                Location = new Point(300, 400), // Встановлюємо позицію для синусоїди
                Owner = this // Встановлюємо головне вікно як батьківське
            };
            sineWaveForm.Show();
        }

        private void OpenRotationForm()
        {
            RotationForm rotationForm = new RotationForm
            {
                StartPosition = FormStartPosition.Manual,
                Location = new Point(700, 400), // Встановлюємо позицію для обертання
                Owner = this // Встановлюємо головне вікно як батьківське
            };
            rotationForm.Show();
        }

        // Клас для анімації кульки
        private class BallForm : Form
        {
            private Thread thread;
            private ManualResetEvent pauseEvent = new ManualResetEvent(true);

            public BallForm()
            {
                this.Load += BallForm_Load;
                this.FormClosed += (s, e) => thread?.Abort();
                this.Size = new Size(400, 300);

                Button pauseButton = new Button { Text = "Пауза", Location = new Point(10, 10) };
                pauseButton.Click += (s, e) => pauseEvent.Reset();
                Controls.Add(pauseButton);

                Button resumeButton = new Button { Text = "Відновити", Location = new Point(100, 10) };
                resumeButton.Click += (s, e) => pauseEvent.Set();
                Controls.Add(resumeButton);
            }

            private void BallForm_Load(object sender, EventArgs e)
            {
                thread = new Thread(AnimateBall) { IsBackground = true };
                thread.Start();
            }

            private void AnimateBall()
            {
                int x = 0, y = 100;
                while (true)
                {
                    pauseEvent.WaitOne();
                    x += 10;
                    if (x > this.ClientSize.Width) x = 0;

                    this.Invoke((MethodInvoker)delegate
                    {
                        using (Graphics g = this.CreateGraphics())
                        {
                            g.Clear(Color.White);
                            g.FillEllipse(Brushes.DarkSlateBlue, x, y, 50, 50);
                        }
                    });
                    Thread.Sleep(50);
                }
            }
        }

        // Клас для анімації прямокутника
        private class RectangleForm : Form
        {
            private Thread thread;
            private ManualResetEvent pauseEvent = new ManualResetEvent(true);

            public RectangleForm()
            {
                this.Load += RectangleForm_Load;
                this.FormClosed += (s, e) => thread?.Abort();
                this.Size = new Size(400, 300);

                Button pauseButton = new Button { Text = "Пауза", Location = new Point(10, 10) };
                pauseButton.Click += (s, e) => pauseEvent.Reset();
                Controls.Add(pauseButton);

                Button resumeButton = new Button { Text = "Відновити", Location = new Point(100, 10) };
                resumeButton.Click += (s, e) => pauseEvent.Set();
                Controls.Add(resumeButton);
            }

            private void RectangleForm_Load(object sender, EventArgs e)
            {
                thread = new Thread(AnimateRectangle) { IsBackground = true };
                thread.Start();
            }

            private void AnimateRectangle()
            {
                int width = 10, height = 10;
                bool increasing = true;
                while (true)
                {
                    pauseEvent.WaitOne();
                    if (increasing)
                    {
                        width += 5;
                        height += 5;
                        if (width > 100) increasing = false;
                    }
                    else
                    {
                        width -= 5;
                        height -= 5;
                        if (width < 50) increasing = true;
                    }

                    this.Invoke((MethodInvoker)delegate
                    {
                        using (Graphics g = this.CreateGraphics())
                        {
                            g.Clear(Color.White);
                            g.FillRectangle(Brushes.DarkCyan, 150, 100, width, height);
                        }
                    });
                    Thread.Sleep(100);
                }
            }
        }

        // Клас для анімації синусоїди
        private class SineWaveForm : Form
        {
            private Thread thread;
            private ManualResetEvent pauseEvent = new ManualResetEvent(true);

            public SineWaveForm()
            {
                this.Load += SineWaveForm_Load;
                this.FormClosed += (s, e) => thread?.Abort();
                this.Size = new Size(400, 300);

                Button pauseButton = new Button { Text = "Пауза", Location = new Point(10, 10) };
                pauseButton.Click += (s, e) => pauseEvent.Reset();
                Controls.Add(pauseButton);

                Button resumeButton = new Button { Text = "Відновити", Location = new Point(100, 10) };
                resumeButton.Click += (s, e) => pauseEvent.Set();
                Controls.Add(resumeButton);
            }

            private void SineWaveForm_Load(object sender, EventArgs e)
            {
                thread = new Thread(AnimateSineWave) { IsBackground = true };
                thread.Start();
            }

            private void AnimateSineWave()
            {
                int x = 0;
                while (true)
                {
                    pauseEvent.WaitOne();
                    x += 5;
                    if (x > this.ClientSize.Width) x = 0;

                    this.Invoke((MethodInvoker)delegate
                    {
                        using (Graphics g = this.CreateGraphics())
                        {
                            g.Clear(Color.White);
                            Pen sinePen = new Pen(Color.DeepSkyBlue, 2);
                            Point previousPoint = new Point(0, this.ClientSize.Height / 2);

                            for (int i = 0; i < this.ClientSize.Width; i += 5)
                            {
                                int y = (int)(Math.Sin((i + x) * 0.1) * 50 + this.ClientSize.Height / 2);
                                Point currentPoint = new Point(i, y);
                                g.DrawLine(sinePen, previousPoint, currentPoint);
                                previousPoint = currentPoint;
                            }
                        }
                    });
                    Thread.Sleep(150);
                }
            }
        }

        // Клас для анімації обертання
        private class RotationForm : Form
        {
            private Thread thread;
            private ManualResetEvent pauseEvent = new ManualResetEvent(true);

            public RotationForm()
            {
                this.Load += RotationForm_Load;
                this.FormClosed += (s, e) => thread?.Abort();
                this.Size = new Size(400, 300);

                Button pauseButton = new Button { Text = "Пауза", Location = new Point(10, 10) };
                pauseButton.Click += (s, e) => pauseEvent.Reset();
                Controls.Add(pauseButton);

                Button resumeButton = new Button { Text = "Відновити", Location = new Point(100, 10) };
                resumeButton.Click += (s, e) => pauseEvent.Set();
                Controls.Add(resumeButton);
            }

            private void RotationForm_Load(object sender, EventArgs e)
            {
                thread = new Thread(AnimateRotation) { IsBackground = true };
                thread.Start();
            }

            private void AnimateRotation()
            {
                float angle = 0;
                Pen thickPen = new Pen(Color.DarkTurquoise, 5);
                while (true)
                {
                    pauseEvent.WaitOne();
                    angle += 0.1f;
                    if (angle > 2 * Math.PI) angle = 0;

                    this.Invoke((MethodInvoker)delegate
                    {
                        using (Graphics g = this.CreateGraphics())
                        {
                            g.Clear(Color.White);
                            g.DrawLine(thickPen, 200, 150,
                                (float)(200 + 100 * Math.Cos(angle)),
                                (float)(150 + 100 * Math.Sin(angle)));
                        }
                    });
                    Thread.Sleep(50);
                }
            }
        }
    }
}
