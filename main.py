from pygame.sprite import groupcollide

from bubble import *

# level bubbles
bubbles = pygame.sprite.Group()

# explosions when bubble dies
projectiles = pygame.sprite.Group()

def checkCollisions():
    ballsHit = groupcollide(bubbles, projectiles, False, True)

    for bubble in ballsHit.items():
        newExplosion = bubble[0].hit()

        if newExplosion != None:
            bubbles.remove(bubble[0])

            projectiles.add(newExplosion[0][0])
            projectiles.add(newExplosion[0][1])
            projectiles.add(newExplosion[0][2])
            projectiles.add(newExplosion[0][3])


#Project main loop
def main():
    pygame.init()
    win = pygame.display.set_mode((800, 800))
    pygame.display.set_caption("Bubble blast")
    run = True

    #create bubble list
    for i in range(0, 5):
        for j in range(0, 5):
            bubbles.add(Bubble((100*i + 50, 100*j + 50), 4))

    while run:
        #check mouse events
        for event in pygame.event.get():

            #check mouse click on exit button
            if event.type == pygame.QUIT:
                run = False

            #check mouse click on bubble
            if event.type == pygame.MOUSEBUTTONUP:
                for bubble in bubbles:
                    if bubble.rect.collidepoint(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]):
                        #if bubble is clicked, make it get hit
                        newExplosion = bubble.hit()

                        #if bubble dies, add explosions
                        if newExplosion != None:
                            bubbles.remove(bubble)

                            projectiles.add(newExplosion[0][0])
                            projectiles.add(newExplosion[0][1])
                            projectiles.add(newExplosion[0][2])
                            projectiles.add(newExplosion[0][3])


        #update bubbles, projectiles
        bubbles.update()
        projectiles.update()

        #check collisions between projectiles and bubbles
        checkCollisions()

        # draw all entities
        bubbles.draw(win)
        projectiles.draw(win)

        #update whole screen
        pygame.display.flip()

        #fill background
        win.fill((0, 0, 0))


    pygame.quit()

main()