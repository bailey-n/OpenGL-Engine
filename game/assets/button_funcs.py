import logging
import math


# A place to store specific button functions
class ButtonFuncs:
    def switch_to_secondary_texture(button):
        if hasattr(button, 'switch_to_texture'):
            button.switch_to_texture(1)
        else:
            logging.warning(f' Failed to execute button function \'switch_to_secondary_texture\':'
                            f' {button.__class__.__name__} does not have required attributes')

    def switch_to_default_texture(button):
        if hasattr(button, 'switch_to_texture') and hasattr(button, 'rescale'):
            button.rescale((2, 0.5))
            button.switch_to_texture(0)
        else:
            logging.warning(f' Failed to execute button function \'switch_to_default_texture\':'
                            f' {button.__class__.__name__} does not have required attributes')

    def switch_to_tertiary_texture(button):
        if hasattr(button, 'switch_to_texture'):
            button.switch_to_texture(2)
        else:
            logging.warning(f' Failed to execute button function \'switch_to_tertiary_texture\':'
                            f' {button.__class__.__name__} does not have required attributes')

    def switch_to_quaternary_texture(button):
        if hasattr(button, 'switch_to_texture'):
            button.switch_to_texture(3)
        else:
            logging.warning(f' Failed to execute button function \'switch_to_quaternary_texture\':'
                            f' {button.__class__.__name__} does not have required attributes')

    def rotate(button):
        if hasattr(button, 'rotateBy') and hasattr(button, 'hover_time'):
            button.rotateBy(math.atan(button.hover_time) / 20)
        else:
            logging.warning(f' Failed to execute button function \'rotate\':'
                            f' {button.__class__.__name__} does not have required attributes')

    def grow(button):
        if hasattr(button, 'scale') and hasattr(button, 'rescale'):
            scale = (button.scale[0] * 1.01, button.scale[1] * 1.01)
            button.rescale(scale)
        else:
            logging.warning(f' Failed to execute button function \'grow\':'
                            f' {button.__class__.__name__} does not have required attributes')

