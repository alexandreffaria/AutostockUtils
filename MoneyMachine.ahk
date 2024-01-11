F2::ExitApp

; Set the range of time in milliseconds
MinTime := 30000 ; 1/2 minute in milliseconds 
MaxTime := 60000 ; 1 minutes in milliseconds

F1::
   Loop
   {
        Loop, 25
        {
            Click, Left
            SendInput, /imagine
            Sleep, 500
            SendInput, {Enter}
            SendInput, {LWin Down}v{LWin Up}
            Sleep, 1000  ; delay to ensure the paste window appears

            DownNum := A_Index - 1
            Loop, %DownNum%
            {
                SendInput, {Down}
                Sleep, 50
            }
            Sleep, 1000
            SendInput, {Enter}
            Sleep, 500  ; delay to ensure the paste action completes and paste window disappears
            SendInput, {Space}
            SendInput, full screen, sharp focus, stock image, 8k, ultra realistic --ar 16:9 --c 20
            Send, {Enter}

            ; Generate a random time within the specified range
            Random, RandomTime, %MinTime%, %MaxTime%
            Sleep, %RandomTime% 
        }
    }
return
