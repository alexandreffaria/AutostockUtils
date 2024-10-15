from typing import Dict, Any

def get_dark_mode_styles() -> Dict[str, Any]:
    return {
        'background': '#2E2E2E',
        'foreground': '#FFFFFF',
        'label': {
            'bg': '#2E2E2E',
            'fg': '#FFFFFF'
        },
        'button': {
            'bg': '#3E3E3E',
            'fg': '#FFFFFF',
            'activebackground': '#5E5E5E',
            'activeforeground': '#FFFFFF'
        }
    }
