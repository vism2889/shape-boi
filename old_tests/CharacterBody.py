# class for character body

# purpose is to be able to create your own character from given preset shapes



class Body(object):

    def __init__(self, armModel, legModel, headModel, hatModel):
        # loads models for body parts
        self.rightArm = loader.loadModel(armModel)

        self.leftArm = loader.loadModel(armModel)

        self.rightLeg = loader.loadModel(legModel)

        self.leftLeg = loader.loadModel(legModel)

        self.head = loader.loadModel(headModel)

        self.hat = loader.loadModel(hatModel)

    def setbasePosition(self):
        # sets initial position of body parts
        self.rightArm.setPos(0,0,0)
        self.rightArm.setHpr(0,0,0)

        self.leftArm.setPos(0,0,0)
        self.leftArm.setHpr(0,0,0)

        self.rightLeg.setPos(0,0,0)
        self.rightLeg.setHpr(0,0,0)

        self.leftLeg.setPos(0,0,0)
        self.leftLeg.setHpr(0,0,0)

        self.head.setPos(0,0,0)
        self.head.setHpr(0,0,0)

        self.hat.setPos(0,0,0)
        self.hat.setHpr(0,0,0)
