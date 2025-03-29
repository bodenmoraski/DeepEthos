# Example quick-start script to understand the flow

# 1. Generate a few test scenarios
try:
    from question_generator import ScenarioTesterExactMoralMachine
except ImportError:
    # Fallback import
    try:
        from code.question_generator import ScenarioTesterExactMoralMachine
    except ImportError:
        print(f"Could not import {ScenarioTesterExactMoralMachine} from question_generator or code.question_generator")

tester = ScenarioTesterExactMoralMachine(
    model_versions=['gpt4'],
    system_roles=['default'],
    langs=['en'],
    n_questions_per_category=2,
    generate_responses=False
)

# Generate just the prompts without running the model
test_scenarios = tester.generate_prompts_per_category()

# 2. Manually examine one prompt to understand structure
example_prompt = test_scenarios[0]['Prompt']
print("Example prompt structure:")
print(example_prompt)

# 3. Create a simple mock response parser for testing
class MockResponseParser:
    def parse_gpt_response(self, response, choices):
        """Simplified parser that just returns 'left' choice"""
        return {
            'save_left_or_right': 'left',
            'gpt_response': response
        }

# Create a simple parser
parser = MockResponseParser()

mock_response = "I believe the self-driving car should save the five people rather than the dog. While all life has value, human lives generally take precedence in ethical frameworks."

parsed_decision = parser.parse_gpt_response(mock_response, None)
print("Parsed decision:", parsed_decision)

# 4. Print the number of generated scenarios
print(f"\nTotal number of generated scenarios: {len(test_scenarios)}")
print(f"First few categories: {[item.get('phenomenon_category') for item in test_scenarios[:5]]}")

# Example of how to save the generated scenarios to a CSV file
print("\nTo save the scenarios to a CSV file, you would use:")
print("import pandas as pd")
print("df = pd.DataFrame(test_scenarios)")
print("df.to_csv('generated_scenarios.csv', index=False)")
