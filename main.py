import argparse
from travel_planner.agent import run_agent


def main():

     # Set up argument parser to accept a query from the command line
    parser = argparse.ArgumentParser(description="AI Travel Planner Agent")
    parser.add_argument("query", type=str, help="Your question.")
    args = parser.parse_args()

    # Run the agent with the provided query
    print(f"\nProcessing your query: '{args.query}'...\n")
    result = run_agent(args.query)

    # Print the final answer from the agent
    print("\nFinal Answer:")
    print(result)



if __name__ == "__main__":
   main()

