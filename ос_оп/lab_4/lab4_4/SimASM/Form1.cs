using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Windows.Forms;
using ASMEngine;

namespace SimASM
{
    public partial class Form1 : Form
    {
        private string? sourceFilename;
        private string? binFilename;

        public Form1()
        {
            InitializeComponent();
        }

        private void Form1_Load(object sender, EventArgs e)
        {
            chkMakeCom.Checked = Settings.IfMakeCom;

            // Default folders
            var srcDir = Path.Combine(Application.StartupPath, "source");
            Directory.CreateDirectory(srcDir);
            openFileDialog1.InitialDirectory = srcDir;
            saveFileDialog1.InitialDirectory = srcDir;

            // Default workdir
            folderBrowserDialog1.SelectedPath = Path.Combine(Application.StartupPath, "bin");

            // Load example if exists
            var example = Path.Combine(srcDir, "try.asm");
            if (!File.Exists(example))
            {
                File.WriteAllText(example, ExamplePrograms.BasicExample(), System.Text.Encoding.ASCII);
            }
            LoadSource(example);
        }

        private void LoadSource(string filename)
        {
            sourceFilename = filename;
            txtSource.Text = File.ReadAllText(filename, System.Text.Encoding.ASCII);
            this.Text = "SimASM (Lab 4) - " + Path.GetFileName(filename);
            binFilename = null;
        }

        private void btnOpen_Click(object sender, EventArgs e)
        {
            if (openFileDialog1.ShowDialog() == DialogResult.OK)
            {
                LoadSource(openFileDialog1.FileName);
            }
        }

        private void btnSaveAsm_Click(object sender, EventArgs e)
        {
            if (sourceFilename == null)
            {
                if (saveFileDialog1.ShowDialog() == DialogResult.OK)
                {
                    sourceFilename = saveFileDialog1.FileName;
                }
                else return;
            }
            File.WriteAllText(sourceFilename!, txtSource.Text, System.Text.Encoding.ASCII);
            this.Text = "SimASM (Lab 4) - " + Path.GetFileName(sourceFilename);
        }

        private void chkMakeCom_CheckedChanged(object sender, EventArgs e)
        {
            Settings.IfMakeCom = chkMakeCom.Checked;
            binFilename = null;
        }

        private void btnWorkDir_Click(object sender, EventArgs e)
        {
            if (folderBrowserDialog1.ShowDialog() == DialogResult.OK)
            {
                Settings.WorkDir = folderBrowserDialog1.SelectedPath + Path.DirectorySeparatorChar;
                binFilename = null;
            }
        }

        private void btnCompile_Click(object sender, EventArgs e)
        {
            CompileInternal(saveBinary: false);
        }

        private void btnCompileSave_Click(object sender, EventArgs e)
        {
            CompileInternal(saveBinary: true);
        }

        private void txtSource_TextChanged(object sender, EventArgs e)
        {
            binFilename = null;
        }

        private void CompileInternal(bool saveBinary)
        {
            txtErrors.Clear();
            txtBinPreview.Clear();
            grid.Rows.Clear();

            try
            {
                // Save ASM optionally
                if (sourceFilename != null)
                {
                    File.WriteAllText(sourceFilename, txtSource.Text, System.Text.Encoding.ASCII);
                }

                var lines = txtSource.Lines.ToList();
                var asm = new ASMFile(lines)
                {
                    MakeComFile = Settings.IfMakeCom
                };

                var res = asm.OutCodes();

                foreach (var x in res)
                {
                    grid.Rows.Add(
                        x.LineNumber.ToString("0000"),
                        x.Address.ToString("X4"),
                        x.CodeHex,
                        x.Source
                    );
                }

                var bin = asm.GetBinary();

                // preview hex dump
                txtBinPreview.Text = HexDump.ToHexDump(bin, origin: 0x100);

                if (saveBinary)
                {
                    if (sourceFilename == null)
                    {
                        // ask where to save asm first
                        if (saveFileDialog1.ShowDialog() == DialogResult.OK)
                        {
                            sourceFilename = saveFileDialog1.FileName;
                            File.WriteAllText(sourceFilename, txtSource.Text, System.Text.Encoding.ASCII);
                        }
                        else return;
                    }

                    binFilename = Path.Combine(Settings.WorkDir, Path.GetFileNameWithoutExtension(sourceFilename) + (Settings.IfMakeCom ? ".com" : ".bin"));
                    Directory.CreateDirectory(Settings.WorkDir);
                    File.WriteAllBytes(binFilename, bin);

                    MessageBox.Show($"Saved: {binFilename}", "OK", MessageBoxButtons.OK, MessageBoxIcon.Information);
                }

                tabs.SelectedTab = tabTable;
            }
            catch (CompileError ce)
            {
                txtErrors.Text = $"Compile error!\nLine {ce.LineNumber:0000}: {ce.Message}";
                tabs.SelectedTab = tabErrors;
            }
            catch (Exception ex)
            {
                txtErrors.Text = "Unexpected error:\n" + ex;
                tabs.SelectedTab = tabErrors;
            }
        }
    }
}
