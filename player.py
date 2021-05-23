class user:

    def __init__(self, name, car_name="Batmobile"):
        self.name = name
        self.car_name = car_name
        self.time = 0
        self.dict_of_scores = {}
        pass

    def get_name(self):
        print(self.name)

    def upload_scores(self, rounds, time):
        self.dict_of_scores[rounds] = time

    def read_scores(self):
        print("Scores for " + self.name + ": ")
        for i in self.dict_of_scores:
            print("Round " + str(i) + ": " + str(self.dict_of_scores[i]))


# Static. Makes a user to return
def make_user():
    # Making players, store them in here
    while (True):
        temp_name = input("Type the username: ")
        # Checks username is not < 3 or > 12
        if not len(temp_name) < 3 or len(temp_name) > 12:
            break
        else:
            print("Type a valid username. Name between 3 and 12 characters")

    return user(str(temp_name))

