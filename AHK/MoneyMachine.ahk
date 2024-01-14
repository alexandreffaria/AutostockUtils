#Requires AutoHotkey v2.0

F4::ExitApp

; Set the range of time in milliseconds
MinTime := 90000 ; 45s 
MaxTime := 110000 ; 90s

; Generate a random time within the specified range

F2::Pause -1
F1::{

    SelectedFile := FileSelect(3, , "Open a file", "Text Documents (*.txt)")
    if SelectedFile = ""
        ExitApp

    Loop{
        Sleep 2000
        Loop read, SelectedFile
        {
            RandomTime := Random(MinTime,MaxTime)
            ; tooltip  A_Index " : " A_LoopReadLine " " RandomTime
            Click
            SendInput "/imagine"
            Sleep 1000
            SendInput "{Enter}"
            SendInput A_LoopReadLine
            SendInput " cinematic, shot by hasselblad X1D, editorial photogtaphy, " ; bbc, planet earth,
            SendInput "Sony FE 24-70mm f/2.8 GM " ; Lens
            SendInput "--ar 16:9" ; AR
            Sleep 1000
            SendInput "{Enter}"
            Sleep RandomTime
        }
    } 
}
