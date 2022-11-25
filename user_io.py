from geom import Point2d

# keyboard
class KeyboardInput:
    fwd_pressed = False
    bwd_pressed = False
    right_pressed = False
    left_pressed = False

    def fwdCb():
        KeyboardInput.fwd_pressed = True
    def unfwdCb():
        KeyboardInput.fwd_pressed = False
    def leftCb():
        KeyboardInput.left_pressed = True
    def unleftCb():
        KeyboardInput.left_pressed = False
    def bwdCb():
        KeyboardInput.bwd_pressed = True
    def unbwdCb():
        KeyboardInput.bwd_pressed = False
    def rightCb():
        KeyboardInput.right_pressed = True
    def unrightCb():
        KeyboardInput.right_pressed = False


def fwdProj():
    return float(KeyboardInput.fwd_pressed) - float(KeyboardInput.bwd_pressed)
def rightProj():
    return float(KeyboardInput.right_pressed) - float(KeyboardInput.left_pressed)
def normalizedMovement():
    # y = fwdProj()
    # x = rightProj()
    # n = math.sqrt(x*x + y*y)
    vec = Point2d(rightProj(), fwdProj())
    n = vec.norm()
    if n > 0:
        # return x/n, y/n
        return vec / n
    else:
        # return 0.0, 0.0
        return vec
    # return x/n, y/n if n > 0 else 0.0, 0.0
