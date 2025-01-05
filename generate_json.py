import os
import json
import random

def create_structure_json(template_path, output_folder, mod_id, structure_name, biomes, salt, size, start_height, terrain_adaptation, spacing, separation, is_nether, is_template_pool=False):
    """
    Creates a JSON file in the 'structure' folder with specified variables.

    Args:
        template_path (str): Path to the template TXT file.
        output_folder (str): Path to the output folder (e.g., 'structure').
        mod_id (str): Value to replace the placeholder for MOD_ID.
        structure_name (str): Value to replace the placeholder for STRUCTURE_NAME.
        biomes (str): Value to replace the placeholder for BIOMES.
    """
    # Load the template TXT
    with open(template_path, 'r') as template_file:
        template_str = template_file.read()

    # Replace placeholders with the provided values
    template_str = template_str.replace("<MOD_ID>", mod_id)
    template_str = template_str.replace("<STRUCTURE_NAME>", structure_name)
    template_str = template_str.replace("<BIOMES>", biomes)
    template_str = template_str.replace("<SALT>", salt)
    template_str = template_str.replace("<RADIUS>", str(size[0]))
    template_str = template_str.replace("<RANGE>", str(size[1]))
    template_str = template_str.replace("<START_HEIGHT>", start_height)
    template_str = template_str.replace("<TERRAIN_ADAPTATION>", terrain_adaptation)
    template_str = template_str.replace("<SPACING>", str(spacing))
    template_str = template_str.replace("<SEPARATION>", str(separation))
    template_str = template_str.replace("<NETHER>", "_nether" if is_nether else "")

    # Convert the modified string to a Python dictionary
    modified_json = json.loads(template_str)

    # Create the 'structure' folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)

    # Define the output file path
    if is_template_pool:
        output_file_path = os.path.join(output_folder, f"{structure_name}_start_pool.json")
    else:
        output_file_path = os.path.join(output_folder, f"{structure_name}.json")

    # Save the modified JSON
    with open(output_file_path, 'w') as output_file:
        json.dump(modified_json, output_file, indent=4)
    
    print(f"\033[92mJSON file created: {output_file_path}\033[0m")

def generate_integer_string():
    # Generate the first digit (1-9)
    first_digit = random.randint(1, 9)
    # Generate the remaining 8 digits (0-9)
    remaining_digits = [random.randint(0, 9) for _ in range(8)]
    # Combine the digits into a single string
    integer_string = str(first_digit) + ''.join(map(str, remaining_digits))
    return integer_string

def define_spacing(size):
    # outputs two variables based on size (small, medium, large, custom)
    if size == "small":
        radius = 1
        range = 3
    elif size == "medium":
        radius = 3
        range = 5
    elif size == "large":
        radius = 5
        range = 8
    else:
        radius = int(input("Enter custom radius: "))
        range = int(input("Enter custom range: "))
    return [radius, range]

def define_start_height(start_height):
    # outputs a variable based on start_height
    if " to " in start_height:
        start_height = start_height.split(" to ")
        return f'{{"type": "minecraft:uniform", "max_inclusive": {{"absolute": {start_height[1]}}}, "min_inclusive": {{"absolute": {start_height[0]}}}}}'
    elif isinstance(start_height, (int, float)) or start_height.lstrip('-').isdigit():  # else is a single number
        return f'{{"absolute": {start_height}}}'
    else:  # return error to console
        raise ValueError("Invalid start_height format. Expected 'number' or 'number to number'.")

def define_rarity(rarity):
    # outputs spacing and separation based on rarity (1 most - 10 least common)
    # the whole integer values should be randomized by +-10%
    # the most common structures should have spacing of ~20 and separation of ~5
    # the rarest structures should have a spacing of ~120 and separation of ~20
    # most structures should be between 30-60 and 20-50
    # the spacing must always be the highest int

    if not (1 <= rarity <= 10):
        raise ValueError("Rarity must be between 1 and 10")

    # Define base values for spacing and separation
    base_spacing = 20 + (rarity - 1) * 10
    base_separation = 5 + (rarity - 1) * 2

    # Apply randomization of +-10%
    spacing = int(base_spacing * random.uniform(0.9, 1.1))
    separation = int(base_separation * random.uniform(0.9, 1.1))

    # Ensure spacing is always higher than separation
    if spacing <= separation:
        spacing = separation + 5

    return spacing, separation

# Main function to get user input and create JSON files
def main():
    mod_id = input("\nEnter mod_id: ")
    output_base_folder = os.path.join("output", mod_id.upper())  # Base folder where the JSON will be saved

    while True:
        print("\n--- New Structure Settings ---")
        biomes = input("Enter biomes: ")
        structure_name = input("Enter structure name: ")
        size = define_spacing(input("Enter size (small, medium, large, custom): "))
        start_height = define_start_height(input("Enter start height (e.g., '0' or '0 to 10'): "))
        terrain_adaptation = input("Enter terrain adaptation: (none, beard_thin, beard_box, bury, encapsulate): ")
        rarity = int(input("Enter rarity (1-10): "))
        spacing, separation = define_rarity(rarity)
        is_nether = input("Is this structure in the nether? (y/n): ").lower() == "y"

        while True:
            salt = generate_integer_string()
            for template_path, subfolder in template_paths.items():
                output_folder = os.path.join(output_base_folder, subfolder)
                is_template_pool = subfolder == "template_pool"
                create_structure_json(template_path, output_folder, mod_id, structure_name, biomes, salt, size, start_height, terrain_adaptation, spacing, separation, is_nether, is_template_pool)

            another_same_settings = input("\nDo you want to create another structure with the same settings? (y/n): ").lower()
            if another_same_settings != "y":
                break
            structure_name = input("Enter new structure name: ")

        another = input("\nDo you want to create another structure with different settings? (y/n): ").lower()
        if another != "y":
            break

# Example usage
template_paths = {
    "templates/template_structure.txt": "structure",
    "templates/template_structure_set.txt": "structure_set",
    "templates/template_template_pool.txt": "template_pool"
}

if __name__ == "__main__":
    main()
