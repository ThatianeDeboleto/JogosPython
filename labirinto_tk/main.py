"""
This is a basic example of using KekGL
Use 'a', 'w', 's', 'd' to move, arrows to rotate
"""

import time

import UIManager
from models import labyrinth_model, corner_model, pyramid_model
from KekGL import *

window = UIManager.Window()
window.set_fullscreen()
window.show_canvas()

BM = UIManager.BindingManager(window)

IM = UIManager.ImageManager()
IM.add('bentley', 'images/bentley.gif')

SM = UIManager.SoundManager()
SM.add('bentley', 'sounds/bentley.mp3')
SM.add('goagain', 'sounds/goagain.mp3')
SM.add('steps', 'sounds/steps.mp3')

BM.bind('Forward', 87)
BM.bind('Left', 65)
BM.bind('Right', 68)
BM.bind('Backward', 83)
BM.bind('Q', 81)
BM.bind('E', 69)
BM.bind('ArrowUp', 38)
BM.bind('ArrowLeft', 37)
BM.bind('ArrowRight', 39)
BM.bind('ArrowDown', 40)
BM.bind('ESC', 27)
BM.bind('F', 70)

transform_1 = Matrix(4, 4, [
    [2, 0, 0, 0],
    [0, 0, -2, 0],
    [0, -2, 0, 0],
    [20, 25, -70, 1]
])

transform_map = Matrix(4, 4, [
    [0.25, 0, 0, 0],
    [0, 0, -0.25, 0],
    [0, -0.25, 0, 0],
    [0, 25, -400, 1]
])

transform_corner_start = Matrix(4, 4, [
    [2, 0, 0, 0],
    [0, 0, -2, 0],
    [0, -2, 0, 0],
    [0, 25, -400, 1]
])

transform_along_y1 = Matrix(4, 4, [
    [1, 0, 0, 0],
    [0, 1, 0, 0],
    [0, 0, 1, 0],
    [0, 4, 0, 1]
])

transform_along_y2 = Matrix(4, 4, [
    [1, 0, 0, 0],
    [0, 1, 0, 0],
    [0, 0, 1, 0],
    [0, -4, 0, 1]
])

transform_d = Matrix(4, 4, [
    [1, 0, 0, 0],
    [0, 1, 0, 0],
    [0, 0, 1, 0],
    [-4, 0, 0, 1]
])

transform_a = Matrix(4, 4, [
    [1, 0, 0, 0],
    [0, 1, 0, 0],
    [0, 0, 1, 0],
    [4, 0, 0, 1]
])

transform_q = Matrix(4, 4, [
    [1, 0, 0, 0],
    [0, 1, 0, 0],
    [0, 0, 1, 0],
    [0, 0, 4, 1]
])

transform_e = Matrix(4, 4, [
    [1, 0, 0, 0],
    [0, 1, 0, 0],
    [0, 0, 1, 0],
    [0, 0, -4, 1]
])

ang = 0.04

transform_rot_up = Matrix(4, 4, [
    [1, 0, 0, 0],
    [0, cos(-ang), sin(-ang), 0],
    [0, -sin(-ang), cos(-ang), 0],
    [0, 0, 0, 1]
])

transform_rot_down = Matrix(4, 4, [
    [1, 0, 0, 0],
    [0, cos(ang), sin(ang), 0],
    [0, -sin(ang), cos(ang), 0],
    [0, 0, 0, 1]
])


def transform_rot_y(angle):
    return Matrix(4, 4, [
        [1, 0, 0, 0],
        [0, cos(angle), sin(angle), 0],
        [0, -sin(angle), cos(angle), 0],
        [0, 0, 0, 1]
    ])


# these two matrices move camera along world's horizontal axis
def transform_w(phi):
    return Matrix(4, 4, [
        [1, 0, 0, 0],
        [0, 1, 0, 0],
        [0, 0, 1, 0],
        [0, -2*sin(phi), 2*cos(phi), 1]
    ])


def transform_s(phi):
    return Matrix(4, 4, [
        [1, 0, 0, 0],
        [0, 1, 0, 0],
        [0, 0, 1, 0],
        [0, 2*sin(phi), -2*cos(phi), 1]
    ])


