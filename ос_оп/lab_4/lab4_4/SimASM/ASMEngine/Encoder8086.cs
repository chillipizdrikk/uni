using System;
using System.Collections.Generic;
using System.Linq;
using System.Text.RegularExpressions;

namespace ASMEngine
{
    public class EncodedInstr
    {
        public byte[] Bytes { get; set; } = Array.Empty<byte>();
        public List<Fixup> Fixups { get; set; } = new();
    }

    public class Encoder8086
    {
        private readonly Dictionary<string, ushort> _symtab;
        private readonly List<Fixup> _fixups;
        private readonly Func<string, ushort>? _resolveSymbolOrThrow;

        public Encoder8086(Dictionary<string, ushort> symtab, List<Fixup> fixups, Func<string, ushort>? resolveSymbolOrThrow = null)
        {
            _symtab = symtab;
            _fixups = fixups;
            _resolveSymbolOrThrow = resolveSymbolOrThrow;
        }

        public EncodedInstr Encode(int lineNumber, ushort address, string opcode, List<string> operands)
        {
            opcode = opcode.ToUpperInvariant();

            return opcode switch
            {
                "NOP" => Simple(new byte[] { 0x90 }),
                "RET" => Simple(new byte[] { 0xC3 }),
                "INT" => EncodeINT(lineNumber, operands),
                "MOV" => EncodeMOV(lineNumber, address, operands),
                "ADD" => EncodeALU(lineNumber, address, operands, alu: "ADD"),
                "SUB" => EncodeALU(lineNumber, address, operands, alu: "SUB"),
                "CMP" => EncodeALU(lineNumber, address, operands, alu: "CMP"),
                "INC" => EncodeIncDec(lineNumber, operands, inc: true),
                "DEC" => EncodeIncDec(lineNumber, operands, inc: false),
                "JMP" => EncodeJmp(lineNumber, address, operands, cond: null),
                "JE" or "JZ" => EncodeJmp(lineNumber, address, operands, cond: "JE"),
                "JNE" or "JNZ" => EncodeJmp(lineNumber, address, operands, cond: "JNE"),
                _ => throw new CompileError(lineNumber, $"Unsupported opcode: {opcode}")
            };
        }

        private EncodedInstr Simple(byte[] bytes) => new() { Bytes = bytes };

        private EncodedInstr EncodeINT(int lineNumber, List<string> ops)
        {
            if (ops.Count != 1) throw new CompileError(lineNumber, "INT expects 1 operand");
            byte imm = AsmUtil.ParseNumberByte(ops[0]);
            return Simple(new byte[] { 0xCD, imm });
        }

        private EncodedInstr EncodeIncDec(int lineNumber, List<string> ops, bool inc)
        {
            if (ops.Count != 1) throw new CompileError(lineNumber, (inc ? "INC" : "DEC") + " expects 1 operand");
            var op = ops[0].Trim();
            if (!AsmUtil.IsReg16(op)) throw new CompileError(lineNumber, "INC/DEC supported only for 16-bit registers in this lab subset");
            int reg = AsmUtil.Reg16[op];
            byte b = (byte)((inc ? 0x40 : 0x48) + reg);
            return Simple(new byte[] { b });
        }

        private EncodedInstr EncodeJmp(int lineNumber, ushort addr, List<string> ops, string? cond)
        {
            if (ops.Count != 1) throw new CompileError(lineNumber, "JMP/Jcc expects 1 operand");
            string target = ops[0].Trim();

            // placeholder: we decide rel8 vs rel16 after symtab known; here:
            // - JE/JNE always short in this simplified assembler
            // - JMP: try short if possible at pass2, else near rel16 (E9)
            if (cond is "JE")
            {
                var bytes = new byte[] { 0x74, 0x00 };
                AddFixup(lineNumber, kind: FixupKind.Rel8, symbol: target, outputOffset: -1, instrAddr: addr, instrLen: 2);
                return new EncodedInstr { Bytes = bytes };
            }
            if (cond is "JNE")
            {
                var bytes = new byte[] { 0x75, 0x00 };
                AddFixup(lineNumber, kind: FixupKind.Rel8, symbol: target, outputOffset: -1, instrAddr: addr, instrLen: 2);
                return new EncodedInstr { Bytes = bytes };
            }

            // JMP
            // We'll emit near JMP (E9 cw) always to be safe. (Still allowed for .COM)
            // If you want short, change to EB cb and Rel8.
            var b2 = new byte[] { 0xE9, 0x00, 0x00 };
            AddFixup(lineNumber, kind: FixupKind.Rel16, symbol: target, outputOffset: -1, instrAddr: addr, instrLen: 3);
            return new EncodedInstr { Bytes = b2 };
        }

