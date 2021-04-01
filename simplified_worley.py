import pygame
import sys
import numpy as np
from numba import jit
SCREEN_SIZE = WIDTH, HEIGHT = 400, 400

@jit(nopython = True)
def calc_rgb_noise(pixel_array, indexes):
    points = np.random.randint(-100,WIDTH+100,(20,2))
    noise_values = np.empty((WIDTH,HEIGHT,3))
    for pixel in pixel_array:
        delta = pixel-points
        distances = np.sqrt(np.sum(delta*delta, axis=1))
        distances = np.sort(distances)
        for i in range(3):
            noise_values[pixel[0]][pixel[1]][i] = distances[indexes[i]]#/(indexes[i]+2)   
    noise_values /= WIDTH//2
    noise_values  *= 255
    for i, val in np.ndenumerate(noise_values):
        if val > 255:
            noise_values[i] = 255
    return noise_values

if __name__ == '__main__':
    pygame.init()
    window = pygame.display.set_mode(SCREEN_SIZE)
    pixel_array = np.array([x[0] for x in np.ndenumerate(pygame.surfarray.pixels_blue(window))])
    clock = pygame.time.Clock()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                print('Exiting')
                sys.exit()
        rgb_noise_map = calc_rgb_noise(pixel_array,np.random.randint(0,4,3))
        #rgb_noise_map = calc_rgb_noise(pixel_array,(0,0,0))
        pygame.surfarray.blit_array(window,rgb_noise_map)
        pygame.display.update()
        clock.tick()
        print(clock.get_time())