# these two matrices rotate camera relative to the world vertical axis
def tr_rot_right(phi):
    global ang
    c = cos(-ang)
    s = sin(-ang)
    anc = cos(phi)
    ans = sin(phi)
    return Matrix(4, 4, [
        [c, s*ans, -s*anc, 0],
        [-s*ans, anc**2*(1-c)+c, anc*ans*(1-c), 0],
        [s*anc, anc*ans*(1-c), ans**2*(1-c)+c, 0],
        [0, 0, 0, 1]
    ])


def tr_rot_left(phi):
    global ang
    c = cos(ang)
    s = sin(ang)
    anc = cos(phi)
    ans = sin(phi)
    return Matrix(4, 4, [
        [c, s*ans, -s*anc, 0],
        [-s*ans, anc**2*(1-c)+c, anc*ans*(1-c), 0],
        [s*anc, anc*ans*(1-c), ans**2*(1-c)+c, 0],
        [0, 0, 0, 1]
    ])


def transform_rot_x(angle, deviation_angle):
    c = cos(angle)
    s = -sin(angle)
    anc = cos(deviation_angle)
    ans = sin(deviation_angle)
    return Matrix(4, 4, [
        [c, s*ans, -s*anc, 0],
        [-s*ans, anc**2*(1-c)+c, anc*ans*(1-c), 0],
        [s*anc, anc*ans*(1-c), ans**2*(1-c)+c, 0],
        [0, 0, 0, 1]
    ])


transform_rot_left = Matrix(4, 4, [
    [cos(ang), 0, -sin(ang), 0],
    [0, 1, 0, 0],
    [sin(ang), 0, cos(ang), 0],
    [0, 0, 0, 1]
])

transform_rot_right = Matrix(4, 4, [
    [cos(-ang), 0, -sin(-ang), 0],
    [0, 1, 0, 0],
    [sin(-ang), 0, cos(-ang), 0],
    [0, 0, 0, 1]
])

transform_rot_z1 = Matrix(4, 4, [
    [cos(ang), sin(ang), 0, 0],
    [-sin(ang), cos(ang), 0, 0],
    [0, 0, 1, 0],
    [0, 0, 0, 1]
])

transform_rot_z2 = Matrix(4, 4, [
    [cos(ang), sin(ang), 0, 0],
    [-sin(ang), cos(ang), 0, 0],
    [0, 0, 1, 0],
    [0, 0, 0, 1]
])

# coordinates of the view pyramid's vertices
l, t, r, b = -window.SCREEN_WIDTH/20, window.SCREEN_HEIGHT/20, window.SCREEN_WIDTH/20, -window.SCREEN_HEIGHT/20
n, f = 70, 100

proj_matrix = Matrix(4, 4, [
    [2*n/(r-l), 0, 0, 0],
    [0, 2*n/(t-b), 0, 0],
    [(r+l)/(r-l), (t+b)/(t-b), -(f+n)/(f-n), -1],
    [0, 0, -2*f*n/(f-n), 0]
])


def toCanv(prim):
    crds_row = []
    for i in range(prim.s_crds.rows):
        crds_row += prim.s_crds[i]
    return crds_row


pyramid = Object(pyramid_model)
pyramid.toWorld(transform_1)

corner = Object(corner_model)
corner.toWorld(transform_corner_start)

labyrinth = Object(labyrinth_model)
labyrinth.toWorld(transform_map)

player = Player()
player.matrix = Matrix(4, 4, [
    [1, 0, 0, 0],
    [0, 1, 0, 0],
    [0, 0, 1, 0],
    [12, 9, -415, 1]])
Labirinth = World(player, labyrinth)
Labirinth.canv_draw = lambda prim: \
    window.canv.create_polygon(*toCanv(prim), outline=prim.outline, width=prim.width, fill=prim.color)
Labirinth.projection_matrix = proj_matrix
Labirinth.set_screen_resolution(window.SCREEN_WIDTH, window.SCREEN_HEIGHT)

Labirinth.BSP_create()
Labirinth.update()
Labirinth.draw()

fps = 0.0
fps_time_start = 0.0
counter = 0
previous_mouse_position = window.tk.winfo_pointerx()-window.tk.winfo_rootx(), \
                          window.tk.winfo_pointery()-window.tk.winfo_rooty()
k = 0


