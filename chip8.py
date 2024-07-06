# Importing 
import pyglet
import random
import os
import sys

# game menu
game_choice = str()
while game_choice == str():
    os.system('cls')
    print("Choose A Game:\n1. Brick Break\n2. Connect 4\n3. Pong\n4. Tic Tac Toe\n5. To Quit")
    input_value = int(input("Enter which game to play: "))
    match input_value:
        case 1:
            game_choice = "BRIX"
        case 2:
            game_choice = "CONNECT4"
        case 3:
            game_choice = "PONG"
        case 4:
            game_choice = "TICTAC"
        case 5:
            sys.exit(0)
        case _:
            game_choice = str()
    

# Creating variables
display = [0] *2048
memory = [0] * 4096
registers = [0] * 16
index = 0
delay_timer = 0
sound_timer = 0
program_counter = 0x200
stack = []
key_inputs = [0]*16
fonts = [0xF0, 0x90, 0x90, 0x90, 0xF0, # 0
           0x20, 0x60, 0x20, 0x20, 0x70, # 1
           0xF0, 0x10d, 0xF0, 0x80, 0xF0, # 2
           0xF0, 0x10, 0xF0, 0x10, 0xF0, # 3
           0x90, 0x90, 0xF0, 0x10, 0x10, # 4
           0xF0, 0x80, 0xF0, 0x10, 0xF0, # 5
           0xF0, 0x80, 0xF0, 0x90, 0xF0, # 6
           0xF0, 0x10, 0x20, 0x40, 0x40, # 7
           0xF0, 0x90, 0xF0, 0x90, 0xF0, # 8
           0xF0, 0x90, 0xF0, 0x10, 0xF0, # 9
           0xF0, 0x90, 0xF0, 0x90, 0x90, # A
           0xE0, 0x90, 0xE0, 0x90, 0xE0, # B
           0xF0, 0x80, 0x80, 0x80, 0xF0, # C
           0xE0, 0x90, 0x90, 0x90, 0xE0, # D
           0xF0, 0x80, 0xF0, 0x80, 0xF0, # E
           0xF0, 0x80, 0xF0, 0x80, 0x80  # F
]
KEY_MAP = {pyglet.window.key._1: 0x1,
           pyglet.window.key._2: 0x2,
           pyglet.window.key._3: 0x3,
           pyglet.window.key._4: 0xc,
           pyglet.window.key.Q: 0x4,
           pyglet.window.key.W: 0x5,
           pyglet.window.key.E: 0x6,
           pyglet.window.key.R: 0xd,
           pyglet.window.key.A: 0x7,
           pyglet.window.key.S: 0x8,
           pyglet.window.key.D: 0x9,
           pyglet.window.key.F: 0xe,
           pyglet.window.key.Z: 0xa,
           pyglet.window.key.X: 0,
           pyglet.window.key.C: 0xb,
           pyglet.window.key.V: 0xf
}
window = pyglet.window.Window(width = 700 , height = 400)
image = pyglet.resource.image('pixel.png')
music = pyglet.resource.media('buzz.wav', streaming=False)

# creating batches of image
batch = pyglet.graphics.Batch()
sprites = []
for i in range(2048):
    sprites.append(pyglet.sprite.Sprite(image,batch=batch))

# Adding data into memory
# Fonts addition
for i in range(80):
    memory[i] = fonts[i]

# Instructions addition
binary = open(game_choice, "rb").read()
for i in range(len(binary)):
    memory[i+0x200] = binary[i]

