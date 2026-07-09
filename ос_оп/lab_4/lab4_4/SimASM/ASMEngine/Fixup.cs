namespace ASMEngine
{
    public enum FixupKind
    {
        Abs16,   // absolute address (word)
        Rel8,    // short relative
        Rel16    // near relative
    }

    public class Fixup
    {
        public int LineNumber { get; set; }
        public int OutputOffset { get; set; }  // index in output buffer
        public ushort InstrAddress { get; set; } // address of instruction start
        public int InstrLength { get; set; } // instruction length in bytes
        public string Symbol { get; set; } = "";
        public FixupKind Kind { get; set; }
    }
}
