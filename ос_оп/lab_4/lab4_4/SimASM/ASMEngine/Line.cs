namespace ASMEngine
{
    public class Line
    {
        public int LineNumber { get; set; }
        public ushort Address { get; set; }
        public string Source { get; set; } = "";
        public byte[] Code { get; set; } = new byte[0];

        public string CodeHex => HexDump.ToHex(Code);
    }
}