# Main loop
@window.event
def on_draw():
    global program_counter
    global delay_timer
    global sound_timer
    global index
    should_draw = False

    # Instruction handling
    opcode = (memory[program_counter] << 8) | memory[program_counter + 1]
    value = (opcode & 0xf000) >> 12
    vx = (opcode & 0x0f00) >> 8
    vy = (opcode & 0x00f0) >> 4
    match value:
        case 0x0:
            value = (opcode & 0x000f)
            match value:
                case 0x0:
                    window.clear()
                case 0xE:
                    if len(stack) != 0:
                        program_counter = stack.pop()
        case 0x1:
            program_counter = (opcode & 0x0fff)
            program_counter -= 2
        case 0x2:
            stack.append(program_counter)
        case 0x3:
            if  registers[vx] == (opcode & 0x00ff):
                program_counter += 2
        case 0x4:
            if  registers[vx] != (opcode & 0x00ff):
                program_counter += 2
        case 0x5:
            if registers[vx] == registers[vy]:
                program_counter += 2
        case 0x6:
            registers[vx] = (opcode & 0x00ff)
        case 0x7:
            registers[vx] +=  (opcode & 0x00ff)
        case 0x8:
            value = (opcode & 0x000f)
            match value:
                case 0x0:
                    registers[vx] = registers[vy]
                case 0x1:
                    registers[vx] = registers[vx] | registers[vy]
                case 0x2:
                    registers[vx] = registers[vx] & registers[vy]
                case 0x3:
                    registers[vx] = registers[vx] ^ registers[vy]
                case 0x4:
                    if registers[vx] + registers[vy] > 225:
                        registers[15] = 1
                    else:
                        registers[15] = 0
                    registers[vx] = (registers[vx] + registers[vy]) & 0x00ff
                case 0x5:
                    if registers[vx] > registers[vy]:
                        registers[15] = 1
                    else:
                        registers[15] = 0
                    registers[vx] = registers[vx] - registers[vy]
                case 0x6:
                    if bin(registers[vx])[-1] == '1':
                        registers[15] = 1
                    else:
                        registers[15] = 0
                    registers[vx] = registers[vx] >> 1
                case 0x7:
                    if registers[vy] > registers[vx]:
                        registers[15] = 1
                    else:
                        registers[15] = 0
                    registers[vx] = registers[vy] - registers[vx]
                case 0xE:
                    if bin(registers[vx])[0] == '1':
                        registers[15] = 1
                    else:
                        registers[15] = 0
                    registers[vx] = registers[vx] << 1
        case 0x9:
            if registers[vx] != registers[vy]:
                program_counter += 2
        case 0xA:
            index = (opcode & 0x0fff)
        case 0xB:
            program_counter = (opcode & 0x0fff) + registers[0]
            program_counter -= 2
        case 0xC:
            registers[vx] = (random.randint(0,255) & (opcode & 0x00ff))
        case 0xD:
            registers[0xf] = 0
            for row in range(opcode & 0x000f):
                sprite = memory[index + row]
                for column in range(8):
                    if registers[vx] + column >= 64 or registers[vy] + row >= 32:
                        continue
                    binary_value = (sprite >> (7 - column)) & 1
                    if display[registers[vy] + row + (registers[vx] + column) * 32] & 1:
                        registers[0xf] = 1
                    display[registers[vy] + row + (registers[vx] + column) * 32] ^= binary_value
            should_draw = True
        case 0xE:
            value = (opcode & 0x000f)
            match value:
                case 0xE:
                    if key_inputs[registers[vx]] == 1:
                        program_counter += 2
                case 0x1:
                    if key_inputs[registers[vx]] == 0:
                        program_counter += 2
        case 0xF:
            value = (opcode & 0x00ff)
            match value:
                case 0x07:
                    registers[vx] = delay_timer
                case 0x0A:
                    i = 0
                    while i < 16:
                        if key_inputs[i] == 1:
                            registers[vx] = i
                            break
                        i += 1
                    else:
                        registers[vx] = -1
                case 0x15:
                    delay_timer = registers[vx]
                case 0x18:
                    sound_timer = registers[vx]
                case 0x1E:
                    index = index + registers[vx]
                case 0x29:
                    index = 5 * registers[vx]
                case 0x33:
                    number = registers[vx]
                    i = 2
                    while i >= 0:
                        memory[index + i] = number % 10
                        number = number // 10
                        i-=1
                case 0x55:
                    for i in range(vx+1):
                        memory[i + index] = registers[i]
                case 0x65:
                    for i in range(vx+1):
                        registers[i] = memory[i + index]
    
    # Incrementing to next instruction
    program_counter += 2

    # drawing on the screen
    if should_draw:
        for i in range(2048):
            if display[i] == 1:
                sprites[i].x = ((i - ( i % 32)) // 32) * 10
                sprites[i].y = (i % 32) * 10
                sprites[i].batch = batch
            else:
                sprites[i].batch = None
        window.clear()
        batch.draw()
        window.flip()
        should_draw = False

    # decrementing delay and sound timer
    if delay_timer > 0 :
        delay_timer -= 1

    if sound_timer > 0:
        sound_timer -= 1
        if sound_timer == 0:
            music.play()

@window.event
# checks if any of the keys is pressed or not
def on_key_press(symbol, modifiers):
    key_inputs[KEY_MAP[symbol]] = 1

@window.event
# checks if any of the keys is released or not
def on_key_release(symbol, modifiers):
    key_inputs[KEY_MAP[symbol]] = 0

pyglet.app.run()