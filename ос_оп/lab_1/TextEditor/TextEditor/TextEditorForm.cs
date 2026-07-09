using System;
using System.IO;
using System.Text;
using System.Linq;
using System.Windows.Forms;

namespace TextEditor
{
    public partial class TextEditorForm : Form
    {
        private string currentFilePath = "";
        private Encoding currentEncoding = Encoding.UTF8;
        private bool isModified = false;

        public TextEditorForm()
        {
            InitializeComponent();
            this.Text = "Text Editor - Untitled";
            this.WindowState = FormWindowState.Maximized;
        }

        private void InitializeComponent()
        {
            this.SuspendLayout();

            // Меню
            MenuStrip menuStrip = new MenuStrip();

            ToolStripMenuItem fileMenu = new ToolStripMenuItem("&File");
            fileMenu.DropDownItems.Add("&Open", null, OpenFile_Click);
            fileMenu.DropDownItems.Add("&Save", null, SaveFile_Click);
            fileMenu.DropDownItems.Add("Save &As", null, SaveAsFile_Click);
            fileMenu.DropDownItems.Add(new ToolStripSeparator());
            fileMenu.DropDownItems.Add("E&xit", null, Exit_Click);

            ToolStripMenuItem editMenu = new ToolStripMenuItem("&Edit");
            editMenu.DropDownItems.Add("&Undo", null, Undo_Click);
            editMenu.DropDownItems.Add("&Redo", null, Redo_Click);
            editMenu.DropDownItems.Add(new ToolStripSeparator());
            editMenu.DropDownItems.Add("Cu&t", null, Cut_Click);
            editMenu.DropDownItems.Add("&Copy", null, Copy_Click);
            editMenu.DropDownItems.Add("&Paste", null, Paste_Click);
            editMenu.DropDownItems.Add(new ToolStripSeparator());
            editMenu.DropDownItems.Add("Select &All", null, SelectAll_Click);
            editMenu.DropDownItems.Add("&Find", null, Find_Click);
            editMenu.DropDownItems.Add("&Replace", null, Replace_Click);

            ToolStripMenuItem encodingMenu = new ToolStripMenuItem("&Encoding");
            encodingMenu.DropDownItems.Add("UTF-8", null, SetEncodingUTF8_Click);
            encodingMenu.DropDownItems.Add("Windows-1251 (ANSI)", null, SetEncodingANSI_Click);
            encodingMenu.DropDownItems.Add("ASCII", null, SetEncodingASCII_Click);

            ToolStripMenuItem helpMenu = new ToolStripMenuItem("&Help");
            helpMenu.DropDownItems.Add("&About", null, About_Click);

            menuStrip.Items.Add(fileMenu);
            menuStrip.Items.Add(editMenu);
            menuStrip.Items.Add(encodingMenu);
            menuStrip.Items.Add(helpMenu);

            // Текстовий редактор
            RichTextBox textBox = new RichTextBox();
            textBox.Name = "textBox";
            textBox.Dock = DockStyle.Fill;
            textBox.Font = new System.Drawing.Font("Courier New", 11);
            textBox.TextChanged += TextBox_TextChanged;

            // Статус бар
            StatusStrip statusStrip = new StatusStrip();
            ToolStripStatusLabel encodingLabel = new ToolStripStatusLabel("UTF-8");
            encodingLabel.Name = "encodingLabel";
            statusStrip.Items.Add(encodingLabel);

            this.Controls.Add(textBox);
            this.Controls.Add(statusStrip);
            this.Controls.Add(menuStrip);

            this.MainMenuStrip = menuStrip;
            this.Name = "TextEditorForm";
            this.Text = "Text Editor";
            this.FormClosing += TextEditorForm_FormClosing;

            this.ResumeLayout(false);
            this.PerformLayout();
        }

        private RichTextBox GetTextBox() => this.Controls["textBox"] as RichTextBox;
        private StatusStrip GetStatusStrip() => this.Controls.OfType<StatusStrip>().FirstOrDefault();

