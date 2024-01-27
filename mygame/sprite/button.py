
from ..core.locals import Image
from .sprite import Sprite

class Button(Sprite):
    """Create a three-state-button from a given three-tile-image, update on mouse hover and post event on click"""

    descriptor: str = 'button'
    folderpath = "G:/NEW/Assets/defaults/"
    filename = "three_stage_button-48x16.png"
    filepath = folderpath + filename

    def __init__(self, image = None, name = None, scale = 4) -> None:
        """Three state button [inactive, hovered, active] with written name, post user event on click"""
        image = Image(self.filepath, scale) if image is None else image
        assert image.get_width() % 3 == 0, "Image width for button is not divisible by 3."
        w = image.get_width() // 3
        h = image.get_height()
        self.name = name
        self.surfaces = {
            'inactive': image.subsurface(0 * w, 0, w, h),
            'hovered': image.subsurface(1 * w, 0, w, h),
            'active': image.subsurface(2 * w, 0, w, h)
            }
        self.state = 'inactive'
        self.surface = self.surfaces[self.state]
        self.rectangle = self.surface.get_rect()

    def handle(self, event):
        """Handle events and activate or deactivate object"""
        if self.clicked(event):
            self.state = 'active'
            self.post('button_press', button = self)
        elif self.released(event):
            self.state = 'inactive'

    def update(self):
        """Update the surface every frame"""
        if self.state != 'active':
            self.state = 'hovered' if self.collides_mouse() else 'inactive'
        self.surface = self.surfaces[self.state]

    def get_tooltip_lines(self):
        """Get lines to be rendered by sprite tooltip"""
        return [
            f'Button: {str(self.name).title()}',
            f'- - -',
            f'State: {self.state}',
            f'Post USER_EVENT on click',
            ]