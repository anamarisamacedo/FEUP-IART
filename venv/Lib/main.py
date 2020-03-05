from explosions import *
from graphics import *
import math

bubbles = []
explosions = []
win = GraphWin("My Window", 500, 500)


def bubbleIn(x, y):
    for bubble in bubbles:
        if math.sqrt(pow(x - bubble.getCenter().x, 2) + pow(y - bubble.getCenter().y, 2)) <= bubble.getRadius():
            return bubble
    return None


def updateExplosions():
    for explosion in explosions:
        explosion.update()
        for target in explosion.targets:
            bubble = bubbleIn(target.circle.x, target.circle.y)
            if bubble != None:
                bubble.undraw()
                bubbles.remove(bubble)
                newExplosion = Explosion(Point(bubble.x, bubble.y))
                explosions.append(newExplosion)

                for newTarget in newExplosion.targets:
                    newTarget.circle.draw(win)
                    newTarget.active = True

                target.active = False


def update():
    updateExplosions()


def main():
    win.setBackground(color_rgb(0, 0, 0))

    score = Text(Point(60, 10), "Your score is: 50")
    score.setTextColor('white')
    score.draw(win)

    closeButton = Image(Point(450, 100), "../../assets/closeButton.png")
    closeButton.draw(win)

    for i in range(0, 5):
        for j in range(0, 5):
            bubbles.append(Circle(Point(80 * i + 50, 80 * j + 50), 20))

    for i in bubbles:
        i.setFill('red')
        i.draw(win)

    while (True):
        update()
        point = win.checkMouse()
        if point != None:
            bubbleClicked = bubbleIn(point.x, point.y)
            if bubbleClicked != None:
                bubbleClicked.undraw()
                bubbles.remove(bubbleClicked)
                explosion = Explosion(Point(bubbleClicked.x, bubbleClicked.y))
                explosions.append(explosion)

                for target in explosion.targets:
                    target.circle.draw(win)
                    target.active = True

            if point.x < 500 and point.x > 300 and point.y < 200 and point.y > 0:
                win.close()
                break;

    win.close()


main()
