using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;

namespace ASMEngine
{
    public class ASMFile
    {
        private readonly List<string> _lines;

        public bool MakeComFile { get; set; } = true;

        private readonly Dictionary<string, ushort> _symtab = new(StringComparer.OrdinalIgnoreCase);
        private readonly List<Fixup> _fixups = new();
        private readonly List<Line> _outLines = new();
        private readonly List<byte> _output = new();

        private ushort _loc = 0x100;
        private ushort _origin = 0x100;

        public ASMFile(List<string> lines)
        {
            _lines = lines;
        }

        public List<Line> OutCodes()
        {
            Pass1();
            Pass2();
            return _outLines;
        }

        public byte[] GetBinary() => _output.ToArray();

        private void Pass1()
        {
            _symtab.Clear();
            _fixups.Clear();
            _outLines.Clear();
            _output.Clear();
            _loc = 0x100;
            _origin = 0x100;

            for (int i = 0; i < _lines.Count; i++)
            {
                int lineNo = i;
                var parsed = Parser.Parse(_lines[i]);
                if (parsed.Label != null)
                {
                    if (_symtab.ContainsKey(parsed.Label))
                        throw new CompileError(lineNo, $"Duplicate label: {parsed.Label}");
                    _symtab[parsed.Label] = _loc;
                }

                if (parsed.Opcode == null)
                {
                    // empty or label-only
                    continue;
                }

                var op = parsed.Opcode.ToUpperInvariant();

                if (op == "ORG")
                {
                    if (parsed.Operands.Count != 1) throw new CompileError(lineNo, "ORG expects 1 operand");
                    _origin = AsmUtil.ParseNumberWord(parsed.Operands[0]);
                    _loc = _origin;
                    continue;
                }

                if (op == "END")
                {
                    // stop processing
                    break;
                }

                if (op == "DB" || op == "DW")
                {
                    var data = EncodeData(lineNo, op, parsed.Operands);
                    EmitLine(lineNo, _loc, _lines[i], data);
                    _loc += (ushort)data.Length;
                    continue;
                }

                // instruction
                var encoder = new Encoder8086(_symtab, _fixups);
                var enc = encoder.Encode(lineNo, _loc, op, parsed.Operands);

                // patch fixup output offsets (now we know where bytes land in output)
                int startOffset = _output.Count;
                foreach (var fx in enc.Fixups)
                {
                    fx.OutputOffset = startOffset + FindFixupOffsetInside(enc.Bytes, fx.Kind);
                    fx.InstrAddress = _loc;
                    fx.InstrLength = enc.Bytes.Length;
                    _fixups.Add(fx);
                }

                EmitLine(lineNo, _loc, _lines[i], enc.Bytes);
                _loc += (ushort)enc.Bytes.Length;
            }
        }

        private int FindFixupOffsetInside(byte[] bytes, FixupKind kind)
        {
            // For our encoding, fixups are always the last byte(s) for rel/abs we wrote as 00.
            // rel8: last 1 byte
            // rel16/abs16: last 2 bytes
            return kind switch
            {
                FixupKind.Rel8 => bytes.Length - 1,
                FixupKind.Rel16 => bytes.Length - 2,
                FixupKind.Abs16 => bytes.Length - 2,
                _ => bytes.Length - 2
            };
        }

        private void EmitLine(int lineNo, ushort addr, string src, byte[] bytes)
        {
            _outLines.Add(new Line
            {
                LineNumber = lineNo,
                Address = addr,
                Source = src,
                Code = bytes
            });
            _output.AddRange(bytes);
        }

        private byte[] EncodeData(int lineNo, string directive, List<string> operands)
        {
            if (operands.Count == 0) return Array.Empty<byte>();

            var bytes = new List<byte>();
            bool isWord = directive.Equals("DW", StringComparison.OrdinalIgnoreCase);

            foreach (var op in operands)
            {
                var t = op.Trim();
                if (AsmUtil.IsStringLiteral(t))
                {
                    var s = AsmUtil.Unquote(t);
                    bytes.AddRange(Encoding.ASCII.GetBytes(s));
                }
                else
                {
                    if (isWord)
                    {
                        ushort w = AsmUtil.ParseNumberWord(t);
                        bytes.Add((byte)(w & 0xFF));
                        bytes.Add((byte)(w >> 8));
                    }
                    else
                    {
                        byte b = AsmUtil.ParseNumberByte(t);
                        bytes.Add(b);
                    }
                }
            }

            return bytes.ToArray();
        }

        private void Pass2()
        {
            foreach (var fx in _fixups)
            {
                if (!_symtab.TryGetValue(fx.Symbol, out var target))
                    throw new CompileError(fx.LineNumber, $"Undefined symbol: {fx.Symbol}");

                if (fx.Kind == FixupKind.Abs16)
                {
                    PatchWord(fx.OutputOffset, target);
                }
                else if (fx.Kind == FixupKind.Rel8)
                {
                    // rel = target - (ip_after)
                    int ipAfter = fx.InstrAddress + fx.InstrLength;
                    int rel = target - ipAfter;
                    if (rel < -128 || rel > 127)
                        throw new CompileError(fx.LineNumber, $"Short jump out of range to {fx.Symbol} (rel={rel})");
                    _output[fx.OutputOffset] = (byte)(rel & 0xFF);
                }
                else if (fx.Kind == FixupKind.Rel16)
                {
                    int ipAfter = fx.InstrAddress + fx.InstrLength;
                    int rel = target - ipAfter;
                    PatchWord(fx.OutputOffset, (ushort)(rel & 0xFFFF));
                }
            }
        }

        private void PatchWord(int offset, ushort value)
        {
            if (offset < 0 || offset + 1 >= _output.Count)
                throw new Exception("Internal patch out of range");
            _output[offset] = (byte)(value & 0xFF);
            _output[offset + 1] = (byte)(value >> 8);
        }
    }
}
