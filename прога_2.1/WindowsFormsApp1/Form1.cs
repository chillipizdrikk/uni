using System;
using System.Collections.ObjectModel;
using System.ComponentModel;
using System.Drawing;
using System.Windows.Forms;
using static System.Windows.Forms.VisualStyles.VisualStyleElement.Button;

namespace RadioGroupControl
{
    public partial class RadioGroup : UserControl
    {
        // Колекція для зберігання імен радіокнопок
        private ObservableCollection<string> names = new ObservableCollection<string>();

        // Список радіокнопок, який автоматично оновлюється при зміні колекції імен
        private BindingList<RadioButton> buttons = new BindingList<RadioButton>();

        // Індекс вибраної радіокнопки
        private int indexSelected = -1; // Ініціалізація недійсним індексом

        // Подія, яка викликається при зміні вибраної радіокнопки
        public event EventHandler SelectedIndexChanged;

        public RadioGroup()
        {
            InitializeComponent();
            names.CollectionChanged += Names_CollectionChanged;
        }

        private void Names_CollectionChanged(object sender, System.Collections.Specialized.NotifyCollectionChangedEventArgs e)
        {
            UpdateButtons();
            OnItemsChanged(EventArgs.Empty); // Виклик події ItemsChanged
        }

        // Подія, яка викликається при зміні колекції імен
        public event EventHandler ItemsChanged;

        protected virtual void OnItemsChanged(EventArgs e)
        {
            ItemsChanged?.Invoke(this, e);
        }

        // Властивість для отримання та задання тексту RadioGroup
        [Browsable(true)]
        [DesignerSerializationVisibility(DesignerSerializationVisibility.Visible)]
        public override string Text
        {
            get { return groupBox1.Text; }
            set { groupBox1.Text = value; }
        }

        // Властивість для зберігання колекції імен радіокнопок
        [Category("Data")]
        [Description("The names of radio buttons in the group.")]
        [DesignerSerializationVisibility(DesignerSerializationVisibility.Content)]
        public ObservableCollection<string> Items
        {
            get { return names; }
            set { names = value; }
        }

        // Властивість для задання або отримання індексу вибраної радіокнопки
        public int IndexSelected
        {
            get { return indexSelected; }
            set
            {
                if (indexSelected != value && value >= 0 && value < buttons.Count)
                {
                    indexSelected = value;
                    buttons[indexSelected].Checked = true;
                    OnSelectedIndexChanged(); // Виклик події SelectedIndexChanged
                }
            }
        }

        // Метод для виклику події SelectedIndexChanged
        protected virtual void OnSelectedIndexChanged()
        {
            SelectedIndexChanged?.Invoke(this, EventArgs.Empty);
        }

        // Метод для оновлення радіокнопок на формі
        private void UpdateButtons()
        {
            foreach (var button in buttons)
            {
                button.CheckedChanged -= RadioButton_CheckedChanged; // Відключення обробника події
            }

            foreach (var button in buttons)
            {
                Controls.Remove(button);
                button.Dispose();
            }
            buttons.Clear();

            foreach (var name in names)
            {
                var button = new RadioButton();
                button.Text = name;
                button.AutoSize = true;
                button.CheckedChanged += RadioButton_CheckedChanged; // Підключення обробника події
                buttons.Add(button);
            }

            ArrangeButtons();
        }

        // Метод для розташування радіокнопок на формі
        private void ArrangeButtons()
        {
            var yPos = 20; // Початкова Y-позиція
            var xPos = 20; // Початкова X-позиція
            foreach (var button in buttons)
            {
                button.Location = new Point(xPos, yPos);
                yPos += button.Height + 5; // Відступ між кнопками
                Controls.Add(button);
            }
        }

        // Обробник події зміни вибору радіокнопки
        private void RadioButton_CheckedChanged(object sender, EventArgs e)
        {
            var radioButton = (RadioButton)sender;
            IndexSelected = buttons.IndexOf(radioButton);
        }
    }
}