        private EncodedInstr EncodeMOV(int lineNumber, ushort addr, List<string> ops)
        {
            if (ops.Count != 2) throw new CompileError(lineNumber, "MOV expects 2 operands");
            string dst = AsmUtil.StripPtr(ops[0]);
            string src = AsmUtil.StripPtr(ops[1]);

            // reg, imm
            if (AsmUtil.IsReg16(dst) && IsImmediate(src))
            {
                int reg = AsmUtil.Reg16[dst];
                ushort imm = ParseImmOrSymbolWord(lineNumber, src, addr, needsFixupAbs: false, out var fix);
                var bytes = new List<byte> { (byte)(0xB8 + reg), (byte)(imm & 0xFF), (byte)(imm >> 8) };
                var ei = new EncodedInstr { Bytes = bytes.ToArray() };
                if (fix != null) ei.Fixups.Add(fix);
                return ei;
            }
            if (AsmUtil.IsReg8(dst) && IsImmediate(src))
            {
                int reg = AsmUtil.Reg8[dst];
                byte imm = (byte)(ParseImmOrSymbolWord(lineNumber, src, addr, needsFixupAbs: false, out var fix) & 0xFF);
                var bytes = new List<byte> { (byte)(0xB0 + reg), imm };
                var ei = new EncodedInstr { Bytes = bytes.ToArray() };
                if (fix != null) ei.Fixups.Add(fix);
                return ei;
            }

            // reg, reg
            if (AsmUtil.IsReg16(dst) && AsmUtil.IsReg16(src))
            {
                // 8B /r  (reg <- r/m)
                return EncodeRMReg(lineNumber, opcode: 0x8B, reg: AsmUtil.Reg16[dst], rmIsReg: true, rmReg: AsmUtil.Reg16[src], rmOp: null);
            }
            if (AsmUtil.IsReg8(dst) && AsmUtil.IsReg8(src))
            {
                return EncodeRMReg(lineNumber, opcode: 0x8A, reg: AsmUtil.Reg8[dst], rmIsReg: true, rmReg: AsmUtil.Reg8[src], rmOp: null);
            }

            // reg <- mem
            if ((AsmUtil.IsReg16(dst) || AsmUtil.IsReg8(dst)) && IsMemory(src))
            {
                bool is8 = AsmUtil.IsReg8(dst);
                int reg = is8 ? AsmUtil.Reg8[dst] : AsmUtil.Reg16[dst];
                byte op = is8 ? (byte)0x8A : (byte)0x8B; // reg <- r/m
                return EncodeRMReg(lineNumber, opcode: op, reg: reg, rmIsReg: false, rmReg: 0, rmOp: src);
            }

            // mem <- reg
            if (IsMemory(dst) && (AsmUtil.IsReg16(src) || AsmUtil.IsReg8(src)))
            {
                bool is8 = AsmUtil.IsReg8(src);
                int reg = is8 ? AsmUtil.Reg8[src] : AsmUtil.Reg16[src];
                byte op = is8 ? (byte)0x88 : (byte)0x89; // r/m <- reg
                return EncodeRMReg(lineNumber, opcode: op, reg: reg, rmIsReg: false, rmReg: 0, rmOp: dst);
            }

            // mem <- imm (subset)
            if (IsMemory(dst) && IsImmediate(src))
            {
                // C7 /0 iw (word) ; C6 /0 ib (byte) -- we'll choose word by default
                // If user wrote BYTE PTR, they'd expect byte; we stripped PTR. Keep it word.
                ushort imm = ParseImmOrSymbolWord(lineNumber, src, addr, needsFixupAbs: false, out var fix);
                var ea = EncodeEA(lineNumber, dst, addr);
                var bytes = new List<byte>();
                bytes.Add(0xC7);
                bytes.Add((byte)((ea.Mod << 6) | (0 << 3) | ea.Rm)); // /0
                bytes.AddRange(ea.DispBytes);
                bytes.Add((byte)(imm & 0xFF));
                bytes.Add((byte)(imm >> 8));
                var ei = new EncodedInstr { Bytes = bytes.ToArray() };
                if (ea.Fixup != null) ei.Fixups.Add(ea.Fixup);
                if (fix != null) ei.Fixups.Add(fix);
                return ei;
            }

            throw new CompileError(lineNumber, $"Unsupported MOV form: {dst}, {src}");
        }

