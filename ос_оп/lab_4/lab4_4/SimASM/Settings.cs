using System.IO;
using System.Windows.Forms;

namespace SimASM
{
    public static class Settings
    {
        public static bool IfMakeCom = true;
        public static string WorkDir = InitDir();

        private static string InitDir()
        {
            var dir = Path.Combine(Application.StartupPath, "bin");
            Directory.CreateDirectory(dir);
            return dir + Path.DirectorySeparatorChar;
        }
    }
}
