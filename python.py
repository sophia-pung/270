from bs4 import BeautifulSoup

# Define the electoral data for the 2020 election
state_results = {
    "WI": {"trump": 47, "biden": 47},
    "ME": {"trump": 35.9, "biden": 47.2},
    "CT": {"trump": 38.8, "biden": 49.9},
    "IL": {"trump": 33.5, "biden": 46.0},
    "OR": {"trump": 40.0, "biden": 52.0},
    "NY": {"trump": 37.0, "biden": 50.8},
    "RI": {"trump": 33.0, "biden": 49.6},
    "HI": {"trump": 38.0, "biden": 57.0},
    "VA": {"trump": 39.0, "biden": 47.4},
    "MN": {"trump": 42, "biden": 44},
    "CA": {"trump": 33.2, "biden": 55.3},
    "MD": {"trump": 33.2, "biden": 57.9},
    "MA": {"trump": 25.4, "biden": 53.1},
    "VT": {"trump": 28.4, "biden": 57.7},
    "WA": {"trump": 42.5, "biden": 46.9},
    "NH": {"trump": 44.4, "biden": 51.2},
    "CO": {"trump": 39.8, "biden": 46.7},
    "NM": {"trump": 41.1, "biden": 48.6},
    "NJ": {"trump": 38.6, "biden": 46.6},
    "PA": {"trump": 46, "biden": 43},
    "MI": {"trump": 46, "biden": 44},
    "OH": {"trump": 50.8, "biden": 39.9},
    "IA": {"trump": 48.5, "biden": 36.3},
    "AK": {"trump": 52.9, "biden": 38.6},
    "KS": {"trump": 46.2, "biden": 31.9},
    "MO": {"trump": 48.8, "biden": 33.1},
    "SC": {"trump": 51.3, "biden": 35.6},
    "LA": {"trump": 51.5, "biden": 35.5},
    "IN": {"trump": 53.9, "biden": 34.4},
    "AL": {"trump": 56.1, "biden": 36.1},
    "MS": {"trump": 54.5, "biden": 35.5},
    "MT": {"trump": 53.3, "biden": 32.8},
    "UT": {"trump": 50.6, "biden": 29.8},
    "NE": {"trump": 57.3, "biden": 33.5},
    "OK": {"trump": 57.7, "biden": 32.6},
    "TN": {"trump": 57.3, "biden": 31.5},
    "KY": {"trump": 55.0, "biden": 28.4},
    "ID": {"trump": 53.5, "biden": 26.8},
    "SD": {"trump": 54.4, "biden": 27.3},
    "AZ": {"trump": 46, "biden": 42},
    "AR": {"trump": 56.2, "biden": 24.9},
    "WV": {"trump": 58.2, "biden": 23.8},
    "ND": {"trump": 53.2, "biden": 17.8},
    "GA": {"trump": 48, "biden": 42},
    "NC": {"trump": 45, "biden": 39},
    "WY": {"trump": 67.2, "biden": 15.9},
    "NV": {"trump": 49, "biden": 42},
    "TX": {"trump": 48.9, "biden": 40.5},
    "FL": {"trump": 50.6, "biden": 41.9},
}

# Function to mix colors based on vote percentages and closeness
def mix_colors(trump_pct, biden_pct):
    diff = abs(trump_pct - biden_pct)
    if diff <= 3:
        # Blend in purple based on how close the results are
        purple_ratio = (2 - diff) / 2
        trump_red = 255 * (trump_pct / 100) * (1 - purple_ratio) + 128 * purple_ratio
        biden_blue = 255 * (biden_pct / 100) * (1 - purple_ratio) + 128 * purple_ratio
    elif trump_pct > biden_pct:
        return "#FF0000" 
    elif trump_pct < biden_pct:
        return "#0000FF"
    
    red = int(trump_red)
    blue = int(biden_blue)
    return f'#{red:02x}00{blue:02x}'