def loop():
    global k, previous_mouse_position
    global fps, fps_time_start, counter
    start_time = time.time()

    if BM.isPressed('ESC'):
        window.tk.config(cursor="")
        window.canv.destroy()
        window.game_is_on = False
        IM.draw('bentley')

        label_pause = UIManager.Label(text='PAUSE', width=20, height=2, bg='grey', font='30',
                                      x=window.SCREEN_WIDTH/5*2, y=window.SCREEN_HEIGHT/20)

        button_music_on = UIManager.Button(window, text='Sound ON',
                                           x=window.SCREEN_WIDTH/10, y=window.SCREEN_HEIGHT/5)
        button_music_on.bind("<Button-1>", lambda event: SM.play('bentley'))

        button_music_off = UIManager.Button(window, text='Sound OFF',
                                            x=window.SCREEN_WIDTH/10, y=window.SCREEN_HEIGHT/4)
        button_music_off.bind("<Button-1>", lambda event: SM.stop('bentley'))

        def button_continue_func(event):
            global previous_mouse_position
            window.show_canvas()
            previous_mouse_position = window.tk.winfo_pointerx()-window.tk.winfo_rootx(), \
                                      window.tk.winfo_pointery()-window.tk.winfo_rooty()

        button_continue = UIManager.Button(window, text='Continue',
                                           x=window.SCREEN_WIDTH/1.25, y=window.SCREEN_HEIGHT/5)
        button_continue.bind("<Button-1>", button_continue_func)

        button_quit = UIManager.Button(window, text='Quit',
                                       x=window.SCREEN_WIDTH/1.25, y=window.SCREEN_HEIGHT/4)
        button_quit.bind("<Button-1>", lambda event: quit(0))

        button_mlg = UIManager.Button(window, text='FLEX BUTTON.',
                                      x=window.SCREEN_WIDTH/9, y=window.SCREEN_HEIGHT/1.25)
        button_mlg.bind("<Button-1>", lambda event: None)

        k = 0

        def bentley_motion():
            global k
            k += 1
            IM.place('bentley', x=-10*k, y=0)
            if k == 100:
                k = 0
                IM.place('bentley', x=0, y=0)
            if window.game_is_on:
                IM.undraw('bentley')
                loop()
            else:
                window.tk.after(10, bentley_motion)

        bentley_motion()

    if window.game_is_on:
        allowed_directions = Labirinth.get_allowed_directions()  # get some restrictions to moving
        motion_x, motion_y = 0, 0

        if window.tk == window.tk.focus_get():
            x = window.tk.winfo_pointerx()-window.tk.winfo_rootx()
            y = window.tk.winfo_pointery()-window.tk.winfo_rooty()
            motion_x, motion_y = x-previous_mouse_position[0], y-previous_mouse_position[1]
            previous_mouse_position = window.SCREEN_WIDTH/2, window.SCREEN_HEIGHT/2
            window.canv.event_generate('<Motion>', warp=True, x=window.SCREEN_WIDTH/2, y=window.SCREEN_HEIGHT/2)

        if BM.isPressed('Forward'):
            if len(allowed_directions) == 0:
                player.move_along_z(player.speed, player.deviation_angle)  # if there are no restrictions
            else:
                move = True
                move_x = (player.matrix[1][0]*sin(player.deviation_angle)-player.matrix[2][0]*cos(
                    player.deviation_angle))*player.speed  # coords of mooving
                move_y = (player.matrix[1][1]*sin(player.deviation_angle)-player.matrix[2][1]*cos(
                    player.deviation_angle))*player.speed
                move_z = (player.matrix[1][2]*sin(player.deviation_angle)-player.matrix[2][2]*cos(
                    player.deviation_angle))*player.speed

                for direct in allowed_directions:
                    # give a permission to move if True by checking a direction of moving
                    if direct[0]*move_x+direct[1]*move_y+direct[2]*move_z < 0:
                        move = False
                if move:
                    player.move_along_z(player.speed, player.deviation_angle)

        if BM.isPressed('Left'):
            if len(allowed_directions) == 0:
                player.move_along_x(-player.speed)
            else:
                move = True
                move_x = player.matrix[0][0]*(-player.speed)
                move_y = player.matrix[0][1]*(-player.speed)
                move_z = player.matrix[0][2]*(-player.speed)

                for direct in allowed_directions:
                    if direct[0]*move_x+direct[1]*move_y+direct[2]*move_z < 0:
                        move = False
                if move:
                    player.move_along_x(-player.speed)

        if BM.isPressed('Backward'):
            if len(allowed_directions) == 0:
                player.move_along_z(-player.speed, player.deviation_angle)
            else:
                move = True
                move_x = (player.matrix[1][0]*sin(player.deviation_angle)-
                          player.matrix[2][0]*cos(player.deviation_angle))*(-player.speed)
                move_y = (player.matrix[1][1]*sin(player.deviation_angle)-
                          player.matrix[2][1]*cos(player.deviation_angle))*(-player.speed)
                move_z = (player.matrix[1][2]*sin(player.deviation_angle)-
                          player.matrix[2][2]*cos(player.deviation_angle))*(-player.speed)

                for direct in allowed_directions:
                    if direct[0]*move_x+direct[1]*move_y+direct[2]*move_z < 0:
                        move = False
                if move:
                    player.move_along_z(-player.speed, player.deviation_angle)

        if BM.isPressed('Right'):
            if len(allowed_directions) == 0:
                player.move_along_x(player.speed)
            else:
                move = True
                move_x = player.matrix[0][0]*player.speed
                move_y = player.matrix[0][1]*player.speed
                move_z = player.matrix[0][2]*player.speed

                for direct in allowed_directions:
                    if direct[0]*move_x+direct[1]*move_y+direct[2]*move_z < 0:
                        move = False
                if move:
                    player.move_along_x(player.speed)

        if BM.isPressed('Q'):
            if len(allowed_directions) == 0:
                player.move_along_y(player.speed)
            else:
                move = True
                move_x = player.matrix[1][0]*player.speed
                move_y = player.matrix[1][1]*player.speed
                move_z = player.matrix[1][2]*player.speed

                for direct in allowed_directions:
                    if direct[0]*move_x+direct[1]*move_y+direct[2]*move_z < 0:
                        move = False
                if move:
                    player.move_along_y(player.speed)

        if BM.isPressed('E'):
            if len(allowed_directions) == 0:
                player.move_along_y(-player.speed)
            else:
                move = True
                move_x = player.matrix[1][0]*-player.speed
                move_y = player.matrix[1][1]*-player.speed
                move_z = player.matrix[1][2]*-player.speed

                for direct in allowed_directions:
                    if direct[0]*move_x+direct[1]*move_y+direct[2]*move_z < 0:
                        move = False
                if move:
                    player.move_along_y(-player.speed)

        if BM.isPressed('ArrowUp') and player.deviation_angle <= 1.5:
            player.deviation_angle += 0.04
            player.move(transform_rot_up)

        if BM.isPressed('ArrowLeft'):
            player.move(tr_rot_left(player.deviation_angle))

        if BM.isPressed('ArrowDown') and player.deviation_angle >= -1.5:
            player.deviation_angle -= 0.04
            player.move(transform_rot_down)

        if BM.isPressed('ArrowRight'):
            player.move(tr_rot_right(player.deviation_angle))

        if motion_x != 0:
            player.move(transform_rot_x(motion_x/400, player.deviation_angle))

        if motion_y > 0 and player.deviation_angle >= -1.5:
            mot_y = motion_y
            player.deviation_angle -= mot_y/400
            player.move(transform_rot_y(mot_y/400))

        if motion_y < 0 and player.deviation_angle <= 1.5:
            mot_y = motion_y
            player.deviation_angle += -mot_y/400
            player.move(transform_rot_y(mot_y/400))

        if BM.isPressed('F'):
            SM.play('goagain')

        player.isMoving = \
            BM.isPressed('Forward') or BM.isPressed('Backward') or BM.isPressed('Left') or BM.isPressed('Right')
        if player.isMoving:
            if not SM.isPlaying('steps'):
                SM.play('steps',  start_ms=0, end_ms=29000)
        else:
            SM.stop('steps')

        window.canv.delete(UIManager.tk.ALL)

        Labirinth.update()
        Labirinth.draw()

        # canv.create_text(300, 300, text='fps: ' + str(fps))
        # canv.create_text(300, 500, text='player_crds: ' + str(player.matrix[3]))

        window.canv.update()

        counter += 1
        if counter == 10:
            fps = 10/(time.time()-fps_time_start)
            fps_time_start = time.time()
            counter = 1

        dt = int((time.time()-start_time)*1000)
        window.canv.create_text(300, 400, text='dt: '+str(dt))

        if dt >= 34:
            window.tk.after(0, loop)
        else:
            window.tk.after(34, loop)


loop()

UIManager.tk.mainloop()