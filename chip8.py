# basic imports
import time 
import os
import random

# chip - 8 variables
display = [[0 for _ in range(64)] for _ in range(32)]
memory = [0] * 4096
registers = [0] * 16
index = 0
delay_timer = 0
sound_timer = 0
program_counter = 0x200
stack = []


# feeding values to the memory
with open("c8_test.c8","rb") as file:
    data = file.read()
for info in range(0,len(data)):
        memory[info + 0x200] = data[info]

# main cycle
while True:
    increment = 2
    opcode = (memory[program_counter] << 8) | memory[program_counter + 1] 
    hex_opcode = hex(opcode)
    value = (opcode & 0xf000) >> 12
    vx = (opcode & 0x0f00) >> 8
    vy = (opcode & 0x00f0) >> 4
    match value:
        case 0x0:
            value = (opcode & 0x000f)
            match value:
                case 0x0:
                    display = [[0 for _ in range(64)] for _ in range(32)]
                case 0xE:
                    if len(stack) != 0:
                        program_counter = stack.pop()
        case 0x1:
            program_counter = (opcode & 0x0fff)
            increment = 0
        case 0x2:
            stack.append(program_counter)
        case 0x3:
            if  registers[vx] == (opcode & 0x00ff):
                increment = 4
        case 0x4:
            if  registers[vx] != (opcode & 0x00ff):
                increment = 4
        case 0x5:
            if registers[vx] == registers[vy]:
                increment = 4
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
                increment = 4
        case 0xA:
            index = (opcode & 0x0fff)
        case 0xB:
            program_counter = (opcode & 0x0fff) + registers[0]
            increment = 0
        case 0xC:
            registers[vx] = (random.randint(0,255) & (opcode & 0x00ff))
        case 0xD:
            for row in range(opcode & 0x000f):
                sprite = str(bin(memory[index + row]))[2:]
                for i in range(8):
                    if registers[vx] + row >= 0 and registers[vx] + row <= 31 and registers[vy] + i >= 0 and registers[vy] + i <= 61: 
                        display[registers[vx] + row][registers[vy] + i] = int(sprite[i])
        case 0xE:
            value = (opcode & 0x000f)
            match value:
                case 0xE:
                    pass
                case 0x1:
                    pass
        case 0xF:
            value = (opcode & 0x00ff)
            match value:
                case 0x07:
                    registers[vx] = delay_timer 
                case 0x0A:
                    registers[vx] = input("Enter value")
                case 0x15:
                    delay_timer = registers[vx]
                case 0x18:
                    sound_timer = registers[vx]
                case 0x1E:
                    index = index + registers[vx]
                case 0x29:
                    pass
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
    program_counter += increment
    os.system("cls")
    for i in display:
        for j in i:
            if j == 1:
                print(" ",end=" ")
            else:
                print("O",end=" ")
        print()
    print("opcode", hex(opcode))
    time.sleep(1/60)