using System;

namespace ASMEngine
{
    public class CompileError : Exception
    {
        public int LineNumber { get; }

        public CompileError(int lineNumber, string message) : base(message)
        {
            LineNumber = lineNumber;
        }
    }
}
