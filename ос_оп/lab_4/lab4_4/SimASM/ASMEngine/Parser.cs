using System;
using System.Collections.Generic;
using System.Linq;
using System.Text.RegularExpressions;

namespace ASMEngine
{
    public record ParsedLine(string Original, string? Label, string? Opcode, List<string> Operands);

    public static class Parser
    {
        private static readonly HashSet<string> KnownMnemonics = new(StringComparer.OrdinalIgnoreCase)
        {
            "ORG","DB","DW","END",
            "MOV","ADD","SUB","CMP","INC","DEC","JMP","JE","JZ","JNE","JNZ","INT","NOP","RET"
        };

        public static ParsedLine Parse(string line)
        {
            var original = line;

            var semi = line.IndexOf(';');
            if (semi >= 0) line = line.Substring(0, semi);

            line = line.Trim();
            if (string.IsNullOrWhiteSpace(line))
                return new ParsedLine(original, null, null, new List<string>());

            string? label = null;

            var m = Regex.Match(line, @"^\s*([A-Za-z_][A-Za-z0-9_]*)\s*:\s*(.*)$");
            if (m.Success)
            {
                label = m.Groups[1].Value;
                line = m.Groups[2].Value.Trim();
            }

            if (string.IsNullOrWhiteSpace(line))
                return new ParsedLine(original, label, null, new List<string>());

            var firstSplit = SplitFirstToken(line);
            string first = firstSplit.token;
            string restAfterFirst = firstSplit.rest;

            if (label == null && !KnownMnemonics.Contains(first))
            {
                var secondSplit = SplitFirstToken(restAfterFirst.TrimStart());
                if (!string.IsNullOrWhiteSpace(secondSplit.token) && KnownMnemonics.Contains(secondSplit.token))
                {
                    label = first;
                    first = secondSplit.token;
                    restAfterFirst = secondSplit.rest;
                }
            }

            var opcode = first.ToUpperInvariant();
            var ops = new List<string>();

            if (!string.IsNullOrWhiteSpace(restAfterFirst))
                ops = SplitOperands(restAfterFirst.Trim());

            return new ParsedLine(original, label, opcode, ops);
        }

        private static (string token, string rest) SplitFirstToken(string s)
        {
            s = s ?? "";
            int i = 0;
            while (i < s.Length && char.IsWhiteSpace(s[i])) i++;
            int start = i;
            while (i < s.Length && !char.IsWhiteSpace(s[i])) i++;
            string token = s.Substring(start, i - start);
            string rest = i < s.Length ? s.Substring(i).TrimStart() : "";
            return (token, rest);
        }

        private static List<string> SplitOperands(string s)
        {
            var ops = new List<string>();
            int i = 0;
            while (i < s.Length)
            {
                while (i < s.Length && char.IsWhiteSpace(s[i])) i++;
                if (i >= s.Length) break;

                if (s[i] == '"')
                {
                    int j = i + 1;
                    while (j < s.Length && s[j] != '"') j++;
                    if (j >= s.Length) throw new Exception("Unterminated string literal");
                    ops.Add(s.Substring(i, j - i + 1).Trim());
                    i = j + 1;
                }
                else
                {
                    int j = i;
                    int bracket = 0;
                    while (j < s.Length)
                    {
                        if (s[j] == '[') bracket++;
                        if (s[j] == ']') bracket--;
                        if (bracket == 0 && s[j] == ',') break;
                        j++;
                    }
                    ops.Add(s.Substring(i, j - i).Trim());
                    i = j;
                }

                while (i < s.Length && (s[i] == ',' || char.IsWhiteSpace(s[i]))) i++;
            }
            return ops.Where(x => x.Length > 0).ToList();
        }
    }
}