        private EncodedInstr EncodeALU(int lineNumber, ushort addr, List<string> ops, string alu)
        {
            if (ops.Count != 2) throw new CompileError(lineNumber, $"{alu} expects 2 operands");

            string dst = AsmUtil.StripPtr(ops[0]);
            string src = AsmUtil.StripPtr(ops[1]);

            // reg, imm (word only in this subset)
            if (AsmUtil.IsReg16(dst) && IsImmediate(src))
            {
                // 81 /digit iw
                int digit = alu switch { "ADD" => 0, "SUB" => 5, "CMP" => 7, _ => 0 };
                var modrm = (byte)(0xC0 | (digit << 3) | AsmUtil.Reg16[dst]);
                ushort imm = ParseImmOrSymbolWord(lineNumber, src, addr, needsFixupAbs: false, out var fix);
                var bytes = new List<byte> { 0x81, modrm, (byte)(imm & 0xFF), (byte)(imm >> 8) };
                var ei = new EncodedInstr { Bytes = bytes.ToArray() };
                if (fix != null) ei.Fixups.Add(fix);
                return ei;
            }

            // reg, reg
            if (AsmUtil.IsReg16(dst) && AsmUtil.IsReg16(src))
            {
                byte op = alu switch { "ADD" => (byte)0x03, "SUB" => (byte)0x2B, "CMP" => (byte)0x3B, _ => (byte)0x03 };
                // op reg, r/m
                return EncodeRMReg(lineNumber, opcode: op, reg: AsmUtil.Reg16[dst], rmIsReg: true, rmReg: AsmUtil.Reg16[src], rmOp: null);
            }

            // reg, mem
            if (AsmUtil.IsReg16(dst) && IsMemory(src))
            {
                byte op = alu switch { "ADD" => (byte)0x03, "SUB" => (byte)0x2B, "CMP" => (byte)0x3B, _ => (byte)0x03 };
                return EncodeRMReg(lineNumber, opcode: op, reg: AsmUtil.Reg16[dst], rmIsReg: false, rmReg: 0, rmOp: src);
            }

            // mem, reg  (subset)
            if (IsMemory(dst) && AsmUtil.IsReg16(src))
            {
                byte op = alu switch { "ADD" => (byte)0x01, "SUB" => (byte)0x29, "CMP" => (byte)0x39, _ => (byte)0x01 };
                // op r/m, reg
                return EncodeRMReg(lineNumber, opcode: op, reg: AsmUtil.Reg16[src], rmIsReg: false, rmReg: 0, rmOp: dst);
            }

            throw new CompileError(lineNumber, $"Unsupported {alu} form: {dst}, {src}");
        }

        private bool IsImmediate(string s)
        {
            s = s.Trim();
            if (_symtab.ContainsKey(s)) return true;
            if (Regex.IsMatch(s, @"^'.'$")) return true;
            if (Regex.IsMatch(s, @"^(0x)?[0-9A-Fa-f]+h?$")) return true;
            if (Regex.IsMatch(s, @"^[0-9]+$")) return true;
            return false;
        }

        private bool IsMemory(string s)
        {
            s = s.Trim();
            if (AsmUtil.LooksLikeMemory(s)) return true;
            // label without brackets treated as direct memory in this subset (for MOV DX, pv1)
            if (Regex.IsMatch(s, @"^[A-Za-z_][A-Za-z0-9_]*$")) return true;
            return false;
        }

        private ushort ParseImmOrSymbolWord(int lineNumber, string token, ushort addr, bool needsFixupAbs, out Fixup? fixup)
        {
            token = token.Trim();
            fixup = null;

            if (_symtab.TryGetValue(token, out var val))
            {
                return val;
            }

            // if it looks like symbol but not known yet -> fixup
            if (Regex.IsMatch(token, @"^[A-Za-z_][A-Za-z0-9_]*$"))
            {
                fixup = new Fixup
                {
                    LineNumber = lineNumber,
                    OutputOffset = -1, // patched by caller when bytes appended
                    InstrAddress = addr,
                    InstrLength = 0,
                    Symbol = token,
                    Kind = FixupKind.Abs16
                };
                return 0;
            }

            return AsmUtil.ParseNumberWord(token);
        }

