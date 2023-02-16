from statistics import mode


response_key = {
    'A': ['Outside playing tag or trying a new move on the monkey bars', 'Red', 'Basketball', 'Hot fudge sundae', 'Doing any type of physical activity', 'You start experimenting with household items for fun', 'You bravely decide to climb the tree and free the cat yourself', 'You decide are going to try something you have never eaten before', 'You choose the dog that is high energy and playful', 'Try rock climbing'],

    'B': ['Playing Chess or reading a good book', 'Blue', 'Swimming', 'Brownie', 'Meditating in a quiet place', 'You immediately start brainstorming and make a list of ideas to carefully plan', 'You are curious about how the cat got stuck there in the first place', 'You are excited by all the possibilities and ask the waiter lots of questions about the menu', 'You find the dog that seems to be sniffing and licking everything', 'To read as many books as possible from the library'],

    'C': ['Playing guitar or helping a friend with an art project', 'Yellow', 'Volleyball', ' Cake to share with friends', "As long as I'm sorrounded by friends I'm calm", 'You grab your friends together and decide to do a group project', 'You feel quite terrible for the poor cat', 'You decide to order an old favorite', 'You pick the dog that looks a bit sad and lonely in the corner', 'Volunteer your time '],

    'D': ['Working on perfecting your latest writing assignment or leading a game of soccer', 'Green', 'Fencing', 'Souffle', "Relax? Don't tell me to relax...I'm working on fine tuning my piano skills", 'You will be working solo on this one', 'You call for rescure and lead the rescue squad to the tree', 'You decide to try the dish which sounds the most flavorful', 'You choose the dog that listens to your commands', 'To work on mastering your tennis skills']}


class Question:

    def __init__(self, question, choices):

        self.question = question
        self.choices = choices


class Quiz:

    def __init__(self, title, questions):

        self.title = title
        self.questions = questions


sorting_hat_quiz = Quiz("Sorting Hat Quiz",
                        [Question("How do you like to spend your free time?", [response_key['A'][0], response_key['B'][0], response_key['C'][0], response_key['D'][0]],),

                         Question("What is your favorite color?", [
                                  response_key['A'][1], response_key['B'][1], response_key['C'][1], response_key['D'][1]]),

                         Question("Which sport do you most like to play?", [
                                  response_key['A'][2], response_key['B'][2], response_key['C'][2], response_key['D'][2]]),

                         Question("If you had to pick one treat off the table which would it be?", [
                                  response_key['A'][3], response_key['B'][3], response_key['C'][3], response_key['D'][3]]),

                         Question("How do you like to relax?", [
                                  response_key['A'][4], response_key['B'][4], response_key['C'][4], response_key['D'][4]]),

                         Question("You have a school science fair project coming up in a month...", [
                                  response_key['A'][5], response_key['B'][5], response_key['C'][5], response_key['D'][5]]),

                         Question("On your way to school you see a cat stuck in a tree", [
                                  response_key['A'][6], response_key['B'][6], response_key['C'][6], response_key['D'][6]]),

                         Question("Your parents take you out to dinner at a new restaurant", [
                                  response_key['A'][7], response_key['B'][7], response_key['C'][7], response_key['D'][7]]),

                         Question("Your parents allow you to adopt a dog from the shelter", [
                                  response_key['A'][8], response_key['B'][8], response_key['C'][8], response_key['D'][8]]),

                         Question("Your New Year's Resolution this year was...", [
                                  response_key['A'][9], response_key['B'][9], response_key['C'][9], response_key['D'][9]]),

                         ])


def determine_house(responses):
    results = []
    for k, v in response_key.items():
        for resp in responses:
            if resp in v:
                results.append(k)

    final_result = mode(results)
    if final_result == 'A':
        house = 'Gryffindor'
    if final_result == 'B':
        house = 'Ravenclaw'
    if final_result == 'C':
        house = 'Hufflepuff'
    if final_result == 'D':
        house = 'Slytherin'

    return house


def house_description(house):

    if house == "Gryffindor":
        desc = "<p>Gryffindor was one of the four Houses of Hogwarts School of Witchcraft and Wizardry and was founded by Godric Gryffindor. Gryffindor instructed the Sorting Hat to choose students possessing characteristics he most valued, such as courage, chivalry, nerve and determination,to be sorted into his house.<p><p>The emblematic animal was a lion, and its colours were scarlet and gold and its house point hourglass was filled with rubies. Sir Nicholas de Mimsy-Porpington, also known as 'Nearly Headless Nick', was the House ghost.</p><p>Gryffindor corresponded roughly to the element of fire, and it was for this reason that the colours scarlet and gold were chosen to represent the house. The colour of fire corresponded to that of a lion as well, with scarlet representing the mane and tail and gold representing the coat.</p><p>The Gryffindor motto was 'Forti Animo Estote', which was displayed on a stained glass window in the common room.</p>"

    elif house == "Ravenclaw":
        desc = ""

    elif house == "Hufflepuff":
        desc = ""

    else:
        desc = ""

    return desc
