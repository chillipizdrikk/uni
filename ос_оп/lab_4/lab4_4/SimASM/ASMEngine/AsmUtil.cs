using System;
using System.Collections.Generic;
using System.Globalization;
using System.Text.RegularExpressions;

namespace ASMEngine
{
    public static class AsmUtil
    {
        public static readonly Dictionary<string, int> Reg16 = new(StringComparer.OrdinalIgnoreCase)
        {
            ["AX"]=0, ["CX"]=1, ["DX"]=2, ["BX"]=3, ["SP"]=4, ["BP"]=5, ["SI"]=6, ["DI"]=7
        };

        public static readonly Dictionary<string, int> Reg8 = new(StringComparer.OrdinalIgnoreCase)
        {
            ["AL"]=0, ["CL"]=1, ["DL"]=2, ["BL"]=3, ["AH"]=4, ["CH"]=5, ["DH"]=6, ["BH"]=7
        };

        public static bool IsReg16(string s) => Reg16.ContainsKey(s);
        public static bool IsReg8(string s) => Reg8.ContainsKey(s);
        public static bool IsRegister(string s) => IsReg16(s) || IsReg8(s);

        public static ushort ParseNumberWord(string token)
        {
            token = token.Trim();
            // allow trailing 'h' hex
            if (token.EndsWith("H", StringComparison.OrdinalIgnoreCase))
            {
                var hex = token.Substring(0, token.Length - 1);
                return ushort.Parse(hex, NumberStyles.HexNumber, CultureInfo.InvariantCulture);
            }
            if (token.StartsWith("0x", StringComparison.OrdinalIgnoreCase))
            {
                return ushort.Parse(token.Substring(2), NumberStyles.HexNumber, CultureInfo.InvariantCulture);
            }
            if (token.StartsWith("'") && token.EndsWith("'") && token.Length == 3)
            {
                return (ushort)(byte)token[1];
            }
            // decimal
            return ushort.Parse(token, CultureInfo.InvariantCulture);
        }

        public static byte ParseNumberByte(string token)
        {
            var w = ParseNumberWord(token);
            if (w > 255) throw new Exception("Byte constant out of range");
            return (byte)w;
        }

        public static bool IsStringLiteral(string token) =>
            token.Length >= 2 && token.StartsWith("\"") && token.EndsWith("\"");

        public static string Unquote(string token) => token.Substring(1, token.Length - 2);

        public static bool LooksLikeMemory(string op) =>
            op.Contains("[") && op.Contains("]");

        public static string StripPtr(string op)
        {
            // allow "word ptr ..." or "byte ptr ..."
            op = Regex.Replace(op, @"\b(BYTE|WORD)\s+PTR\b", "", RegexOptions.IgnoreCase).Trim();
            return op;
        }
    }
}