        private void AddFixup(int lineNumber, FixupKind kind, string symbol, int outputOffset, ushort instrAddr, int instrLen)
        {
            _fixups.Add(new Fixup
            {
                LineNumber = lineNumber,
                Kind = kind,
                Symbol = symbol,
                OutputOffset = outputOffset,
                InstrAddress = instrAddr,
                InstrLength = instrLen
            });
        }

        private EncodedInstr EncodeRMReg(int lineNumber, byte opcode, int reg, bool rmIsReg, int rmReg, string? rmOp)
        {
            var bytes = new List<byte> { opcode };
            if (rmIsReg)
            {
                byte modrm = (byte)(0xC0 | (reg << 3) | rmReg);
                bytes.Add(modrm);
                return new EncodedInstr { Bytes = bytes.ToArray() };
            }
            else
            {
                var ea = EncodeEA(lineNumber, rmOp!, 0); // addr passed via caller in cases where symbol fixup needed, handled inside EA with Abs16 fixup
                byte modrm = (byte)((ea.Mod << 6) | (reg << 3) | ea.Rm);
                bytes.Add(modrm);
                bytes.AddRange(ea.DispBytes);
                var ei = new EncodedInstr { Bytes = bytes.ToArray() };
                if (ea.Fixup != null) ei.Fixups.Add(ea.Fixup);
                return ei;
            }
        }

        private class EAResult
        {
            public int Mod;
            public int Rm;
            public byte[] DispBytes = Array.Empty<byte>();
            public Fixup? Fixup;
        }

