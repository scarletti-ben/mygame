
import math

class AlignParameters:
    def __init__(self):
        self.pos = (0, 0)
        self.rot = (0, 0, 0)
        self.scale = 1

def get_align_hand_parameters(align_amount, x_offset, y_offset, z_rot_offset, hand_cards_count):
    align_parameters = [AlignParameters() for _ in range(align_amount)]

    if align_amount == 1:
        align_parameters[0].pos = (0, 0)
        align_parameters[0].rot = (0, 0, 0)
        align_parameters[0].scale = 1
        return align_parameters
    elif align_amount < 1:
        return align_parameters  # There are no cards

    modulo = align_amount % 2
    is_even = modulo == 0

    x_start_pos = -1
    y_start_pos = -1
    z_start_rot = -1

    if not is_even:
        mid_index = (align_amount // 2) + modulo  # Get the middle card
        x_start_pos = x_offset / 2 * (align_amount // 2 + modulo)  # Account for the middle number
        y_start_pos = y_offset * (align_amount // 2 + modulo)
        z_start_rot = z_rot_offset * (align_amount // 2 + modulo)
    else:
        mid_index = hand_cards_count // 2
        x_start_pos = x_offset / 2 * (align_amount // 2)
        y_start_pos = y_offset * (align_amount // 2)
        z_start_rot = z_rot_offset * (align_amount // 2)

    prev_pos = (-x_start_pos, -y_start_pos)
    prev_z_rot = z_start_rot
    target_pos = prev_pos
    target_z_rot = prev_z_rot

    target_x_offset = x_offset
    target_y_offset = y_offset

    align_parameters[0].pos = target_pos
    align_parameters[0].rot = (0, 0, target_z_rot)
    align_parameters[0].scale = 1

    for i in range(1, align_amount):
        target_pos = prev_pos
        if (is_even and i > align_amount // 2) or (not is_even and i > mid_index):
            target_y_offset = -abs(y_offset)
        elif not is_even and i == mid_index - 1:
            target_pos = (prev_pos[0] + target_x_offset, prev_pos[1] + target_y_offset)
            target_z_rot = 0
            align_parameters[i].pos = target_pos
            align_parameters[i].rot = (0, 0, target_z_rot)
            align_parameters[i].scale = 1
            prev_pos = target_pos
            prev_z_rot = target_z_rot
            continue

        target_pos = (prev_pos[0] + x_offset, prev_pos[1] + target_y_offset)
        target_z_rot = prev_z_rot - z_rot_offset

        if i == mid_index or i == mid_index - 1:
            if is_even and i == mid_index:
                target_z_rot = -prev_z_rot
            target_pos = (target_pos[0], -target_y_offset)

        align_parameters[i].pos = target_pos
        align_parameters[i].rot = (0, 0, target_z_rot)
        align_parameters[i].scale = 1
        prev_pos = target_pos
        prev_z_rot = target_z_rot

    return align_parameters

# Example usage:
align_amount = 5
x_offset = 30
y_offset = 20
z_rot_offset = math.radians(10)
hand_cards_count = 10

align_params = get_align_hand_parameters(align_amount, x_offset, y_offset, z_rot_offset, hand_cards_count)
for i, params in enumerate(align_params):
    print(f"Card {i + 1}: Pos={params.pos}, Rot={params.rot}, Scale={params.scale}")
