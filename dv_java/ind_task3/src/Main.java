import javax.swing.*;
import javax.swing.table.DefaultTableModel;
import java.awt.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.awt.event.MouseAdapter;
import java.awt.event.MouseEvent;
import java.io.*;
import java.util.Vector;

class AddressBookApp extends JFrame {

    private JTable contactTable;
    private DefaultTableModel tableModel;
    private JLabel statusLabel;
    private JTextField searchField;

    public AddressBookApp() {
        setTitle("Address Book");
        setSize(800, 600);
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        setLocationRelativeTo(null);

        setLayout(new BorderLayout());

        // Створення меню
        createMenu();

        // Створення панелі інструментів
        createToolbar();

        // Створення таблиці для відображення контактів
        createTable();

        // Створення рядка стану
        createStatusBar();

        // Додавання контекстного меню
        addContextMenu();

        setVisible(true);
    }

    private void createMenu() {
        JMenuBar menuBar = new JMenuBar();
        JMenu fileMenu = new JMenu("File");
        JMenuItem newItem = new JMenuItem("New");
        JMenuItem saveItem = new JMenuItem("Save");
        JMenuItem loadItem = new JMenuItem("Load");
        JMenuItem exitItem = new JMenuItem("Exit");

        fileMenu.add(newItem);
        fileMenu.add(saveItem);
        fileMenu.add(loadItem);
        fileMenu.addSeparator();
        fileMenu.add(exitItem);

        menuBar.add(fileMenu);
        setJMenuBar(menuBar);

        // Обробники подій
        newItem.addActionListener(e -> showCustomDialog());
        saveItem.addActionListener(e -> saveContactsToFile());
        loadItem.addActionListener(e -> loadContactsFromFile());
        exitItem.addActionListener(e -> System.exit(0));
    }

    private void createToolbar() {
        JToolBar toolBar = new JToolBar();
        JButton addButton = new JButton("Add Contact");
        JButton editButton = new JButton("Edit Contact");
        JButton deleteButton = new JButton("Delete Contact");

        // Поле для пошуку контактів
        searchField = new JTextField(15);
        JButton searchButton = new JButton("Search");

        toolBar.add(addButton);
        toolBar.add(editButton);
        toolBar.add(deleteButton);
        toolBar.add(new JLabel("Search:"));
        toolBar.add(searchField);
        toolBar.add(searchButton);

        add(toolBar, BorderLayout.NORTH);

        addButton.addActionListener(e -> showCustomDialog());
        editButton.addActionListener(e -> editContact());
        deleteButton.addActionListener(e -> deleteContact());
        searchButton.addActionListener(e -> searchContacts());
    }

    private void createTable() {
        String[] columnNames = {"Name", "Surname", "Phone", "Email"};
        tableModel = new DefaultTableModel(columnNames, 0);
        contactTable = new JTable(tableModel);
        JScrollPane scrollPane = new JScrollPane(contactTable);

        add(scrollPane, BorderLayout.CENTER);
    }

    private void createStatusBar() {
        statusLabel = new JLabel("Ready");
        add(statusLabel, BorderLayout.SOUTH);
    }

