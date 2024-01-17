F2::ExitApp

F8::
    Loop, 25
    {

        SendInput, {Enter}
        Sleep, 300

        SendInput, {LWin Down}v{LWin Up}
        Sleep, 500

        DownNum := A_Index - 1
        Loop, %DownNum%
        {
            SendInput, {Down}
            Sleep, 50
        }
        Sleep, 500
        SendInput, {Enter}
        Sleep, 500
    }
return
