from pygame.sprite import groupcollide

from bubble import *

# level bubbles
bubbles = pygame.sprite.Group()

# explosions when bubble dies
projectiles = pygame.sprite.Group()

def checkCollisions():
    #dictionary with bubbles and projectiles which collided
    #this function also removes all colliding projectiles from the list
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
def game(startGrid):
    pygame.init()
    win = pygame.display.set_mode((len(startGrid[0])*100, len(startGrid)*100))
    pygame.display.set_caption("Bubble blast")
    run = True

    #create bubble list
    for i in range(0, len(startGrid[0])):
        for j in range(0, len(startGrid)):
            bubbles.add(Bubble((100*i + 50, 100*j + 50), startGrid[j][i]))

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


startGrid = []
startGrid.append([1, 2, 1, 1])
startGrid.append([1, 2, 1, 1])
startGrid.append([1, 2, 1, 1])
startGrid.append([2, 1, 1, 2])
startGrid.append([3, 1, 3, 3])
startGrid.append([2, 1, 2, 1])


game(startGrid)