    private void showCustomDialog() {
        JDialog dialog = new JDialog(this, "Add New Contact", true);
        dialog.setSize(400, 300);
        dialog.setLayout(new GridBagLayout());
        GridBagConstraints gbc = new GridBagConstraints();
        gbc.insets = new Insets(5, 5, 5, 5);
        gbc.fill = GridBagConstraints.HORIZONTAL;

        // Поле для імені
        gbc.gridx = 0;
        gbc.gridy = 0;
        dialog.add(new JLabel("Name:"), gbc);
        gbc.gridx = 1;
        JTextField nameField = new JTextField(15);
        dialog.add(nameField, gbc);

        // Поле для прізвища
        gbc.gridx = 0;
        gbc.gridy = 1;
        dialog.add(new JLabel("Surname:"), gbc);
        gbc.gridx = 1;
        JTextField surnameField = new JTextField(15);
        dialog.add(surnameField, gbc);

        // Поле для телефону
        gbc.gridx = 0;
        gbc.gridy = 2;
        dialog.add(new JLabel("Phone:"), gbc);
        gbc.gridx = 1;
        JTextField phoneField = new JTextField(15);
        dialog.add(phoneField, gbc);

        // Поле для електронної пошти
        gbc.gridx = 0;
        gbc.gridy = 3;
        dialog.add(new JLabel("Email:"), gbc);
        gbc.gridx = 1;
        JTextField emailField = new JTextField(15);
        dialog.add(emailField, gbc);

        // Checkbox "Favorite"
        gbc.gridx = 0;
        gbc.gridy = 4;
        dialog.add(new JLabel("Favorite:"), gbc);
        gbc.gridx = 1;
        JCheckBox favoriteCheckBox = new JCheckBox();
        dialog.add(favoriteCheckBox, gbc);

        // Перемикач для статі
        gbc.gridx = 0;
        gbc.gridy = 5;
        dialog.add(new JLabel("Gender:"), gbc);
        gbc.gridx = 1;
        JPanel genderPanel = new JPanel(new FlowLayout(FlowLayout.LEFT, 0, 0));
        JRadioButton maleRadio = new JRadioButton("Male");
        JRadioButton femaleRadio = new JRadioButton("Female");
        ButtonGroup genderGroup = new ButtonGroup();
        genderGroup.add(maleRadio);
        genderGroup.add(femaleRadio);
        genderPanel.add(maleRadio);
        genderPanel.add(femaleRadio);
        dialog.add(genderPanel, gbc);

        // Випадаючий список "Category"
        gbc.gridx = 0;
        gbc.gridy = 6;
        dialog.add(new JLabel("Category:"), gbc);
        gbc.gridx = 1;
        JComboBox<String> categoryComboBox = new JComboBox<>(new String[]{"Friend", "Family", "Work", "Other"});
        dialog.add(categoryComboBox, gbc);

        // Кнопка збереження
        gbc.gridx = 0;
        gbc.gridy = 7;
        gbc.gridwidth = 2;
        gbc.anchor = GridBagConstraints.CENTER;
        JButton saveButton = new JButton("Save");
        saveButton.addActionListener(e -> {
            String name = nameField.getText();
            String surname = surnameField.getText();
            String phone = phoneField.getText();
            String email = emailField.getText();
            tableModel.addRow(new Object[]{name, surname, phone, email});
            dialog.dispose();
        });
        dialog.add(saveButton, gbc);
        // Центрування діалогу на екрані
        dialog.setLocationRelativeTo(this);

        dialog.setVisible(true);
    }


    private void addContextMenu() {
        JPopupMenu contextMenu = new JPopupMenu();
        JMenuItem addItem = new JMenuItem("Add Contact");
        JMenuItem editItem = new JMenuItem("Edit Contact");
        JMenuItem deleteItem = new JMenuItem("Delete Contact");

        contextMenu.add(addItem);
        contextMenu.add(editItem);
        contextMenu.add(deleteItem);

        addItem.addActionListener(e -> showCustomDialog());
        editItem.addActionListener(e -> editContact());
        deleteItem.addActionListener(e -> deleteContact());

        contactTable.addMouseListener(new MouseAdapter() {
            @Override
            public void mousePressed(MouseEvent e) {
                if (e.isPopupTrigger()) {
                    contextMenu.show(e.getComponent(), e.getX(), e.getY());
                }
            }

            @Override
            public void mouseReleased(MouseEvent e) {
                if (e.isPopupTrigger()) {
                    contextMenu.show(e.getComponent(), e.getX(), e.getY());
                }
            }
        });
    }

    private void saveContactsToFile() {
        try (PrintWriter writer = new PrintWriter(new FileWriter("contacts.txt"))) {
            for (int i = 0; i < tableModel.getRowCount(); i++) {
                writer.println(tableModel.getValueAt(i, 0) + "," +
                        tableModel.getValueAt(i, 1) + "," +
                        tableModel.getValueAt(i, 2) + "," +
                        tableModel.getValueAt(i, 3));
            }
            statusLabel.setText("Contacts saved successfully!");
        } catch (IOException e) {
            statusLabel.setText("Error saving contacts.");
        }
    }

    private void loadContactsFromFile() {
        try (BufferedReader reader = new BufferedReader(new FileReader("contacts.txt"))) {
            tableModel.setRowCount(0);
            String line;
            while ((line = reader.readLine()) != null) {
                String[] contact = line.split(",");
                tableModel.addRow(contact);
            }
            statusLabel.setText("Contacts loaded successfully!");
        } catch (IOException e) {
            statusLabel.setText("Error loading contacts.");
        }
    }

    private void editContact() {
        int selectedRow = contactTable.getSelectedRow();
        if (selectedRow != -1) {
            String name = (String) tableModel.getValueAt(selectedRow, 0);
            String surname = (String) tableModel.getValueAt(selectedRow, 1);
            String phone = (String) tableModel.getValueAt(selectedRow, 2);
            String email = (String) tableModel.getValueAt(selectedRow, 3);
            showEditDialog(name, surname, phone, email, selectedRow);
        } else {
            JOptionPane.showMessageDialog(this, "Please select a contact to edit.");
        }
    }

    private void deleteContact() {
        int selectedRow = contactTable.getSelectedRow();
        if (selectedRow != -1) {
            tableModel.removeRow(selectedRow);
        } else {
            JOptionPane.showMessageDialog(this, "Please select a contact to delete.");
        }
    }