# Function to determine opacity based on vote difference and electoral votes
def calculate_opacity(trump_pct, biden_pct, electoral_votes):
    diff = abs(trump_pct - biden_pct)
    base_opacity = 10
    
    if diff < 1:
        base_opacity = 90
    elif diff < 5:
        base_opacity = 60
    elif diff < 10:
        base_opacity = 30
    else:
        base_opacity = 10

    # Adjust opacity based on electoral votes with a more nuanced impact
    if electoral_votes >= 30:
        weighted_opacity = base_opacity * 0.8  # Further reduce the impact for very high electoral votes
    elif electoral_votes >= 20:
        weighted_opacity = base_opacity * 1.0
    elif electoral_votes >= 10:
        weighted_opacity = base_opacity * 1.1
    else:
        weighted_opacity = base_opacity * 0.8

    # Cap the weighted opacity at 100
    final_opacity = min(weighted_opacity, 100)
    
    return final_opacity

# Electoral votes data
electoral_votes = {
    "AL": 9, "AK": 3, "AZ": 11, "AR": 6, "CA": 55, "CO": 9, "CT": 7, "DE": 3, "DC": 3,
    "FL": 29, "GA": 16, "HI": 4, "ID": 4, "IL": 20, "IN": 11, "IA": 6, "KS": 6, "KY": 8,
    "LA": 8, "ME": 4, "MD": 10, "MA": 11, "MI": 16, "MN": 10, "MS": 6, "MO": 10, "MT": 3,
    "NE": 5, "NV": 6, "NH": 4, "NJ": 14, "NM": 5, "NY": 29, "NC": 15, "ND": 3, "OH": 18,
    "OK": 7, "OR": 7, "PA": 20, "RI": 4, "SC": 9, "SD": 3, "TN": 11, "TX": 38, "UT": 6,
    "VT": 3, "VA": 13, "WA": 12, "WV": 5, "WI": 10, "WY": 3
}

# Update the colors for each state
state_colors = {}
for state, results in state_results.items():
    trump_pct = results["trump"]
    biden_pct = results["biden"]
    color = mix_colors(trump_pct, biden_pct)
    opacity = calculate_opacity(trump_pct, biden_pct, electoral_votes[state])
    state_colors[state] = (color, opacity)

# Load the SVG file
with open('States.svg', 'r') as file:
    svg_content = file.read()

# Parse the SVG content
soup = BeautifulSoup(svg_content, 'xml')

# Update the colors for each state and add electoral votes text for swing states
for state, (color, opacity) in state_colors.items():
    state_elements = []
    
    if state in ["HI", "MI"]:
        state_elements.extend(soup.find_all(attrs={"id": state}))
        state_elements.extend(soup.find_all(attrs={"inkscape:label": state}))
    else:
        state_elements = soup.find_all(id=state)
    
    if state_elements:
        for state_element in state_elements:
            if state_element.has_attr('style'):
                del state_element['style']  # Remove style attribute if it exists
            state_element['fill'] = color
            state_element['fill-opacity'] = str(opacity / 100)

            # Add electoral votes text for swing states
            diff = abs(state_results[state]["trump"] - state_results[state]["biden"])
            if diff < 5:  # Define swing state as vote difference < 5%
                bbox = state_element.get("bbox", None)
                if bbox:
                    bbox_values = [float(val) for val in bbox.split(",")]
                    x = (bbox_values[0] + bbox_values[2]) / 2
                    y = (bbox_values[1] + bbox_values[3]) / 2
                else:
                    x, y = 0, 0  # Default values in case bbox is not available
                text_element = soup.new_tag("text", x=str(x), y=str(y))
                text_element.string = str(electoral_votes[state])
                text_element['text-anchor'] = "middle"
                text_element['style'] = "font-size:24px; font-weight:bold; fill:#FFFFFF;"  # White color text
                state_element.append(text_element)
    else:
        print(f"State {state} not found in SVG.")

# Save the updated SVG content to a new file
with open('updated_map25.svg', 'w') as file:
    file.write(str(soup))

print("SVG map updated with election results.")