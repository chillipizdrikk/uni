namespace MobileTopUpTerminal
{
    partial class Form1
    {
        /// <summary>
        /// Required designer variable.
        /// </summary>
        private System.ComponentModel.IContainer components = null;

        /// <summary>
        /// Clean up any resources being used.
        /// </summary>
        /// <param name="disposing">true if managed resources should be disposed; otherwise, false.</param>
        protected override void Dispose(bool disposing)
        {
            if (disposing && (components != null))
            {
                components.Dispose();
            }
            base.Dispose(disposing);
        }

        #region Windows Form Designer generated code

        /// <summary>
        /// Required method for Designer support - do not modify
        /// the contents of this method with the code editor.
        /// </summary>
        private void InitializeComponent()
        {
            this.phoneNumberTextBox = new System.Windows.Forms.TextBox();
            this.amountTextBox = new System.Windows.Forms.TextBox();
            this.operatorComboBox = new System.Windows.Forms.ComboBox();
            this.topUpButton = new System.Windows.Forms.Button();
            this.phoneNumberLabel = new System.Windows.Forms.Label();
            this.amountLabel = new System.Windows.Forms.Label();
            this.languageLabel = new System.Windows.Forms.Label();
            this.operatorLabel = new System.Windows.Forms.Label();
            this.languageComboBox = new System.Windows.Forms.ComboBox();
            this.cardNumberTextBox = new System.Windows.Forms.TextBox();
            this.expiryDateTextBox = new System.Windows.Forms.TextBox();
            this.cvvTextBox = new System.Windows.Forms.TextBox();
            this.cardNumberLabel = new System.Windows.Forms.Label();
            this.expiryDateLabel = new System.Windows.Forms.Label();
            this.cvvLabel = new System.Windows.Forms.Label();
            this.pinTextBox = new System.Windows.Forms.TextBox();
            this.pinLabel = new System.Windows.Forms.Label(); // Доданий рядок
            // Додано поле для введення відсотка благодійності
            this.charityTextBox = new System.Windows.Forms.TextBox();
            // Додано мітку для поля благодійності
            this.charityLabel = new System.Windows.Forms.Label();
            // Додано мітку для попередження про комісію
            this.commissionLabel = new System.Windows.Forms.Label();

            this.SuspendLayout();
            // 
            // phoneNumberTextBox
            // 
            this.phoneNumberTextBox.Location = new System.Drawing.Point(150, 30);
            this.phoneNumberTextBox.Name = "phoneNumberTextBox";
            this.phoneNumberTextBox.Size = new System.Drawing.Size(150, 20);
            this.phoneNumberTextBox.TabIndex = 0;
            // 
            // amountTextBox
            // 
            this.amountTextBox.Location = new System.Drawing.Point(150, 70);
            this.amountTextBox.Name = "amountTextBox";
            this.amountTextBox.Size = new System.Drawing.Size(150, 20);
            this.amountTextBox.TabIndex = 1;
            // 
            // operatorComboBox
            // 
            this.operatorComboBox.FormattingEnabled = true;
            this.operatorComboBox.Location = new System.Drawing.Point(150, 110);
            this.operatorComboBox.Name = "operatorComboBox";
            this.operatorComboBox.Size = new System.Drawing.Size(150, 21);
            this.operatorComboBox.TabIndex = 2;
            // 
            // topUpButton
            // 
            this.topUpButton.Location = new System.Drawing.Point(100, 370);
            this.topUpButton.Name = "topUpButton";
            this.topUpButton.Size = new System.Drawing.Size(150, 23);
            this.topUpButton.TabIndex = 3;
            this.topUpButton.Text = "Поповнити";
            this.topUpButton.UseVisualStyleBackColor = true;
            this.topUpButton.Click += new System.EventHandler(this.topUpButton_Click);
            // 
            // phoneNumberLabel
            // 
            this.phoneNumberLabel.AutoSize = true;
            this.phoneNumberLabel.Location = new System.Drawing.Point(30, 30);
            this.phoneNumberLabel.Name = "phoneNumberLabel";
            this.phoneNumberLabel.Size = new System.Drawing.Size(101, 13);
            this.phoneNumberLabel.TabIndex = 4;
            this.phoneNumberLabel.Text = "Номер телефону:";
            // 
            // amountLabel
            // 
            this.amountLabel.AutoSize = true;
            this.amountLabel.Location = new System.Drawing.Point(30, 70);
            this.amountLabel.Name = "amountLabel";
            this.amountLabel.Size = new System.Drawing.Size(103, 13);
            this.amountLabel.TabIndex = 5;
            this.amountLabel.Text = "Сума поповнення:";
            // 
            // operatorLabel
            // 
            this.operatorLabel.AutoSize = true;
            this.operatorLabel.Location = new System.Drawing.Point(30, 110);
            this.operatorLabel.Name = "operatorLabel";
            this.operatorLabel.Size = new System.Drawing.Size(61, 13);
            this.operatorLabel.TabIndex = 6;
            this.operatorLabel.Text = "Оператор:";
            // 
            // languageComboBox
            // 
            this.languageComboBox.FormattingEnabled = true;
            this.languageComboBox.Location = new System.Drawing.Point(150, 5);
            this.languageComboBox.Name = "languageComboBox";
            this.languageComboBox.Size = new System.Drawing.Size(151, 21);
            this.languageComboBox.TabIndex = 7;
            this.languageComboBox.SelectedIndexChanged += new System.EventHandler(this.languageComboBox_SelectedIndexChanged);
            // 
            // languageLabel
            //
            this.languageLabel.AutoSize = true;
            this.languageLabel.Location = new System.Drawing.Point(30, 5);
            this.languageLabel.Name = "languageLabel";
            this.languageLabel.Size = new System.Drawing.Size(83, 13);
            this.languageLabel.TabIndex = 8;
            this.languageLabel.Text = "Оберіть мову:";
            // 
            // cardNumberTextBox
            // 
            this.cardNumberTextBox.Location = new System.Drawing.Point(150, 150);
            this.cardNumberTextBox.Name = "cardNumberTextBox";
            this.cardNumberTextBox.Size = new System.Drawing.Size(150, 20);
            this.cardNumberTextBox.TabIndex = 9;
            // 
            // expiryDateTextBox
            // 
            this.expiryDateTextBox.Location = new System.Drawing.Point(150, 190);
            this.expiryDateTextBox.Name = "expiryDateTextBox";
            this.expiryDateTextBox.Size = new System.Drawing.Size(150, 20);
            this.expiryDateTextBox.TabIndex = 10;
            // 
            // cvvTextBox
            // 
            this.cvvTextBox.Location = new System.Drawing.Point(150, 230);
            this.cvvTextBox.Name = "cvvTextBox";
            this.cvvTextBox.PasswordChar = '*';
            this.cvvTextBox.Size = new System.Drawing.Size(150, 20);
            this.cvvTextBox.TabIndex = 11;
            // 
            // cardNumberLabel
            // 
            this.cardNumberLabel.AutoSize = true;
            this.cardNumberLabel.Location = new System.Drawing.Point(30, 150);
            this.cardNumberLabel.Name = "cardNumberLabel";
            this.cardNumberLabel.Size = new System.Drawing.Size(79, 13);
            this.cardNumberLabel.TabIndex = 12;
            this.cardNumberLabel.Text = "Номер картки:";
            // 
            // expiryDateLabel
            // 
            this.expiryDateLabel.AutoSize = true;
            this.expiryDateLabel.Location = new System.Drawing.Point(30, 190);
            this.expiryDateLabel.Name = "expiryDateLabel";
            this.expiryDateLabel.Size = new System.Drawing.Size(65, 13);
            this.expiryDateLabel.TabIndex = 13;
            this.expiryDateLabel.Text = "Термін дії:";
            // 
            // cvvLabel
            // 
            this.cvvLabel.AutoSize = true;
            this.cvvLabel.Location = new System.Drawing.Point(30, 230);
            this.cvvLabel.Name = "cvvLabel";
            this.cvvLabel.Size = new System.Drawing.Size(57, 13);
            this.cvvLabel.TabIndex = 14;
            this.cvvLabel.Text = "CVV код:";
            // 
            // pinTextBox
            // 
            this.pinTextBox.Location = new System.Drawing.Point(150, 270);
            this.pinTextBox.Name = "pinTextBox";
            this.pinTextBox.PasswordChar = '*';
            this.pinTextBox.Size = new System.Drawing.Size(150, 20);
            this.pinTextBox.TabIndex = 15;
            // 
            // pinLabel
            // 
            this.pinLabel.AutoSize = true;
            this.pinLabel.Location = new System.Drawing.Point(30, 270);
            this.pinLabel.Name = "pinLabel";
            this.pinLabel.Size = new System.Drawing.Size(48, 13);
            this.pinLabel.TabIndex = 16;
            this.pinLabel.Text = "PIN код:";
            // 
            // charityTextBox
            // 
            this.charityTextBox.Location = new System.Drawing.Point(170, 310);
            this.charityTextBox.Name = "charityTextBox";
            this.charityTextBox.Size = new System.Drawing.Size(130, 20);
            this.charityTextBox.TabIndex = 17;
            // 
            // charityLabel
            // 
            this.charityLabel.AutoSize = true;
            this.charityLabel.Location = new System.Drawing.Point(30, 310);
            this.charityLabel.Name = "charityLabel";
            this.charityLabel.Size = new System.Drawing.Size(154, 13);
            this.charityLabel.TabIndex = 18;
            this.charityLabel.Text = "Відсоток благодійності:";
            //
            // commissionLabel
            //
            this.commissionLabel.AutoSize = true;
            this.commissionLabel.Location = new System.Drawing.Point(30, 330);
            this.commissionLabel.Name = "commissionLabel";
            this.commissionLabel.Size = new System.Drawing.Size(100, 13);
            this.commissionLabel.TabIndex = 19;
            this.commissionLabel.Text = "Комісія банку: 3%";

            // 
            // Form1
            // 
            this.ClientSize = new System.Drawing.Size(334, 400);
            this.Controls.Add(this.pinLabel);
            this.Controls.Add(this.pinTextBox);
            this.Controls.Add(this.cvvLabel);
            this.Controls.Add(this.expiryDateLabel);
            this.Controls.Add(this.cardNumberLabel);
            this.Controls.Add(this.cvvTextBox);
            this.Controls.Add(this.expiryDateTextBox);
            this.Controls.Add(this.cardNumberTextBox);
            this.Controls.Add(this.languageComboBox);
            this.Controls.Add(this.operatorLabel);
            this.Controls.Add(this.amountLabel);
            this.Controls.Add(this.languageLabel);
            this.Controls.Add(this.phoneNumberLabel);
            this.Controls.Add(this.topUpButton);
            this.Controls.Add(this.operatorComboBox);
            this.Controls.Add(this.amountTextBox);
            this.Controls.Add(this.phoneNumberTextBox);
            this.Controls.Add(this.charityTextBox);
            this.Controls.Add(this.charityLabel);
            this.Controls.Add(this.commissionLabel);
            this.Name = "Form1";
            this.Text = "Термінал поповнення";
            this.ResumeLayout(false);
            this.PerformLayout();

        }

        #endregion

        private System.Windows.Forms.TextBox phoneNumberTextBox;
        private System.Windows.Forms.TextBox amountTextBox;
        private System.Windows.Forms.ComboBox operatorComboBox;
        private System.Windows.Forms.Button topUpButton;
        private System.Windows.Forms.Label phoneNumberLabel;
        private System.Windows.Forms.Label amountLabel;
        private System.Windows.Forms.Label languageLabel;
        private System.Windows.Forms.Label operatorLabel;
        private System.Windows.Forms.ComboBox languageComboBox;
        private System.Windows.Forms.TextBox cardNumberTextBox;
        private System.Windows.Forms.TextBox expiryDateTextBox;
        private System.Windows.Forms.TextBox cvvTextBox;
        private System.Windows.Forms.Label cardNumberLabel;
        private System.Windows.Forms.Label expiryDateLabel;
        private System.Windows.Forms.Label cvvLabel;
        private System.Windows.Forms.TextBox pinTextBox;
        private System.Windows.Forms.Label pinLabel;
        // Додано поля для введення відсотка благодійності
        private System.Windows.Forms.TextBox charityTextBox;
        // Додано мітку для поля благодійності
        private System.Windows.Forms.Label charityLabel;
        // Додано мітку для попередження про комісію
        private System.Windows.Forms.Label commissionLabel;

    }
}