        private void OpenFile_Click(object sender, EventArgs e)
        {
            using (OpenFileDialog openFileDialog = new OpenFileDialog())
            {
                openFileDialog.Filter = "Text files (*.txt)|*.txt|All files (*.*)|*.*";
                openFileDialog.Title = "Open File";

                if (openFileDialog.ShowDialog() == DialogResult.OK)
                {
                    try
                    {
                        currentFilePath = openFileDialog.FileName;
                        DetectAndLoadEncoding();
                        this.Text = $"Text Editor - {Path.GetFileName(currentFilePath)}";
                        isModified = false;
                    }
                    catch (Exception ex)
                    {
                        MessageBox.Show($"Error opening file: {ex.Message}", "Error", MessageBoxButtons.OK, MessageBoxIcon.Error);
                    }
                }
            }
        }

        private void DetectAndLoadEncoding()
        {
            byte[] fileBytes = File.ReadAllBytes(currentFilePath);

            // Спроба визначити кодування
            Encoding detectedEncoding = DetectEncoding(fileBytes);

            try
            {
                string content = detectedEncoding.GetString(fileBytes);
                GetTextBox().Text = content;
                currentEncoding = detectedEncoding;
                UpdateEncodingLabel();
            }
            catch
            {
                // Якщо не вдалось, пропонуємо виконати вибір вручну
                ShowEncodingSelectionDialog(fileBytes);
            }
        }

        private Encoding DetectEncoding(byte[] fileBytes)
        {
            // Перевірка на BOM
            if (fileBytes.Length >= 3 && fileBytes[0] == 0xEF && fileBytes[1] == 0xBB && fileBytes[2] == 0xBF)
                return Encoding.UTF8;

            if (fileBytes.Length >= 2 && fileBytes[0] == 0xFF && fileBytes[1] == 0xFE)
                return Encoding.Unicode;

            // Спроба визначити UTF-8
            if (IsValidUTF8(fileBytes))
                return Encoding.UTF8;

            // За замовчуванням - Windows-1251
            return Encoding.GetEncoding(1251);
        }

        private bool IsValidUTF8(byte[] data)
        {
            int i = 0;
            while (i < data.Length)
            {
                if ((data[i] & 0x80) == 0)
                {
                    i++;
                }
                else if ((data[i] & 0xE0) == 0xC0)
                {
                    if (i + 1 >= data.Length || (data[i + 1] & 0xC0) != 0x80)
                        return false;
                    i += 2;
                }
                else if ((data[i] & 0xF0) == 0xE0)
                {
                    if (i + 2 >= data.Length || (data[i + 1] & 0xC0) != 0x80 || (data[i + 2] & 0xC0) != 0x80)
                        return false;
                    i += 3;
                }
                else if ((data[i] & 0xF8) == 0xF0)
                {
                    if (i + 3 >= data.Length || (data[i + 1] & 0xC0) != 0x80 || (data[i + 2] & 0xC0) != 0x80 || (data[i + 3] & 0xC0) != 0x80)
                        return false;
                    i += 4;
                }
                else
                    return false;
            }
            return true;
        }

        private void ShowEncodingSelectionDialog(byte[] fileBytes)
        {
            using (EncodingSelectionForm form = new EncodingSelectionForm())
            {
                if (form.ShowDialog() == DialogResult.OK)
                {
                    currentEncoding = form.SelectedEncoding;
                    string content = currentEncoding.GetString(fileBytes);
                    GetTextBox().Text = content;
                    UpdateEncodingLabel();
                }
            }
        }

        private void SaveFile_Click(object sender, EventArgs e)
        {
            if (string.IsNullOrEmpty(currentFilePath))
            {
                SaveAsFile_Click(sender, e);
            }
            else
            {
                SaveFileInternal();
            }
        }

