# Guide to working with the chatbot

1. Use Google Sheets to get your questions. 
    - "Rules3",  Current tab with Responsible person
    - "Rules Updated" automatically filled tab with latest changes from the all group members
    
    - Use convert_json.py to download/upload your changes
    
    - The easiest way is to use just functions merge_json and comment json files that you don't need

2. To launch the chatbot, execute the "chatbot.py" script.

3. The chatbot will display the intent tag and its corresponding probability, like this: {"intent": "Netherlands", "probability": "0.998"}. This means that the intent is "Netherlands," and the probability is 0.998.

4. How to improve accuracy? If the probability is low and the intent tag is incorrect, follow these steps:

![image](https://github.com/rubinov2016/ANN-chatbot/assets/24795926/a823ce3d-6f7f-4192-98fa-7942d417d0a5)

3.1. The main method is to add all possible questions to patterns
Modify the "intents.json" file and add the same question to the "patterns" section of the corresponding intent tag. For example
![image](https://github.com/rubinov2016/ANN-chatbot/assets/24795926/34bd5aa9-81bf-40ef-bd93-cdcedccda09c)

3.2. Then, retrain the chatbot by:
    Running "training.py"
    Running "chatbot.py"

3.3. Ask the same question. If the problem resolved, you can move to another rule (tag, class of questions)
![image](https://github.com/rubinov2016/ANN-chatbot/assets/24795926/23a18dbb-186e-4784-b42c-d22436a2f914)

3.2. If the issue remains, please communicate it with your colleagues. 
We will collectively decide on the next course of action.

4. RULES FOR UNDERSCORE
   Regarding collocations or double words, some terms should treated as joint words (e.g., "Group A" or "South America").
   To treat them as a single object, you can use underscores during training (e.g., "Group_A").
   During training, the program creates a mapping table like this:
   ![image](https://github.com/rubinov2016/ANN-chatbot/assets/24795926/670cc393-5236-49b7-bda4-5f90182e1ae2)

When a user inputs "Group A," it will automatically convert to "group_a."

6. You don't need to be concerned about capitalization.
   The program converts messages and patterns from the JSON file to lowercase, so "Senegal" becomes "senegal."
  Don't convert the answers or responses to lowercase:
  
  ![image](https://github.com/rubinov2016/ANN-chatbot/assets/24795926/f545e9ca-125f-45d4-a0c1-d3c068124986)