    private void showEditDialog(String name, String surname, String phone, String email, int row) {
        JDialog dialog = new JDialog(this, "Edit Contact", true);
        dialog.setSize(400, 300);
        dialog.setLayout(new GridBagLayout());
        GridBagConstraints gbc = new GridBagConstraints();
        gbc.insets = new Insets(5, 5, 5, 5);
        gbc.fill = GridBagConstraints.HORIZONTAL;

        // Поле для імені
        gbc.gridx = 0;
        gbc.gridy = 0;
        dialog.add(new JLabel("Name:"), gbc);
        gbc.gridx = 1;
        JTextField nameField = new JTextField(name, 15);
        dialog.add(nameField, gbc);

        // Поле для прізвища
        gbc.gridx = 0;
        gbc.gridy = 1;
        dialog.add(new JLabel("Surname:"), gbc);
        gbc.gridx = 1;
        JTextField surnameField = new JTextField(surname, 15);
        dialog.add(surnameField, gbc);

        // Поле для телефону
        gbc.gridx = 0;
        gbc.gridy = 2;
        dialog.add(new JLabel("Phone:"), gbc);
        gbc.gridx = 1;
        JTextField phoneField = new JTextField(phone, 15);
        dialog.add(phoneField, gbc);

        // Поле для електронної пошти
        gbc.gridx = 0;
        gbc.gridy = 3;
        dialog.add(new JLabel("Email:"), gbc);
        gbc.gridx = 1;
        JTextField emailField = new JTextField(email, 15);
        dialog.add(emailField, gbc);

        // Checkbox "Favorite"
        gbc.gridx = 0;
        gbc.gridy = 4;
        dialog.add(new JLabel("Favorite:"), gbc);
        gbc.gridx = 1;
        JCheckBox favoriteCheckBox = new JCheckBox();
        dialog.add(favoriteCheckBox, gbc);

        // Перемикач для статі
        gbc.gridx = 0;
        gbc.gridy = 5;
        dialog.add(new JLabel("Gender:"), gbc);
        gbc.gridx = 1;
        JPanel genderPanel = new JPanel(new FlowLayout(FlowLayout.LEFT, 0, 0));
        JRadioButton maleRadio = new JRadioButton("Male");
        JRadioButton femaleRadio = new JRadioButton("Female");
        ButtonGroup genderGroup = new ButtonGroup();
        genderGroup.add(maleRadio);
        genderGroup.add(femaleRadio);
        genderPanel.add(maleRadio);
        genderPanel.add(femaleRadio);
        dialog.add(genderPanel, gbc);

        // Випадаючий список "Category"
        gbc.gridx = 0;
        gbc.gridy = 6;
        dialog.add(new JLabel("Category:"), gbc);
        gbc.gridx = 1;
        JComboBox<String> categoryComboBox = new JComboBox<>(new String[]{"Friend", "Family", "Work", "Other"});
        dialog.add(categoryComboBox, gbc);

        // Кнопка збереження
        gbc.gridx = 0;
        gbc.gridy = 7;
        gbc.gridwidth = 2;
        gbc.anchor = GridBagConstraints.CENTER;
        JButton saveButton = new JButton("Save");
        saveButton.addActionListener(e -> {
            tableModel.setValueAt(nameField.getText(), row, 0);
            tableModel.setValueAt(surnameField.getText(), row, 1);
            tableModel.setValueAt(phoneField.getText(), row, 2);
            tableModel.setValueAt(emailField.getText(), row, 3);
            dialog.dispose();
        });
        dialog.add(saveButton, gbc);
        // Центрування діалогу на екрані
        dialog.setLocationRelativeTo(this);

        dialog.setVisible(true);
    }


    private void searchContacts() {
        String searchTerm = searchField.getText().toLowerCase();
        if (searchTerm.isEmpty()) {
            JOptionPane.showMessageDialog(this, "Enter a name or surname to search.");
            return;
        }

        contactTable.clearSelection();
        boolean found = false;

        for (int i = 0; i < tableModel.getRowCount(); i++) {
            String name = ((String) tableModel.getValueAt(i, 0)).toLowerCase();
            String surname = ((String) tableModel.getValueAt(i, 1)).toLowerCase();
            if (name.contains(searchTerm) || surname.contains(searchTerm)) {
                contactTable.addRowSelectionInterval(i, i);
                found = true;
            }
        }

        if (found) {
            statusLabel.setText("Contacts found.");
        } else {
            statusLabel.setText("No contacts found.");
        }
    }



    public static void main(String[] args) {
        SwingUtilities.invokeLater(AddressBookApp::new);
    }
}
