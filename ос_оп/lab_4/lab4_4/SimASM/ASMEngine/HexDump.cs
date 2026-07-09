using System;
using System.Text;

namespace ASMEngine
{
    public static class HexDump
    {
        public static string ToHex(byte[] bytes)
        {
            if (bytes.Length == 0) return "";
            var sb = new StringBuilder(bytes.Length * 3);
            for (int i = 0; i < bytes.Length; i++)
            {
                if (i != 0) sb.Append(' ');
                sb.Append(bytes[i].ToString("X2"));
            }
            return sb.ToString();
        }

        public static string ToHexDump(byte[] bytes, int origin = 0x100, int bytesPerLine = 16)
        {
            var sb = new StringBuilder();
            for (int i = 0; i < bytes.Length; i += bytesPerLine)
            {
                sb.Append((origin + i).ToString("X4"));
                sb.Append(": ");
                int end = Math.Min(bytes.Length, i + bytesPerLine);
                for (int j = i; j < end; j++)
                {
                    sb.Append(bytes[j].ToString("X2"));
                    sb.Append(' ');
                }
                sb.AppendLine();
            }
            return sb.ToString();
        }
    }
}
