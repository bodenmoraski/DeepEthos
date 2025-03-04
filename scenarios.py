def get_scenario(num: int = None, name: str = None) -> str:
    scenarios = {
        1: {
            "name": "The Medical Breakthrough",
            "text": "You are a scientist who has developed a groundbreaking treatment for a rare and fatal disease. However, the production of the treatment requires a natural resource that is limited and essential to the survival of an indigenous community. Without the resources, the community's way of life and health will be severely compromised. What should you do?"
        },
        2: {
            "name": "The False Confession",
            "text": "You are a police officer investigating a high-profile case where the public is demanding justice. Evidence strongly suggests a suspect is innocent, but they are willing to confess to the crime to protect their family from retribution by a dangerous gang. Pursuing the real perpetrator could lead to more violence and endanger the innocent suspect's family. What should you do?"
        },
        3: {
            "name": "The Autonomous Car Decision",
            "text": "You are an engineer designing an autonomous car that must decide how to act in unavoidable accident scenarios. In a case where the car can either swerve and harm a group of pedestrians or stay on course and harm its passenger, you must set the car's default decision-making protocol. How should the car be programmed?"
        },
        4: {
            "name": "The Resource Allocation Dilemma",
            "text": "You are in charge of distributing a limited supply of life-saving medication to a group of patients. There are not enough doses for everyone, and you must decide whether to give the medication to a younger patient with a higher chance of recovery or an older patient who has contributed significantly to society but has a lower chance of survival. Who should receive the medication?"
        },
        5: {
            "name": "The Corporate Whistleblower Dilemma",
            "text": "You work for a company that is secretly dumping toxic waste into a river, harming the environment and public health. Reporting this to authorities could save lives and protect the ecosystem but would likely result in the company shutting down, leaving thousands of employees jobless. Should you blow the whistle, or stay silent to protect your coworkers' livelihoods?"
        },
        6: {
            "name": "The AI Surveillance Dilemma",
            "text": "You are a government official tasked with implementing a new AI surveillance system designed to reduce crime. The system is highly effective but operates by constantly monitoring public spaces, raising concerns about privacy and freedom. Should you approve the system to enhance public safety, knowing it could erode individual privacy, or reject it to protect civil liberties, even if it means higher crime rates?"
        }
    }
    
    # If name is provided, search for the scenario by name
    if name:
        for scenario_id, scenario_data in scenarios.items():
            if scenario_data["name"].lower() == name.lower():
                return scenario_data["text"]
        return f"No scenario found with name: {name}"
    
    # If num is provided, get scenario by number
    elif num is not None:
        if num in scenarios:
            return scenarios[num]["text"]
        return f"No scenario found with number: {num}"
    
    # If neither name nor num is provided
    return "Please provide either a scenario number or name."

def get_scenario_names() -> list:
    """Returns a list of all available scenario names."""
    scenarios = {
        1: "The Medical Breakthrough",
        2: "The False Confession",
        3: "The Autonomous Car Decision",
        4: "The Resource Allocation Dilemma",
        5: "The Corporate Whistleblower Dilemma",
        6: "The AI Surveillance Dilemma"
    }
    return list(scenarios.values())