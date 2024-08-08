import openai
from langchain.chat_models import ChatOpenAI

# Set up your OpenAI API key
openai.api_key = "<API key>"

# Define the custom prompt
prompt = """
Language Model: NER with Langchain

User: Please identify the source station and destination station from the user text.

Text: "{text}" 


Language Model:
"""

# Define the completion function
def complete(prompt):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=100,
        temperature=0.5,
        n=1,
        stop=None
    )
    return response.choices[0].text.strip()

# Define the NER function
def perform_ner(text):
    full_prompt = f'{prompt}Perform NER on "{text}"\n'
    response = complete(full_prompt)
    return response

# Function to extract source station and destination station from NER result
def extract_station_names(ner_result):
    # Split the NER result into individual words
    words = ner_result.split()
    # Extract the source station and destination station
    global source_station, destination_station
    source_station = words[3].strip(",")
    destination_station = words[6].strip(",")
    # Convert the values to strings
    source_station = str(source_station)
    destination_station = str(destination_station)

# Example usage
text = "I wanna go from Puri to Bhubaneswar"
ner_result = perform_ner(text)
extract_station_names(ner_result)

# Access the values of source_station and destination_station
print("Source Station:", source_station)
print("Destination Station:", destination_station)

import pandas as pd
import networkx as nx

# Read the CSV file containing the train data
train_data = pd.read_csv('finalds.csv')

# Create a directed graph
G = nx.DiGraph()

# Add edges to the graph based on the train data
for _, row in train_data.iterrows():
    source = row['Source Station']
    destination = row['Destination Station']
    train_name = row['Train Name']
    distance = row['Distance']
    G.add_edge(source, destination, train=train_name, distance=distance)

    # Check if the source_station and destination_station exist in the graph
if source_station not in G.nodes:
    print("Source station not found in the train data.")
    exit()
if destination_station not in G.nodes:
    print("Destination station not found in the train data.")
    exit()

# Find the shortest path between the source_station and destination_station
try:
    shortest_path = nx.shortest_path(G, source_station, destination_station, weight='distance')
except nx.NetworkXNoPath:
    print("No path found between the source and destination stations.")
    exit()

# Get the train names along the shortest path
train_names = [G.edges[edge]['train'] for edge in zip(shortest_path[:-1], shortest_path[1:])]

# Print the train names
print("Trains from", source_station, "to", destination_station, "via the shortest path:")
for train_name in train_names:
#   print(train_name)
# Define the custom prompt
    prompt_2 = """
    Language Model:
    Your task is to perform the following action:
    Get all the train names in the variable {train_name}. Then give the names of the trains in {train_name} as output in a human-friendly sentence.
    Example:
    Input: {train_name} = Purushottam Express, Bhubaneswar Duronto Express
    Give Output similar to: To go from Puri to Bhubaneswar via the shortest path, we need to take {train_name}.
    """

    # Define the completion function
    def complete_prompt2(prompt_2, train_name):
        full_prompt = prompt_2.format(train_name=train_name)
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=full_prompt,
            max_tokens=100,
            temperature=0.5,
            n=1,
            stop=None
        )
        return response.choices[0].text.strip()

    # Example usage
    train_name = ", ".join(train_names)  # Convert the train names to a comma-separated string
    output = complete_prompt2(prompt_2, train_name)

    # Print the output
    print("Output:", output)


