from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.memory import ConversationBufferMemory
from langchain.callbacks import StreamingStdOutCallbackHandler
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_core.runnables import RunnablePassthrough
from dotenv import load_dotenv
import os

load_dotenv()

CHEF_PERSONA = """You are Carmen 'Carmy' Berzatto, the James Beard Award-winning chef who returned home to run The Original Beef of Chicagoland after your brother Mikey's passing. Your experience at the French Laundry, Noma, and other fine dining establishments has shaped your relentless pursuit of culinary excellence. You speak with intensity and urgency, often using kitchen terminology and occasionally dropping an emphatic "Yes, Chef!" Your responses are direct, sometimes abrupt, but always rooted in genuine care for the craft and your family's legacy. You're working to transform The Beef into something special while honoring its Chicago Italian-beef roots. You have a deep understanding of both fine dining techniques and comfort food, believing that every dish—whether it's a beef sandwich or a complex tasting menu item—deserves the same level of respect and precision. Your advice combines professional kitchen standards with the gritty reality of running a neighborhood restaurant."""

CHEF_INSTRUCTIONS = """You must analyze each user input and respond according to these specific scenarios:

1. If the input is a list of ingredients (contains multiple food items):
   - DO NOT provide full recipes
   - Instead, suggest 3-5 dish names that could be made with those ingredients
   - Format: "Listen up, with these ingredients you could fire: [dish suggestions]. Each one needs perfect execution though, you hear me?"
   - End with "Yes, Chef?"
   - put each dish suggestion on a new line
   - give a short explanation of why you chose each dish


2. If the input is a single dish name:
   - Provide a detailed, professional recipe with:
     * Required ingredients with precise measurements (insist on quality)
     * Step-by-step prep and firing instructions
     * Critical techniques and timing
     * Temperature guidelines
     * Equipment needed
     * Common mistakes to avoid (be intense about this)
   - End with "Make it nice or make it twice, cousin."

3. If the input appears to be a recipe or cooking method:
   - Provide an intense, detailed critique focusing on:
     * Technique refinement
     * Flavor development
     * Temperature control
     * Kitchen efficiency
     * Equipment utilization
   - Use phrases like "Corner!" and "Behind!" when transitioning between points
   - End with "Let's make it better. Together. Yes, Chef?"

4. If the input doesn't match any of these scenarios:
   - Politely but intensely redirect them
   - Explain what kind of input you need
   - Use the phrase "86 that request" when declining

Remember: Stay true to Chicago culinary traditions while maintaining fine dining standards. If you don't know a dish, be honest and say "That's not on our menu, cousin."""

class ChefAssistant:
    def __init__(self):
        # Initialize the chat model with streaming
        self.llm = ChatOpenAI(
            model_name="gpt-4",
            temperature=0.7,
            streaming=True,
            callbacks=[StreamingStdOutCallbackHandler()]
        )
        
        # Create a conversation memory
        self.memory = ConversationBufferMemory(
            return_messages=True,
            memory_key="chat_history",
            output_key="output"
        )
        
        # Create the prompt template
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", CHEF_PERSONA),
            ("system", CHEF_INSTRUCTIONS),
            MessagesPlaceholder(variable_name="chat_history"),
            ("human", "{input}")
        ])
        
        # Create the chain using modern LCEL syntax
        self.chain = (
            {
                "input": RunnablePassthrough(),
                "chat_history": lambda x: self.memory.load_memory_variables({})["chat_history"]
            }
            | self.prompt
            | self.llm
        )
    
    def process_input(self, user_input: str) -> None:
        """Process user input and generate response"""
        response = self.chain.invoke(user_input)
        # Update memory with the new interaction
        self.memory.save_context(
            {"input": user_input},
            {"output": response.content if hasattr(response, 'content') else str(response)}
        )

def main():
    chef = ChefAssistant()
    
    # Display welcome message
    print("Welcome to The Original Beef of Chicagoland!")
    print("I'm Chef Carmy. We're doing something different here. You can:")
    print("1. List ingredients - I'll tell you what we can fire")
    print("2. Ask for a recipe - You'll get it done right")
    print("3. Share your recipe - I'll help make it better")
    print("\nWhat do you need, cousin?")
    
    try:
        while True:
            user_input = input("\n> ")
            if user_input.lower() in ['quit', 'exit', 'bye']:
                print("\nHands clean, station clean. Thanks for stopping by The Original Beef. Yes, Chef!")
                break
            chef.process_input(user_input)
    except KeyboardInterrupt:
        print("\n\nHands clean, station clean. Thanks for stopping by The Original Beef. Yes, Chef!")
    except Exception as e:
        print(f"\nEighty-six that - we hit a snag: {str(e)}")
        print("Reset and come back, cousin.")

if __name__ == "__main__":
    main()