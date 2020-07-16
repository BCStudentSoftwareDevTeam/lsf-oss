from enum import Enum

class ButtonStatus(Enum):
    show_rehire_button = 0
    show_withdraw_button = 1
    show_withdraw_correction_buttons = 2
    show_release_adjustment_rehire_buttons = 3
    show_release_rehire_buttons = 4
    no_buttons_pending_forms = 5
