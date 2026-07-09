namespace SimASM
{
    partial class Form1
    {
        private System.ComponentModel.IContainer components = null;

        protected override void Dispose(bool disposing)
        {
            if (disposing && (components != null))
            {
                components.Dispose();
            }
            base.Dispose(disposing);
        }

        #region Windows Form Designer generated code

        private void InitializeComponent()
        {
            this.splitContainer1 = new System.Windows.Forms.SplitContainer();
            this.lblSource = new System.Windows.Forms.Label();
            this.txtSource = new System.Windows.Forms.RichTextBox();
            this.panelTop = new System.Windows.Forms.Panel();
            this.btnOpen = new System.Windows.Forms.Button();
            this.btnSaveAsm = new System.Windows.Forms.Button();
            this.btnCompile = new System.Windows.Forms.Button();
            this.btnCompileSave = new System.Windows.Forms.Button();
            this.chkMakeCom = new System.Windows.Forms.CheckBox();
            this.txtWorkDir = new System.Windows.Forms.TextBox();
            this.btnWorkDir = new System.Windows.Forms.Button();
            this.lblWorkDir = new System.Windows.Forms.Label();
            this.tabs = new System.Windows.Forms.TabControl();
            this.tabRun = new System.Windows.Forms.TabPage();
            this.lblBinPreview = new System.Windows.Forms.Label();
            this.txtBinPreview = new System.Windows.Forms.RichTextBox();
            this.tabErrors = new System.Windows.Forms.TabPage();
            this.txtErrors = new System.Windows.Forms.RichTextBox();
            this.tabTable = new System.Windows.Forms.TabPage();
            this.grid = new System.Windows.Forms.DataGridView();
            this.colLine = new System.Windows.Forms.DataGridViewTextBoxColumn();
            this.colAddr = new System.Windows.Forms.DataGridViewTextBoxColumn();
            this.colCode = new System.Windows.Forms.DataGridViewTextBoxColumn();
            this.colSource = new System.Windows.Forms.DataGridViewTextBoxColumn();
            this.openFileDialog1 = new System.Windows.Forms.OpenFileDialog();
            this.saveFileDialog1 = new System.Windows.Forms.SaveFileDialog();
            this.folderBrowserDialog1 = new System.Windows.Forms.FolderBrowserDialog();
            ((System.ComponentModel.ISupportInitialize)(this.splitContainer1)).BeginInit();
            this.splitContainer1.Panel1.SuspendLayout();
            this.splitContainer1.Panel2.SuspendLayout();
            this.splitContainer1.SuspendLayout();
            this.panelTop.SuspendLayout();
            this.tabs.SuspendLayout();
            this.tabRun.SuspendLayout();
            this.tabErrors.SuspendLayout();
            this.tabTable.SuspendLayout();
            ((System.ComponentModel.ISupportInitialize)(this.grid)).BeginInit();
            this.SuspendLayout();
            // 
            // splitContainer1
            // 
            this.splitContainer1.Dock = System.Windows.Forms.DockStyle.Fill;
            this.splitContainer1.Location = new System.Drawing.Point(0, 0);
            this.splitContainer1.Name = "splitContainer1";
            // 
            // splitContainer1.Panel1
            // 
            this.splitContainer1.Panel1.Controls.Add(this.txtSource);
            this.splitContainer1.Panel1.Controls.Add(this.lblSource);
            this.splitContainer1.Panel1.Controls.Add(this.panelTop);
            // 
            // splitContainer1.Panel2
            // 
            this.splitContainer1.Panel2.Controls.Add(this.tabs);
            this.splitContainer1.Size = new System.Drawing.Size(1200, 720);
            this.splitContainer1.SplitterDistance = 560;
            this.splitContainer1.TabIndex = 0;
            // 
            // lblSource
            // 
            this.lblSource.AutoSize = true;
            this.lblSource.Location = new System.Drawing.Point(10, 56);
            this.lblSource.Name = "lblSource";
            this.lblSource.Size = new System.Drawing.Size(97, 20);
            this.lblSource.TabIndex = 2;
            this.lblSource.Text = "ASM source:";
            // 
            // txtSource
            // 
            this.txtSource.Anchor = ((System.Windows.Forms.AnchorStyles)((((System.Windows.Forms.AnchorStyles.Top | System.Windows.Forms.AnchorStyles.Bottom)
            | System.Windows.Forms.AnchorStyles.Left)
            | System.Windows.Forms.AnchorStyles.Right)));
            this.txtSource.Font = new System.Drawing.Font("Consolas", 10F);
            this.txtSource.Location = new System.Drawing.Point(10, 80);
            this.txtSource.Name = "txtSource";
            this.txtSource.Size = new System.Drawing.Size(540, 630);
            this.txtSource.TabIndex = 1;
            this.txtSource.Text = "";
            this.txtSource.TextChanged += new System.EventHandler(this.txtSource_TextChanged);
            // 
            // panelTop
            // 
            this.panelTop.Controls.Add(this.btnOpen);
            this.panelTop.Controls.Add(this.btnSaveAsm);
            this.panelTop.Controls.Add(this.btnCompile);
            this.panelTop.Controls.Add(this.btnCompileSave);
            this.panelTop.Controls.Add(this.chkMakeCom);
            this.panelTop.Controls.Add(this.txtWorkDir);
            this.panelTop.Controls.Add(this.btnWorkDir);
            this.panelTop.Controls.Add(this.lblWorkDir);
            this.panelTop.Dock = System.Windows.Forms.DockStyle.Top;
            this.panelTop.Location = new System.Drawing.Point(0, 0);
            this.panelTop.Name = "panelTop";
            this.panelTop.Size = new System.Drawing.Size(560, 50);
            this.panelTop.TabIndex = 0;
            // 
            // btnOpen
            // 
            this.btnOpen.Location = new System.Drawing.Point(10, 10);
            this.btnOpen.Name = "btnOpen";
            this.btnOpen.Size = new System.Drawing.Size(80, 30);
            this.btnOpen.TabIndex = 0;
            this.btnOpen.Text = "Open";
            this.btnOpen.UseVisualStyleBackColor = true;
            this.btnOpen.Click += new System.EventHandler(this.btnOpen_Click);
            // 
            // btnSaveAsm
            // 
            this.btnSaveAsm.Location = new System.Drawing.Point(96, 10);
            this.btnSaveAsm.Name = "btnSaveAsm";
            this.btnSaveAsm.Size = new System.Drawing.Size(80, 30);
            this.btnSaveAsm.TabIndex = 1;
            this.btnSaveAsm.Text = "Save";
            this.btnSaveAsm.UseVisualStyleBackColor = true;
            this.btnSaveAsm.Click += new System.EventHandler(this.btnSaveAsm_Click);
            // 
            // btnCompile
            // 
            this.btnCompile.Location = new System.Drawing.Point(182, 10);
            this.btnCompile.Name = "btnCompile";
            this.btnCompile.Size = new System.Drawing.Size(90, 30);
            this.btnCompile.TabIndex = 2;
            this.btnCompile.Text = "Compile";
            this.btnCompile.UseVisualStyleBackColor = true;
            this.btnCompile.Click += new System.EventHandler(this.btnCompile_Click);
            // 
            // btnCompileSave
            // 
            this.btnCompileSave.Location = new System.Drawing.Point(278, 10);
            this.btnCompileSave.Name = "btnCompileSave";
            this.btnCompileSave.Size = new System.Drawing.Size(135, 30);
            this.btnCompileSave.TabIndex = 3;
            this.btnCompileSave.Text = "Compile && Save";
            this.btnCompileSave.UseVisualStyleBackColor = true;
            this.btnCompileSave.Click += new System.EventHandler(this.btnCompileSave_Click);
            // 
            // chkMakeCom
            // 
            this.chkMakeCom.AutoSize = true;
            this.chkMakeCom.Checked = true;
            this.chkMakeCom.CheckState = System.Windows.Forms.CheckState.Checked;
            this.chkMakeCom.Location = new System.Drawing.Point(420, 14);
            this.chkMakeCom.Name = "chkMakeCom";
            this.chkMakeCom.Size = new System.Drawing.Size(95, 24);
            this.chkMakeCom.TabIndex = 4;
            this.chkMakeCom.Text = "Make .COM";
            this.chkMakeCom.UseVisualStyleBackColor = true;
            this.chkMakeCom.CheckedChanged += new System.EventHandler(this.chkMakeCom_CheckedChanged);
            // 
            // lblWorkDir
            // 
            this.lblWorkDir.AutoSize = true;
            this.lblWorkDir.Location = new System.Drawing.Point(520, 0);
            this.lblWorkDir.Name = "lblWorkDir";
            this.lblWorkDir.Size = new System.Drawing.Size(0, 20);
            this.lblWorkDir.TabIndex = 7;
            // 
            // txtWorkDir
            // 
            this.txtWorkDir.Anchor = ((System.Windows.Forms.AnchorStyles)(((System.Windows.Forms.AnchorStyles.Top | System.Windows.Forms.AnchorStyles.Left)
            | System.Windows.Forms.AnchorStyles.Right)));
            this.txtWorkDir.Location = new System.Drawing.Point(520, 12);
            this.txtWorkDir.Name = "txtWorkDir";
            this.txtWorkDir.ReadOnly = true;
            this.txtWorkDir.Size = new System.Drawing.Size(0, 27);
            this.txtWorkDir.TabIndex = 6;
            // 
            // btnWorkDir
            // 
            this.btnWorkDir.Location = new System.Drawing.Point(520, 10);
            this.btnWorkDir.Name = "btnWorkDir";
            this.btnWorkDir.Size = new System.Drawing.Size(0, 30);
            this.btnWorkDir.TabIndex = 5;
            this.btnWorkDir.Text = "Set";
            this.btnWorkDir.UseVisualStyleBackColor = true;
            this.btnWorkDir.Click += new System.EventHandler(this.btnWorkDir_Click);
            // 
            // tabs
            // 
            this.tabs.Controls.Add(this.tabTable);
            this.tabs.Controls.Add(this.tabErrors);
            this.tabs.Controls.Add(this.tabRun);
            this.tabs.Dock = System.Windows.Forms.DockStyle.Fill;
            this.tabs.Location = new System.Drawing.Point(0, 0);
            this.tabs.Name = "tabs";
            this.tabs.SelectedIndex = 0;
            this.tabs.Size = new System.Drawing.Size(636, 720);
            this.tabs.TabIndex = 0;
            // 
            // tabRun
            // 
            this.tabRun.Controls.Add(this.txtBinPreview);
            this.tabRun.Controls.Add(this.lblBinPreview);
            this.tabRun.Location = new System.Drawing.Point(4, 29);
            this.tabRun.Name = "tabRun";
            this.tabRun.Padding = new System.Windows.Forms.Padding(10);
            this.tabRun.Size = new System.Drawing.Size(628, 687);
            this.tabRun.TabIndex = 2;
            this.tabRun.Text = "Binary";
            this.tabRun.UseVisualStyleBackColor = true;
            // 
            // lblBinPreview
            // 
            this.lblBinPreview.AutoSize = true;
            this.lblBinPreview.Location = new System.Drawing.Point(13, 13);
            this.lblBinPreview.Name = "lblBinPreview";
            this.lblBinPreview.Size = new System.Drawing.Size(164, 20);
            this.lblBinPreview.TabIndex = 0;
            this.lblBinPreview.Text = "Binary preview (hex):";
            // 
            // txtBinPreview
            // 
            this.txtBinPreview.Anchor = ((System.Windows.Forms.AnchorStyles)((((System.Windows.Forms.AnchorStyles.Top | System.Windows.Forms.AnchorStyles.Bottom)
            | System.Windows.Forms.AnchorStyles.Left)
            | System.Windows.Forms.AnchorStyles.Right)));
            this.txtBinPreview.Font = new System.Drawing.Font("Consolas", 10F);
            this.txtBinPreview.Location = new System.Drawing.Point(13, 36);
            this.txtBinPreview.Name = "txtBinPreview";
            this.txtBinPreview.ReadOnly = true;
            this.txtBinPreview.Size = new System.Drawing.Size(602, 638);
            this.txtBinPreview.TabIndex = 1;
            this.txtBinPreview.Text = "";
            // 
            // tabErrors
            // 
            this.tabErrors.Controls.Add(this.txtErrors);
            this.tabErrors.Location = new System.Drawing.Point(4, 29);
            this.tabErrors.Name = "tabErrors";
            this.tabErrors.Padding = new System.Windows.Forms.Padding(10);
            this.tabErrors.Size = new System.Drawing.Size(628, 687);
            this.tabErrors.TabIndex = 1;
            this.tabErrors.Text = "Errors";
            this.tabErrors.UseVisualStyleBackColor = true;
            // 
            // txtErrors
            // 
            this.txtErrors.Dock = System.Windows.Forms.DockStyle.Fill;
            this.txtErrors.Font = new System.Drawing.Font("Consolas", 10F);
            this.txtErrors.Location = new System.Drawing.Point(10, 10);
            this.txtErrors.Name = "txtErrors";
            this.txtErrors.ReadOnly = true;
            this.txtErrors.Size = new System.Drawing.Size(608, 667);
            this.txtErrors.TabIndex = 0;
            this.txtErrors.Text = "";
            // 
            // tabTable
            // 
            this.tabTable.Controls.Add(this.grid);
            this.tabTable.Location = new System.Drawing.Point(4, 29);
            this.tabTable.Name = "tabTable";
            this.tabTable.Padding = new System.Windows.Forms.Padding(10);
            this.tabTable.Size = new System.Drawing.Size(628, 687);
            this.tabTable.TabIndex = 0;
            this.tabTable.Text = "Compilation table";
            this.tabTable.UseVisualStyleBackColor = true;
            // 
            // grid
            // 
            this.grid.AllowUserToAddRows = false;
            this.grid.AllowUserToDeleteRows = false;
            this.grid.AutoSizeColumnsMode = System.Windows.Forms.DataGridViewAutoSizeColumnsMode.Fill;
            this.grid.ColumnHeadersHeightSizeMode = System.Windows.Forms.DataGridViewColumnHeadersHeightSizeMode.AutoSize;
            this.grid.Columns.AddRange(new System.Windows.Forms.DataGridViewColumn[] {
            this.colLine,
            this.colAddr,
            this.colCode,
            this.colSource});
            this.grid.Dock = System.Windows.Forms.DockStyle.Fill;
            this.grid.Location = new System.Drawing.Point(10, 10);
            this.grid.Name = "grid";
            this.grid.ReadOnly = true;
            this.grid.RowHeadersVisible = false;
            this.grid.RowTemplate.Height = 29;
            this.grid.Size = new System.Drawing.Size(608, 667);
            this.grid.TabIndex = 0;
            // 
            // colLine
            // 
            this.colLine.FillWeight = 12F;
            this.colLine.HeaderText = "Line";
            this.colLine.MinimumWidth = 6;
            this.colLine.Name = "colLine";
            this.colLine.ReadOnly = true;
            // 
            // colAddr
            // 
            this.colAddr.FillWeight = 18F;
            this.colAddr.HeaderText = "Addr";
            this.colAddr.MinimumWidth = 6;
            this.colAddr.Name = "colAddr";
            this.colAddr.ReadOnly = true;
            // 
            // colCode
            // 
            this.colCode.FillWeight = 25F;
            this.colCode.HeaderText = "Code";
            this.colCode.MinimumWidth = 6;
            this.colCode.Name = "colCode";
            this.colCode.ReadOnly = true;
            // 
            // colSource
            // 
            this.colSource.FillWeight = 45F;
            this.colSource.HeaderText = "Source";
            this.colSource.MinimumWidth = 6;
            this.colSource.Name = "colSource";
            this.colSource.ReadOnly = true;
            // 
            // openFileDialog1
            // 
            this.openFileDialog1.Filter = "ASM files (*.asm)|*.asm|All files (*.*)|*.*";
            // 
            // saveFileDialog1
            // 
            this.saveFileDialog1.Filter = "ASM files (*.asm)|*.asm|All files (*.*)|*.*";
            // 
            // Form1
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(8F, 20F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.ClientSize = new System.Drawing.Size(1200, 720);
            this.Controls.Add(this.splitContainer1);
            this.Name = "Form1";
            this.Text = "SimASM (Lab 4)";
            this.Load += new System.EventHandler(this.Form1_Load);
            this.splitContainer1.Panel1.ResumeLayout(false);
            this.splitContainer1.Panel1.PerformLayout();
            this.splitContainer1.Panel2.ResumeLayout(false);
            ((System.ComponentModel.ISupportInitialize)(this.splitContainer1)).EndInit();
            this.splitContainer1.ResumeLayout(false);
            this.panelTop.ResumeLayout(false);
            this.panelTop.PerformLayout();
            this.tabs.ResumeLayout(false);
            this.tabRun.ResumeLayout(false);
            this.tabRun.PerformLayout();
            this.tabErrors.ResumeLayout(false);
            this.tabTable.ResumeLayout(false);
            ((System.ComponentModel.ISupportInitialize)(this.grid)).EndInit();
            this.ResumeLayout(false);

        }

        #endregion

        private System.Windows.Forms.SplitContainer splitContainer1;
        private System.Windows.Forms.Panel panelTop;
        private System.Windows.Forms.Button btnOpen;
        private System.Windows.Forms.Button btnSaveAsm;
        private System.Windows.Forms.Button btnCompile;
        private System.Windows.Forms.Button btnCompileSave;
        private System.Windows.Forms.CheckBox chkMakeCom;
        private System.Windows.Forms.TextBox txtWorkDir;
        private System.Windows.Forms.Button btnWorkDir;
        private System.Windows.Forms.Label lblWorkDir;
        private System.Windows.Forms.Label lblSource;
        private System.Windows.Forms.RichTextBox txtSource;
        private System.Windows.Forms.TabControl tabs;
        private System.Windows.Forms.TabPage tabTable;
        private System.Windows.Forms.TabPage tabErrors;
        private System.Windows.Forms.TabPage tabRun;
        private System.Windows.Forms.DataGridView grid;
        private System.Windows.Forms.DataGridViewTextBoxColumn colLine;
        private System.Windows.Forms.DataGridViewTextBoxColumn colAddr;
        private System.Windows.Forms.DataGridViewTextBoxColumn colCode;
        private System.Windows.Forms.DataGridViewTextBoxColumn colSource;
        private System.Windows.Forms.RichTextBox txtErrors;
        private System.Windows.Forms.Label lblBinPreview;
        private System.Windows.Forms.RichTextBox txtBinPreview;
        private System.Windows.Forms.OpenFileDialog openFileDialog1;
        private System.Windows.Forms.SaveFileDialog saveFileDialog1;
        private System.Windows.Forms.FolderBrowserDialog folderBrowserDialog1;
    }
}
