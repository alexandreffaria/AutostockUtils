#Requires AutoHotkey v2.0
F2::ExitApp
F1::{
    Loop{
        Sleep 2000
        MouseMove 1200, 350
        Click
        Sleep 300
        MouseMove 1650, 660
        Click
        Sleep 300
        MouseMove 1650, 780
        Click
        Sleep 300
        MouseMove 75, 1000
        Click
        Sleep 7000
        MouseMove 500, 500
        Sleep 300
        Loop 7{
            Click "WheelDown", 60
            Sleep 100
        }
        MouseMove 960, 1000
        Sleep 300
        Click
        Sleep 2000
    }
}

