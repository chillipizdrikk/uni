namespace ASMEngine
{
    public static class ExamplePrograms
    {
        public static string BasicExample() => @"
org 100h

; Prints three prompts and exits.
pv1 db ""Enter first number : $""
pv2 db 13,10,""Enter second number: $""
pv3 db 13,10,""Enter third number : $""

begin:
    mov dx, pv1
    mov ah, 09h
    int 21h

    mov dx, pv2
    mov ah, 09h
    int 21h

    mov dx, pv3
    mov ah, 09h
    int 21h

    mov ax, 4c00h
    int 21h

end begin
".Trim() + "\r\n";
    }
}
