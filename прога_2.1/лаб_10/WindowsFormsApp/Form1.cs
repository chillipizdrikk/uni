using System;
using System.Collections.Generic;
using System.Globalization;
using System.IO;
using System.Linq;
using System.Threading;
using System.Windows.Forms;
using Newtonsoft.Json;
using System.Xml.Serialization;

namespace MobileTopUpTerminal
{
    public partial class Form1 : Form
    {
        private Dictionary<string, List<string>> operators = new Dictionary<string, List<string>>();
        private Dictionary<string, string> languageDict = new Dictionary<string, string>
        {
            { "English", "en-US" },
            { "Українська", "uk-UA" }
        };

        public Form1()
        {
            InitializeComponent();
            LoadOperators();
            LoadLanguages();
        }

        private void LoadLanguages()
        {
            foreach (var language in languageDict.Keys)
            {
                languageComboBox.Items.Add(language);
            }
            languageComboBox.SelectedIndex = 0; // Set English as default language
        }

        private void ChangeLanguage(string culture)
        {
            Thread.CurrentThread.CurrentUICulture = new CultureInfo(culture);

            if (culture == "uk-UA")
            {
                languageLabel.Text = "Оберіть мову:";
                phoneNumberLabel.Text = "Номер телефону:";
                amountLabel.Text = "Сума поповнення:";
                operatorLabel.Text = "Оператор:";
                cardNumberLabel.Text = "Номер картки:";
                expiryDateLabel.Text = "Термін дії:";
                cvvLabel.Text = "CVV код:";
                pinLabel.Text = "PIN код:";
                topUpButton.Text = "Поповнити";
                charityLabel.Text = "Відсоток благодійності:";
                commissionLabel.Text = "Комісія банку: 3%";
            }
            else
            {
                languageLabel.Text = "Choose language:";
                phoneNumberLabel.Text = "Phone Number:";
                amountLabel.Text = "Amount:";
                operatorLabel.Text = "Operator:";
                cardNumberLabel.Text = "Card Number:";
                expiryDateLabel.Text = "Expiry Date:";
                cvvLabel.Text = "CVV Code:";
                pinLabel.Text = "PIN Code:";
                topUpButton.Text = "Top Up";
                charityLabel.Text = "Charity percentage:";
                commissionLabel.Text = "Bank comission: 3%";
            }
        }

        private void LoadOperators()
        {
            string[] lines = File.ReadAllLines("operators.txt");
            foreach (var line in lines)
            {
                var parts = line.Split(':');
                if (parts.Length == 2)
                {
                    var operatorName = parts[0].Trim();
                    var codes = parts[1].Split(',').Select(c => c.Trim()).ToList();
                    operators[operatorName] = codes;
                    operatorComboBox.Items.Add(operatorName);
                }
            }
        }

        private bool ValidatePhoneNumber(string phoneNumber, string operatorName)
        {
            if (phoneNumber.Length != 10 || !phoneNumber.All(char.IsDigit))
            {
                return false;
            }

            var prefix = phoneNumber.Substring(0, 3);
            if (!operators.ContainsKey(operatorName) || !operators[operatorName].Contains(prefix))
            {
                return false;
            }

            return true;
        }

        private bool ValidateCardInfo(string cardNumber, string expiryDate, string cvv)
        {
            if (cardNumber.Length != 16 || !cardNumber.All(char.IsDigit))
            {
                return false;
            }

            if (!DateTime.TryParseExact(expiryDate, "MM/yy", CultureInfo.InvariantCulture, DateTimeStyles.None, out DateTime parsedDate))
            {
                return false;
            }

            if (parsedDate < DateTime.Now)
            {
                return false;
            }

            if (cvv.Length != 3 || !cvv.All(char.IsDigit))
            {
                return false;
            }

            return true;
        }

        private bool ValidatePin(string pin)
        {
            if (pin.Length != 4 || !pin.All(char.IsDigit))
            {
                return false;
            }

            return true;
        }

        private List<UserCard> LoadUserCards(string bankName)
        {
            string filePath = Path.Combine(Application.StartupPath, $"{bankName}.json");

            if (File.Exists(filePath))
            {
                var json = File.ReadAllText(filePath);
                return JsonConvert.DeserializeObject<List<UserCard>>(json);
            }
            return new List<UserCard>();
        }

        private void UpdateUserCards(List<UserCard> userCards, string bankName)
        {
            string filePath = Path.Combine(Application.StartupPath, $"{bankName}.json");

            try
            {
                var json = JsonConvert.SerializeObject(userCards, Formatting.Indented);
                File.WriteAllText(filePath, json);
            }
            catch (Exception ex)
            {
                MessageBox.Show($"An error occurred while updating user cards: {ex.Message}");
            }
        }

