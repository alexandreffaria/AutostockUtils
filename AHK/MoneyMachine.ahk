#SingleInstance Force

F2::ExitApp



F1::

; Set the range of time in milliseconds
MinTime := 70000 ; 45s 
MaxTime := 90000 ; 90s
; Generate a random time within the specified range
Random, RandomTime, %MinTime%, %MaxTime%

   Loop
   {
        Loop, 25
        {
            Click, Left
            SendInput, /imagine
            Sleep, 500
            SendInput, {Enter}
            Sleep, 300 
            SendInput, {LWin Down}v{LWin Up}
            Sleep, 300  ; delay to ensure the paste window appears

            DownNum := A_Index - 1
            Loop, %DownNum%
            {
                SendInput, {Down}
                Sleep, 50
            }
            Sleep, 500
            SendInput, {Enter}
            Sleep, 2000  ; delay to ensure the paste action completes and paste window disappears
            SendInput, {Space}
            SendInput, full screen, sharp focus, stock image, 8k, ultra hd, ultra realistic, in the style of realistic hyper-detailed, topcor 58mm f/1.4  --ar 16:9 --c 80
            Send, {Enter}

            
            Sleep, %RandomTime% 
        }
    }
return