        private void SaveAsFile_Click(object sender, EventArgs e)
        {
            using (SaveFileDialog saveFileDialog = new SaveFileDialog())
            {
                saveFileDialog.Filter = "Text files (*.txt)|*.txt|All files (*.*)|*.*";
                saveFileDialog.Title = "Save File As";

                if (saveFileDialog.ShowDialog() == DialogResult.OK)
                {
                    currentFilePath = saveFileDialog.FileName;
                    SaveFileInternal();
                    this.Text = $"Text Editor - {Path.GetFileName(currentFilePath)}";
                }
            }
        }

        private void SaveFileInternal()
        {
            try
            {
                byte[] content = currentEncoding.GetBytes(GetTextBox().Text);
                File.WriteAllBytes(currentFilePath, content);
                isModified = false;
                MessageBox.Show("File saved successfully!", "Success", MessageBoxButtons.OK, MessageBoxIcon.Information);
            }
            catch (Exception ex)
            {
                MessageBox.Show($"Error saving file: {ex.Message}", "Error", MessageBoxButtons.OK, MessageBoxIcon.Error);
            }
        }

        private void SetEncodingUTF8_Click(object sender, EventArgs e)
        {
            currentEncoding = Encoding.UTF8;
            UpdateEncodingLabel();
            ReloadWithNewEncoding();
        }

        private void SetEncodingANSI_Click(object sender, EventArgs e)
        {
            currentEncoding = Encoding.GetEncoding(1251);
            UpdateEncodingLabel();
            ReloadWithNewEncoding();
        }

        private void SetEncodingASCII_Click(object sender, EventArgs e)
        {
            currentEncoding = Encoding.ASCII;
            UpdateEncodingLabel();
            ReloadWithNewEncoding();
        }

        private void ReloadWithNewEncoding()
        {
            if (!string.IsNullOrEmpty(currentFilePath) && File.Exists(currentFilePath))
            {
                try
                {
                    byte[] fileBytes = File.ReadAllBytes(currentFilePath);
                    string content = currentEncoding.GetString(fileBytes);
                    GetTextBox().Text = content;
                }
                catch (Exception ex)
                {
                    MessageBox.Show($"Error reloading with new encoding: {ex.Message}", "Error", MessageBoxButtons.OK, MessageBoxIcon.Error);
                }
            }
        }

        private void UpdateEncodingLabel()
        {
            var statusStrip = GetStatusStrip();
            if (statusStrip != null)
            {
                var label = statusStrip.Items["encodingLabel"] as ToolStripStatusLabel;
                if (label != null)
                {
                    if (currentEncoding == Encoding.UTF8)
                        label.Text = "UTF-8";
                    else if (currentEncoding.CodePage == 1251)
                        label.Text = "Windows-1251 (ANSI)";
                    else if (currentEncoding == Encoding.ASCII)
                        label.Text = "ASCII";
                }
            }
        }

        private void Cut_Click(object sender, EventArgs e) => GetTextBox().Cut();
        private void Copy_Click(object sender, EventArgs e) => GetTextBox().Copy();
        private void Paste_Click(object sender, EventArgs e) => GetTextBox().Paste();
        private void SelectAll_Click(object sender, EventArgs e) => GetTextBox().SelectAll();
        private void Undo_Click(object sender, EventArgs e) => GetTextBox().Undo();
        private void Redo_Click(object sender, EventArgs e) => GetTextBox().Redo();

        private void Find_Click(object sender, EventArgs e)
        {
            string searchText = Microsoft.VisualBasic.Interaction.InputBox("Find:", "Find");
            if (!string.IsNullOrEmpty(searchText))
            {
                int index = GetTextBox().Text.IndexOf(searchText);
                if (index >= 0)
                {
                    GetTextBox().Select(index, searchText.Length);
                    GetTextBox().Focus();
                }
                else
                {
                    MessageBox.Show("Text not found.", "Find", MessageBoxButtons.OK, MessageBoxIcon.Information);
                }
            }
        }