        private void UpdateBalance(string cardNumber, double amount)
        {
            string bankName = operatorComboBox.SelectedItem?.ToString(); // Get the selected operator name
            var userCards = LoadUserCards(bankName);
            var card = userCards.FirstOrDefault(c => c.CardNumber == cardNumber);
            if (card != null)
            {
                card.Balance += amount;
                UpdateUserCards(userCards, bankName); // Pass the bank name to the method
                PrintReceipt(phoneNumberTextBox.Text, operatorComboBox.SelectedItem?.ToString(), amount, cardNumberTextBox.Text, cvvTextBox.Text);
                MessageBox.Show("Top-up successful!");
            }
            else
            {
                MessageBox.Show("Card not found!");
            }
        }

        private void PrintReceipt(string phoneNumber, string operatorName, double amount, string cardNumber, string cvv)
        {
            DialogResult result = MessageBox.Show("Would you like to print the receipt?", "Print Receipt", MessageBoxButtons.YesNo);
            if (result == DialogResult.Yes)
            {
                string maskedCardNumber = MaskCardNumber(cardNumber);
                string maskedCVV = MaskCVV(cvv);
                Receipt receipt = new Receipt
                {
                    PhoneNumber = phoneNumber,
                    Operator = operatorName,
                    Amount = amount,
                    Date = DateTime.Now,
                    MaskedCardNumber = maskedCardNumber,
                    MaskedCVV = maskedCVV
                };

                // Write receipt to XML file
                string receiptFilePath = Path.Combine(Application.StartupPath, "receipt.xml");
                XmlSerializer serializer = new XmlSerializer(typeof(Receipt));
                using (TextWriter writer = new StreamWriter(receiptFilePath))
                {
                    serializer.Serialize(writer, receipt);
                }

                MessageBox.Show("Receipt printed successfully!");
            }
        }

        private string MaskCardNumber(string cardNumber)
        {
            if (cardNumber.Length < 4)
                return cardNumber;

            string masked = new string('*', cardNumber.Length - 4) + cardNumber.Substring(cardNumber.Length - 4);
            return masked;
        }

        private string MaskCVV(string cvv)
        {
            return new string('*', cvv.Length);
        }

        private void topUpButton_Click(object sender, EventArgs e)
        {
            string phoneNumber = phoneNumberTextBox.Text;
            string operatorName = operatorComboBox.SelectedItem?.ToString();
            double amount;
            if (!double.TryParse(amountTextBox.Text, out amount))
            {
                MessageBox.Show("Invalid amount!");
                return;
            }
            double charityPercentage;
            if (!double.TryParse(charityTextBox.Text, out charityPercentage))
            {
                MessageBox.Show("Invalid charity percentage!");
                return;
            }

            double commission = amount * 0.03; // Assuming bank commission is 3%

            string cardNumber = cardNumberTextBox.Text;
            string expiryDate = expiryDateTextBox.Text;
            string cvv = cvvTextBox.Text;
            string pin = pinTextBox.Text;

            if (operatorName == null)
            {
                MessageBox.Show("Please select an operator.");
                return;
            }

            if (!ValidatePhoneNumber(phoneNumber, operatorName))
            {
                MessageBox.Show("Invalid phone number for selected operator!");
                return;
            }

            if (!ValidateCardInfo(cardNumber, expiryDate, cvv))
            {
                MessageBox.Show("Invalid card information!");
                return;
            }

            if (!ValidatePin(pin))
            {
                MessageBox.Show("Invalid PIN!");
                return;
            }

            double donationAmount = amount * (charityPercentage / 100);
            double totalAmount = amount + commission;

            UpdateBalance(phoneNumber, totalAmount - donationAmount);
        }

        private void languageComboBox_SelectedIndexChanged(object sender, EventArgs e)
        {
            string selectedLanguage = languageComboBox.SelectedItem.ToString();
            if (languageDict.ContainsKey(selectedLanguage))
            {
                string culture = languageDict[selectedLanguage];
                ChangeLanguage(culture);
            }
        }
    }

    public class UserCard
    {
        public string CardNumber { get; set; }
        public double Balance { get; set; }
        public string ExpiryDate { get; set; } // Add ExpiryDate property
        public string CVV { get; set; } // Add CVV property
        public string PIN { get; set; } // Add PIN property
    }

    public class Receipt
    {
        public string PhoneNumber { get; set; }
        public string Operator { get; set; }
        public double Amount { get; set; }
        public DateTime Date { get; set; }
        public string MaskedCardNumber { get; set; }
        public string MaskedCVV { get; set; }
    }
}

