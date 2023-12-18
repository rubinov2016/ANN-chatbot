# Guide to work with the chatbot

1. To launch the chatbot, execute the "chatbot.py" script.

2. The chatbot will display the intent tag and its corresponding probability, like this: {"intent": "Netherlands", "probability": "0.998"}. This means that the intent is "Netherlands," and the probability is 0.998.

3. If the probability is low and the intent tag is incorrect, follow these steps:
3.1. Modify the "intents.json" file and add the same question to the "patterns" section of the corresponding intent tag. For example, if you asked "the Senegal games" and received an incorrect response with a low probability, you can add "the Senegal games" to the JSON file:
   
   ![image](https://github.com/rubinov2016/ANN-chatbot/assets/24795926/0bd3aa17-f754-470e-877a-bbdfb8e57167)

Then, retrain the chatbot by:
    Running "training.py"
    Running "chatbot.py"
3.2. If the issue persists, please communicate it with your colleagues. We will collectively decide on the next course of action.


5. Regarding collocations or double words, some phrases are treated as separate words by default (e.g., "Group A" or "South America"). To treat them as a single word, you can use underscores during training (e.g., "Group_A"). During training, the program creates a mapping table like this:
   
  ![image](https://github.com/rubinov2016/ANN-chatbot/assets/24795926/670cc393-5236-49b7-bda4-5f90182e1ae2)
  
  When a user inputs "Group A," it will automatically convert to "group_a."

6. You don't need to be concerned about capitalization. The program converts messages and patterns from the JSON file to lowercase, so "Senegal" becomes "senegal."
  Don't convert the answers or responses to lowercase:
  
  ![image](https://github.com/rubinov2016/ANN-chatbot/assets/24795926/f545e9ca-125f-45d4-a0c1-d3c068124986)