        private void Replace_Click(object sender, EventArgs e)
        {
            string searchText = Microsoft.VisualBasic.Interaction.InputBox("Find:", "Replace");
            if (!string.IsNullOrEmpty(searchText))
            {
                string replaceText = Microsoft.VisualBasic.Interaction.InputBox("Replace with:", "Replace");
                GetTextBox().Text = GetTextBox().Text.Replace(searchText, replaceText);
                isModified = true;
            }
        }

        private void Exit_Click(object sender, EventArgs e)
        {
            this.Close();
        }

        private void About_Click(object sender, EventArgs e)
        {
            MessageBox.Show(
                "Text Editor v1.0\n\n" +
                "Features:\n" +
                "- Support for UTF-8, Windows-1251 (ANSI), and ASCII encodings\n" +
                "- Automatic encoding detection\n" +
                "- Find and Replace functionality\n" +
                "- Standard text editing operations",
                "About Text Editor",
                MessageBoxButtons.OK,
                MessageBoxIcon.Information);
        }

        private void TextBox_TextChanged(object sender, EventArgs e)
        {
            isModified = true;
        }

        private void TextEditorForm_FormClosing(object sender, FormClosingEventArgs e)
        {
            if (isModified)
            {
                DialogResult result = MessageBox.Show(
                    "Do you want to save changes before closing?",
                    "Unsaved Changes",
                    MessageBoxButtons.YesNoCancel,
                    MessageBoxIcon.Question);

                if (result == DialogResult.Yes)
                {
                    SaveFile_Click(null, null);
                }
                else if (result == DialogResult.Cancel)
                {
                    e.Cancel = true;
                }
            }
        }
    }

    public partial class EncodingSelectionForm : Form
    {
        public Encoding SelectedEncoding { get; private set; }

        public EncodingSelectionForm()
        {
            InitializeComponent();
        }

        private void InitializeComponent()
        {
            this.SuspendLayout();

            Label label = new Label();
            label.Text = "Select encoding:";
            label.Location = new System.Drawing.Point(20, 20);
            label.AutoSize = true;

            ComboBox comboBox = new ComboBox();
            comboBox.Name = "encodingComboBox";
            comboBox.Location = new System.Drawing.Point(20, 50);
            comboBox.Width = 250;
            comboBox.Items.AddRange(new object[] { "UTF-8", "Windows-1251 (ANSI)", "ASCII" });
            comboBox.SelectedIndex = 0;
            comboBox.DropDownStyle = ComboBoxStyle.DropDownList;

            Button okButton = new Button();
            okButton.Text = "OK";
            okButton.Location = new System.Drawing.Point(95, 100);
            okButton.Click += (s, e) =>
            {
                int index = comboBox.SelectedIndex;
                SelectedEncoding = index switch
                {
                    0 => Encoding.UTF8,
                    1 => Encoding.GetEncoding(1251),
                    2 => Encoding.ASCII,
                    _ => Encoding.UTF8
                };
                this.DialogResult = DialogResult.OK;
                this.Close();
            };

            Button cancelButton = new Button();
            cancelButton.Text = "Cancel";
            cancelButton.Location = new System.Drawing.Point(180, 100);
            cancelButton.Click += (s, e) =>
            {
                this.DialogResult = DialogResult.Cancel;
                this.Close();
            };

            this.Controls.Add(label);
            this.Controls.Add(comboBox);
            this.Controls.Add(okButton);
            this.Controls.Add(cancelButton);

            this.Text = "Select Encoding";
            this.Width = 300;
            this.Height = 180;
            this.StartPosition = FormStartPosition.CenterParent;
            this.FormBorderStyle = FormBorderStyle.FixedDialog;
            this.MaximizeBox = false;
            this.MinimizeBox = false;

            this.ResumeLayout(false);
        }
    }
}