        // 8086 16-bit addressing:
        // r/m:
        // 000 [BX+SI], 001 [BX+DI], 010 [BP+SI], 011 [BP+DI],
        // 100 [SI],    101 [DI],    110 [BP] or disp16 when MOD=00, 111 [BX]
        private EAResult EncodeEA(int lineNumber, string op, ushort instrAddr)
        {
            op = op.Trim();
            op = AsmUtil.StripPtr(op);

            // Direct label without brackets => direct memory disp16
            if (!AsmUtil.LooksLikeMemory(op) && Regex.IsMatch(op, @"^[A-Za-z_][A-Za-z0-9_]*$"))
            {
                // MOD=00, R/M=110, disp16
                var r = new EAResult { Mod = 0, Rm = 6 };
                if (_symtab.TryGetValue(op, out var addr))
                {
                    r.DispBytes = new byte[] { (byte)(addr & 0xFF), (byte)(addr >> 8) };
                }
                else
                {
                    r.DispBytes = new byte[] { 0x00, 0x00 };
                    r.Fixup = new Fixup
                    {
                        LineNumber = lineNumber,
                        Kind = FixupKind.Abs16,
                        Symbol = op,
                        OutputOffset = -1,
                        InstrAddress = instrAddr,
                        InstrLength = 0
                    };
                }
                return r;
            }

            // strip brackets [ ... ]
            var inner = op;
            if (AsmUtil.LooksLikeMemory(op))
            {
                int l = op.IndexOf('[');
                int rbr = op.LastIndexOf(']');
                if (l < 0 || rbr < 0 || rbr <= l) throw new CompileError(lineNumber, "Bad memory operand");
                inner = op.Substring(l + 1, rbr - l - 1).Trim();
            }

            // Support: BX, BP, SI, DI, BX+SI, BX+DI, BP+SI, BP+DI, plus optional +disp or label+SI etc.
            // Normalize: replace spaces
            inner = inner.Replace(" ", "");

            // Extract displacement or label part like LABEL+SI or SI+8 etc.
            string expr = inner;
            int disp = 0;
            string? label = null;

            // If contains + or - split into base and disp/label
            // We'll allow forms: SI+8, BX-2, LABEL+SI, LABEL+SI+8
            var tokens = Regex.Split(expr, @"(?=[\+\-])").Where(t => t.Length > 0).ToList();
            // tokens like ["LABEL", "+SI", "+8"]
            string first = tokens[0];
            var parts = new List<string> { first };
            for (int i = 1; i < tokens.Count; i++) parts.Add(tokens[i]);

            // Determine base terms (registers) and optional label
            var regs = new List<string>();
            if (!string.IsNullOrEmpty(first))
            {
                // first may be reg or label
                if (AsmUtil.IsRegister(first))
                    regs.Add(first.ToUpperInvariant());
                else if (Regex.IsMatch(first, @"^[A-Za-z_][A-Za-z0-9_]*$"))
                    label = first;
                else if (Regex.IsMatch(first, @"^[0-9A-Fa-f]+h?$") || Regex.IsMatch(first, @"^[0-9]+$") || first.StartsWith("0x", StringComparison.OrdinalIgnoreCase))
                    disp += AsmUtil.ParseNumberWord(first);
                else
                    throw new CompileError(lineNumber, $"Unsupported memory expression: {op}");
            }

            foreach (var p in parts.Skip(1))
            {
                // p begins with + or -
                int sign = p[0] == '-' ? -1 : 1;
                var term = p.Substring(1);
                if (term.Length == 0) continue;

                if (AsmUtil.IsRegister(term))
                    regs.Add(term.ToUpperInvariant());
                else if (Regex.IsMatch(term, @"^[A-Za-z_][A-Za-z0-9_]*$"))
                {
                    if (label != null) throw new CompileError(lineNumber, "Too many symbols in address expression");
                    label = term;
                }
                else
                {
                    disp += sign * (short)AsmUtil.ParseNumberWord(term);
                }
            }

            regs = regs.Select(rg => rg.ToUpperInvariant()).ToList();

            // Map regs combination to rm
            int rm;
            if (regs.Count == 1)
            {
                rm = regs[0] switch
                {
                    "SI" => 4,
                    "DI" => 5,
                    "BP" => 6,
                    "BX" => 7,
                    _ => throw new CompileError(lineNumber, "Only SI/DI/BP/BX are supported in memory operand in this subset")
                };
            }
            else if (regs.Count == 2)
            {
                var a = regs[0];
                var b = regs[1];
                var combo = (a, b);
                // order-independent
                bool hasBX = a == "BX" || b == "BX";
                bool hasBP = a == "BP" || b == "BP";
                bool hasSI = a == "SI" || b == "SI";
                bool hasDI = a == "DI" || b == "DI";

                if (hasBX && hasSI) rm = 0;
                else if (hasBX && hasDI) rm = 1;
                else if (hasBP && hasSI) rm = 2;
                else if (hasBP && hasDI) rm = 3;
                else throw new CompileError(lineNumber, "Unsupported register pair in memory operand");
            }
            else
            {
                throw new CompileError(lineNumber, "Too many registers in memory operand");
            }

            // Determine displacement
            var dispBytes = new List<byte>();
            int mod;

            // Special case: [BP] cannot be encoded with MOD=00 and RM=110 (that means disp16)
            // so if rm==6 and no disp, force MOD=01 disp8=0
            bool hasDisp = disp != 0;
            if (!hasDisp && rm == 6 && label == null)
            {
                mod = 1;
                dispBytes.Add(0x00);
            }
            else if (!hasDisp && label == null)
            {
                mod = 0;
            }
            else
            {
                // if disp fits in int8 use MOD=01 else MOD=10
                if (disp >= -128 && disp <= 127)
                {
                    mod = 1;
                    dispBytes.Add((byte)(disp & 0xFF));
                }
                else
                {
                    mod = 2;
                    dispBytes.Add((byte)(disp & 0xFF));
                    dispBytes.Add((byte)((disp >> 8) & 0xFF));
                }
            }

            // If label exists, treat it as additional disp16 added to base:
            // We'll encode it as MOD=10 disp16 (safe), unless already MOD=10 with disp16.
            Fixup? fix = null;
            if (label != null)
            {
                // Force MOD=10 disp16 + existing disp (we'll store just symbol address; at patch time user expects absolute address, not base+symbol.
                // In this simplified lab subset, we interpret LABEL[SI] as disp16=address(LABEL) with base SI.
                mod = 2;
                dispBytes.Clear();
                dispBytes.Add(0x00); dispBytes.Add(0x00);
                fix = new Fixup
                {
                    LineNumber = lineNumber,
                    Kind = FixupKind.Abs16,
                    Symbol = label,
                    OutputOffset = -1,
                    InstrAddress = instrAddr,
                    InstrLength = 0
                };
            }

            return new EAResult { Mod = mod, Rm = rm, DispBytes = dispBytes.ToArray(), Fixup = fix };
        }
    }
}
